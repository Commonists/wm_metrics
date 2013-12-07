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
    """Return a date object representing the given MediaWiki timestamp."""
    return datetime.date(int(date[0:4]), int(date[5:7]), int(date[8:10]))


def title_to_identifier(title):
    """Return the Trutat identifier in a given filename."""
    id_search = re.search(r" - (?P<id>51Fi.+?) - ", title)
    if id_search:
        identifier = id_search.group('id')
        return identifier


def parse_xml_dump(xml_dump):
    """Return a list of the edits in a Wikimedia Commons dump."""
    edits = []
    revision_categories = {}
    doc = xml.dom.minidom.parse(xml_dump)
    for mediawiki_node in doc.childNodes:
        if mediawiki_node.localName == u'mediawiki':
            for page_node in mediawiki_node.childNodes:
                for revision_node in page_node.childNodes:
                    title = handle_node(page_node, u'title')
                    revision_categories[title] = []
                    if revision_node.localName == u'revision':
                        username = handle_node(revision_node, u'username')
                        timestamp = handle_node(revision_node, u'timestamp')
                        text = handle_node(revision_node, u'text')
                        edits.append((username, timestamp_to_date(timestamp), title))
                        #cats = get_categories_from_text(text)
                        #revision_categories[title].append(cats)
    return edits


def get_categories_from_text(edit):
    """Return the categories contained in a given wikitext."""
    cat_pattern = r"\[\[Category:(?P<cat>.+?)(\|.*?)?\]\]"
    return map(lambda x: x[0], re.findall(cat_pattern, edit))


def analyse_edits(edits, bottomDate, topDate):
    all_pages = list(set(map(lambda x: x[2], edits)))

    #print allPages
    edits_filtered = filter(lambda x: bottomDate < x[1] < topDate, edits)
    edits_filtered = edits
    usernames = set(map(lambda x: x[0], edits_filtered))
    page_edited = list(set(map(lambda x: x[2], edits_filtered)))

    text = "Sur la période considérée, %s modifications ont été effectuées" \
           "par %s utilisateurs sur %s documents distincts "
    print text % (len(edits_filtered), len(usernames), len(page_edited))

    #globalUsage = listGlobalUsage(allPages)

    #print globalUsage

    #buildUsageReport(globalUsage)

    user_contribs = {}
    for username in usernames:
        user_contribs[username] = map(lambda x: x[1], filter(lambda x: x[0] == username, edits_filtered))
    return user_contribs


def list_global_usage(all_pages):
    r = range(0, len(all_pages), 50)
    r2 = r[1:] + [None]
    return reduce(lambda x, y: x + y, map(lambda x: query_global_usage(all_pages[x[0]:x[1]]), zip(r, r2)))


def build_usage_report(global_usage):

    def build_usage_line(file_usage):
        title = file_usage[0][5:]
        print title
        print title_to_identifier(title)

        def build_usage_subLine(usage):
            return "\item \lienProjet{%s}{%s}" % usage


        return "\item \commonsFileLink{%s}{%s}, sur \lienProjet{%s}{%s}" % (title, title_to_identifier(title), usage[1])

    for item in global_usage:
        print build_usage_line(item)


        #report=u"""Sur la période observée, %s images étaient utilisées sur les projets Wikimedia :
        #\\begin{itemize}

        #\item \commonsFileLink{Toulouse._Foire_à_l’ail._24_août_1899_(1899)_-_51Fi49_-_Fonds_Trutat.jpg}{51Fi49}, sur \articleWP{Ail cultivé}, consulté 7571 fois ce mois
        #\item \commonsFileLink{Toulouse._Racleurs_de_rails._Place_du_Pont._25_juin_1899_(1899)_-_51Fi60_-_Fonds_Trutat.jpg}{51Fi60}, sur \articleWP{Tramway de Toulouse}
        #\\end{itemize}

        #"""


def build_report_from_user_list(user_edits):
    nb_users = len(user_edits.keys())
    the_list = python_list_to_latex_description(user_edits.keys(), map(build_user_item, user_edits.values()))
    report = u"""Sur la période observée, %s utilisateurs ont contribué au corpus :
  %s
  """ % (nb_users, the_list)
    return report


def accordEnNombre(number, singular, plural):
    if number > 1:
        return u"%s %s" % (number, plural)
    else:
        return u"%s %s" % (number, singular)


def build_user_item(edits):
    return accordEnNombre(len(edits), u"modification", u"modifications")


def python_list_to_latex_description(list1, list2):
    return u"""\\begin{description}  %s\n\\end{description}
  """ % (u"".join(map(lambda x, y: u"\n	\item[%s] \hfill \\\\ %s " % (x, y), list1, list2)))


def python_list_to_latex_itemize(my_list):
    return u"""\
  \\begin{itemize}
  \t\item %s
  \\end{itemize}""" % (u"\n\t\item ".join(my_list))


def query_global_usage(filelist):
    if len(filelist) is 0:
        return []
    params = {
        'action': 'query',
        'prop': 'globalusage',
        'titles': "|".join(filelist),
        'gulimit': '500',
    }

    query_result = query.GetData(params, encodeTitle=False)

    def retrieve_from_globa_usage(global_usage):
        if len(global_usage) is 0:
            return []
        else:
            return map(lambda x: (x["wiki"], x["title"]), global_usage)

    return filter(lambda x: len(x[1]) > 0, map(lambda x: (x["title"], retrieve_from_globa_usage(x["globalusage"])),
                                               query_result["query"]["pages"].values()))


if __name__ == "__main__":
    xmlFile = "Wikimedia+Commons-20130207231014.xml"
    edits = parse_xml_dump(xmlFile)

    userContribs = analyse_edits(edits, datetime.date(2011, 01, 01), datetime.date(2011, 11, 30))
    x = datetime.date(2011, 01, 15)
    #print x > datetime.date(2011, 01, 01) and x < datetime.date(2013, 11, 30)

    #print userContribs
    for user in userContribs.keys():
        print "%s : %s" % (user, len(userContribs[user]))
        #print
        #for date in userContribs[user]:
            #print date
    print build_report_from_user_list(userContribs)
