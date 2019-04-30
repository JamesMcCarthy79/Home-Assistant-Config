"""Creates Google Fit sensors.
At the moment, provides following measurements:
    - steps
    - distance
    - time
    - calories
    - weight
    - height
Sensor is designed to be flexible and allow customization to add new Google Fit
dimensions with minimal effort with relative knowledge of Python and Fitness
Rest API.
In order to add this component as is, add a new sensor:
sensor:
  - platform: google_fit
    name: Google Fit
    client_id: your_client_id
    client_secret: your_client_secret
In order to generate your client_id and client_secret, see the prerequisites
for Google Calender component:
https://www.home-assistant.io/components/calendar.google/#prerequisites
To make sensor work you have to enable Fintness API in your project.
In oder to enable Fitness API open Google cloud console: 
https://console.cloud.google.com/apis/library/fitness.googleapis.com
and enable API.
It is recommendable to store client_id and client_secret as secret as
possible. You can read about it on:
https://www.home-assistant.io/docs/configuration/secrets/
Example:
  - platform: google_fit
    name: Bob
    client_id: !secret google_fit_client_id
    client_secret: !secret google_fit_client_secret
"""

import logging
import os
import time
import voluptuous
from datetime import datetime, timedelta
from homeassistant import const
from homeassistant import util
from homeassistant.helpers import config_validation
from homeassistant.helpers import entity
from homeassistant.helpers.event import track_time_change
from homeassistant.util.dt import utc_from_timestamp

REQUIREMENTS = [
    'google-api-python-client==1.6.4',
    'oauth2client==4.0.0',
    'httplib2'
]

_LOGGER = logging.getLogger(__name__)

# Sensor details.
SENSOR = 'google_fit'

# Sensor base attributes.
ATTR_LAST_UPDATED = 'last_updated'
CONF_CLIENT_ID = 'client_id'
CONF_CLIENT_SECRET = 'client_secret'
DEFAULT_NAME = 'Google Fit'
DEFAULT_CREDENTIALS_FILE = '.google_fit.credentials.json'
ICON = 'mdi:heart-pulse'
MIN_TIME_BETWEEN_SCANS = timedelta(minutes=10)
MIN_TIME_BETWEEN_UPDATES = timedelta(minutes=10)
TOKEN_FILE = '.{}.token'.format(SENSOR)
SENSOR_NAME = '{} {}'

# # Define schema of sensor.
PLATFORM_SCHEMA = config_validation.PLATFORM_SCHEMA.extend({
    voluptuous.Required(CONF_CLIENT_ID): config_validation.string,
    voluptuous.Required(CONF_CLIENT_SECRET): config_validation.string,

    voluptuous.Optional(
        const.CONF_NAME,
        default=DEFAULT_NAME
    ): config_validation.string,

})

# Define base notifications.
NOTIFICATION_ID = 'google_fit_notification'
NOTIFICATION_TITLE = 'Google Fit Setup'

# Google Fit API URL.
API_VERSION = 'v1'
API_USER_ID = 'me'
WEIGHT = 'weight'
HEIGHT = 'height'
DISTANCE = 'distance'
STEPS = 'steps'
MOVE_TIME = 'move time'
CALORIES = 'calories'
SLEEP = 'sleep'

# Endpoint scopes required for the sensor.
# Read more: https://developers.google.com/fit/rest/v1/authorization

SCOPES = ['https://www.googleapis.com/auth/fitness.body.read',
          'https://www.googleapis.com/auth/fitness.body.write',
          'https://www.googleapis.com/auth/fitness.activity.read',
          'https://www.googleapis.com/auth/fitness.location.read']

def _today_dataset_start():
    today = datetime.today().date()
    return int(time.mktime(today.timetuple()) * 1000000000)

def _today_dataset_end():
    now = datetime.today()
    return int(time.mktime(now.timetuple()) * 1000000000)

