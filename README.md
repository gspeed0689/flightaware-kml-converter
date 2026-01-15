# FlightAware KML Converter

After I fly I like to download the KML flight record from FlightAware, a web service that tracks planes. 
In the past I have used the built in KML converter tools in ArcGIS, QGIS, and GDAL, 
however they have their own opinions on what is really a very simple file. 
In this repository I have created a single page Streamlit app to load a KML file from FlightAware, 
and convert it to a better format that isn't optimized for display. 

Do not use or adapt this dashboard and abuse the FlightAware service by downloading tons of files, I would like to keep using this free service they have. 
If this does get abused then it might be shut off, then I would need to setup a Pi with an ADS-B recorder to get a pro account with them. 

This project is made with the following packages:

* Streamlit
* Folium and Streamlit-Folium
* Mercantile
* GeoPandas

## How to use this package

From the FAConvert folder, run `streamlit run 00_✈️_Flight_Aware_Converter.py` 

Upload a KML and download as a GeoJSON or GeoPackage

## Possibile Future Features

This project could also probably linked directly to PostGIS and you could automate the upload of this data to your local favorite GeoDatabase.