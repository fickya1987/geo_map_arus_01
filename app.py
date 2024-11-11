# app.py

import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

# Load data
@st.cache_data
def load_data():
    return pd.read_excel("Perdagangan Antar Wilayah.xlsx")

# Load Indonesian Provinces GeoJSON
@st.cache_data
def load_geojson():
    # Using a GeoJSON file of Indonesia's provinces
    gdf = gpd.read_file("indonesia.geojson")  # Make sure you have this file or download from a reliable source
    return gdf

# Main App
st.title("Perdagangan Antar Wilayah di Indonesia")

# Load the data
data = load_data()
st.write("Data Perdagangan Antar Wilayah:", data)

# Filter options
provinsi = st.selectbox("Pilih Provinsi:", data['Provinsi'].unique())

# Visualize the data by province
st.subheader(f"Visualisasi Data Perdagangan: {provinsi}")
filtered_data = data[data['Provinsi'] == provinsi]
st.write(filtered_data)

# Load GeoJSON for provinces
geojson_data = load_geojson()

# Merge data with GeoJSON for location plotting
merged = geojson_data.merge(data, left_on='provinsi', right_on='Provinsi', how='inner')

# Map setup
m = folium.Map(location=[-2.5, 118], zoom_start=5)

# Marker Cluster for all points
marker_cluster = MarkerCluster().add_to(m)
for idx, row in merged.iterrows():
    folium.Marker(
        location=[row['geometry'].centroid.y, row['geometry'].centroid.x],
        popup=f"{row['Provinsi']}: {row['Data Perdagangan']} ",  # customize based on your data
        tooltip=row['Provinsi']
    ).add_to(marker_cluster)

# Render Map in Streamlit
st.subheader("Peta Provinsi dan Perdagangan")
st_data = st_folium(m, width=700, height=500)

# Additional Feature: Route Mapping (Optional, needs API integration)
st.subheader("Simulasi Rute Antar Provinsi (opsional)")
start_province = st.selectbox("Pilih Provinsi Awal:", data['Provinsi'].unique())
end_province = st.selectbox("Pilih Provinsi Akhir:", data['Provinsi'].unique())

st.write("Silakan masukkan API tambahan untuk rute antar lokasi (opsional).")
