"""
Support for Australian BOM (Bureau of Meteorology) weather forecast service.
For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/sensor.bom_forecast
"""
import datetime
import ftplib
import io
import logging
import re
#import xml
import xml.etree.ElementTree

import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (
    CONF_MONITORED_CONDITIONS, TEMP_CELSIUS, CONF_NAME, ATTR_ATTRIBUTION,
    ATTR_FRIENDLY_NAME, CONF_LATITUDE, CONF_LONGITUDE, CONF_ICON)
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle
import homeassistant.helpers.config_validation as cv

_FIND_QUERY = "./forecast/area[@type='location']/forecast-period[@index='{}']/*[@type='{}']"
_FIND_QUERY_2 = "./forecast/area[@type='metropolitan']/forecast-period[@index='{}']/text[@type='forecast']"
            
_LOGGER = logging.getLogger(__name__)

ATTR_ICON = 'icon'
ATTR_ISSUE_TIME_LOCAL = 'issue_time_local'
ATTR_PRODUCT_ID = 'product_id'
ATTR_PRODUCT_LOCATION = 'product_location'
ATTR_PRODUCT_NAME = 'product_name'
ATTR_SENSOR_ID = 'sensor_id'
ATTR_START_TIME_LOCAL = 'start_time_local'

CONF_ATTRIBUTION = 'Data provided by the Australian Bureau of Meteorology'
CONF_DAYS = 'forecast_days'
CONF_PRODUCT_ID = 'product_id'
CONF_REST_OF_TODAY = 'rest_of_today'
CONF_FRIENDLY = 'friendly'
CONF_FRIENDLY_STATE_FORMAT = 'friendly_state_format'

MIN_TIME_BETWEEN_UPDATES = datetime.timedelta(minutes=60)

