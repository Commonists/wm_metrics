#!/usr/bin/python
# -*- coding: utf-8  -*-
""" wmflabs_queries.py regroups query builder functions in order to generate queries for wmflabs databases.
"""


def category_flatt(category):
    """
    category_flattening
            List all subcategories of given category
    """
    return """SELECT page.page_title
	FROM categorylinks
	JOIN page ON page.page_id = categorylinks.cl_from
	WHERE page.page_namespace = 14 AND categorylinks.cl_to = '%s";""" % (category)


def main():
    categories = category(
        "Content_media_by_years_and_quarters_-_Supported_by_Wikimedia_France_-_2014_-_2")
    print categories

if __name__ == "__main__":
    main()
