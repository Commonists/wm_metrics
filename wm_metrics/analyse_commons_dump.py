# -*- coding: utf-8 -*-

"""Analysing a Commons collection to retrieve fancy statistics."""

import xml.dom.minidom
import re
import datetime
from collections import Counter

from wm_metrics.categorisation_statistics import make_categorisation_report


class DumpMediaCollection(dict):

    """Representation of a MediaCollection, dump style."""

    def __init__(self):
        super(DumpMediaCollection, self).__init__()

    def init_from_xml_dump(self, xml_dump):
        """Initialise the object using an XML dump."""
        self.update(parse_xml_dump(xml_dump))

    def get_state(self, target_datetime):
        """Return a Collection at the time given."""
        collection = DumpMediaCollection()
        for page_id, page in self.items():
            revisions_bis = [revision for revision in page.revisions
                             if revision.timestamp < target_datetime]
            if revisions_bis:
                new_page = page
                new_page.revisions = revisions_bis
                collection[page_id] = new_page
        return collection

    def get_initial_state(self):
        """Return a Collection in its initial state."""
        collection = DumpMediaCollection()
        for page_id, page in self.items():
            min_timestamp = min([x.timestamp for x in page.revisions])
            first_revision = [revision for revision in page.revisions
                              if revision.timestamp is min_timestamp]
            new_page = CommonsPage()
            new_page.title = page.title
            new_page.revisions = first_revision
            collection[page_id] = new_page
        return collection

    def get_differential(self, start_date, end_date):
        """Return a difference between two dates."""
        usernames = set()
        pages_edited = set()
        final_revisions = list()
        for page_id, page in self.items():
            revisions = [revision for revision in page.revisions
                         if start_date < revision.timestamp < end_date]
            usernames.update([revision.username for revision in revisions])
            if revisions:
                pages_edited.add(page_id)
                final_revisions.extend(revisions)
        return final_revisions, usernames, pages_edited

    def simple_diff_report(self, start_date, end_date):
        """Return an activity text report in a given timeframe.

        This report on the number of edits, editors and files
        touched between two given dates.
        """
        diff = self.get_differential(start_date, end_date)
        final_revisions, usernames, pages_edited = diff
        text = ("Between %s and %s, %s edits were made "
                "by %s users on %s distinct files")
        return text % (start_date.date().isoformat(), end_date.date().isoformat(),
                       len(final_revisions), len(usernames), len(pages_edited))

    def simple_all_time_report(self):
        """Return an activity text report since the beginning to now.

        This report on the number of edits, editors and files
        touched between two given dates.
        """
        return self.simple_diff_report(datetime.datetime.min, datetime.datetime.max)

    def get_valued_images(self):
        """Return a list of valued images in the collection."""
        return [page_id for (page_id, page) in self.items()
                if page.get_top_revision().is_valued_image()]

    def categorisation_report(self):
        """Return a text categorisation report.

        Iterate over the pages of the media collection, get the top revision,
        and collects the categories in two Counters - one indexed by category
        and the other one by file.
        """

        categories_counter = Counter()
        categories_count_per_file = Counter()
        for page_id, page in self.items():
            categories = page.get_top_revision().get_categories()
            categories_counter.update(categories)
            categories_count_per_file[page_id] = len(categories)
        return make_categorisation_report(categories_counter, categories_count_per_file)


class CommonsPage(object):

    """Represent a page."""

    def __init__(self, title=None, revisions=None):
        # super(CommonsPage, self).__init__()
        self.title = title
        if not revisions:
            revisions = []
        self.revisions = revisions

    def __repr__(self):
        return "%s (%s)" % (self.title, len(self.revisions))

    def get_top_revision(self):
        """Return the most recent CommonsRevision.

        We assume the revisions list is ordered by time
        (which is the case when initialized with a dump)

        """
        return self.revisions[-1]


class CommonsRevision(object):

    """Representation of a Revision (timestamp + username + wikitext)."""

    def __init__(self, timestamp=None, username=None, wikitext=None):
        # super(CommonsRevision, self).__init__()
        self.timestamp = timestamp
        self.username = username
        self.wikitext = wikitext

    def is_valued_image(self):
        """Return whether the given revision is a Valued Image."""
        vi_pattern = r"""{{VI"""
        if re.search(vi_pattern, self.wikitext):
            return True
        else:
            return False

    def get_categories(self):
        """Return the categories in the given revision."""
        return get_categories_from_text(self.wikitext)

    def __repr__(self):
        return "%s - %s" % (self.timestamp, self.username.encode('utf-8'))


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
    """Return a dictionary from the given dump.

    A dictionary structured as follow:
    {page_id => { CommonsPage(title => "Some title"git
                              revisions => [CommonsRevision, ...] } }

    """
    collection = {}
    doc = xml.dom.minidom.parse(xml_dump)
    for mediawiki_node in doc.childNodes:
        if mediawiki_node.localName == u'mediawiki':
            for page_node in mediawiki_node.childNodes:
                if page_node.localName == u'page':
                    page_id = handle_node(page_node, u'id')
                    page_title = handle_node(page_node, u'title')
                    revisions = []
                    revision_nodes = [node for node in page_node.childNodes
                                      if node.localName == u'revision']
                    for revision_node in revision_nodes:
                        timestamp = handle_node(revision_node, u'timestamp')
                        username = handle_node(revision_node, u'username')
                        if not username:
                            username = handle_node(revision_node, u'ip')
                        revision = CommonsRevision(timestamp=timestamp_to_date(timestamp),
                                                   wikitext=handle_node(
                                                       revision_node, u'text'),
                                                   username=username)
                        revisions.append(revision)
                    collection[page_id] = CommonsPage(page_title, revisions)
    return collection


def get_categories_from_text(edit):
    """Return the categories contained in a given wikitext."""
    cat_pattern = r"\[\[Category:(?P<cat>.+?)(\|.*?)?\]\]"
    return [x[0] for x in re.findall(cat_pattern, edit)]


def main():
    pass

if __name__ == "__main__":
    main()
