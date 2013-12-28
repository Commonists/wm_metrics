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