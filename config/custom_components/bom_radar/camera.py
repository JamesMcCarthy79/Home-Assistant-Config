"""
Camera that loads a picture from a local file.
For more details about this platform, please refer to the documentation at
https://github.com/bremor/bom_radar/
"""
import datetime as DT
import ftplib
import io
import logging
import mimetypes
import os
import requests
from PIL import Image

import voluptuous as vol

from homeassistant.const import CONF_NAME
from homeassistant.components.camera import (
    Camera, CAMERA_SERVICE_SCHEMA, DOMAIN, PLATFORM_SCHEMA)
from homeassistant.helpers import config_validation as cv

_LOGGER = logging.getLogger(__name__)

CONF_PRODUCT_ID = 'product_id'
DEFAULT_NAME = 'BOM Radar'
SERVICE_BOM_RADAR_UPDATE = 'bom_radar_update'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_PRODUCT_ID): cv.string,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string
})

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Camera that works with local files."""
    camera = BOMRadar(config[CONF_NAME], config[CONF_PRODUCT_ID])

    def update_bom_radar_service(call):
        """Update the file path."""
        camera.update_file_path()
        return True

    hass.services.register(
        DOMAIN,
        SERVICE_BOM_RADAR_UPDATE,
        update_bom_radar_service)

    add_entities([camera])

class BOMRadar(Camera):
    """Representation of a local file camera."""

    def __init__(self, name, product_id):
        """Initialize Local File Camera component."""
        super().__init__()
        self._animation_file_obj = None
        self._base_image = None
        self._frames = []
        self._latest_frame_datetime = None
        self._name = name
        self._product_id = product_id

    def camera_image(self):
        """Return image response."""
        return self.radar_update()

    def update_file_path(self):
        """Update the file_path."""
        self.schedule_update_ha_state()

    def radar_update(self):

        if not self._base_image:
            self.radar_background()

        if self._latest_frame_datetime and (self._latest_frame_datetime > (DT.datetime.utcnow().replace(second=0, microsecond=0) - DT.timedelta(minutes=10))):
            return self._animation_file_obj.getvalue()

        ftp = ftplib.FTP('ftp.bom.gov.au')
        ftp.login()
        ftp.cwd('anon/gen/radar/')

        i = 60
        while i >= 3:
            frame_datetime = DT.datetime.utcnow().replace(second=0, microsecond=0) - DT.timedelta(minutes=i)

            if self._latest_frame_datetime and self._latest_frame_datetime > frame_datetime:
                i -= 1
                continue
            elif self._latest_frame_datetime == frame_datetime:
                i -= 6
                continue

            frame_string = "{}.T.%Y%m%d%H%M.png".format(self._product_id)
            filename = frame_datetime.strftime(frame_string)

            file_obj = io.BytesIO()

            try:
                ftp.retrbinary('RETR ' + filename, file_obj.write)
                self._latest_frame_datetime = frame_datetime
                image = Image.open(file_obj).convert('RGBA')
                frame = self._base_image.copy()
                frame.paste(image, (0,0),image)
                self._frames.append(frame)
                if len(self._frames) > 6:
                    self._frames.pop(0)
                i -= 6
            except ftplib.all_errors:
                i -= 1

        ftp.quit()

        self._animation_file_obj = io.BytesIO()
        self._frames[0].save(self._animation_file_obj, format='GIF',
                            save_all=True,
                            append_images=self._frames[1:]+[self._frames[-1],self._frames[-1]],
                            duration=400,
                            loop=0)

        return self._animation_file_obj.getvalue()

    def radar_background(self): 

        layers = ['legend.0', 'background', 'topography', 'locations', 'range']
        url_builder = 'http://www.bom.gov.au/products/radar_transparencies/{}.{}.png'.format(self._product_id,'{}')

        for layer in layers:

            url = url_builder.format(layer) 

            if layer == 'legend.0':
                url = url.replace(self._product_id, 'IDR')
                self._base_image = Image.open(io.BytesIO(requests.get(url).content)).convert('RGBA')
            else:
                image = Image.open(io.BytesIO(requests.get(url).content)).convert('RGBA')
                self._base_image.paste(image, (0,0),image)

    @property
    def name(self):
        """Return the name of this camera."""
        return self._name