def _get_client(token_file):
        """Get the Google Fit service with the storage file token.
        Args:
          token_file: str, File path for API token.
        Return:
          Google Fit API client.
        """
        import httplib2
        from googleapiclient import discovery as google_discovery
        from oauth2client import file as oauth2file

        if not os.path.isfile(token_file):
            return

        credentials = oauth2file.Storage(token_file).get()
        http = credentials.authorize(httplib2.Http())
        service = google_discovery.build(
            'fitness', API_VERSION, http=http, cache_discovery=False)
        return service

def setup(hass, config):
    """Set up the Google Fit platform."""
    token_file = hass.config.path(TOKEN_FILE)
    if not os.path.isfile(token_file):
        return do_authentication(hass, config)

    return True


def do_authentication(hass, config):
    """Notify user of actions and authenticate.
    Notify user of user_code and verification_url then poll until we have an
    access token.
    """
    from oauth2client import client as oauth2client
    from oauth2client import file as oauth2file

    oauth = oauth2client.OAuth2WebServerFlow(
        client_id=config[CONF_CLIENT_ID],
        client_secret=config[CONF_CLIENT_SECRET],
        scope=SCOPES,
        redirect_uri='Home-Assistant.io',
    )

    try:
        dev_flow = oauth.step1_get_device_and_user_codes()
    except oauth2client.OAuth2DeviceCodeError as err:
        hass.components.persistent_notification.create(
            'Error: {}<br />You will need to restart hass after fixing.'
            ''.format(err),
            title=NOTIFICATION_TITLE,
            notification_id=NOTIFICATION_ID)
        return False

    hass.components.persistent_notification.create(
        'In order to authorize Home-Assistant to view your Google Fit data '
        'you must visit: <a href="{}" target="_blank">{}</a> and enter '
        'code: {}'.format(dev_flow.verification_url,
                          dev_flow.verification_url,
                          dev_flow.user_code),
        title=NOTIFICATION_TITLE, notification_id=NOTIFICATION_ID
    )

    def step2_exchange(now):
        """Keep trying to validate the user_code until it expires."""
        if now >= util.dt.as_local(dev_flow.user_code_expiry):
            hass.components.persistent_notification.create(
                'Authentication code expired, please restart '
                'Home-Assistant and try again',
                title=NOTIFICATION_TITLE,
                notification_id=NOTIFICATION_ID)
            listener()

        try:
            credentials = oauth.step2_exchange(device_flow_info=dev_flow)
        except oauth2client.FlowExchangeError:
            # not ready yet, call again
            return

        storage = oauth2file.Storage(hass.config.path(TOKEN_FILE))
        storage.put(credentials)
        listener()

    listener = track_time_change(hass, step2_exchange,
                                 second=range(0, 60, dev_flow.interval))
    return True


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Adds sensor platform to the list of platforms."""
    setup(hass, config)

    token_file = hass.config.path(TOKEN_FILE)
    client = _get_client(token_file)
    name = config.get(const.CONF_NAME)
    add_devices([GoogleFitWeightSensor(client, name),
                 GoogleFitHeightSensor(client, name),
                 GoogleFitStepsSensor(client, name),
                 GoogleFitSleepSensor(client, name),
                 GoogleFitMoveTimeSensor(client, name),
                 GoogleFitCaloriesSensor(client, name),
                 GoogleFitDistanceSensor(client, name)], True)


class GoogleFitSensor(entity.Entity):
    """Representation of a Google Fit Sensor.
    Currently supported: Weight and Last Update for Weight.
    However, the sensor it is designed to be extensible for other measures.
    """

    def __init__(self, client, name):
        """Initializes the sensor.
        token_file: str, File path for API token.
        name: str, Name of the sensor.
        unit_of_measurement: str, Unit of measurement of sensor.
        """
        # Authenticate to application.
        self._client = client

        # Device name.
        self._name = name
        self._state = const.STATE_UNKNOWN
        self._last_updated = const.STATE_UNKNOWN

    @property
    def state(self):
        """Returns the state of the sensor."""
        return self._state

    @property
    def last_updated(self):
        """Returns date when it was last updated."""
        return utc_from_timestamp(self._last_updated)

    @property
    def name(self):
        """Returns the name of the sensor."""
        return SENSOR_NAME.format(self._name, self._name_suffix)

    @property
    def unit_of_measurement(self):
        """Returns the unit of measurement."""
        raise NotImplementedError

    @property
    def icon(self):
        """Return the icon."""
        raise NotImplementedError

    @property
    def state_attributes(self):
        """Returns the state attributes. """
        return {
            const.ATTR_FRIENDLY_NAME: self.name,
            const.ATTR_UNIT_OF_MEASUREMENT: self.unit_of_measurement,
            ATTR_LAST_UPDATED: self.last_updated,
        }

    @property
    def device_state_attributes(self):
        """Return device specific state attributes."""
        return self._attributes


    @util.Throttle(MIN_TIME_BETWEEN_SCANS, MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        """Fetches new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        raise NotImplementedError

    @property
    def _name_suffix(self):
        """Returns the name suffix of the sensor."""
        raise NotImplementedError

    def _get_datasources(self, data_type_name):
        """Gets data sources information for weight data.
        Args:
          data_type_name: str, Type of data sources to retrieve.
        Returns:
          Dictionary containing all available data sources.
        """
        datasources_request = self._client.users().dataSources().list(
            userId=API_USER_ID,
            dataTypeName=data_type_name,
        )
        data = datasources_request.execute()
        return data.get('dataSource')

    def _get_dataset(self, source):
        dataset = "%s-%s" % (_today_dataset_start(), _today_dataset_end())

        return self._client.users().dataSources(). \
            datasets(). \
            get(userId=API_USER_ID, dataSourceId=source, datasetId=dataset). \
            execute()

