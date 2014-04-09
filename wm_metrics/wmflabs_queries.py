#!/usr/bin/python
# -*- coding: utf-8  -*-

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