PRODUCT_ID_LAT_LON_LOCATION = {
    'IDD10150': [-12.47, 130.85, 'Darwin', 'City'],
    'IDN10035': [-35.31, 149.20, 'Canberra', 'City'],
    'IDN10064': [-33.86, 151.21, 'Sydney', 'City'],
    'IDN11051': [-32.89, 151.71, 'Newcastle', 'City'],
    'IDN11052': [-33.44, 151.36, 'Central Coast', 'City'],
    'IDN11053': [-34.56, 150.79, 'Wollongong', 'City'],
    'IDN11055': [-36.49, 148.29, 'Alpine Centres', 'City'],
    'IDQ10095': [-27.48, 153.04, 'Brisbane', 'City'],
    'IDQ10610': [-27.94, 153.43, 'Gold Coast', 'City'],
    'IDQ10611': [-26.60, 153.09, 'Sunshine Coast', 'City'],
    'IDS10034': [-34.93, 138.58, 'Adelaide', 'City'],
    'IDT13600': [-42.89, 147.33, 'Hobart', 'City'],
    'IDT13610': [-41.42, 147.12, 'Launceston', 'City'],
    'IDV10450': [-37.83, 144.98, 'Melbourne', 'City'],
    'IDV10701': [-38.17, 144.38, 'Geelong', 'City'],
    'IDV10702': [-38.31, 145.00, 'Mornington Peninsula', 'City'],
    'IDW12300': [-31.92, 115.87, 'Perth', 'City'],
    'IDD10161': [-23.70, 133.88, 'Alice Springs', 'Town'],
    'IDD10199': [-12.18, 136.78, 'Nhulunbuy', 'Town'],
    'IDD10200': [-14.47, 132.26, 'Katherine', 'Town'],
    'IDD10201': [-25.24, 130.99, 'Yulara', 'Town'],
    'IDD10202': [-12.67, 132.84, 'Jabiru', 'Town'],
    'IDD10203': [-19.56, 134.22, 'Tennant Creek', 'Town'],
    'IDD10204': [-14.24, 129.52, 'Wadeye', 'Town'],
    'IDD10205': [-12.05, 134.23, 'Maningrida', 'Town'],
    'IDD10206': [-12.49, 130.99, 'Palmerston', 'Town'],
    'IDD10209': [39.78, -100.45, 'Wurrimiyanga', 'Town'],
    'IDN11101': [-30.51, 151.67, 'Armidale', 'Town'],
    'IDN11102': [-35.71, 150.18, 'Batemans Bay', 'Town'],
    'IDN11103': [-31.97, 141.45, 'Broken Hill', 'Town'],
    'IDN11104': [-31.50, 145.83, 'Cobar', 'Town'],
    'IDN11105': [-30.17, 153.00, 'Coffs Harbour', 'Town'],
    'IDN11106': [-32.25, 148.60, 'Dubbo', 'Town'],
    'IDN11107': [-34.75, 149.72, 'Goulburn', 'Town'],
    'IDN11108': [-34.29, 146.06, 'Griffith', 'Town'],
    'IDN11109': [-33.71, 150.31, 'Katoomba', 'Town'],
    'IDN11110': [-28.79, 153.27, 'Lismore', 'Town'],
    'IDN11111': [-33.28, 149.10, 'Orange', 'Town'],
    'IDN11112': [-31.43, 152.91, 'Port Macquarie', 'Town'],
    'IDN11113': [-30.92, 150.91, 'Tamworth', 'Town'],
    'IDN11114': [-35.12, 147.37, 'Wagga Wagga', 'Town'],
    'IDN11116': [-34.48, 150.42, 'Bowral', 'Town'],
    'IDN11117': [-31.91, 152.46, 'Taree', 'Town'],
    'IDN11118': [-36.68, 149.84, 'Bega', 'Town'],
    'IDN11119': [-36.24, 149.13, 'Cooma', 'Town'],
    'IDN11121': [-28.18, 153.55, 'Tweed Heads', 'Town'],
    'IDQ10900': [-25.90, 139.35, 'Birdsville', 'Town'],
    'IDQ10901': [-24.87, 152.35, 'Bundaberg', 'Town'],
    'IDQ10902': [-16.92, 145.77, 'Cairns', 'Town'],
    'IDQ10903': [-26.41, 146.24, 'Charleville', 'Town'],
    'IDQ10904': [-20.07, 146.27, 'Charters Towers', 'Town'],
    'IDQ10906': [-23.53, 148.16, 'Emerald', 'Town'],
    'IDQ10907': [-23.84, 151.26, 'Gladstone', 'Town'],
    'IDQ10908': [-28.55, 150.31, 'Goondiwindi', 'Town'],
    'IDQ10909': [-26.20, 152.66, 'Gympie', 'Town'],
    'IDQ10910': [-25.30, 152.85, 'Hervey Bay', 'Town'],
    'IDQ10911': [-27.62, 152.76, 'Ipswich', 'Town'],
    'IDQ10913': [-23.44, 144.26, 'Longreach', 'Town'],
    'IDQ10914': [-21.14, 149.19, 'Mackay', 'Town'],
    'IDQ10915': [-25.54, 152.70, 'Maryborough', 'Town'],
    'IDQ10916': [-20.73, 139.49, 'Mount Isa', 'Town'],
    'IDQ10918': [-23.38, 150.51, 'Rockhampton', 'Town'],
    'IDQ10919': [-26.57, 148.79, 'Roma', 'Town'],
    'IDQ10922': [-27.56, 151.95, 'Toowoomba', 'Town'],
    'IDQ10923': [-19.26, 146.82, 'Townsville', 'Town'],
    'IDQ10925': [-12.64, 141.87, 'Weipa', 'Town'],
    'IDS11001': [-33.04, 137.58, 'Whyalla', 'Town'],
    'IDS11002': [-34.72, 135.86, 'Port Lincoln', 'Town'],
    'IDS11003': [-34.17, 140.75, 'Renmark', 'Town'],
    'IDS11004': [-37.83, 140.78, 'Mount Gambier', 'Town'],
    'IDS11016': [-35.06, 138.86, 'Mount Barker', 'Town'],
    'IDT13501': [-41.05, 145.91, 'Burnie', 'Town'],
    'IDT13502': [-41.93, 147.50, 'Campbell Town', 'Town'],
    'IDT13503': [-41.18, 146.36, 'Devonport', 'Town'],
    'IDT13504': [-42.78, 147.06, 'New Norfolk', 'Town'],
    'IDT13505': [-42.08, 145.56, 'Queenstown', 'Town'],
    'IDT13506': [-41.16, 147.51, 'Scottsdale', 'Town'],
    'IDT13507': [-40.84, 145.13, 'Smithton', 'Town'],
    'IDT13508': [-41.32, 148.25, 'St Helens', 'Town'],
    'IDT13509': [-42.15, 145.33, 'Strahan', 'Town'],
    'IDT13510': [-42.12, 148.08, 'Swansea', 'Town'],
    'IDT13511': [-41.16, 146.17, 'Ulverstone', 'Town'],
    'IDV10703': [-36.12, 146.89, 'Albury/Wodonga', 'Town'],
    'IDV10704': [-37.83, 147.63, 'Bairnsdale', 'Town'],
    'IDV10705': [-37.56, 143.86, 'Ballarat', 'Town'],
    'IDV10706': [-36.76, 144.28, 'Bendigo', 'Town'],
    'IDV10707': [-38.34, 143.59, 'Colac', 'Town'],
    'IDV10708': [-36.13, 144.75, 'Echuca', 'Town'],
    'IDV10710': [-37.74, 142.02, 'Hamilton', 'Town'],
    'IDV10711': [-36.71, 142.20, 'Horsham', 'Town'],
    'IDV10712': [-38.18, 146.27, 'Latrobe Valley', 'Town'],
    'IDV10714': [-34.18, 142.16, 'Mildura', 'Town'],
    'IDV10715': [-37.15, 146.43, 'Mount Buller', 'Town'],
    'IDV10716': [-37.83, 145.35, 'Mount Dandenong', 'Town'],
    'IDV10717': [-36.98, 147.13, 'Mount Hotham', 'Town'],
    'IDV10718': [-37.70, 148.46, 'Orbost', 'Town'],
    'IDV10719': [-38.11, 147.06, 'Sale', 'Town'],
    'IDV10721': [-37.02, 145.14, 'Seymour', 'Town'],
    'IDV10722': [-36.38, 145.40, 'Shepparton', 'Town'],
    'IDV10723': [-35.34, 143.56, 'Swan Hill', 'Town'],
    'IDV10725': [-36.36, 146.32, 'Wangaratta', 'Town'],
    'IDV10726': [-38.38, 142.48, 'Warrnambool', 'Town'],
    'IDV10728': [-38.61, 145.59, 'Wonthaggi', 'Town'],
    'IDV10730': [-37.14, 145.20, 'Falls Creek', 'Town'],
    'IDW14101': [-17.96, 122.22, 'Broome', 'Town'],
    'IDW14102': [-20.31, 118.58, 'Port Hedland', 'Town'],
    'IDW14103': [-20.74, 116.85, 'Karratha', 'Town'],
    'IDW14104': [-23.36, 119.73, 'Newman', 'Town'],
    'IDW14105': [-21.93, 114.13, 'Exmouth', 'Town'],
    'IDW14106': [-24.88, 113.66, 'Carnarvon', 'Town'],
    'IDW14107': [-28.77, 114.61, 'Geraldton', 'Town'],
    'IDW14108': [-30.75, 121.47, 'Kalgoorlie', 'Town'],
    'IDW14109': [-33.33, 115.64, 'Bunbury', 'Town'],
    'IDW14110': [-35.02, 117.88, 'Albany', 'Town'],
    'IDW14111': [-33.86, 121.89, 'Esperance', 'Town'],
    'IDW14112': [-15.77, 128.74, 'Kununurra', 'Town'],
    'IDW14113': [-26.59, 118.50, 'Meekatharra', 'Town'],
    'IDW14114': [-32.53, 115.72, 'Mandurah', 'Town'],
    'IDW14115': [-33.64, 115.35, 'Busselton', 'Town']
}

