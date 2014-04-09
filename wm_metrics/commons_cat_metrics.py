import MySQLdb
import mw_util
from argparse import ArgumentParser
import wmflabs_queries

T1 = "20140101000000"  
T2 = "20140401000000"

class CommonsCatMetrics:
	"""Wrapper class for the Category Metrics"""
	def __init__(self, category):
		self.catname = category
		self.catsql = category.replace(" ", "_")
		self.db = MySQLdb.connect(host="commonswiki.labsdb", db="commonswiki_p", read_default_file="~/replica.my.cnf")
		self.cursor = self.db.cursor()

	def get_nb_uploaders(self, timestamp1, timestamp2):
		"""Amount of uploaders on the period"""
		query = wmflabs_queries.count_uploaders_in_category(self.catsql, timestamp1, timestamp2)
		self.cursor.execute(query)
		return long(self.cursor.fetchone()[0])

	def get_nb_files(self, timestamp1, timestamp2):
		query = wmflabs_queries.count_files_in_category(self.catsql, timestamp1, timestamp2)
		self.cursor.execute(query)
		return long(self.cursor.fetchone()[0])

	def get_nb_featured_files(self, timestamp1, timestamp2):
		query = wmflabs_queries.count_featured_files_in_category(self.catsql, timestamp1, timestamp2)
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
	args = parser.parse_args()
	metrics = CommonsCatMetrics(args.category)
	print "nb uploaders: %d\nnb files: %d\nnb featured content: %d" % (metrics.get_nb_uploaders(T1, T2), metrics.get_nb_files(T1, T2), 	metrics.get_nb_featured_files(T1, T2))
	metrics.glamorous()
	metrics.close()

if __name__ == "__main__":
	main()