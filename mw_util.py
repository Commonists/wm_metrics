# -*- coding: utf-8 -*-
#!/usr/bin/python

"""
mw_util.py
	Set of helper functions while dealing with MediaWiki.

	str2cat
		Adds prefix Category if string doesn't have it.
"""

def str2cat(category):
	"""
	Returns a category name starting with Category:
	"""
	prefix = "Category:"
	if not category.startswith(prefix):
		return "%s%s" % (prefix, category)
	else:
		return category