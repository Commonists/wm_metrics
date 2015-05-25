"""
This script computes metrics for FDC on an image category of Wikimedia Commons.

The following line computes metrics for files in "Media supported by Wikimedia France"
and for the FDC report of year 2012-2013 round 2 quarter 3

python commons_cat_metrics.py --year 2012-2013 --round 2 --quarter 3 --category "Media supported by Wikimedia France"

Please use python commons_cat_metrics.py -h for more information
"""
import MySQLdb
import logging
from argparse import ArgumentParser
import wmflabs_queries
import fdc

def get_commons_db():
    """Returns an instance of MySQLdb.connect() to tool labs SQL for Wikimedia Commons"""
    return MySQLdb.connect(host="commonswiki.labsdb", db="commonswiki_p", read_default_file="~/replica.my.cnf", charset='utf8')


class CommonsCatMetrics:

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


def main():
    """Commons Cat Metrics."""
    parser = ArgumentParser(description="Commons Cat Metrics")

    parser.add_argument("-c", "--category",
                        type=str,
                        dest="category",
                        metavar="CAT",
                        required=True,
                        help="The Commons category without Category:")
    parser.add_argument("-y", "--year",
                        type=str,
                        dest="years",
                        metavar="YEAR",
                        required=True,
                        help="The FDC year, e.g 2011-2012")
    parser.add_argument("-r", "--round",
                        type=int,
                        dest="round",
                        metavar="ROUND",
                        required=True,
                        help="The FDC round, i.e. 1 or 2")
    parser.add_argument("-q", "--quarter",
                        type=int,
                        dest="quarter",
                        metavar="QUARTER",
                        required=True,
                        help="The reporting quarter")
    # FDC round
    args = parser.parse_args()
    category = args.category.decode('utf-8')
    years = [int(y) for y in args.years.split('-')]

    fdc_round = fdc.Round(years[0], years[1], args.round)

    time_period = fdc_round.to_period_for_quarter(args.quarter)

    metrics = CommonsCatMetrics(category, time_period)
    global_usage = metrics.get_global_usage()
    nb_files = metrics.get_nb_files_alltime()
    pixel_count = metrics.get_pixel_count()

    # printing results
    print "nb uploaders: %d\nnb files: %d\nnb featured content: %d" % (metrics.get_nb_uploaders(), metrics.get_nb_files(), metrics.get_nb_featured_files())
    print "global usage(as of now):"
    print "\tnb files: %d" % nb_files
    print "\ttotal usages: %d" % global_usage['total usage']
    print "\timages in use: %d (%.2f %%)" % (global_usage['images used'], 100. * float(global_usage['images used']) / nb_files)
    print "\tnb wiki: %d" % global_usage['nb wiki']
    print "pixels: %d" % pixel_count

    # closing SQL connection
    metrics.close()

if __name__ == "__main__":
    main()
