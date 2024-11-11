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
    # Load the uploaded GeoJSON file
    gdf = gpd.read_file("indonesia.geojson")
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

# Display GeoJSON structure to understand columns
st.write("GeoJSON Columns:", geojson_data.columns)

# Adjust column names if necessary based on GeoJSON file
geojson_data = geojson_data.rename(columns={"state": "Provinsi"})  # Change "state" to match actual column name if necessary

# Standardize the 'Provinsi' column in both dataframes for consistency
geojson_data['Provinsi'] = geojson_data['Provinsi'].str.strip().str.upper()
data['Provinsi'] = data['Provinsi'].str.strip().str.upper()

# Merge data with GeoJSON based on 'Provinsi'
merged = geojson_data.merge(data, on='Provinsi', how='inner')

# Confirm merged data
st.write("Merged data:", merged)

# Map setup
m = folium.Map(location=[-2.5, 118], zoom_start=5)

# Marker Cluster for all points
marker_cluster = MarkerCluster().add_to(m)
for idx, row in merged.iterrows():
    # Update 'Nilai Perdagangan' based on actual column name in your data
    popup_info = f"{row['Provinsi']}: {row.get('Nilai Perdagangan', 'Data Tidak Tersedia')}"
    
    folium.Marker(
        location=[row['geometry'].centroid.y, row['geometry'].centroid.x],
        popup=popup_info,
        tooltip=row['Provinsi']
    ).add_to(marker_cluster)

# Render Map in Streamlit
st.subheader("Peta Provinsi dan Perdagangan")
st_data = st_folium(m, width=700, height=500)

# Optional: Route Mapping Simulation (requires API for real routing)
st.subheader("Simulasi Rute Antar Provinsi (opsional)")
start_province = st.selectbox("Pilih Provinsi Awal:", data['Provinsi'].unique())
end_province = st.selectbox("Pilih Provinsi Akhir:", data['Provinsi'].unique())

st.write("Silakan masukkan API tambahan untuk rute antar lokasi (opsional).")
