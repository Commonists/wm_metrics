#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import urllib


class Traffic:

    """Wikipedia article statistics."""

    def __init__(self, title, site):
        self.site = site
        self.title = title

    def _make_url(self, year, month):
        """Make the URL to the JSON output of stats.grok.se service."""
        return "http://stats.grok.se/json/{0:s}/{1:d}{2:02d}/{3:s}".format(self.site, year, month, self.title)

    def _make_url_latest(self, latest):
        """Make URL to the JSON output of stats.grok.se service for lastest traffic.

        Args:
            latest (int): 30, 60 or 90
        """
        if not latest in [30, 60, 90]:
            raise ValueError("Expected 30, 60 or 90 instead of %s" % (latest))
        return "http://stats.grok.se/json/{0:s}/latest{1:d}/{2:s}".format(self.site, latest, self.title)

    def get_month_traffic(self, year, month):
        """Fetch the month traffic statistics."""
        return json.loads(urllib.urlopen(self._make_url(year, month)).read())

    def get_latest_traffic(self, latest):
        """Fetch the latest traffic statistics."""
        return json.loads(urllib.urlopen(self._make_url_latest(latest)).read())
