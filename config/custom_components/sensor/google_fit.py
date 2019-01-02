"""Creates a Google Fit sensors.
At the moment, provides two measurements:
  - weight: in KG.
  - steps 
  - last_updated: entry of the current weight point.
Sensor is designed to be flexible and allow customization to add new Google Fit
dimensions with minimal effort with relative knowledge of Python and Fitness
Rest API.
In order to add this component as is, add a new sensor:
sensor:
  - platform: google_fit
    client_id: your_client_id
    client_secret: your_client_secret
In order to generate your client_id and client_secret, see the prerequisites for
Google Fit component:
https://www.home-assistant.io/components/calendar.google/#prerequisites
It is recommendable to store keep client_id and client_secret as secret as
possible. You can read about it on:
https://www.home-assistant.io/docs/configuration/secrets/
Example:
  - platform: google_fit
    client_id: !secret google_fit_client_id
    client_secret: !secret google_fit_client_secret
"""

import os

import enum
import httplib2
import logging
import voluptuous
import time
from datetime import datetime, timedelta
from googleapiclient import discovery as google_discovery
import json
from homeassistant import const
from homeassistant import util
from homeassistant.components import sensor
from homeassistant.helpers import entity
from homeassistant.helpers import config_validation
from homeassistant.helpers.event import track_time_change

from oauth2client import client as oauth2client
from oauth2client import file as oauth2file

REQUIREMENTS = [
    'google-api-python-client==1.6.4',
    'oauth2client==4.0.0',
]

_LOGGER = logging.getLogger(__name__)

# Sensor details.
SENSOR = 'google_fit'

# Sensor base attributes.
ATTR_LAST_UPDATED = 'last_updated'
CONF_CLIENT_ID = 'client_id'
CONF_CLIENT_SECRET = 'client_secret'
DEFAULT_NAME = 'google_fit'
DEFAULT_CREDENTIALS_FILE = '.google_fit.credentials.json'
ICON = 'mdi:heart-pulse'
MIN_TIME_BETWEEN_SCANS = timedelta(minutes=10)
MIN_TIME_BETWEEN_UPDATES = timedelta(minutes=10)
TOKEN_FILE = '.{}.token'.format(SENSOR)

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
WEIGHT ='weight'
DISTANCE = 'distance'
STEPS = 'steps'
TIME = 'time'
CALORIES = 'calories'

# Endpoint scopes required for the sensor.
# Read more: https://developers.google.com/fit/rest/v1/authorization

SCOPES = ['https://www.googleapis.com/auth/fitness.body.read',
          'https://www.googleapis.com/auth/fitness.activity.read',
          'https://www.googleapis.com/auth/fitness.location.read']

STEPS_DATA_SOURCE = "derived:com.google.step_count.delta:com.google.android.gms:estimated_steps"
MOVE_TIME_DATA_SOURCE = "derived:com.google.active_minutes:com.google.android.gms:merge_active_minutes"
DISTANCE_DATA_SOURCE = "derived:com.google.distance.delta:com.google.android.gms:merge_distance_delta"

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
    add_devices([GoogleFitSensor(token_file, 'Weight', 'Kg', WEIGHT),
                 GoogleFitSensor(token_file, 'Steps', 'Steps', STEPS),
                 GoogleFitSensor(token_file, 'Time', 'min', TIME),
                 GoogleFitSensor(token_file, 'Distance', 'km', DISTANCE)], True)


