#!/usr/bin/python
# -*- coding: utf-8  -*-
""" wmflabs_queries.py regroups query builder functions in order to generate queries for wmflabs databases.
"""

def list_files_in_category(category, t1, t2):
	"""
	list_files_in_category
		List all files in category uploaded between timestamp t1 and t2
	"""
	return u"""SELECT /* SLOW_OK */ page.page_title, image.img_timestamp, oldimage.oi_timestamp
FROM image
CROSS JOIN page ON image.img_name = page.page_title 
CROSS JOIN categorylinks ON page.page_id = categorylinks.cl_from
LEFT JOIN oldimage ON image.img_name = oldimage.oi_name AND oldimage.oi_timestamp = (SELECT MIN(o.oi_timestamp) FROM oldimage o WHERE o.oi_name = image.img_name)
WHERE  
    categorylinks.cl_to = '%s'
    AND IF(oldimage.oi_timestamp IS NULL, img_timestamp, oldimage.oi_timestamp)  BETWEEN %s AND %s
ORDER BY img_timestamp ASC;""" % (category, t1, t2)

def count_files_in_category(category, t1, t2):
	"""
	count_files_in_category
		List all files in category uploaded between timestamp t1 and t2
	"""
	return u"""SELECT /* SLOW_OK */ COUNT(page.page_title) AS IMAGES
FROM image
CROSS JOIN page ON image.img_name = page.page_title 
CROSS JOIN categorylinks ON page.page_id = categorylinks.cl_from
LEFT JOIN oldimage ON image.img_name = oldimage.oi_name AND oldimage.oi_timestamp = (SELECT MIN(o.oi_timestamp) FROM oldimage o WHERE o.oi_name = image.img_name)
WHERE  
    categorylinks.cl_to = '%s'
    AND IF(oldimage.oi_timestamp IS NULL, img_timestamp, oldimage.oi_timestamp)  BETWEEN %s AND %s
ORDER BY img_timestamp ASC;""" % (category, t1, t2)

def count_files_in_category_alltime(category):
	return u"""
		SELECT /* SLOW_OK */ COUNT(page.page_title) AS IMAGES
		FROM image
		CROSS JOIN page ON image.img_name = page.page_title 
		CROSS JOIN categorylinks ON page.page_id = categorylinks.cl_from
		WHERE
			categorylinks.cl_to = '%s';
	""" % category

def count_uploaders_in_category(category, t1, t2):
	"""
	count_uploaders_in_category
		Count distinct users that have uploaded a files that belongs to category between timestamp t1 and t2
	"""
	return u"""SELECT /* SLOW_OK */ COUNT(DISTINCT img_user_text) AS USER 
FROM image
CROSS JOIN page ON image.img_name = page.page_title 
CROSS JOIN categorylinks ON page.page_id = categorylinks.cl_from
LEFT JOIN oldimage ON image.img_name = oldimage.oi_name AND oldimage.oi_timestamp = (SELECT MIN(o.oi_timestamp) FROM oldimage o WHERE o.oi_name = image.img_name)
WHERE  
    categorylinks.cl_to = '%s'
    AND IF(oldimage.oi_timestamp IS NULL, img_timestamp, oldimage.oi_timestamp)  BETWEEN %s AND %s
ORDER BY img_timestamp ASC;""" % (category, t1, t2)

def count_featured_files_in_category(category, t1, t2):
	return u"""SELECT /* SLOW_OK */ COUNT(*)
FROM 
	(SELECT /* SLOW_OK */ page.page_title
	   FROM image
	   CROSS JOIN page ON image.img_name = page.page_title 
	   CROSS JOIN categorylinks ON page.page_id = categorylinks.cl_from
	   CROSS JOIN categorylinks c2 ON page.page_id = c2.cl_from
	   LEFT JOIN oldimage ON image.img_name = oldimage.oi_name AND oldimage.oi_timestamp = (SELECT MIN(o.oi_timestamp) FROM oldimage o WHERE o.oi_name = image.img_name)
	   WHERE  
	       categorylinks.cl_to = '%s'
	      AND IF(oldimage.oi_timestamp is NULL, img_timestamp, oldimage.oi_timestamp)  BETWEEN %s AND %s
	      AND (c2.cl_to = "Quality_images" OR c2.cl_to = "Valued_images_supported_by_Wikimedia_France" OR c2.cl_to = "Featured_pictures_supported_by_Wikimedia_France")
   GROUP BY page.page_title
   ORDER BY img_timestamp ASC) labels;""" % (category, t1, t2)

def global_usage_count(category, main=False):
	query = """
			SELECT /* SLOW_OK */ 
				COUNT(page.page_title) AS total_usage,
				COUNT(DISTINCT page.page_title) AS images_used,
				COUNT(DISTINCT gil.gil_wiki) AS nb_wiki
			FROM image
			CROSS JOIN page ON image.img_name = page.page_title 
			CROSS JOIN categorylinks ON page.page_id = categorylinks.cl_from
			CROSS JOIN globalimagelinks gil ON gil.gil_to = image.img_name
			WHERE
				categorylinks.cl_to ='%s'""" % category
	if main:
		return query + " AND gil.gil_page_namespace_id = 0 AND (gil.gil_wiki!='metawiki')"
	else:
		return query
