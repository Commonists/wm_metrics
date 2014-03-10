# -*- coding: utf-8 -*-

import xml.dom.minidom
import re
import datetime


def handle_node(node, tag_name):
    """Return the contents of a tag based on his given name inside of a given node."""
    element = node.getElementsByTagName(tag_name)
    if element.length > 0:
        if element.item(0).hasChildNodes():
            return element.item(0).childNodes.item(0).data.rstrip()
    return ""


def timestamp_to_date(date):
    """Return a datetime object representing the given MediaWiki timestamp."""
    return datetime.datetime(int(date[0:4]),
                             int(date[5:7]),
                             int(date[8:10]),
                             int(date[11:13]),
                             int(date[14:16]),
                             int(date[17:19]),
                             )


def parse_xml_dump(xml_dump):
    """Return a list of the edits in a Wikimedia Commons dump."""
    edits = []
    doc = xml.dom.minidom.parse(xml_dump)
    for mediawiki_node in doc.childNodes:
        if mediawiki_node.localName == u'mediawiki':
            for page_node in mediawiki_node.childNodes:
                for revision_node in page_node.childNodes:
                    title = handle_node(page_node, u'title')
                    if revision_node.localName == u'revision':
                        username = handle_node(revision_node, u'username')
                        timestamp = handle_node(revision_node, u'timestamp')
                        edits.append((username, timestamp_to_date(timestamp), title))
    return edits


def get_categories_from_text(edit):
    """Return the categories contained in a given wikitext."""
    cat_pattern = r"\[\[Category:(?P<cat>.+?)(\|.*?)?\]\]"
    return map(lambda x: x[0], re.findall(cat_pattern, edit))



def main():
    pass

if __name__ == "__main__":
    main()