class GoogleFitSensor(entity.Entity):
    """Representation of a Google Fit Sensor.
    Currently supported: Weight and Last Update for Weight.
    However, the sensor it is designed to be extensible for other measures.
    """

    def __init__(self, token_file, name, unit_of_measurement, sensor_type):
        """Initializes the sensor.
        token_file: str, File path for API token.
        name: str, Name of the sensor.
        unit_of_measurement: str, Unit of measurement of sensor.
        """
        # Authenticate to application.
        self._client = self._get_client(token_file)

        # Device name.
        self._name = name
        self.type = sensor_type
        self._state = const.STATE_UNKNOWN
        self._steps = const.STATE_UNKNOWN
        self._weight = const.STATE_UNKNOWN
        self._unit_of_measurement = unit_of_measurement
        self._last_updated = const.STATE_UNKNOWN

    def _get_client(self, token_file):
        """Get the Google Fit service with the storage file token.
        Args:
          token_file: str, File path for API token.
        Return:
          Google Fit API client.
        """
        if not os.path.isfile(token_file):
            return

        credentials = oauth2file.Storage(token_file).get()
        http = credentials.authorize(httplib2.Http())
        service = google_discovery.build(
            'fitness', 'v1', http=http, cache_discovery=False)
        return service

    def nanoseconds(self, nanotime):
        """ Convert epoch time with nanoseconds to human-readable. """
        dt = datetime.fromtimestamp(nanotime // 1000000000)
        return dt.strftime('%Y-%m-%d %H:%M:%S')

    @property
    def name(self):
        """Returns the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Returns the state of the sensor. Currently: weight."""
        return self._state

    @property
    def steps(self):
        """Returns steps."""
        return self._steps

    @property
    def weight(self):
        """Returns weight."""
        return self._weight

    @property
    def unit_of_measurement(self):
        """Returns the unit of measurement."""
        return self._unit_of_measurement

    @property
    def last_updated(self):
        """Returns date when it was last updated."""
        return self._last_updated

    @property
    def state_attributes(self):
        """Returns the state attributes. """
        return {
            const.ATTR_FRIENDLY_NAME: self._name,
            const.ATTR_UNIT_OF_MEASUREMENT: self._unit_of_measurement,
            ATTR_LAST_UPDATED: self._last_updated,
        }

    @util.Throttle(MIN_TIME_BETWEEN_SCANS, MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        """Fetches new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        if not self._client:
            return

        if self.type == 'weight':
            self._update_weight_data()
        if self.type == 'steps':
            self._update_steps_data()
        if self.type == 'time':
            self._update_move_time_data()
        if self.type == 'distance':
            self._update_distance_data()

    def _get_datasources(self, data_type_name):
        """Gets data sources information for weight data.
        Args:
          data_type_name: str, Type of data sources to retrieve.
        Returns:
          Dictionary containing all available data sources.
        """
        datasources_request = self._client.users().dataSources().list(
            userId='me',
            dataTypeName=data_type_name,
        )
        data = datasources_request.execute()
        return data.get('dataSource')

    def _update_weight_data(self):
        """Extracts the relevant data points for the sensor from the Fitness API."""
        weight_datasources = self._get_datasources('com.google.weight')

        weight_datapoints = {}
        for datasource in weight_datasources:
            datasource_id = datasource.get('dataStreamId')
            weight_request = self._client.users().dataSources().dataPointChanges().list(
                userId='me',
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
            self._weight = last_weight
            print("Weight ", str(last_weight))

    def _update_steps_data(self):
        """Extracts the relevant data points for the sensor from the Fitness API."""

        TODAY = datetime.today().date()
        NOW = datetime.today()
        START = int(time.mktime(TODAY.timetuple()) * 1000000000)
        END = int(time.mktime(NOW.timetuple()) * 1000000000)
        DATA_SET = "%s-%s" % (START, END)

        dataset = self._client.users().dataSources(). \
            datasets(). \
            get(userId='me', dataSourceId=STEPS_DATA_SOURCE, datasetId=DATA_SET). \
            execute()
        starts = []
        ends = []
        values = []
        for point in dataset["point"]:
            if int(point["startTimeNanos"]) > START:
                starts.append(int(point["startTimeNanos"]))
                ends.append(int(point["endTimeNanos"]))
                values.append(point['value'][0]['intVal'])
            # print("From: ", self.nanoseconds(min(starts)))
            # print("To: ", self.nanoseconds(max(ends)))
            # print("Steps: %d" % sum(values))
        self._state = sum(values)
        self._steps = sum(values)
        print("Steps:", sum(values))

    def _update_move_time_data(self):
        """Extracts the relevant data points for the sensor from the Fitness API."""

        TODAY = datetime.today().date()
        NOW = datetime.today()
        START = int(time.mktime(TODAY.timetuple()) * 1000000000)
        END = int(time.mktime(NOW.timetuple()) * 1000000000)
        DATA_SET = "%s-%s" % (START, END)

        move_time_dataset = self._client.users().dataSources(). \
            datasets(). \
            get(userId='me', dataSourceId=MOVE_TIME_DATA_SOURCE, datasetId=DATA_SET). \
            execute()
        starts = []
        ends = []
        values = []
        for point in move_time_dataset["point"]:
            if int(point["startTimeNanos"]) > START:
                starts.append(int(point["startTimeNanos"]))
                ends.append(int(point["endTimeNanos"]))
                values.append(point['value'][0]['intVal'])
        self._state = sum(values)
        print("Move time: ", self._state)

    def _update_distance_data(self):
            TODAY = datetime.today().date()
            NOW = datetime.today()
            START = int(time.mktime(TODAY.timetuple()) * 1000000000)
            END = int(time.mktime(NOW.timetuple()) * 1000000000)
            DATA_SET = "%s-%s" % (START, END)

            distance_dataset = self._client.users().dataSources(). \
                datasets(). \
                get(userId='me', dataSourceId=DISTANCE_DATA_SOURCE, datasetId=DATA_SET). \
                execute()
            starts = []
            ends = []
            values = []
            for point in distance_dataset["point"]:
                if int(point["startTimeNanos"]) > START:
                    starts.append(int(point["startTimeNanos"]))
                    ends.append(int(point["endTimeNanos"]))
                    values.append(point['value'][0]['fpVal'])
            self._state = round(sum(values)/1000,2)
            print("Distance: ", sum(values)/1000)