-- category_metrics.sql is a set of query for tools of wmflabs
-- it is designed in order to help Program leaders to evaluate their program

-- Parameters:
-- 		cat: category on which we are going to compute metrics
--		t1:  period start
--		t2:  period end
SET @cat = "Media_supported_by_Wikimedia_France", @t1 = 20131001000000,  @t2 = 20140101000000;

-- List files
SELECT /* SLOW_OK */ page.page_title, image.img_timestamp, oldimage.oi_timestamp
   FROM image
   CROSS JOIN page ON image.img_name = page.page_title 
   CROSS JOIN categorylinks ON page.page_id = categorylinks.cl_from
   LEFT JOIN oldimage ON image.img_name = oldimage.oi_name AND oldimage.oi_timestamp = (SELECT MIN(o.oi_timestamp) FROM oldimage o WHERE o.oi_name = image.img_name)
   WHERE  
       categorylinks.cl_to = @cat
      AND IF(oldimage.oi_timestamp IS NULL, img_timestamp, oldimage.oi_timestamp)  BETWEEN @t1 AND @t2
   ORDER BY img_timestamp ASC;

-- Count files
SELECT /* SLOW_OK */ COUNT(page.page_title)
   FROM image
   CROSS JOIN page ON image.img_name = page.page_title 
   CROSS JOIN categorylinks ON page.page_id = categorylinks.cl_from
   LEFT JOIN oldimage ON image.img_name = oldimage.oi_name AND oldimage.oi_timestamp = (SELECT MIN(o.oi_timestamp) FROM oldimage o WHERE o.oi_name = image.img_name)
   WHERE  
       categorylinks.cl_to = @cat
      AND IF(oldimage.oi_timestamp IS NULL, img_timestamp, oldimage.oi_timestamp)  BETWEEN @t1 AND @t2
   ORDER BY img_timestamp ASC;


-- Count quality images
SELECT /* SLOW_OK */ COUNT(page.page_title)
   FROM image
   CROSS JOIN page ON image.img_name = page.page_title 
   CROSS JOIN categorylinks ON page.page_id = categorylinks.cl_from
   CROSS JOIN categorylinks c2 ON page.page_id = c2.cl_from
   LEFT JOIN oldimage ON image.img_name = oldimage.oi_name AND oldimage.oi_timestamp = (SELECT MIN(o.oi_timestamp) FROM oldimage o WHERE o.oi_name = image.img_name)
   WHERE  
       categorylinks.cl_to = @cat
      AND IF(oldimage.oi_timestamp IS NULL, img_timestamp, oldimage.oi_timestamp)  BETWEEN @t1 AND @t2
      AND c2.cl_to = "Quality_images"
   ORDER BY img_timestamp ASC;


-- Count featured pictures on Wikimedia Commons
SELECT /* SLOW_OK */ COUNT(page.page_title)
   FROM image
   CROSS JOIN page ON image.img_name = page.page_title 
   CROSS JOIN categorylinks ON page.page_id = categorylinks.cl_from
   CROSS JOIN categorylinks c2 ON page.page_id = c2.cl_from
   LEFT JOIN oldimage ON image.img_name = oldimage.oi_name AND oldimage.oi_timestamp = (SELECT MIN(o.oi_timestamp) FROM oldimage o WHERE o.oi_name = image.img_name)
   WHERE  
       categorylinks.cl_to = @cat
      AND IF(oldimage.oi_timestamp IS NULL, img_timestamp, oldimage.oi_timestamp)  BETWEEN @t1 AND @t2
      AND c2.cl_to = "Featured_pictures_on_Wikimedia_Commons"
   ORDER BY img_timestamp ASC;

-- Count Valued images
SELECT /* SLOW_OK */ COUNT(page.page_title)
   FROM image
   CROSS JOIN page ON image.img_name = page.page_title 
   CROSS JOIN categorylinks ON page.page_id = categorylinks.cl_from
   CROSS JOIN categorylinks c2 ON page.page_id = c2.cl_from
   LEFT JOIN oldimage ON image.img_name = oldimage.oi_name AND oldimage.oi_timestamp = (SELECT MIN(o.oi_timestamp) FROM oldimage o WHERE o.oi_name = image.img_name)
   WHERE  
       categorylinks.cl_to = @cat
      AND IF(oldimage.oi_timestamp IS NULL, img_timestamp, oldimage.oi_timestamp)  BETWEEN @t1 AND @t2
      AND c2.cl_to = "Valued_images_sorted_by_promotion_date"
   ORDER BY img_timestamp ASC;
   
-- Count files which are Quality Image or Valued Image or Featured picture on Wikimedia Commons
SELECT /* SLOW_OK */ COUNT(*)
   FROM 
	   (SELECT /* SLOW_OK */ page.page_title
	   FROM image
	   CROSS JOIN page ON image.img_name = page.page_title 
	   CROSS JOIN categorylinks ON page.page_id = categorylinks.cl_from
	   CROSS JOIN categorylinks c2 ON page.page_id = c2.cl_from
	   LEFT JOIN oldimage ON image.img_name = oldimage.oi_name AND oldimage.oi_timestamp = (SELECT MIN(o.oi_timestamp) FROM oldimage o WHERE o.oi_name = image.img_name)
	   WHERE  
	       categorylinks.cl_to = @cat
	      AND IF(oldimage.oi_timestamp is NULL, img_timestamp, oldimage.oi_timestamp)  BETWEEN @t1 AND @t2
	      AND (c2.cl_to = "Quality_images" OR c2.cl_to = "Valued_images_supported_by_Wikimedia_France" OR c2.cl_to = "Featured_pictures_supported_by_Wikimedia_France")
   GROUP BY page.page_title
   ORDER BY img_timestamp ASC) labels;

-- Count uploaders of files in @cat between @t1 and @t2
SELECT /* SLOW_OK */ COUNT(DISTINCT img_user_text) AS USER 
   FROM image
   CROSS JOIN page ON image.img_name = page.page_title 
   CROSS JOIN categorylinks ON page.page_id = categorylinks.cl_from
   LEFT JOIN oldimage ON image.img_name = oldimage.oi_name AND oldimage.oi_timestamp = (SELECT MIN(o.oi_timestamp) FROM oldimage o WHERE o.oi_name = image.img_name)
   WHERE  
       categorylinks.cl_to = @cat
      AND IF(oldimage.oi_timestamp IS NULL, img_timestamp, oldimage.oi_timestamp)  BETWEEN @t1 AND @t2
   ORDER BY img_timestamp ASC;
