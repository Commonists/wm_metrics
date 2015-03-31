"""
This script computes metrics for FDC on an image category of Wikimedia Commons.

The following line computes metrics for files in "Media supported by Wikimedia France"
and for the FDC report of year 2012-2013 round 2 quarter 3

python commons_cat_metrics.py --year 2012-2013 --round 2 --quarter 3 --category "Media supported by Wikimedia France"

Please use python commons_cat_metrics.py -h for more information
"""
import fdc
import MySQLdb
import mw_util
from argparse import ArgumentParser
import wmflabs_queries


def get_commons_db():
    """Returns an instance of MySQLdb.connect() to tool labs SQL for Wikimedia Commons"""
    return MySQLdb.connect(host="commonswiki.labsdb", db="commonswiki_p", read_default_file="~/replica.my.cnf", charset='utf8')


class Indicators:

    """ This class allows to generate fdc.Indicator for:
            file upload count
            file labels count
            file uploader count
    """

    def __init__(self, category, fdc_round, cursor=None):
        """ Constructor

        Args:
            category (string): Category name (without 'Category:' prefix)
            fdc_round (fdc.Round): FDC round
            cursor (MySQLdb cursor): optional connection to mysql server
        """
        # All quarters
        self.category = category
        self.cursor = cursor
        self.fdc_round = fdc_round
        self.quarters = [CommonsCatMetrics(category, fdc_round, i + 1, cursor=cursor)
                         for i in range(4)]
        self.nb_files = None
        self.nb_labels = None
        self.nb_uploaders = None
        self.global_usage = None

    def nb_files_indicator(self, name):
        """ Returns an FDC indicator with count of files uploaded during q1, q2, q3, q4 and total (value). 

        Args:
            name (str): name of the fdc.Indicator

        Returns:
            fdc.Indicator with the number of file for each quarter and total over the whole period
        """
        if self.nb_files is None:
            self.nb_files = [self.quarters[i].get_nb_files() for i in range(4)]
        return fdc.Indicator(name,
                             q1=self.nb_files[0],
                             q2=self.nb_files[1],
                             q3=self.nb_files[2],
                             q4=self.nb_files[3],
                             value=sum(self.nb_files))

    def nb_labels_indicator(self, name):
        """ Returns an FDC indicator with count of files uploaded during q1, q2, q3, q4 and total and which
        are either FP, QI or VI.

        Args:
            name (str): name of the fdc.Indicator
        """
        if self.nb_labels is None:
            self.nb_labels = [
                self.quarters[i].get_nb_featured_files() for i in range(4)]
        return fdc.Indicator(name,
                             q1=self.nb_labels[0],
                             q2=self.nb_labels[1],
                             q3=self.nb_labels[2],
                             q4=self.nb_labels[3],
                             value=sum(self.nb_labels))

    def __percent(self, a, b, decimals=2):
        """ Percentage of a/b rounded with decimals. If b==0 it returns None.

        Args:
            a: numerator
            b: denominator
            decimals: amount of decimals to return (default 2)

        Returns:
            100*a/b 
        """
        if b == 0:
            return None
        else:
            return round(100 * float(a) / b, decimals)

    def pct_labels_indicator(self, name):
        """ Returns an FDC indicator with percentage of files uploaded during q1, q2, q3, q4 and total and which
            are either FP, QI or VI.

            Args:
                name (str): name of the fdc.Indicator
        """
        if self.nb_files is None:
            self.nb_files = [self.quarters[i].get_nb_files() for i in range(4)]
        if self.nb_labels is None:
            self.nb_labels = [
                self.quarters[i].get_nb_featured_files() for i in range(4)]
        return fdc.Indicator(name,
                             q1=self.__percent(
                                 self.nb_labels[0], self.nb_files[0]),
                             q2=self.__percent(
                                 self.nb_labels[1], self.nb_files[1]),
                             q3=self.__percent(
                                 self.nb_labels[2], self.nb_files[2]),
                             q4=self.__percent(
                                 self.nb_labels[3], self.nb_files[3]),
                             value=self.__percent(sum(self.nb_labels), sum(self.nb_files)))

    def nb_uploaders_indicator(self, name):
        """ Returns an FDC indicator with count of uploaders that have uploaded during q1, q2, q3, q4 and total (value). 

        Args:
            name (str): name of the fdc.Indicator

        Returns:
            fdc.Indicator with the number of file for each quarter and total over the whole period
        """
        if self.nb_uploaders is None:
            self.nb_uploaders = [
                self.quarters[i].get_nb_uploaders() for i in range(4)]

        cat = self.category.replace(" ", "_")
        query = wmflabs_queries.count_uploaders_in_category(
            cat, self.fdc_round.full_period()['start'], self.fdc_round.full_period()['end'])
        self.cursor.execute(query)
        total = long(self.cursor.fetchone()[0])

        return fdc.Indicator(name,
                             q1=self.nb_uploaders[0],
                             q2=self.nb_uploaders[1],
                             q3=self.nb_uploaders[2],
                             q4=self.nb_uploaders[3],
                             value=total)

    def total_usage_indicator(self, name):
        """ Returns an FDC indicator with count of usages of image from the category.

        Args:
            name (str): name of the fdc.Indicator
        """
        if self.global_usage is None:
            self.global_usage = self.quarters[0].get_global_usage()
        return fdc.Indicator(name, value=self.global_usage['total usage'])

    def nb_image_used_indicator(self, name):
        """ Returns an FDC indicator with count of image used from the category. 

        Args:
            name (str): name of the fdc.Indicator
        """
        if self.global_usage is None:
            self.global_usage = self.quarters[0].get_global_usage()
        return fdc.Indicator(name, value=self.global_usage['images used'])

    def nb_wiki_indicator(self, name):
        """ Returns an FDC indicator with count of wiki using an image from the category. 

        Args:
            name (str): name of the fdc.Indicator
        """
        if self.global_usage is None:
            self.global_usage = self.quarters[0].get_global_usage()
        return fdc.Indicator(name, value=self.global_usage['nb wiki'])

    def pixel_count_indicator(self, name):
        if self.pixel_count is None:
            self.pixel_count = [
                self.quarters[i].get_pixel_count() for i in range(4)]

        return fdc.Indicator(name,
                             q1=self.pixel_count[0],
                             q2=self.pixel_count[1],
                             q3=self.pixel_count[2],
                             q4=self.pixel_count[3],
                             value=sum(self.pixel_count))