class GoogleFitWeightSensor(GoogleFitSensor):
    @property
    def unit_of_measurement(self):
        """Returns the unit of measurement."""
        return const.MASS_KILOGRAMS

    @property
    def icon(self):
        """Return the icon."""
        return 'mdi:weight-kilogram'

    @property
    def _name_suffix(self):
        """Returns the name suffix of the sensor."""
        return WEIGHT

    @util.Throttle(MIN_TIME_BETWEEN_SCANS, MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        """Extracts the relevant data points for from the Fitness API."""
        if not self._client:
            return

        weight_datasources = self._get_datasources('com.google.weight')

        weight_datapoints = {}
        for datasource in weight_datasources:
            datasource_id = datasource.get('dataStreamId')
            weight_request = self._client.users().dataSources().\
                dataPointChanges().list(
                    userId=API_USER_ID,
                    dataSourceId=datasource_id,
                )
            weight_data = weight_request.execute()
            weight_inserted_datapoints = weight_data.get('insertedDataPoint')

            for datapoint in weight_inserted_datapoints:
                point_value = datapoint.get('value')
                if not point_value:
                    continue
                weight = point_value[0].get('fpVal')
                if not weight:
                    continue
                weight = round(weight, 2)
                last_update_milis = int(datapoint.get('modifiedTimeMillis', 0))
                if not last_update_milis:
                    continue
                weight_datapoints[last_update_milis] = weight

        if weight_datapoints:
            time_updates = list(weight_datapoints.keys())
            time_updates.sort(reverse=True)

            last_time_update = time_updates[0]
            last_weight = weight_datapoints[last_time_update]

            self._last_updated = round(last_time_update / 1000)
            self._state = last_weight
            print("Weight: ", last_weight)
            self._attributes = {}


class GoogleFitHeightSensor(GoogleFitSensor):
    @property
    def unit_of_measurement(self):
        """Returns the unit of measurement."""
        return const.LENGTH_CENTIMETERS

    @property
    def icon(self):
        """Return the icon."""
        return 'mdi:ruler'

    @property
    def _name_suffix(self):
        """Returns the name suffix of the sensor."""
        return HEIGHT

    @util.Throttle(MIN_TIME_BETWEEN_SCANS, MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        """Extracts the relevant data points for from the Fitness API."""
        height_datasources = self._get_datasources('com.google.height')

        height_datapoints = {}
        for datasource in height_datasources:
            datasource_id = datasource.get('dataStreamId')
            height_request = self._client.users().dataSources().\
                dataPointChanges().list(
                    userId=API_USER_ID,
                    dataSourceId=datasource_id,
                )
            height_data = height_request.execute()
            height_inserted_datapoints = height_data.get('insertedDataPoint')

            for datapoint in height_inserted_datapoints:
                point_value = datapoint.get('value')
                if not point_value:
                    continue
                height = point_value[0].get('fpVal')
                if not height:
                    continue
                height = round(height * 100, 2)
                last_update_milis = int(datapoint.get('modifiedTimeMillis', 0))
                if not last_update_milis:
                    continue
                height_datapoints[last_update_milis] = height

        if height_datapoints:
            time_updates = list(height_datapoints.keys())
            time_updates.sort(reverse=True)

            last_time_update = time_updates[0]
            last_height = height_datapoints[last_time_update]

            self._last_updated = round(last_time_update / 1000)
            self._state = last_height
            print("Height: ", last_height)

            self._attributes = {}


class GoogleFitStepsSensor(GoogleFitSensor):
    DATA_SOURCE = "derived:com.google.step_count.delta:" \
                  "com.google.android.gms:estimated_steps"

    @property
    def _name_suffix(self):
        """Returns the name suffix of the sensor."""
        return STEPS

    @property
    def unit_of_measurement(self):
        """Returns the unit of measurement."""
        return STEPS

    @property
    def icon(self):
        """Return the icon."""
        return 'mdi:walk'

    @util.Throttle(MIN_TIME_BETWEEN_SCANS, MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        """Extracts the relevant data points for from the Fitness API."""

        values = []
        for point in self._get_dataset(self.DATA_SOURCE)["point"]:
            if int(point["startTimeNanos"]) > _today_dataset_start():
                values.append(point['value'][0]['intVal'])

        self._last_updated = time.time()
        self._state = sum(values)
        print("Steps: ", sum(values))
        self._attributes = {}


class GoogleFitMoveTimeSensor(GoogleFitSensor):
    DATA_SOURCE = "derived:com.google.active_minutes:" \
                  "com.google.android.gms:merge_active_minutes"

    @property
    def _name_suffix(self):
        """Returns the name suffix of the sensor."""
        return MOVE_TIME

    @property
    def unit_of_measurement(self):
        """Returns the unit of measurement."""
        return 'min'

    @property
    def icon(self):
        """Return the icon."""
        return 'mdi:clock-outline'

    @util.Throttle(MIN_TIME_BETWEEN_SCANS, MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        """Extracts the relevant data points for from the Fitness API."""

        values = []
        for point in self._get_dataset(self.DATA_SOURCE)["point"]:
            if int(point["startTimeNanos"]) > _today_dataset_start():
                values.append(point['value'][0]['intVal'])

        self._last_updated = time.time()
        self._state = sum(values)
        print("Move Time: ", sum(values))
        self._attributes = {}


class GoogleFitCaloriesSensor(GoogleFitSensor):
    DATA_SOURCE = "derived:com.google.calories.expended:" \
                  "com.google.android.gms:merge_calories_expended"

    @property
    def _name_suffix(self):
        """Returns the name suffix of the sensor."""
        return CALORIES

    @property
    def unit_of_measurement(self):
        """Returns the unit of measurement."""
        return CALORIES

    @property
    def icon(self):
        """Return the icon."""
        return 'mdi:food'

    @util.Throttle(MIN_TIME_BETWEEN_SCANS, MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        """Extracts the relevant data points for from the Fitness API."""
        values = []
        for point in self._get_dataset(self.DATA_SOURCE)["point"]:
            if int(point["startTimeNanos"]) > _today_dataset_start():
                values.append(point['value'][0]['fpVal'])

        self._last_updated = time.time()
        self._state = round(sum(values))
        print("Calories: ", round(sum(values)))
        self._attributes = {}


class GoogleFitDistanceSensor(GoogleFitSensor):
    DATA_SOURCE = "derived:com.google.distance.delta:" \
                  "com.google.android.gms:merge_distance_delta"

    @property
    def _name_suffix(self):
        """Returns the name suffix of the sensor."""
        return DISTANCE

    @property
    def unit_of_measurement(self):
        """Returns the unit of measurement."""
        return const.LENGTH_KILOMETERS

    @property
    def icon(self):
        """Return the icon."""
        return 'mdi:map-marker-distance'

    @util.Throttle(MIN_TIME_BETWEEN_SCANS, MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        """Extracts the relevant data points for from the Fitness API."""
        values = []
        for point in self._get_dataset(self.DATA_SOURCE)["point"]:
            if int(point["startTimeNanos"]) > _today_dataset_start():
                values.append(point['value'][0]['fpVal'])

        self._last_updated = time.time()
        self._state = round(sum(values) / 1000, 2)
        print("Distance: ", round(sum(values) / 1000, 2))
        self._attributes = {}

class GoogleFitSleepSensor(GoogleFitSensor):
    DATA_SOURCE = "derived:com.google.step_count.delta:" \
                  "com.google.android.gms:estimated_steps"

    @property
    def _name_suffix(self):
        """Returns the name suffix of the sensor."""
        return SLEEP

    @property
    def unit_of_measurement(self):
        """Returns the unit of measurement."""
        return SLEEP

    @property
    def icon(self):
        """Return the icon."""
        return 'mdi:clock'

    @util.Throttle(MIN_TIME_BETWEEN_SCANS, MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        """Extracts the relevant data points for from the Fitness API."""

        yesterday = datetime.now().replace(hour=17,minute=0,second=0,microsecond=0)
        yesterday = yesterday - timedelta(days=1)
        starttime = yesterday.isoformat("T") + "Z"
        today = datetime.now().replace(hour=11,minute=0,second=0,microsecond=0)
        endtime = today.isoformat("T") + "Z"
        print("Starttime: ", starttime , "Endtime: ", endtime)
        sleep_dataset =  self._client.users().sessions().list(userId='me',fields='session',startTime=starttime,endTime=endtime).execute()
        starts = []
        ends = []
        deep_sleep = []
        light_sleep = []
        # values = []
        #print(sleep_dataset)
        for point in sleep_dataset["session"]:
            if int(point["activityType"]) == 72 :
                starts.append(int(point["startTimeMillis"]))
                ends.append(int(point["endTimeMillis"]))
                if  point["name"].startswith('Deep'):   
                     deep_sleep_start = datetime.fromtimestamp(int(point["startTimeMillis"]) / 1000)
                     deep_sleep_end = datetime.fromtimestamp(int(point["endTimeMillis"]) / 1000)
                     #print(deep_sleep_start, deep_sleep_end , point["name"], "Total: ", (deep_sleep_end - deep_sleep_start) )
                     deep_sleep.append(deep_sleep_end - deep_sleep_start)
                elif  point["name"].startswith('Light'):        
                     light_sleep_start = datetime.fromtimestamp(int(point["startTimeMillis"]) / 1000)
                     light_sleep_end = datetime.fromtimestamp(int(point["endTimeMillis"]) / 1000)
                     #print(light_sleep_start, light_sleep_end , point["name"], "Total: ", (light_sleep_end - light_sleep_start) )
                     light_sleep.append(light_sleep_end - light_sleep_start)
        
        bed_time = datetime.fromtimestamp(round(min(starts) / 1000))
        wake_up_time = datetime.fromtimestamp(round(max(ends) / 1000))
        total_sleep = wake_up_time - bed_time
        total_deep_sleep = sum(deep_sleep,timedelta())
        total_light_sleep = sum(light_sleep, timedelta())
        state_dict = dict({'bed_time': str(bed_time), 'wake_up_time': str(wake_up_time), 'sleep': str(total_sleep), 'deep_sleep': str(total_deep_sleep), 'light_sleep': str(total_light_sleep)})
        # data = {'bed_time': str(bed_time), 'wake_up_time': str(wake_up_time), 'sleep': str(total_sleep)}
        # json_data = json.dumps(data)
        # print("Bed time: ", bed_time)
        # print("Wake up time: ", wake_up_time)
        # print("Sleep: ", total_sleep)
        # print("Deep sleep: ", total_deep_sleep )
        # print("Light sleep: ", total_light_sleep )
        print(state_dict)
     
        self._state = str(total_sleep)
        self._attributes = state_dict
        #self._sleep = json_data
        self._last_updated = time.time()