------------------------------------------------------------------------------
--            Mass upload Metrics for Wikimedia France reporting            --
------------------------------------------------------------------------------


-- Project with Musée des Augustins de Toulouse
------------------------------------------------------------------------------

-- Configuration for Q1
SET @cat = "Media_contributed_by_the_Musée_des_Augustins_de_Toulouse", @t1 = 20130701000000,  @t2 = 20131001000000;

-- On Q1 (round 2 2012-2013)
-- Count files uploaded
SELECT /* SLOW_OK */ COUNT(page.page_title)
   FROM image
   CROSS JOIN page ON image.img_name = page.page_title 
   CROSS JOIN categorylinks ON page.page_id = categorylinks.cl_from
   LEFT JOIN oldimage ON image.img_name = oldimage.oi_name AND oldimage.oi_timestamp = (SELECT MIN(o.oi_timestamp) FROM oldimage o WHERE o.oi_name = image.img_name)
   WHERE  
       categorylinks.cl_to = @cat
      AND IF(oldimage.oi_timestamp IS NULL, img_timestamp, oldimage.oi_timestamp)  BETWEEN @t1 AND @t2
   ORDER BY img_timestamp ASC;

-- On Q1 (round 2 2012-2013)
-- Amount of files with more than 1200px on each side
SELECT /* SLOW_OK */ COUNT(page.page_title)
   FROM image
   CROSS JOIN page ON image.img_name = page.page_title 
   CROSS JOIN categorylinks ON page.page_id = categorylinks.cl_from
   LEFT JOIN oldimage ON image.img_name = oldimage.oi_name AND oldimage.oi_timestamp = (SELECT MIN(o.oi_timestamp) FROM oldimage o WHERE o.oi_name = image.img_name)
   WHERE  
       categorylinks.cl_to = @cat
      AND IF(oldimage.oi_timestamp is NULL, img_timestamp, oldimage.oi_timestamp)  BETWEEN @t1 AND @t2
      AND img_width > 1200
      AND img_height > 1200
;

-- Configuration for Q2
SET @cat = "Media_contributed_by_the_Musée_des_Augustins_de_Toulouse", @t1 = 20131001000000,  @t2 = 20140101000000;

-- On Q2 (round 2 2012-2013)
-- Count files uploaded
SELECT /* SLOW_OK */ COUNT(page.page_title)
   FROM image
   CROSS JOIN page ON image.img_name = page.page_title 
   CROSS JOIN categorylinks ON page.page_id = categorylinks.cl_from
   LEFT JOIN oldimage ON image.img_name = oldimage.oi_name AND oldimage.oi_timestamp = (SELECT MIN(o.oi_timestamp) FROM oldimage o WHERE o.oi_name = image.img_name)
   WHERE  
       categorylinks.cl_to = @cat
      AND IF(oldimage.oi_timestamp IS NULL, img_timestamp, oldimage.oi_timestamp)  BETWEEN @t1 AND @t2
   ORDER BY img_timestamp ASC;

-- Amount of files with more than 1200px on each side
SELECT /* SLOW_OK */ COUNT(page.page_title)
   FROM image
   CROSS JOIN page ON image.img_name = page.page_title 
   CROSS JOIN categorylinks ON page.page_id = categorylinks.cl_from
   LEFT JOIN oldimage ON image.img_name = oldimage.oi_name AND oldimage.oi_timestamp = (SELECT MIN(o.oi_timestamp) FROM oldimage o WHERE o.oi_name = image.img_name)
   WHERE  
       categorylinks.cl_to = @cat
      AND IF(oldimage.oi_timestamp is NULL, img_timestamp, oldimage.oi_timestamp)  BETWEEN @t1 AND @t2
      AND img_width > 1200
      AND img_height > 1200
;

-- Fonds Trutat - Archives municipales de Toulouse
------------------------------------------------------------------------------

-- Configuration for Q1
SET @cat = "Fonds_Trutat_-_Archives_municipales_de_Toulouse", @t1 = 20130701000000,  @t2 = 20131001000000;

-- On Q1 (round 2 2012-2013)
-- Count files uploaded
SELECT /* SLOW_OK */ COUNT(page.page_title)
   FROM image
   CROSS JOIN page ON image.img_name = page.page_title 
   CROSS JOIN categorylinks ON page.page_id = categorylinks.cl_from
   LEFT JOIN oldimage ON image.img_name = oldimage.oi_name AND oldimage.oi_timestamp = (SELECT MIN(o.oi_timestamp) FROM oldimage o WHERE o.oi_name = image.img_name)
   WHERE  
       categorylinks.cl_to = @cat
      AND IF(oldimage.oi_timestamp IS NULL, img_timestamp, oldimage.oi_timestamp)  BETWEEN @t1 AND @t2
   ORDER BY img_timestamp ASC;

-- On Q1 (round 2 2012-2013)
-- Amount of files with more than 1200px on each side
SELECT /* SLOW_OK */ COUNT(page.page_title)
   FROM image
   CROSS JOIN page ON image.img_name = page.page_title 
   CROSS JOIN categorylinks ON page.page_id = categorylinks.cl_from
   LEFT JOIN oldimage ON image.img_name = oldimage.oi_name AND oldimage.oi_timestamp = (SELECT MIN(o.oi_timestamp) FROM oldimage o WHERE o.oi_name = image.img_name)
   WHERE  
       categorylinks.cl_to = @cat
      AND IF(oldimage.oi_timestamp is NULL, img_timestamp, oldimage.oi_timestamp)  BETWEEN @t1 AND @t2
      AND img_width > 1200
      AND img_height > 1200