SENSOR_TYPES = {
    'max': ['air_temperature_maximum', 'Max Temp C', TEMP_CELSIUS, 'mdi:thermometer'],
    'min': ['air_temperature_minimum', 'Min Temp C', TEMP_CELSIUS, 'mdi:thermometer'],
    'chance_of_rain': ['probability_of_precipitation', 'Chance of Rain', '%', 'mdi:water-percent'],
    'possible_rainfall': ['precipitation_range', 'Possible Rainfall', 'mm', 'mdi:water'],
    'summary': ['precis', 'Summary', None, 'mdi:text'],
    'detailed_summary': ['forecast', 'Detailed Summary', None, 'mdi:text'],
    'icon': ['forecast_icon_code', 'Icon', None, None]
}

ICON_MAPPING = {
    '1': 'mdi:weather-sunny',
    '2': 'mdi:weather-night',
    '3': 'mdi:weather-partlycloudy',
    '4': 'mdi:weather-cloudy',
    '6': 'mdi:weather-sunset',
    '8': 'mdi:weather-rainy',
    '9': 'mdi:weather-windy',
    '10': 'mdi:weather-sunset',
    '11': 'mdi:weather-rainy',
    '12': 'mdi:weather-pouring',
    '13': 'mdi:weather-sunset',
    '14': 'mdi:weather-snowy',
    '15': 'mdi:weather-snowy',
    '16': 'mdi:weather-lightning',
    '17': 'mdi:weather-rainy'
}

