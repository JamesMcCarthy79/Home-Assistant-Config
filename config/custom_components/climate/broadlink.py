import asyncio
import logging
import binascii
import socket
import os.path
import voluptuous as vol
import homeassistant.helpers.config_validation as cv

from homeassistant.components.climate import (ClimateDevice, PLATFORM_SCHEMA, STATE_OFF, STATE_IDLE, STATE_HEAT, STATE_COOL, STATE_AUTO,
ATTR_OPERATION_MODE, SUPPORT_OPERATION_MODE, SUPPORT_TARGET_TEMPERATURE, SUPPORT_FAN_MODE)
from homeassistant.const import (ATTR_UNIT_OF_MEASUREMENT, ATTR_TEMPERATURE, CONF_NAME, CONF_HOST, CONF_MAC, CONF_TIMEOUT, CONF_CUSTOMIZE)
from homeassistant.helpers.event import (async_track_state_change)
from homeassistant.core import callback
from homeassistant.helpers.restore_state import async_get_last_state
from configparser import ConfigParser
from base64 import b64encode, b64decode

REQUIREMENTS = ['broadlink==0.9.0']

_LOGGER = logging.getLogger(__name__)

SUPPORT_FLAGS = SUPPORT_TARGET_TEMPERATURE | SUPPORT_OPERATION_MODE | SUPPORT_FAN_MODE

CONF_IRCODES_INI = 'ircodes_ini'
CONF_MIN_TEMP = 'min_temp'
CONF_MAX_TEMP = 'max_temp'
CONF_TARGET_TEMP = 'target_temp'
CONF_TARGET_TEMP_STEP = 'target_temp_step'
CONF_TEMP_SENSOR = 'temp_sensor'
CONF_OPERATIONS = 'operations'
CONF_FAN_MODES = 'fan_modes'
CONF_DEFAULT_OPERATION = 'default_operation'
CONF_DEFAULT_FAN_MODE = 'default_fan_mode'

CONF_DEFAULT_OPERATION_FROM_IDLE = 'default_operation_from_idle'

DEFAULT_NAME = 'Broadlink IR Climate'
DEFAULT_TIMEOUT = 10
DEFAULT_RETRY = 3
DEFAULT_MIN_TEMP = 16
DEFAULT_MAX_TEMP = 30
DEFAULT_TARGET_TEMP = 20
DEFAULT_TARGET_TEMP_STEP = 1
DEFAULT_OPERATION_LIST = [STATE_OFF, STATE_HEAT, STATE_COOL, STATE_AUTO]
DEFAULT_FAN_MODE_LIST = ['low', 'mid', 'high', 'auto']
DEFAULT_OPERATION = 'off'
DEFAULT_FAN_MODE = 'auto'

CUSTOMIZE_SCHEMA = vol.Schema({
    vol.Optional(CONF_OPERATIONS): vol.All(cv.ensure_list, [cv.string]),
    vol.Optional(CONF_FAN_MODES): vol.All(cv.ensure_list, [cv.string])
})

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Required(CONF_HOST): cv.string,
    vol.Required(CONF_MAC): cv.string,
    vol.Required(CONF_IRCODES_INI): cv.string,
    vol.Optional(CONF_TIMEOUT, default=DEFAULT_TIMEOUT): cv.positive_int, 
    vol.Optional(CONF_MIN_TEMP, default=DEFAULT_MIN_TEMP): cv.positive_int,
    vol.Optional(CONF_MAX_TEMP, default=DEFAULT_MAX_TEMP): cv.positive_int,
    vol.Optional(CONF_TARGET_TEMP, default=DEFAULT_TARGET_TEMP): cv.positive_int,
    vol.Optional(CONF_TARGET_TEMP_STEP, default=DEFAULT_TARGET_TEMP_STEP): cv.positive_int,
    vol.Optional(CONF_TEMP_SENSOR): cv.entity_id,
    vol.Optional(CONF_CUSTOMIZE, default={}): CUSTOMIZE_SCHEMA,
    vol.Optional(CONF_DEFAULT_OPERATION, default=DEFAULT_OPERATION): cv.string,
    vol.Optional(CONF_DEFAULT_FAN_MODE, default=DEFAULT_FAN_MODE): cv.string,
    vol.Optional(CONF_DEFAULT_OPERATION_FROM_IDLE): cv.string
})

