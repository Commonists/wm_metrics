#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Compute the induced Category of a Category.

Induced category of a category C is a category created to describe
images of category C.
"""

import os

import mw_util
import mwclient
import MySQLdb
from _mysql_exceptions import OperationalError

NAMESPACE = {'image': 6, 'category': 14}


class DatabaseException(Exception):
    pass


class CategoryInduced:

    def __init__(self, category):
        self.category = category.replace(" ", "_").decode('utf-8')
        # mwclient
        self.site = mwclient.Site('commons.wikimedia.org')
        # results
        self.categories = []
        self.first_images = []
        # db
        self.init_database_connection()
        # TODO: prendre que des images
        self.query = """SELECT page.page_title
FROM page
JOIN categorylinks ON page.page_id = categorylinks.cl_from
WHERE categorylinks.cl_to = %s AND categorylinks.cl_type = "file"
ORDER BY categorylinks.cl_timestamp ASC
LIMIT 1;"""

    def init_database_connection(self):
        """Initialise the connection to the database."""
        try:
            host = "commonswiki.analytics.db.svc.wikimedia.cloud"
            self.db = MySQLdb.connect(host=host,
                                      db="commonswiki_p",
                                      read_default_file=os.path.expanduser("~/replica.my.cnf"),
                                      charset='utf8')
            self.cursor = self.db.cursor()
        except OperationalError:
            raise DatabaseException("Could not connect to host %s" % host)

    def list_category(self):
        """ Returns List categories inside self.category. """
        cat = self.site.Categories[self.category.replace('Category:', '')]
        subcats = [category.name for category in cat
                   if category.namespace == NAMESPACE['category']]
        return set(subcats)

    def first_image(self, category):
        self.catsql = category.replace("Category:", "").replace(" ", "_")
        self.cursor.execute(self.query, self.catsql)
        cat_content = self.catsql.encode('utf-8')
        first_content = [x[0].decode('utf-8') for x in self.cursor.fetchall()]
        res = [cat_content, first_content]
        return res

    def list_images(self):
        """List of images of self.categoryname"""
        cat = self.site.Categories[self.category.replace('Category:', '')]
        return [image.name for image in cat
                if image.namespace == NAMESPACE['category']]

    def update(self, props, lastContinue):
        for p in lastContinue:
            props[p] = lastContinue[p]

    def induce_categories(self):
        self.categories = self.list_category()
        first_images = [self.first_image(x) for x in self.categories]
        first_images.sort()
        self.images = [x.decode('utf-8')[5:].replace(" ", "_")
                       for x in self.list_images()]
        self.images_count = len(self.images)
        self.result = [first_images[x][0] for x in range(len(first_images))
                       if (len(first_images[x][1]) > 0 and
                           first_images[x][1][0] in self.images)]
        self.result.sort()
        self.results_count = len(self.result)
        self.categories_traversed_count = len(first_images)

    def print_report(self):
        print("--------------------first images--------------------")
        print("%s categories to check" % self.categories_traversed_count)
        print("----------------------images------------------------")
        print("%s images" % self.images_count)
        print("----------------------result------------------------")
        print("%s new categories created" % self.results_count)
        print(self.result)


def main():
    from argparse import ArgumentParser
    description = "Computes metrics about a commons category"
    parser = ArgumentParser(description=description)
    parser.add_argument("-c", "--category",
                        type=str,
                        dest="category",
                        metavar="CAT",
                        required=True,
                        help="The category on which we compute metrics")
    args = parser.parse_args()
    category = mw_util.str2cat(args.category)
    ci = CategoryInduced(category)
    ci.induce_categories()
    ci.print_report()


if __name__ == "__main__":
    main()