def validate_days(days):
    """Check that days is within bounds."""
    if days not in range(1,7):
        raise vol.error.Invalid("Forecast Days is out of Range")
    return days

def validate_product_id(product_id):
    """Check that the Product ID is well-formed."""
    if product_id is None or not product_id:
        return product_id
    if not re.fullmatch(r'ID[A-Z]\d\d\d\d\d', product_id):
        raise vol.error.Invalid("Malformed Product ID")
    return product_id

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_MONITORED_CONDITIONS, default=[]):
        vol.All(cv.ensure_list, [vol.In(SENSOR_TYPES)]),
    vol.Optional(CONF_DAYS, default=6): validate_days,
    vol.Optional(CONF_FRIENDLY, default=False): cv.boolean,
    vol.Optional(CONF_FRIENDLY_STATE_FORMAT, default='{summary}'):  cv.string,
    vol.Optional(CONF_NAME, default=''): cv.string,
    vol.Optional(CONF_PRODUCT_ID, default=''): validate_product_id,
    vol.Optional(CONF_REST_OF_TODAY, default=True): cv.boolean,
})

def setup_platform(hass, config, add_entities, discovery_info=None):

    days = config.get(CONF_DAYS)
    friendly = config.get(CONF_FRIENDLY)
    friendly_state_format = config.get(CONF_FRIENDLY_STATE_FORMAT)
    monitored_conditions = config.get(CONF_MONITORED_CONDITIONS)
    name = config.get(CONF_NAME)
    product_id = config.get(CONF_PRODUCT_ID)
    rest_of_today = config.get(CONF_REST_OF_TODAY)

    if not product_id:
        product_id = closest_product_id(
            hass.config.latitude, hass.config.longitude)
        if product_id is None:
            _LOGGER.error("Could not get BOM Product ID from lat/lon")
            return

    bom_forecast_data = BOMForecastData(product_id)

    bom_forecast_data.update()

    if rest_of_today:
        start = 0
    else:
        start = 1

    if friendly:
        for index in range(start, config.get(CONF_DAYS)+1):
            add_entities([BOMForecastSensorFriendly(bom_forecast_data, monitored_conditions,
            index, name, product_id, friendly_state_format)])
    else:
        for index in range(start, config.get(CONF_DAYS)+1):
            for condition in monitored_conditions:    
                add_entities([BOMForecastSensor(bom_forecast_data, condition,
                index, name, product_id)])


class BOMForecastSensor(Entity):
    """Implementation of a BOM forecast sensor."""

    def __init__(self, bom_forecast_data, condition, index, name, product_id):
        """Initialize the sensor."""
        self._bom_forecast_data = bom_forecast_data
        self._condition = condition
        self._index = index
        self._name = name
        self._product_id = product_id
        self.update()
        
    @property
    def name(self):
        """Return the name of the sensor."""
        if not self._name:
            return 'BOM {} {}'.format(
            SENSOR_TYPES[self._condition][1], self._index)
        return 'BOM {} {} {}'.format(self._name,
        SENSOR_TYPES[self._condition][1], self._index)

    @property
    def state(self):
        """Return the state of the sensor."""
        reading = self._bom_forecast_data.get_reading(
            self._condition, self._index)
            
        if  self._condition == 'chance_of_rain':
        	return reading.replace('%', '')
        if  self._condition == 'possible_rainfall':
        	return reading.replace(' mm', '')        	
        return reading

    @property
    def device_state_attributes(self):
        """Return the state attributes of the sensor."""
        attr = {
            ATTR_ATTRIBUTION: CONF_ATTRIBUTION,
            ATTR_SENSOR_ID: self._condition,
            ATTR_ISSUE_TIME_LOCAL: self._bom_forecast_data.get_issue_time_local(),
            ATTR_PRODUCT_ID: self._product_id,
            ATTR_PRODUCT_LOCATION: PRODUCT_ID_LAT_LON_LOCATION[self._product_id][2],
            ATTR_START_TIME_LOCAL: self._bom_forecast_data.get_start_time_local(self._index),
            ATTR_ICON: SENSOR_TYPES[self._condition][3]
        }
        if self._name:
            attr[ATTR_PRODUCT_NAME] = self._name

        return attr

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return SENSOR_TYPES[self._condition][2]

    def update(self):
        """Fetch new state data for the sensor."""
        self._bom_forecast_data.update()

