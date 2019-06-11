import json
import logging
from urllib import parse

import voluptuous as vol
import homeassistant.helpers.config_validation as cv
try:
    # Pre v0.91
    from homeassistant.components.media_player.kodi import (
        CONF_TCP_PORT, DEFAULT_TCP_PORT, KodiDevice)
except ImportError:
    # >= v0.91
    from homeassistant.components.kodi.media_player import (
        CONF_TCP_PORT, DEFAULT_TCP_PORT, KodiDevice)
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (
    CONF_HOST, CONF_PASSWORD, CONF_PORT, CONF_USERNAME)
from homeassistant.helpers.entity import Entity


__version__ = '0.2.5'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_HOST, default='localhost'): cv.string,
    vol.Optional(CONF_PORT, default=8080): cv.port,
    vol.Optional(CONF_TCP_PORT, default=DEFAULT_TCP_PORT): cv.port,
    vol.Inclusive(CONF_USERNAME, 'auth'): cv.string,
    vol.Inclusive(CONF_PASSWORD, 'auth'): cv.string,
})
_LOGGER = logging.getLogger(__name__)


async def async_setup_platform(hass, config, async_add_entities,
                               discovery_info=None):
    sensors = [
        KodiRecentlyAddedMoviesSensor(hass, config),
        KodiRecentlyAddedTVSensor(hass, config)
    ]
    async_add_entities(sensors, True)


class KodiMediaSensor(Entity):

    def __init__(self, hass, config):
        self.kodi = KodiDevice(
            hass, self.name, config.get(CONF_HOST), config.get(CONF_PORT),
            config.get(CONF_TCP_PORT), username=config.get(CONF_USERNAME),
            password=config.get(CONF_PASSWORD))
        self._state = None
        self.data = []

    @property
    def state(self):
        return self._state


class KodiRecentlyAddedTVSensor(KodiMediaSensor):

    properties = [
        'art', 'dateadded', 'episode', 'fanart', 'firstaired', 'playcount',
        'rating', 'runtime', 'season', 'showtitle', 'title'
    ]

    @property
    def name(self):
        return 'kodi_recently_added_tv'

    @property
    def device_state_attributes(self):
        attrs = {}
        card_json = [{
            'title_default': '$title',
            'line1_default': '$episode',
            'line2_default': '$release',
            'line3_default': '$rating - $runtime',
            'line4_default': '$number',
            'icon': 'mdi:arrow-down-bold',
        }]
        for show in self.data:
            try:
                card = {
                    'airdate': show['dateadded'].replace(' ', 'T') + 'Z',
                    'episode': show['title'],
                    'fanart': '',
                    'flag': show['playcount'] == 0,
                    'genres': '',
                    'number': 'S{0:0>2}E{1:0>2}'.format(
                        show['season'], show['episode']),
                    'poster': '',
                    'release': '$day, $date',
                    'runtime': show['runtime'] // 60,
                    'title': show['showtitle'],
                    'studio': '',
                }
                rating = round(show['rating'], 1)
                if rating:
                    rating = '\N{BLACK STAR} {}'.format(rating)
                card['rating'] = rating
                fanart = show['art'].get('tvshow.fanart', '')
                poster = show['art'].get('tvshow.poster', '')
                if fanart:
                    card['fanart'] = parse.unquote(fanart)[8:].strip('/')
                if poster:
                    card['poster'] = parse.unquote(poster)[8:].strip('/')
            except KeyError:
                _LOGGER.exception('Error parsing key from tv blob: %s', show)
            card_json.append(card)
        attrs['data'] = json.dumps(card_json)
        return attrs

    async def async_update(self):
        result = await self.kodi.async_call_method(
            'VideoLibrary.GetRecentlyAddedEpisodes',
            properties=self.properties)
        if result:
            try:
                self.data = result['episodes']
            except KeyError:
                _LOGGER.exception(
                    'Unexpected result while fetching tv shows: %s', result)


class KodiRecentlyAddedMoviesSensor(KodiMediaSensor):

    properties = [
        'art', 'dateadded', 'genre', 'playcount', 'premiered', 'rating',
        'runtime', 'studio', 'title']

    @property
    def name(self):
        return 'kodi_recently_added_movies'

    @property
    def device_state_attributes(self):
        attrs = {}
        card_json = [{
            'title_default': '$title',
            'line1_default': '$genres',
            'line2_default': '$release',
            'line3_default': '$rating - $runtime',
            'line4_default': '$studio',
            'icon': 'mdi:arrow-down-bold',
        }]
        for show in self.data:
            try:
                card = {
                    'aired': show['premiered'],
                    'airdate': show['dateadded'].replace(' ', 'T') + 'Z',
                    'flag': show['playcount'] == 0,
                    'genres': ','.join(show['genre']),
                    'rating': round(show['rating'], 1),
                    'release': '$date',
                    'runtime': show['runtime'] // 60,
                    'title': show['title'],
                    'studio': ','.join(show['studio']),
                }
                rating = round(show['rating'], 1)
                if rating:
                    rating = '\N{BLACK STAR} {}'.format(rating)
                card['rating'] = rating
                fanart = show['art'].get('fanart', '')
                poster = show['art'].get('poster', '')
            except KeyError:
                _LOGGER.exception(
                    'Error parsing key from movie blob: %s', show)
            if fanart:
                fanart = parse.unquote(fanart)[8:].strip('/')
            if poster:
                poster = parse.unquote(poster)[8:].strip('/')
            card['fanart'] = fanart
            card['poster'] = poster
            card_json.append(card)
        attrs['data'] = json.dumps(card_json)
        return attrs

    async def async_update(self):
        result = await self.kodi.async_call_method(
            'VideoLibrary.GetRecentlyAddedMovies', properties=self.properties)
        if result:
            try:
                self.data = result['movies']
            except KeyError:
                _LOGGER.exception(
                    'Unexpected result while fetching movies: %s', result)