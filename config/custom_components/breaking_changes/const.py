"""Constants for breaking_changes."""
# Base component constants
DOMAIN = "breaking_changes"
DOMAIN_DATA = "{}_data".format(DOMAIN)
VERSION = "0.2.0"
PLATFORMS = ["sensor"]
REQUIRED_FILES = ["const.py", "sensor.py"]
ISSUE_URL = "https://github.com/custom-components/breaking_changes/issues"

STARTUP = """
-------------------------------------------------------------------
{name}
Version: {version}
This is a custom component
If you have any issues with this you need to open an issue here:
{issueurl}
-------------------------------------------------------------------
"""

# Operational
URL = "https://hachanges.halfdecent.io/{}/json"

# Icons
ICON = "mdi:package-up"

# Configuration
CONF_NAME = "name"

# Defaults
DEFAULT_NAME = "Potential breaking changes"