@asyncio.coroutine
def async_setup_platform(hass, config, async_add_devices, discovery_info=None):
    """Set up the Broadlink IR Climate platform."""
    name = config.get(CONF_NAME)
    ip_addr = config.get(CONF_HOST)
    mac_addr = binascii.unhexlify(config.get(CONF_MAC).encode().replace(b':', b''))
      
    min_temp = config.get(CONF_MIN_TEMP)
    max_temp = config.get(CONF_MAX_TEMP)
    target_temp = config.get(CONF_TARGET_TEMP)
    target_temp_step = config.get(CONF_TARGET_TEMP_STEP)
    temp_sensor_entity_id = config.get(CONF_TEMP_SENSOR)
    operation_list = config.get(CONF_CUSTOMIZE).get(CONF_OPERATIONS, []) or DEFAULT_OPERATION_LIST
    fan_list = config.get(CONF_CUSTOMIZE).get(CONF_FAN_MODES, []) or DEFAULT_FAN_MODE_LIST
    default_operation = config.get(CONF_DEFAULT_OPERATION)
    default_fan_mode = config.get(CONF_DEFAULT_FAN_MODE)
    
    default_operation_from_idle = config.get(CONF_DEFAULT_OPERATION_FROM_IDLE)
    
    import broadlink
    
    broadlink_device = broadlink.rm((ip_addr, 80), mac_addr, None)
    broadlink_device.timeout = config.get(CONF_TIMEOUT)

    try:
        broadlink_device.auth()
    except socket.timeout:
        _LOGGER.error("Failed to connect to Broadlink RM Device")
    
    
    ircodes_ini_file = config.get(CONF_IRCODES_INI)
    
    if ircodes_ini_file.startswith("/"):
        ircodes_ini_file = ircodes_ini_file[1:]
        
    ircodes_ini_path = hass.config.path(ircodes_ini_file)
    
    if os.path.exists(ircodes_ini_path):
        ircodes_ini = ConfigParser()
        ircodes_ini.read(ircodes_ini_path)
    else:
        _LOGGER.error("The ini file was not found. (" + ircodes_ini_path + ")")
        return
    
    async_add_devices([
        BroadlinkIRClimate(hass, name, broadlink_device, ircodes_ini, min_temp, max_temp, target_temp, target_temp_step, temp_sensor_entity_id, operation_list, fan_list, default_operation, default_fan_mode, default_operation_from_idle)
    ])

