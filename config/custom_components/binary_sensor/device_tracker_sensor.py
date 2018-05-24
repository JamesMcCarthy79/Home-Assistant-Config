# """
# Creates a sensor that creates binary sensors from device_tracker devices
# """
import asyncio
import logging

import voluptuous as vol


from homeassistant.core import callback
from homeassistant.components.binary_sensor import BinarySensorDevice, \
    ENTITY_ID_FORMAT, PLATFORM_SCHEMA
from homeassistant.components.device_tracker import ATTR_SOURCE_TYPE
from homeassistant.const import (ATTR_FRIENDLY_NAME, CONF_ENTITIES,
                                 EVENT_HOMEASSISTANT_START)
from homeassistant.exceptions import TemplateError
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity, async_generate_entity_id
from homeassistant.helpers.event import async_track_state_change
from homeassistant.helpers.restore_state import async_get_last_state
from homeassistant.helpers import template as template_helper

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_ENTITIES): cv.entity_ids
})

@asyncio.coroutine
def async_setup_platform(hass, config, async_add_devices, discovery_info=None):
    """Set up the sensors."""
    _LOGGER.info("Starting device tracker sensor")
    sensors = []

    for device in config[CONF_ENTITIES]:

        state_template = "{{{{ is_state('{0}', 'home') }}}}".format(device)
        _LOGGER.debug("Applying template: %s", state_template)

        state_template = template_helper.Template(state_template)
        state_template.hass = hass

        device_state = hass.states.get(device)
        if device_state is not None:
            friendly_name = device_state.attributes.get(ATTR_FRIENDLY_NAME)
            source_type = device_state.attributes.get(ATTR_SOURCE_TYPE)
        else:
            friendly_name = None
            source_type = None

        if friendly_name is None:
            friendly_name = device.split(".", 1)[1]

        sensors.append(
            DeviceTrackerSensor(
                hass,
                "device_tracker_{0}".format(device.split(".", 1)[1]),
                friendly_name,
                source_type,
                state_template,
                device)
        )
    if not sensors:
        _LOGGER.error("No sensors added")
        return False

    async_add_devices(sensors)
    return True


class DeviceTrackerSensor(BinarySensorDevice):
    """Representation of a Device Tracker Sensor."""

    def __init__(self, hass, device_id, friendly_name, source_type,
                 state_template, entity_id):
        """Initialize the sensor."""
        self.hass = hass
        self.entity_id = async_generate_entity_id(ENTITY_ID_FORMAT, device_id,
                                                  hass=hass)
        self._name = friendly_name
        self._source_type = source_type
        self._template = state_template
        self._state = False
        self._entity = entity_id

    @asyncio.coroutine
    def async_added_to_hass(self):
        """Register callbacks."""
        #state = yield from async_get_last_state(self.hass, self.entity_id)
        #if state:
        #    self._state = state.state

        @callback
        def template_sensor_state_listener(entity, old_state, new_state):
            """Handle device state changes."""
            self.hass.async_add_job(self.async_update_ha_state(True))

        @callback
        def template_sensor_startup(event):
            """Update on startup."""
            async_track_state_change(
                self.hass, self._entity, template_sensor_state_listener)

            self.hass.async_add_job(self.async_update_ha_state(True))

        self.hass.bus.async_listen_once(
            EVENT_HOMEASSISTANT_START, template_sensor_startup)

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return {ATTR_SOURCE_TYPE: self._source_type}

    @property
    def should_poll(self):
        """No polling needed."""
        return False

    @property
    def is_on(self):
        """Return true if sensor is on."""
        return self._state

    @property
    def name(self):
        """Return the entity name."""
        return self._name

    # @property
    # def device_class(self):
    #     """Return the class of binary sensor."""
    #     return self._device_class

    @asyncio.coroutine
    def async_update(self):
        """Update the sensor state."""
        _LOGGER.debug('Updating device_tracker_sensor sensor')

        entity_state = self.hass.states.get(self._entity)
        if entity_state is not None:
            device_friendly_name = entity_state.attributes.get(
                ATTR_FRIENDLY_NAME)
            self._source_type = entity_state.attributes.get(ATTR_SOURCE_TYPE)
        else:
            device_friendly_name = None
            self._source_type = None

        if device_friendly_name is not None:
            self._name = device_friendly_name

        try:
            self._state = self._template.async_render().lower() == 'true'
        except TemplateError as ex:
            if ex.args and ex.args[0].startswith(
                    "UndefinedError: 'None' has no attribute"):
                # Common during HA startup - so just a warning
                _LOGGER.warning('Could not render attribute sensor for %s,'
                                ' the state is unknown.', self._entity)
                return
            self._state = False
            _LOGGER.error('Could not attribute sensor for %s: %s',
                          self._entity, ex)