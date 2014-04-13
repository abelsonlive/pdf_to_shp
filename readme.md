STEPS FOR CONVERTING PDFS TO SHAPEFILES
======================================

## Assumptions
You're running Mac OSX 10.9 and have installed [**Inkscape**](http://www.inkscape.org/), [**QGIS**](http://www.qgis.org/), and all of their dependencies.

## 1. Convert PDF to DXF
* Open `raw_pdf/{{division}}.pdf` file in [**Inkscape**](http://www.inkscape.org/).
* delete all vectors except for division boundaries.
* save file as `raw_dxf/{{division}}.dxf`.

## 2. Convert DXF to LINES
* Open `raw_dxf/{{division}}.dxf` in [**QGIS**](http://www.qgis.org/).
* Save file as `raw_shp/{{division}}/{{division}}.shp`.

## 3. Convert LINES to POLYGONS
* Open `raw_shp/{{division}}/{{division}}.shp` in [**QGIS**](http://www.qgis.org/).
* Convert lines to polygons by selecting `Vector -> Geometry Tools -> Lines to Polygons`.
* Save file as `raw_shp_poly/{{division}}/{{division}}.shp`.

## 4. Convert POLYGONS to GEOJSON
* Open `raw_shp_poly/{{division}}/{{division}}.shp` in [**QGIS**](http://www.qgis.org/).
* Save file as `raw_geojson/{{division}}.geojson`.

## 5. Convert Divison Shapefiles to GEOJSON
* Open `divisions_shp/{{division}}/{{division}}.shp` in [**QGIS**](http://www.qgis.org/).
* Save file as `divisions_geojson/{{division}}.geojson`.

## 6. Rescale GEOJSON POLYGONS
* In your terminal run this command:
```
$ python rescale_geojson.py {{division}}
```
* This script runs a linear tranformation on the coordinates of `raw_geojson/{{division}}.geojson`, scaling its bounds to the bounds of `divisions_geojson/{{division}}.geojson`. In
You should now see `villages_geojson/{{division}}.geojson`.

## 7. RESCALED GEOJSON to SHAPEFILE
* Open `raw_geojson/{{division}}.geojson` in [**QGIS**](http://www.qgis.org/).
* Save file as `villages_shp/{{division}}/{{division}}.shp`.

## 8. Upload SHAPEFILE to CartoDB
* Zip-compress the `villages_shp/{{division}}/` directory and open the resulting zip archive in CartoDB. The Username and Password were sent to Carolina, Joe, and Piali in an email with the subject "CARTODB LOGIN INFO."

## 9. MANUALLY EDIT SHAPES
Okay, now for the super boring, tedious, yet EXTREMELY IMPORTANT part.  
* Assess overlaps and manually adjust division shapes using `Edit -> Edit Feature(s)`. Make sure to first activate `Edit Mode` (the pencial icon).
* It helps to have an Satellite baselayer for reference.
* Check for village boundaries that appear to have been split but are actually duplicated because their dividing lines were not fully completed in the conversion process. The best way to do this is to color the polygons by a unique shape ID and find polygons which are abutting and have the same color. Once you locate these you'll have to delete the polygons and manually re-draw them using CartoDB's editing tools.
* If you need to shift the entire set of polygons in one direction, or make them larger or smaller, you should learn and love [ST_TransScale](http://postgis.org/docs/ST_TransScale.html), [ST_Scale](http://postgis.org/docs/ST_Scale.html), and [ST_Affine](http://postgis.org/docs/ST_Affine.html), all of which can be used within CartoDB's SQL terminal.

## 10. MANUALLY LABEL SHAPES
Now that you have nice, clean shapes. You can add labels to them in CartoDB.
* Click on each village polygon and add the village name by referencing the corresponding PDF.  It really helps to have two screens in this process.
* IF you discover any problems with the shapes in this process, go back to step 9.

## 11. CELEBRATE!
This will help:
![beer](http://2.bp.blogspot.com/-6ibmeSJVgiM/Td6RzapA8mI/AAAAAAAAAKQ/DWZwpxwqiCU/s1600/IMG_1245.JPG)