class BroadlinkIRClimate(ClimateDevice):

    def __init__(self, hass, name, broadlink_device, ircodes_ini, min_temp, max_temp, target_temp, target_temp_step, temp_sensor_entity_id, operation_list, fan_list, default_operation, default_fan_mode, default_operation_from_idle):
                 
        """Initialize the Broadlink IR Climate device."""
        self.hass = hass
        self._name = name

        self._min_temp = min_temp
        self._max_temp = max_temp
        self._target_temperature = target_temp
        self._target_temperature_step = target_temp_step
        self._unit_of_measurement = hass.config.units.temperature_unit
        
        self._current_temperature = 0
        self._temp_sensor_entity_id = temp_sensor_entity_id

        self._current_operation = default_operation
        self._current_fan_mode = default_fan_mode
        
        self._operation_list = operation_list
        self._fan_list = fan_list
        
        self._default_operation_from_idle = default_operation_from_idle
                
        self._broadlink_device = broadlink_device
        self._commands_ini = ircodes_ini
        
        if temp_sensor_entity_id:
            async_track_state_change(
                hass, temp_sensor_entity_id, self._async_temp_sensor_changed)
                
            sensor_state = hass.states.get(temp_sensor_entity_id)    
                
            if sensor_state:
                self._async_update_current_temp(sensor_state)
    
    
    def send_ir(self):     
        section = self._current_operation.lower()
        
        if section == 'off':
            value = 'off_command'
        elif section == 'idle':
            value = 'idle_command'
        else: 
            value = self._current_fan_mode.lower() + "_" + str(int(self._target_temperature)) if not section == 'off' else 'off_command'
        
        command = self._commands_ini.get(section, value)
        
        for retry in range(DEFAULT_RETRY):
            try:
                payload = b64decode(command)
                self._broadlink_device.send_data(payload)
                break
            except (socket.timeout, ValueError):
                try:
                    self._broadlink_device.auth()
                except socket.timeout:
                    if retry == DEFAULT_RETRY-1:
                        _LOGGER.error("Failed to send packet to Broadlink RM Device")
        
    
    @asyncio.coroutine
    def _async_temp_sensor_changed(self, entity_id, old_state, new_state):
        """Handle temperature changes."""
        if new_state is None:
            return

        self._async_update_current_temp(new_state)
        yield from self.async_update_ha_state()
        
    @callback
    def _async_update_current_temp(self, state):
        """Update thermostat with latest state from sensor."""
        unit = state.attributes.get(ATTR_UNIT_OF_MEASUREMENT)

        try:
            _state = state.state
            if self.represents_float(_state):
                self._current_temperature = self.hass.config.units.temperature(
                    float(_state), unit)
        except ValueError as ex:
            _LOGGER.error('Unable to update from sensor: %s', ex)    

    def represents_float(self, s):
        try: 
            float(s)
            return True
        except ValueError:
            return False     

    
    @property
    def should_poll(self):
        """Return the polling state."""
        return False

    @property
    def name(self):
        """Return the name of the climate device."""
        return self._name

    @property
    def temperature_unit(self):
        """Return the unit of measurement."""
        return self._unit_of_measurement

    @property
    def current_temperature(self):
        """Return the current temperature."""
        return self._current_temperature
        
    @property
    def min_temp(self):
        """Return the polling state."""
        return self._min_temp
        
    @property
    def max_temp(self):
        """Return the polling state."""
        return self._max_temp    
        
    @property
    def target_temperature(self):
        """Return the temperature we try to reach."""
        return self._target_temperature
        
    @property
    def target_temperature_step(self):
        """Return the supported step of target temperature."""
        return self._target_temperature_step

    @property
    def current_operation(self):
        """Return current operation ie. heat, cool, idle."""
        return self._current_operation

    @property
    def operation_list(self):
        """Return the list of available operation modes."""
        return self._operation_list

    @property
    def current_fan_mode(self):
        """Return the fan setting."""
        return self._current_fan_mode

    @property
    def fan_list(self):
        """Return the list of available fan modes."""
        return self._fan_list
        
    @property
    def supported_features(self):
        """Return the list of supported features."""
        return SUPPORT_FLAGS        
 
    def set_temperature(self, **kwargs):
        """Set new target temperatures."""
        if kwargs.get(ATTR_TEMPERATURE) is not None:
            self._target_temperature = kwargs.get(ATTR_TEMPERATURE)
            
            if not (self._current_operation.lower() == 'off' or self._current_operation.lower() == 'idle'):
                self.send_ir()
            elif self._default_operation_from_idle is not None:
                self.set_operation_mode(self._default_operation_from_idle)
                
                    
            self.schedule_update_ha_state()

    def set_fan_mode(self, fan):
        """Set new target temperature."""
        self._current_fan_mode = fan
        
        if not (self._current_operation.lower() == 'off' or self._current_operation.lower() == 'idle'):
            self.send_ir()
            
        self.schedule_update_ha_state()

    def set_operation_mode(self, operation_mode):
        """Set new target temperature."""
        self._current_operation = operation_mode

        self.send_ir()
        self.schedule_update_ha_state()
        
    @asyncio.coroutine
    def async_added_to_hass(self):
        state = yield from async_get_last_state(self.hass, self.entity_id)
        
        if state is not None:
            self._target_temperature = state.attributes['temperature']
            self._current_operation = state.attributes['operation_mode']
            self._current_fan_mode = state.attributes['fan_mode']
