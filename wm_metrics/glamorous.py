#!/usr/bin/python
"""
glamorous.py
	A Glamorous parser to retieve file usage among the wikimedia projects.
"""
from HTMLParser import HTMLParser
from argparse import ArgumentParser
import urllib

class GlamorousParser(HTMLParser, object):
	"""
	HTML parser glamorous
	"""
	def __init__(self, category):
		super(GlamorousParser, self).__init__()
		self.category = category
		self.page = urllib.urlopen(self.__category_url__()).read()
		self.status = 0
		self.result = dict()
		self.label = None
		self.feed(self.page)

	def __category_url__(self):
		""" 
		Return the URL to glamorous of the category
		"""
		return "http://tools.wmflabs.org/glamtools/glamorous.php?doit=1&category=%s&use_globalusage=1&ns0=1" % self.category

	def handle_starttag(self, tag, attrs):
		if tag == 'th' and self.status==0:
			self.status = 1
		if tag == 'th' and self.status==3:
			self.status = 4 
		if tag == 'td' and self.status==4:
			self.status = 5

	def handle_endtag(self, tag):
		if tag == 'th' and self.status==1:
			self.status=0
		if tag == 'td' and self.status==5:
			self.status=3

	def handle_data(self, data):
		if data.strip() == 'Images used':
			self.status=3
		if self.status==4:
			self.label = data
		if self.status==5:
			self.result[self.label]=data


def main():
	"""Main function of the script glamorous.py."""
	parser = ArgumentParser(description="Glamorous wrapper")

	parser.add_argument("-c", "--category",
                        type=str,
                        dest="category",
                        metavar="CAT",
                        required=True,
                        help="The Commons category without Category:")
	args = parser.parse_args()
	glamorous = GlamorousParser(args.category)
	print glamorous.result

if __name__ == "__main__":
	main()
