"""Sensor platform for breaking_changes."""
from datetime import timedelta
from homeassistant.helpers.entity import Entity
from . import update_data
from .const import DOMAIN_DATA, ICON

SCAN_INTERVAL = timedelta(seconds=10)


async def async_setup_platform(
    hass, config, async_add_entities, discovery_info=None
):  # pylint: disable=unused-argument
    """Setup sensor platform."""
    async_add_entities([BreakingChangesSensor(hass, discovery_info)], True)


class BreakingChangesSensor(Entity):
    """breaking_changes Sensor class."""

    def __init__(self, hass, config):
        self.hass = hass
        self.attr = {}
        self._state = None
        self._name = config["name"]

    async def async_update(self):
        """Update the sensor."""
        # Send update "signal" to the component
        await update_data(self.hass)

        # Get new data (if any)
        updated = self.hass.data[DOMAIN_DATA]

        # Check the data and update the value.
        self._state = len(updated.get("potential", [])) - 1
        self._state = 0 if self._state < 0 else self._state

        # Set/update attributes
        self.attr = updated.get("potential", [])

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return ICON

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return self.attr
