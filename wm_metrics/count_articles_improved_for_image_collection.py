# -*- coding: utf-8 -*-

"""Analysing a Glamorous report to identify articles improved."""

import sys
import xml.dom.minidom


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


def main():
    if len(sys.argv) < 2:
        print "Please provide a Glamourous file"
        sys.exit()
    xml_document = open(sys.argv[1], 'r')
    xml_text = xml_document.read()
    analyse_glamorous_xml(xml_text)


if __name__ == "__main__":
    main()
