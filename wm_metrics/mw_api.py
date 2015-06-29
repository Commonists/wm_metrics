# -*- coding: utf-8 -*-

"""mw_api.py is a simple client to MediaWiki API."""

import urllib
import json
import httplib2

DEFAULT_API = "https://commons.wikimedia.org/w/api.php"
MAX_URL_SIZE = 1024


class MwQueryError(Exception):

    """Exception raised when the client encounters a problem."""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class MwWiki(object):

    """Wiki API"""

    def __init__(self, url_api=DEFAULT_API):
        """ Constructor.

        Args:
                url_api (str): Url of the MediaWiki API
        """
        self.url = url_api

    def __encode_param(self, param):
        """Encode param into unicode if not already unicode."""
        if not isinstance(param, unicode):
            return unicode(param)
        else:
            return param

    def send_to_api(self, request, debug=False):
        """Send a request to mediawiki API.

        Args:
            request (MwApi): Request to send.
            debug (bool): if true, then just only return the string of the
                API request, otherwise return the result.
        """
        # add action to url
        url_req = "%s?action=%s" % (self.url, request.action)
        # add each property
        for k in request.prop:
            url_req += "&%s=%s" % (k, self.__encode_param(request.prop[k]))
        # add the format
        url_req += "&format=%s" % (request.format)
        # print url_req
        if not debug:
            uri = httplib2.iri2uri(unicode(url_req))
            return urllib.urlopen(uri).read()
        else:
            return url_req

    def process_prop_query(self, request, titles):
        """Quick and dirty prop query support."""
        if request.action != 'query' or 'prop' not in request.prop:
            raise MwQueryError('Not a prop query')
        if 'titles' in request.prop:
            raise MwQueryError(
                'process_prop_query should not have titles in the request object')
        url_base = self.send_to_api(request, debug=True)
        url_req = url_base
        results = dict()
        for title in titles:
            # testing length
            if len(url_req) + len(title) + 8 >= MAX_URL_SIZE:
                self.process_prop_query_results(url_req, results)
                # init a new query
                url_req = url_base

            if '&titles' not in url_req:
                url_req += "&titles=%s" % (self.__encode_param(title))
            else:
                url_req += "|%s" % (self.__encode_param(title))
        if len(url_req) > len(url_base):
            self.process_prop_query_results(url_req, results)
        return results

    def process_prop_query_results(self, url_req, results):
        """Process the result of a prop query."""
        try:
            uri = httplib2.iri2uri(unicode(url_req))
            req_result = json.loads(urllib.urlopen(uri).read())
            # req_result = json.loads(self.__get_url(url_req).read())
            if 'query-continue' in req_result:
                raise MwQueryError("continue not supported for prop query")
            r = req_result['query']['pages']
            for p in r:
                results[p] = r[p]
        except KeyError:
            print "Empty result for --> %s" % (url_req)

    def process_query(self, request, previous_result=None):
        """Quick and dirty continue support for list query."""
        results = []
        if previous_result is not None:
            results = previous_result
        if request.action != 'query':
            raise MwQueryError("action is not a query")
        result_name = None
        if 'list' in request.prop:
            result_name = request.prop['list']
        else:
            raise MwQueryError("query has no list")
        query_result = json.loads(self.send_to_api(request))

        results.extend(query_result[request.action][result_name])

        if 'query-continue' in query_result:
            props = request.prop
            # adding information to continue
            continue_args = query_result['query-continue'][result_name]
            for p in continue_args:
                print "\tcontinuing query with %s -> %s" % (p, continue_args)
                props[p] = continue_args[p]
            print "\tresult of query is %d lenght" % (len(results))
            return self.process_query(MwApiQuery(properties=props),
                                      previous_result=results)
        else:
            return results


class MwApi(object):

    """Access to API"""

    def __init__(self, action, properties=None, format="json"):
        """Constructor.

        Args:
            action (str): type of action such as 'query'.
            properties (dict): dictionnary with the properties of the query.
            format (string): format of the query result, default 'json'.
        """
        if properties is None:
            self.prop = dict()
        else:
            self.prop = properties
        self.action = action
        self.format = format


class MwApiQuery(MwApi):

    """Query actions to the API."""

    def __init__(self, properties=None, format="json"):
        """Constructor.

        Args:
            properties (dict): dictionnary with the properties of the query.
            format (string): format of the query result, default 'json'.
        """
        if properties is None:
            self.prop = dict()
        else:
            self.prop = properties
        self.action = 'query'
        self.format = format