class BOMForecastSensorFriendly(Entity):
    """Implementation of a user friendly BOM forecast sensor."""

    def __init__(self, bom_forecast_data, conditions, index, name, product_id, friendly_state_format):
        """Initialize the sensor."""
        self._bom_forecast_data = bom_forecast_data
        self._conditions = conditions
        self._friendly_state_format = friendly_state_format
        self._index = index
        self._name = name
        self._product_id = product_id
        self.update()
        
    @property
    def unique_id(self):
        """Return the entity id of the sensor."""
        if not self._name:
            return '{}'.format(self._index)
        return '{}_{}'.format(self._name, self._index)

    @property
    def state(self):
        """Return the state of the sensor."""
        friendly_state = self._friendly_state_format
        for condition in self._conditions:
            friendly_state = friendly_state.replace('{{{}}}'.format(condition), self._bom_forecast_data.get_reading(condition, self._index))
        return friendly_state

    @property
    def device_state_attributes(self):
        """Return the state attributes of the sensor."""
        attr = {
            ATTR_ICON: self._bom_forecast_data.get_reading('icon', self._index),
            ATTR_ATTRIBUTION: CONF_ATTRIBUTION,
        }
        for condition in self._conditions:
            attribute = self._bom_forecast_data.get_reading(condition, self._index)
            if attribute != 'n/a':
                attr[SENSOR_TYPES[condition][1]] = attribute
        if self._name:
            attr['Name'] = self._name

        weather_forecast_date_string = self._bom_forecast_data.get_start_time_local(self._index).replace(":","")
        weather_forecast_datetime = datetime.datetime.strptime(weather_forecast_date_string, "%Y-%m-%dT%H%M%S%z")
        attr[ATTR_FRIENDLY_NAME] =  weather_forecast_datetime.strftime("%a, %e %b")            
        
        attr["Product ID"] = self._product_id
        attr["Product Location"] = PRODUCT_ID_LAT_LON_LOCATION[self._product_id][2]
        
        return attr

    def update(self):
        """Fetch new state data for the sensor."""
        self._bom_forecast_data.update()

class BOMForecastData:
    """Get data from BOM."""

    def __init__(self, product_id):
        """Initialize the data object."""
        self._product_id = product_id

    def get_reading(self, condition, index):
        """Return the value for the given condition."""
        if condition == 'detailed_summary':
            if PRODUCT_ID_LAT_LON_LOCATION[self._product_id][3] == 'City':
                return self._data.find(_FIND_QUERY_2.format(index)).text
            else:
                return self._data.find(_FIND_QUERY.format(index, 'forecast')).text
        
        find_query = (_FIND_QUERY.format(index, SENSOR_TYPES[condition][0]))
        state = self._data.find(find_query)
        if condition == 'icon':
            return ICON_MAPPING[state.text]
        if state is None:
            if condition == 'possible_rainfall':
                return '0 mm'
            return 'n/a'
        return state.text

    def get_issue_time_local(self):
        """Return the issue time of forecast."""
        issue_time = self._data.find("./amoc/next-routine-issue-time-local")
        if issue_time is None:
            return 'n/a'
        else:
            return issue_time.text

    def get_start_time_local(self, index):
        """Return the start time of forecast."""
        return self._data.find("./forecast/area[@type='location']/"
                               "forecast-period[@index='{}']".format(
                                index)).get("start-time-local")

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        """Get the latest data from BOM."""
        file_obj = io.BytesIO()
        ftp = ftplib.FTP('ftp.bom.gov.au')
        ftp.login()
        ftp.cwd('anon/gen/fwo/')
        ftp.retrbinary('RETR ' + self._product_id + '.xml', file_obj.write)
        file_obj.seek(0)
        ftp.quit()
        tree = xml.etree.ElementTree.parse(file_obj)
        self._data = tree.getroot()

def closest_product_id(lat, lon):
    """Return the closest product ID to our lat/lon."""

    def comparable_dist(product_id):
        """Create a psudeo-distance from latitude/longitude."""
        product_id_lat = PRODUCT_ID_LAT_LON_LOCATION[product_id][0]
        product_id_lon = PRODUCT_ID_LAT_LON_LOCATION[product_id][1]
        return (lat - product_id_lat) ** 2 + (lon - product_id_lon) ** 2

    return min(PRODUCT_ID_LAT_LON_LOCATION, key=comparable_dist)