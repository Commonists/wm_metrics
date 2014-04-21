import fdc
import MySQLdb
import mw_util
from argparse import ArgumentParser
import wmflabs_queries

T1 = "20140101000000"  
T2 = "20140401000000"

class CommonsCatMetrics:
	"""Wrapper class for the Category Metrics"""
	def __init__(self, category, round_fdc, q):
		self.catname = category
		self.catsql = category.replace(" ", "_")
		self.db = MySQLdb.connect(host="commonswiki.labsdb", db="commonswiki_p", read_default_file="~/replica.my.cnf")
		self.cursor = self.db.cursor()
		# round fdc
		timestamps = round_fdc.quarter(q)
		self.timestamp1 = timestamps['start']
		self.timestamp2 = timestamps['end']

	def get_nb_uploaders(self, timestamp1, timestamp2):
		"""Amount of uploaders on the period"""
		query = wmflabs_queries.count_uploaders_in_category(self.catsql, self.timestamp1, self.timestamp2)
		self.cursor.execute(query)
		return long(self.cursor.fetchone()[0])

	def get_nb_files(self, timestamp1, timestamp2):
		query = wmflabs_queries.count_files_in_category(self.catsql, self.timestamp1, self.timestamp2)
		self.cursor.execute(query)
		return long(self.cursor.fetchone()[0])

	def get_nb_featured_files(self, timestamp1, timestamp2):
		query = wmflabs_queries.count_featured_files_in_category(self.catsql, self.timestamp1, self.timestamp2)
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
			'nb wiki': long(result[2]) }

	def get_nb_files_alltime(self):
		""" Returns nb of files in category. """
		query = wmflabs_queries.count_files_in_category_alltime(self.catsql)
		self.cursor.execute(query)
		return long(self.cursor.fetchone()[0])

	def glamorous(self):
		"""wrapper to glamorous"""
		import glamorous
		glamorous = glamorous.GlamorousParser(self.catname)
		glamorous.statistics()

	def close(self):
		self.db.close()

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
	args = parser.parse_args()
	years = [int(y) for y in args.years.split('-')]
	fdc_round = fdc.Round(years[0], years[1], args.round)
	metrics = CommonsCatMetrics(args.category, fdc_round, args.quarter)
	print "nb uploaders: %d\nnb files: %d\nnb featured content: %d" % (metrics.get_nb_uploaders(T1, T2), metrics.get_nb_files(T1, T2), 	metrics.get_nb_featured_files(T1, T2))
	global_usage = metrics.get_global_usage()
	nb_files = metrics.get_nb_files_alltime()
	print "global usage(as of now):"
	print "\tnb files: %d" % nb_files
	print "\ttotal usages: %d" % global_usage['total usage']
	print "\timages in use: %d (%.2f%)" % (global_usage['images used'], 100.*float(global_usage['images used'])/nb_files)
	metrics.close()

if __name__ == "__main__":
	main()