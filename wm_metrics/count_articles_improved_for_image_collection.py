# -*- coding: utf-8 -*-

"""Analysing a Glamorous report to identify articles improved."""

import xml.dom.minidom
import urllib


def handle_node_attribute(node, tag_name, attribute_name):
    """Return the contents of a tag based on his given name inside of a given node."""
    element = node.getElementsByTagName(tag_name)
    attr = element.item(0).getAttribute(attribute_name)
    return attr


def get_articles_from_glamorous_xml(doc):
    articles = []
    for first_node in doc.childNodes:
        if first_node.localName == u'results':
            for details_node in first_node.childNodes:
                if details_node.localName == u'details':
                    for image_node in details_node.childNodes:
                        if image_node.localName == u'image':
                            project = handle_node_attribute(image_node, u'project', u'name')
                            for page_node in image_node.getElementsByTagName('page'):
                                page = page_node.getAttribute('title')
                                articles.append((project, page))
    return articles


def analyse_glamorous_xml(xml_text):
    doc = xml.dom.minidom.parseString(xml_text)
    articles_list = get_articles_from_glamorous_xml(doc)
    fused = ["%s:%s" % page for page in articles_list]
    print '\n'.join(sorted(fused))
    print len(fused)
    print len(set(fused))


def get_data_from_glamorous(category_name):
    url = make_glamorous_url(category_name)
    return urllib.urlopen(url).read()


def make_glamorous_url(category):
    url = 'https://tools.wmflabs.org/glamtools/glamorous.php?doit=1'
    url += '&category=%s' % category
    url += '&use_globalusage=1&ns0=1&show_details=1'
    url += '&projects[wikipedia]=1&projects[wikimedia]=1&projects[wikisource]=1&projects[wikibooks]=1&projects[wikiquote]=1&projects[wiktionary]=1&projects[wikinews]=1&projects[wikivoyage]=1&projects[wikispecies]=1&projects[mediawiki]=1&projects[wikidata]=1&projects[wikiversity]=1'
    url += '&format=xml'
    return url


def analyse_category(category_name):
    data = get_data_from_glamorous(category_name)
    analyse_glamorous_xml(data)


def main():
    from argparse import ArgumentParser

    description = "Export a Wiki category into a cohort"
    parser = ArgumentParser(description=description)

    parser.add_argument(type=str,
                        dest="category",
                        metavar="CATEGORY",
                        help="The Commons category to analyse ")

    args = parser.parse_args()
    category_name = args.category.replace(' ', '_')
    analyse_category(category_name)


if __name__ == "__main__":
    main()
