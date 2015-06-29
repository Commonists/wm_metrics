"""Metrics for FDC on an image category of Wikimedia Commons."""

import logging
import wmflabs_queries
from database_connection import get_commons_db


class CommonsCatMetrics(object):

    """Wrapper class for the Category Metrics"""

    def __init__(self, category, period, cursor=None):
        """Constructor

        Args:
            category (string): Category name (without 'Category:' prefix)
            period (Period): period of time for the metrics observation
            cursor (MySQLdb cursor): optional connection to mysql server
        """
        self.catsql = category.replace(" ", "_")

        if cursor is None:
            db = get_commons_db()
            self.cursor = db.cursor()
        else:
            self.cursor = cursor

        self.timestamp1 = period.start
        self.timestamp2 = period.end

    def get_nb_uploaders(self):
        """Amount of uploaders on the period."""
        query = wmflabs_queries.count_uploaders_in_category()
        self.cursor.execute(query, (self.catsql, self.timestamp1, self.timestamp2))
        return long(self.cursor.fetchone()[0])

    def get_nb_files(self):
        """Amount of files uploaded on the period."""
        query = wmflabs_queries.count_files_in_category()
        self.cursor.execute(query, (self.catsql, self.timestamp1, self.timestamp2))
        return long(self.cursor.fetchone()[0])

    def get_nb_featured_files(self):
        """Amount of files that are either FP, VI or QI on Wikimedia Commons."""
        query = wmflabs_queries.count_featured_files_in_category()
        self.cursor.execute(query, (self.catsql, self.timestamp1, self.timestamp2))
        return long(self.cursor.fetchone()[0])

    def get_global_usage(self, main=False):
        """ Get global usage metrics (total usages, nb of images used, nb of wiki)
        of files in categories.

        Args:
            main (boolean): whether we only count for main namespaces.
        """
        query = wmflabs_queries.global_usage_count(main=main)
        self.cursor.execute(query, (self.catsql))
        result = self.cursor.fetchone()
        return {
            'total usage': long(result[0]),
            'images used': long(result[1]),
            'nb wiki': long(result[2])}

    def get_nb_files_alltime(self):
        """ Returns nb of files in category."""
        query = wmflabs_queries.count_files_in_category_alltime(self.catsql)
        self.cursor.execute(query)
        return long(self.cursor.fetchone()[0])

    def get_pixel_count(self):
        query = wmflabs_queries.pixel_count()
        self.cursor.execute(query, (self.catsql, self.timestamp1, self.timestamp2))
        try:
            count = long(self.cursor.fetchone()[0])
        except TypeError:
            logging.debug('Error querying Pixel Count. Assuming Zero.')
            count = 0
        return count

    def close(self):
        """Close the MariaDB connection."""
        self.cursor.close()

    def make_report(self):
        """Return a text report with all metrics."""
        text_report = ''
        nb_files = self.get_nb_files_alltime()
        pixel_count = self.get_pixel_count()

        global_usage = self.get_global_usage()
        images_in_use = global_usage['images used']
        percent_images_in_use = 100. * float(global_usage['images used']) / nb_files

        text_report += "nb uploaders: %d" % self.get_nb_uploaders()
        text_report += "nb files: %d" % self.get_nb_files(),
        text_report += "nb featured content: %d" % self.get_nb_featured_files()
        text_report += "global usage(as of now):"
        text_report += "\tnb files: %d" % nb_files
        text_report += "\ttotal usages: %d" % global_usage['total usage']
        text_report += "\timages in use: %d (%.2f %%)" % (images_in_use, percent_images_in_use)
        text_report += "\tnb wiki: %d" % global_usage['nb wiki']
        text_report += "pixels: %d" % pixel_count
        return text_report