class CommonsCatMetrics:

    """Wrapper class for the Category Metrics"""

    def __init__(self, category, round_fdc, q, cursor=None):
        """Constructor

        Args:
            category (string): Category name (without 'Category:' prefix)
            round_fdc (fdc.Round): FDC round
            q (int): quarter
            cursor (MySQLdb cursor): optional connection to mysql server
        """
        self.catsql = category.replace(" ", "_")

        if cursor is None:
            db = get_commons_db()
            self.cursor = db.cursor()
        else:
            self.cursor = cursor

        # round fdc
        timestamps = round_fdc.quarter(q)
        self.timestamp1 = timestamps['start']
        self.timestamp2 = timestamps['end']

    def get_nb_uploaders(self):
        """Amount of uploaders on the period."""
        query = wmflabs_queries.count_uploaders_in_category(
            self.catsql, self.timestamp1, self.timestamp2)
        self.cursor.execute(query)
        return long(self.cursor.fetchone()[0])

    def get_nb_files(self):
        """Amount of files uploaded on the period."""
        query = wmflabs_queries.count_files_in_category(
            self.catsql, self.timestamp1, self.timestamp2)
        self.cursor.execute(query)
        return long(self.cursor.fetchone()[0])

    def get_nb_featured_files(self):
        """Amount of files that are either FP, VI or QI on Wikimedia Commons."""
        query = wmflabs_queries.count_featured_files_in_category(
            self.catsql, self.timestamp1, self.timestamp2)
        self.cursor.execute(query)
        return long(self.cursor.fetchone()[0])

    def get_global_usage(self, main=False):
        """ Get global usage metrics (total usages, nb of images used, nb of wiki)
        of files in categories.

        Args:
            main (boolean): whether we only count for main namespaces.
        """
        query = wmflabs_queries.global_usage_count(self.catsql, main=main)
        self.cursor.execute(query)
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
        query = wmflabs_queries.pixel_count(self.catsql, self.timestamp1, self.timestamp2)
        self.cursor.execute(query)
        return long(self.cursor.fetchone()[1])

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

    # fetching metrics
    metrics = CommonsCatMetrics(category, fdc_round, args.quarter)
    global_usage = metrics.get_global_usage()
    nb_files = metrics.get_nb_files_alltime()

    # printing results
    print "nb uploaders: %d\nnb files: %d\nnb featured content: %d" % (metrics.get_nb_uploaders(), metrics.get_nb_files(),  metrics.get_nb_featured_files())
    print "global usage(as of now):"
    print "\tnb files: %d" % nb_files
    print "\ttotal usages: %d" % global_usage['total usage']
    print "\timages in use: %d (%.2f %%)" % (global_usage['images used'], 100. * float(global_usage['images used']) / nb_files)
    print "\tnb wiki: %d" % global_usage['nb wiki']

    # closing SQL connection
    metrics.close()

if __name__ == "__main__":
    main()
