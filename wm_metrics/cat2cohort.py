# -*- coding: utf-8 -*-
#!/usr/bin/python
"""
cat2cohort.py
	The aim of this script is to allow program leaders to export a category
	filled with User pages into a WikiMetrics cohort CSV file in order to 
	perform their evaluation analysis.

	Test:
		python cat2cohort.py -l fr -c "Utilisateur participant au projet Afripédia"
"""
import mw_api, mw_util

def api_url(lang):
	"""
	Returns the URL of the API based on the language of Wikipedia.
	"""
	return "https://%s.wikipedia.org/w/api.php" % (lang)



def list_users(mw, category, lang):
	"""
	List users from a wiki category and print lines of the cohort CSV.
	"""
	list_query = mw_api.MwApiQuery(properties={
				"list"   : "categorymembers",
				"cmtitle": category,
				"cmprop" : "ids|title|timestamp",
				"cmtype" : "page",
				"cmsort" : "sortkey",
				"cmdir"  : "asc",
				"cmlimit": "max"
			})
	for page in mw.process_query(list_query):
		if ":" in page['title']:
			username = page['title'].split(":")[1]
			print "%s, %swiki" % (username, lang)

def main():
	"""
	Main function of the script cat2cohort.py
	"""
	from argparse import ArgumentParser
	description = "Export a Wiki category into a cohort"
	parser = ArgumentParser(description=description)

	parser.add_argument("-c", "--category",
    					type=str,
                        dest="category",
						metavar="CAT",
						required=True,
                        help="The wiki category to export")

	parser.add_argument("-l", "--lang",
                        type=str,
                        dest="lang",
                        metavar="LANG",
                        required=True,
                        help="Wiki language")

	args = parser.parse_args()
	mw = mw_api.MwWiki(url_api=api_url(args.lang))
	user_list = list_users(mw, mw_util.str2cat(args.category), args.lang)

if __name__ == "__main__":
	main()