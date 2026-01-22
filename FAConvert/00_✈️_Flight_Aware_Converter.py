from kmldecode import FlightAwareKML
import streamlit as st
import streamlit_folium as stf
import folium
import shapely

st.title("Flight Aware KML Converter")

st.set_page_config(page_icon="✈️",
                   layout="wide",
                   page_title="FlightAware KML Converter")

kml = st.file_uploader("Upload your FlightAware log KML", 
                       type=["kml", "kmz"])

if kml:
    fakml = FlightAwareKML(kml_str=kml.read())
    # st.code(fakml.airports)
    st.header(fakml.flight_id)
    # st.code(f"{fakml.coords_count} - {fakml.times_count}")
    # st.code(fakml.xml_doc.toprettyxml())
    # st.dataframe(fakml.flight_path)
    # st.code(fakml.line)
    # st.code(dir(farkml.date_range[0]))
    map_width, map_height = 1200, 800
    
    zoom_center = fakml.line_mean
    
    map = folium.Map(location=zoom_center, 
                     zoom_start=fakml.zoom(map_height, map_width), 
                     width=map_width,
                     height=map_height)
    flightpath = folium.PolyLine(fakml.flight_path[["latitude", "longitude"]]).add_to(map)
    for airport in fakml.airports.keys():
        pt = [fakml.airports[airport]["point"].latitude, fakml.airports[airport]["point"].longitude]
        folium.Marker(pt, icon=folium.Icon(color="blue", icon="plane")).add_to(map)
    stf.st_folium(map, width=map_width, height=map_height)

    st.download_button("Download GeoJSON", 
                       data=fakml.geojson, 
                       file_name=f"{fakml.flight_id}_{fakml.date_range[0].isoformat()}.geo.json")
    st.download_button("Download GPX",
                       data=fakml.to_gpx(),
                       file_name=f"{fakml.flight_id}_{fakml.date_range[0].isoformat()}.gpx")