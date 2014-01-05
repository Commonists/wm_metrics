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
			yield (username, lang)


def cat_to_cohort(language, category):
    """Get the user list from the given category and language."""
    mw = mw_api.MwWiki(url_api=api_url(language))
    user_list = list_users(mw, mw_util.str2cat(category), language)
    csv_text = _userlist_to_CSV_cohort(user_list)
    return csv_text


def _userlist_to_CSV_cohort(user_list):
    """Return the given user list as a CSV cohort."""
    return '\n'.join([_make_CSV_line(username, language)
                      for (username, language) in user_list])


def _make_CSV_line(username, language):
    """Return a WikiMetrics compatible CSV line."""
    return "%s, %swiki" % (username, language)


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
	print cat_to_cohort(args.lang, args.category)


if __name__ == "__main__":
	main()