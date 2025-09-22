import xml.etree.ElementTree as ET
import datetime as dt

import numpy as np

from fmiopendata import wfs
from fmiopendata.utils import read_url

TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


class Station(object):
    """Class for holding station data."""

    def __init__(self, xml, mode):
        """Initialize the class."""
        self._xml = ET.fromstring(xml)
        self.latitudes = []
        self.longitudes = []
        self.begin_dates = []
        self.identifiers = []
        self.names = []
        self.types = []

        self._parse(self._xml)

    def _parse_locations(self, xml):
        """Parse location data."""
        for point in xml.findall(wfs.GML_POINT):
            location = tuple(float(p) for p in point.findtext(wfs.GML_POS).split())
            self.latitudes.append(location[0])
            self.longitudes.append(location[1])

    def _parse_ids(self, xml):
        """Parse station identifiers."""
        for id in xml.findall(wfs.INS_ID):
            fmisid = int(id.findtext(wfs.INS_LOCALID))
            self.identifiers.append(fmisid)

    def _parse_times(self, xml):
        """Parse station begin times."""
        for activity in xml.findall(wfs.EF_ACTIVITY_TIME):
            beg = dt.datetime.strptime(activity.findtext(wfs.GML_BEGIN_POSITION), TIME_FORMAT)
            self.begin_dates.append(beg)

    def _parse_types(self, xml):
        """Parse station types."""
        for station_type in xml.findall(wfs.EF_BELONGS_TO):
            stype = station_type.get(wfs.TITLE)
            self.types.append(stype)

    def _parse_names(self, xml):
        """Parse station names."""
        for monitoring_facility in xml.findall(wfs.EF_MONITORING_FACILITY):
            name = monitoring_facility.findtext(wfs.EF_NAME)
            self.names.append(name)

    def _parse(self, xml):
        """Parse data."""
        self._parse_locations(xml)
        self._parse_ids(xml)
        self._parse_times(xml)
        self._parse_types(xml)
        self._parse_names(xml)


def download_and_parse(query_id, args=None):
    """Download and parse the given stored query."""
    url = wfs.STORED_QUERY_URL + query_id
    if args:
        url = url + "&" + "&".join(args)
    xml = read_url(url)
    mode = query_id.split("::")[-1]
    return Station(xml, mode)
