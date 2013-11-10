# -*- coding: utf-8 -*-
#!/usr/bin/python

import mw_api, json, codecs

class CommonsMetrics:
	def __init__(self, category):
		self.commons 	= mw_api.MwWiki(url_api='https://commons.wikimedia.org/w/api.php')
		self.category 	= category
		self.qi 		= 0
		self.vi			= 0
		self.fp			= 0
		self.uploaders	= []
		self.hd_images	= []
		self.hd_4k		= []


	def list_category(self):
		import os.path

		cache_name = "cache/%s.cache" % (self.category)
		result = None

		if os.path.exists(cache_name):
			cache = codecs.open(cache_name, 'r', 'utf-8')
			result = json.loads(cache.read())
		else:
			result = self.commons.process_query(mw_api.MwApiQuery(
			properties={
				"list"   : "categorymembers",
				"cmtitle": self.category,
				"cmprop" : "ids|title|timestamp",
				"cmtype" : "file",
				"cmsort" : "timestamp",
				"cmdir"  : "asc",
				"cmlimit": "max"
			}))
			# removing duplicates
			file_titles = dict()
			for line in result:
				title = line['title']
				pageid= line['pageid']
				if not (pageid in file_titles.keys()):
					file_titles[pageid] = title
			cache_file = codecs.open(cache_name, 'w', 'utf-8')
			cache_file.write(json.dumps(file_titles))
			cache_file.close()
		return result

	def labels_for_image(self, image_title):
		result = json.loads(self.commons.send_to_api(mw_api.MwApiQuery(
			properties={
				"prop"		: "categories",
				"clshow"	: "hidden",
				"titles"	: image_title,
				"clcategories": "Category:Quality images|Category:Featured pictures on Wikimedia Commons|Category:Valued images sorted by promotion date"
			})))
		try:
			result = result['query']['pages']
			first_page = result.keys()[0]
			return result[first_page]['categories']
		except KeyError:
			return []

	def image_info(self, image_title):
		result = json.loads(self.commons.send_to_api(mw_api.MwApiQuery(
			properties={
				"prop"		: "imageinfo",
				"iiprop"	: "timestamp|user|size",
				"iilimit"	: "max",
				"titles"	: image_title
			})))
		try:
			result = result['query']['pages']
			first_page = result.keys()[0]
			return result[first_page]['imageinfo']
		except KeyError:
			return []

	def displays(self):
		print """Valued images: %5d
			Quality images: 	%5d"
			Featured pictures:	%5d"  
			Uploaders: 			%5d"
			HD images: 			%5d"
			HD4k images: 		%5d"""\
			% (self.vi, self.qi, self.fp, len(self.uploaders), len(self.hd_images), len(self.hd_4k))

	def computes(self):
		file_list_info = self.list_category()
		print "%s files in %s" % (len(file_list_info), self.category)
		for i in file_list_info.keys():
			labels 	= self.labels_for_image(file_list_info[i])
			ii 		= self.image_info(file_list_info[i])
			ii.reverse()
			#for k in ii[0]:
			#	file_list_info[i][k] = ii[0][k]
			size = int(ii[0]['width']) * int(ii[0]['height'])

			if not (ii[0]['user'] in self.uploaders):
				self.uploaders.append(ii[0]['user'])
			if size > 2000000:
				self.hd_images.append(file_list_info[i])
			if size > 4000000:
				self.hd_images.append(file_list_info[i])
			for l in labels:
				if l['title'] == 'Category:Quality images':
					self.qi += 1
				if l['title'] == 'Category:Featured pictures on Wikimedia Commons':
					self.fp += 1
				if l['title'] == 'Category:Valued images sorted by promotion date':
					self.vi += 1
		self.displays()

# print commons.process_query(list_cat)

category = "Category:Media supported by Wikimedia France"
category = "Category:Wikimedia France - Saint-Sernin"
metrics = CommonsMetrics(category)

metrics.computes()