;

-- Configuration for Q2
SET @cat = "Fonds_Trutat_-_Archives_municipales_de_Toulouse", @t1 = 20131001000000,  @t2 = 20140101000000;

-- On Q2 (round 2 2012-2013)
-- Count files uploaded
SELECT /* SLOW_OK */ COUNT(page.page_title)
   FROM image
   CROSS JOIN page ON image.img_name = page.page_title 
   CROSS JOIN categorylinks ON page.page_id = categorylinks.cl_from
   LEFT JOIN oldimage ON image.img_name = oldimage.oi_name AND oldimage.oi_timestamp = (SELECT MIN(o.oi_timestamp) FROM oldimage o WHERE o.oi_name = image.img_name)
   WHERE  
       categorylinks.cl_to = @cat
      AND IF(oldimage.oi_timestamp IS NULL, img_timestamp, oldimage.oi_timestamp)  BETWEEN @t1 AND @t2
   ORDER BY img_timestamp ASC;

-- Amount of files with more than 1200px on each side
SELECT /* SLOW_OK */ COUNT(page.page_title)
   FROM image
   CROSS JOIN page ON image.img_name = page.page_title 
   CROSS JOIN categorylinks ON page.page_id = categorylinks.cl_from
   LEFT JOIN oldimage ON image.img_name = oldimage.oi_name AND oldimage.oi_timestamp = (SELECT MIN(o.oi_timestamp) FROM oldimage o WHERE o.oi_name = image.img_name)
   WHERE  
       categorylinks.cl_to = @cat
      AND IF(oldimage.oi_timestamp is NULL, img_timestamp, oldimage.oi_timestamp)  BETWEEN @t1 AND @t2
      AND img_width > 1200
      AND img_height > 1200
;

-- Archives Nationales
------------------------------------------------------------------------------

-- Configuration for Q1
SET @cat = "Media_contributed_by_the_Archives_Nationales_(France)", @t1 = 20130701000000,  @t2 = 20131001000000;

-- On Q1 (round 2 2012-2013)
-- Count files uploaded
SELECT /* SLOW_OK */ COUNT(page.page_title)
   FROM image
   CROSS JOIN page ON image.img_name = page.page_title 
   CROSS JOIN categorylinks ON page.page_id = categorylinks.cl_from
   LEFT JOIN oldimage ON image.img_name = oldimage.oi_name AND oldimage.oi_timestamp = (SELECT MIN(o.oi_timestamp) FROM oldimage o WHERE o.oi_name = image.img_name)
   WHERE  
       categorylinks.cl_to = @cat
      AND IF(oldimage.oi_timestamp IS NULL, img_timestamp, oldimage.oi_timestamp)  BETWEEN @t1 AND @t2
   ORDER BY img_timestamp ASC;

-- On Q1 (round 2 2012-2013)
-- Amount of files with more than 1200px on each side
SELECT /* SLOW_OK */ COUNT(page.page_title)
   FROM image
   CROSS JOIN page ON image.img_name = page.page_title 
   CROSS JOIN categorylinks ON page.page_id = categorylinks.cl_from
   LEFT JOIN oldimage ON image.img_name = oldimage.oi_name AND oldimage.oi_timestamp = (SELECT MIN(o.oi_timestamp) FROM oldimage o WHERE o.oi_name = image.img_name)
   WHERE  
       categorylinks.cl_to = @cat
      AND IF(oldimage.oi_timestamp is NULL, img_timestamp, oldimage.oi_timestamp)  BETWEEN @t1 AND @t2
      AND img_width > 1200
      AND img_height > 1200
;

-- Configuration for Q2
SET @cat = "Media_contributed_by_the_Archives_Nationales_(France)", @t1 = 20131001000000,  @t2 = 20140101000000;

-- On Q2 (round 2 2012-2013)
-- Count files uploaded
SELECT /* SLOW_OK */ COUNT(page.page_title)
   FROM image
   CROSS JOIN page ON image.img_name = page.page_title 
   CROSS JOIN categorylinks ON page.page_id = categorylinks.cl_from
   LEFT JOIN oldimage ON image.img_name = oldimage.oi_name AND oldimage.oi_timestamp = (SELECT MIN(o.oi_timestamp) FROM oldimage o WHERE o.oi_name = image.img_name)
   WHERE  
       categorylinks.cl_to = @cat
      AND IF(oldimage.oi_timestamp IS NULL, img_timestamp, oldimage.oi_timestamp)  BETWEEN @t1 AND @t2
   ORDER BY img_timestamp ASC;

-- Amount of files with more than 1200px on each side
SELECT /* SLOW_OK */ COUNT(page.page_title)
   FROM image
   CROSS JOIN page ON image.img_name = page.page_title 
   CROSS JOIN categorylinks ON page.page_id = categorylinks.cl_from
   LEFT JOIN oldimage ON image.img_name = oldimage.oi_name AND oldimage.oi_timestamp = (SELECT MIN(o.oi_timestamp) FROM oldimage o WHERE o.oi_name = image.img_name)
   WHERE  
       categorylinks.cl_to = @cat
      AND IF(oldimage.oi_timestamp is NULL, img_timestamp, oldimage.oi_timestamp)  BETWEEN @t1 AND @t2
      AND img_width > 1200
      AND img_height > 1200
;
