#-*- coding: utf-8 -*-
#!/usr/bin/python

""" Compute the induced Category of a Category.

Induced category of a category C is a category created to describe
images of category C.
"""

import mw_api
import mw_util
import json
import codecs
import MySQLdb
import operator
import sys
from collections import Counter

reload(sys)
sys.setdefaultencoding("utf-8")


class CategoryInduced:

    def __init__(self, category):
        url_api = 'https://commons.wikimedia.org/w/api.php'
        self.commons = mw_api.MwWiki(url_api=url_api)
        self.category = category.replace(" ", "_").decode('utf-8')
        self.categories = []
        self.first_images = []
        """"DB instantiation"""
        self.db = MySQLdb.connect(host="commonswiki.labsdb",
            db="commonswiki_p", read_default_file="~/replica.my.cnf", charset='utf8')
        self.cursor = self.db.cursor()
        # TODO: prendre que des images
        self.query = """SELECT page.page_title
                        FROM page
                        JOIN categorylinks ON page.page_id = categorylinks.cl_from
                        WHERE categorylinks.cl_to = %s AND categorylinks.cl_type = "file"
                        ORDER BY categorylinks.cl_timestamp ASC
                        LIMIT 1;"""

    def list_category(self):
        """ Returns List categories inside self.category. """
        import os.path
        cache_name = "cache/%s.cache" % (self.category)
        result = None
        if False:
            result = None
    #    if os.path.exists(cache_name):
    #        cache = codecs.open(cache_name, 'r', 'utf-8')
    #        result = json.loads(cache.read())
        else:
            res = []
          #  c = Counter()
            lastContinue = ""
            props = {
                "prop": "categories",
                "cllimit": "max",
                #          "cldir" : "ascending",
                "generator": "categorymembers",
                "gcmtitle": self.category,
                "gcmprop": "title",
                "gcmlimit": 20
            }
            while True:
                result = json.loads(
                    self.commons.send_to_api(mw_api.MwApiQuery(properties=props)))
                dic = result[u'query'][u'pages']
                list = sorted(
                    dic.iteritems(), reverse=False, key=operator.itemgetter(1))
                liste2 = [x[1][u'categories']
                          for x in list if u'categories' in x[1].keys()]
                for l in liste2:
                    categories = [x[u'title'] for x in l]
                    res.extend(categories)
       #             c.update(categories)
                if 'query-continue' in result.keys() and 'categorymembers' in result['query-continue'].keys():
                    lastContinue = result['query-continue']['categorymembers']
                    self.update(props, lastContinue)
                else:
                    break
  #  print "%s elements with %s unique ones" % (sum(c.values()), len(c.keys()))
        return set(res)

    def smart_append(self, l2, l1):
        for e in l1:
            if e not in l2:
                l2.append(e)

    def first_image(self, category):
        self.catsql = category.replace("Category:", "").replace(" ", "_")
        self.cursor.execute(self.query, self.catsql)
        cat_content = self.catsql.encode('utf-8')
        first_content = [x[0].decode('utf-8') for x in self.cursor.fetchall()]
        res = [cat_content, first_content]
        return res

    def list_images(self):
        import os.path
        cache_name = "cache/%s.cache" % (self.category)
        list = []
        lastContinue = ""
        props = {
            "list": "categorymembers",
            "cmtitle": self.category,
                    "cmprop": "title",
                    "cmlimit": "max",
        }
        while True:
            result = json.loads(
                self.commons.send_to_api(mw_api.MwApiQuery(props)))
            res1 = [x[u'title'] for x in result[u'query'][u'categorymembers']]
            res = [x.encode('utf-8') for x in res1]
            list.extend(res)
            if 'query-continue' in result.keys() and 'categorymembers' in result['query-continue'].keys():
                lastContinue = result['query-continue']['categorymembers']
                self.update(props, lastContinue)
            else:
                break
        return list

    def update(self, props, lastContinue):
        for p in lastContinue:
            props[p] = lastContinue[p]


def induce_categories(category):
    ci = CategoryInduced(category)
    ci.categories = ci.list_category()
    first_images = [ci.first_image(x) for x in ci.categories]
    first_images.sort()
    categories_count = len(first_images)
    images = [x.decode('utf-8')[5:].replace(" ", "_") for x in ci.list_images()]
    images_count = len(images)
    result = [first_images[x][0] for x in range(len(first_images))
              if (len(first_images[x][1]) > 0
                  and first_images[x][1][0] in images)]
    result.sort()
    results_count = len(result)
    categories_traversed_count = len(first_images)

    print "--------------------first images--------------------"
    print "%s categories to check" % categories_traversed_count
    print "----------------------images------------------------"
    print "%s images" % images_count
    print "----------------------result------------------------"
    print "%s new categories created" % results_count
    print result


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
    induce_categories(category)


if __name__ == "__main__":
    main()
