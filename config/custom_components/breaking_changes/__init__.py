"""
Component to show with breaking_changes.

For more details about this component, please refer to
https://github.com/custom-components/breaking_changes
"""
import os
from datetime import timedelta
import logging
import requests
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.const import EVENT_HOMEASSISTANT_START
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers import discovery
from homeassistant.util import Throttle
from .const import (
    DOMAIN_DATA,
    DOMAIN,
    ISSUE_URL,
    PLATFORMS,
    REQUIRED_FILES,
    STARTUP,
    URL,
    VERSION,
    CONF_NAME,
    DEFAULT_NAME,
)

REQUIREMENTS = ["pyhaversion"]

MIN_TIME_BETWEEN_UPDATES = timedelta(minutes=1)

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema(
    {DOMAIN: vol.Schema({vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string})},
    extra=vol.ALLOW_EXTRA,
)


async def async_setup(hass, config):
    """Set up this component."""

    # Print startup message
    startup = STARTUP.format(name=DOMAIN, version=VERSION, issueurl=ISSUE_URL)
    _LOGGER.info(startup)

    # Check that all required files are present
    file_check = await check_files(hass)
    if not file_check:
        return False

    # Create DATA dict
    hass.data[DOMAIN_DATA] = {}
    hass.data[DOMAIN_DATA]["components"] = ["homeassistant"]
    hass.data[DOMAIN_DATA]["potential"] = {}

    # Load platforms
    for platform in PLATFORMS:
        # Get platform specific configuration
        platform_config = config[DOMAIN]

        hass.async_create_task(
            discovery.async_load_platform(
                hass, platform, DOMAIN, platform_config, config
            )
        )

    async def loaded_platforms(hass):
        """Load platforms after HA startup."""
        for component in hass.config.components:
            hass.data[DOMAIN_DATA]["components"].append(component)

        _LOGGER.debug("Loaded components %s", hass.data[DOMAIN_DATA]["components"])
        await update_data(
            hass, no_throttle=True
        )  # pylint: disable=unexpected-keyword-arg

    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_START, loaded_platforms(hass))

    return True


@Throttle(MIN_TIME_BETWEEN_UPDATES)
async def update_data(hass):
    """Update data."""
    if len(hass.data[DOMAIN_DATA]["components"]) == 1:
        return
    from pyhaversion import Version

    session = async_get_clientsession(hass)
    haversion = Version(hass.loop, session)

    await haversion.get_local_version()
    currentversion = haversion.version.split(".")[1]

    await haversion.get_pypi_version()
    remoteversion = haversion.version.split(".")[1]

    if currentversion == remoteversion:
        _LOGGER.debug(
            "Current version is %s and remote version is %s skipping update",
            currentversion,
            remoteversion,
        )
        return

    versions = []

    for platform in hass.data[DOMAIN_DATA]["components"]:
        if "homeassistant.components." in platform:
            name = platform.split("homeassistant.components.")[1]
            if "." in name:
                name = name.split(".")[0]
            if name not in hass.data[DOMAIN_DATA]["components"]:
                hass.data[DOMAIN_DATA]["components"].append(name)
    _LOGGER.debug("Loaded components - %s", hass.data[DOMAIN_DATA]["components"])

    try:
        _LOGGER.debug("Running update")

        for version in range(int(currentversion) + 1, int(remoteversion) + 1):
            versions.append(version)
            request = requests.get(URL.format(version))
            jsondata = request.json()
            _LOGGER.debug(jsondata)
            for platform in jsondata:
                _LOGGER.debug(platform["component"])
                if platform["component"] is None or platform["component"] is "None":
                    platform["component"] = "homeassistant"
                if platform["component"] in hass.data[DOMAIN_DATA]["components"]:
                    data = {
                        "component": platform["component"],
                        "prlink": platform["prlink"],
                        "doclink": platform["doclink"],
                        "description": platform["description"],
                    }
                    hass.data[DOMAIN_DATA]["potential"][platform["pull_request"]] = data
        hass.data[DOMAIN_DATA]["potential"]["versions"] = versions
    except Exception as error:  # pylint: disable=broad-except
        _LOGGER.error("Could not update data - %s", error)


async def check_files(hass):
    """Return bool that indicates if all files are present."""
    # Verify that the user downloaded all files.
    base = "{}/custom_components/{}/".format(hass.config.path(), DOMAIN)
    missing = []
    for file in REQUIRED_FILES:
        fullpath = "{}{}".format(base, file)
        if not os.path.exists(fullpath):
            missing.append(file)

    if missing:
        _LOGGER.critical("The following files are missing: %s", str(missing))
        returnvalue = False
    else:
        returnvalue = True

    return returnvalue
