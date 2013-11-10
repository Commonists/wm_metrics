# -*- coding: utf-8 -*-
#!/usr/bin/python

import re, urllib, codecs, json

DEFAULT_API="https://commons.wikimedia.org/w/api.php"

def urlEncodeNonAscii(b):
    return re.sub('[\x80-\xFF]', lambda c: '%%%02x' % ord(c.group(0)), b)

class MwQueryError(Exception):
	def __init__(self, value):
	    self.value = value
	def __str__(self): 
		return repr(self.value)

class MwWiki:
	""" 
	Wiki API 
	"""
	def __init__(self, url_api=DEFAULT_API):
		self.url = url_api

	def send_to_api(self, request):
		# add action to url
		url_req = "%s?action=%s" % (self.url, request.action)
		# add each property
		for k in request.prop.keys():
			url_req += "&%s=%s" % (k, urlEncodeNonAscii(request.prop[k]))
		# add the format
		url_req += "&format=%s" % (request.format)
		#print url_req
		return urllib.urlopen(url_req).read()
	
	def process_query(self, request, result=[]):
		"""
		Quick and dirty continue support for list query
		"""
		if request.action != 'query':
			raise MwQueryError("action is not a query")
		result_name = None
		if 'list' in request.prop.keys():
			result_name = request.prop['list']
		else:
			raise MwQueryError("query has no list")
		query_result = json.loads(self.send_to_api(request))

		result.extend(query_result[request.action][result_name])

		if 'query-continue' in query_result.keys():
			props = request.prop
			# adding information to continue
			continue_args = query_result['query-continue'][result_name]
			for p in continue_args:
				print "\tcontinuing query with %s -> %s" % (p, continue_args)
				props[p] = continue_args[p]
			print "\tresult of query is %d lenght" % (len(result))
			return self.process_query(MwApiQuery(properties=props), result=result)
		else:
			return result

class MwApi:
	""" 
	Access to API 
	"""
	def __init__(self, action, properties=dict(), format="json"):
		self.action = action
		self.format = format
		self.prop   = properties

class MwApiQuery(MwApi):
	"""
	Query actions to the API
	"""
	def __init__(self, properties=dict(), format="json"):
		self.action = 'query'
		self.format = format
		self.prop   = properties
