import fdc
from commons_cat_metrics import CommonsCatMetrics
import wmflabs_queries


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

        self.quarters = [CommonsCatMetrics(category, fdc_round.to_period_for_quarter(i + 1), cursor=cursor)
                         for i in range(4)]
        self.nb_files = None
        self.nb_labels = None
        self.nb_uploaders = None
        self.global_usage = None
        self.pixel_count = None

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
        query = wmflabs_queries.count_uploaders_in_category()
        self.cursor.execute(query, (cat, self.fdc_round.full_period()['start'], self.fdc_round.full_period()['end']))
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
