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

# Map setup with restricted zoom levels
m = folium.Map(location=[-2.5, 118], zoom_start=5, min_zoom=4, max_zoom=7)

# Marker Cluster for all points
marker_cluster = MarkerCluster().add_to(m)
for idx, row in merged.iterrows():
    # Create a custom popup with all relevant data for each province
    popup_info = f"""
    <strong>{row['Provinsi']}</strong><br>
    Mode Transportasi Laut: {row.get('Mode Transportasi Laut', 'Data Tidak Tersedia')}<br>
    Volume Total Pembelian: {row.get('Volume Total Pembelian', 'Data Tidak Tersedia')}<br>
    Nilai Pembelian (Triliun RP): {row.get('Nilai Pembelian (Triliun RP)', 'Data Tidak Tersedia')}<br>
    Komoditas Pembelian: {row.get('Komoditas Pembelian', 'Data Tidak Tersedia')}<br>
    Pembelian Terbesar: {row.get('Pembelian Terbesar', 'Data Tidak Tersedia')}<br>
    Volume Total: {row.get('Volume Total', 'Data Tidak Tersedia')}<br>
    Nilai Penjualan (Triliun RP): {row.get('Nilai Penjualan (Triliun RP)', 'Data Tidak Tersedia')}<br>
    Komoditas Penjualan: {row.get('Komoditas Penjualan', 'Data Tidak Tersedia')}<br>
    Penjualan Terbesar: {row.get('Penjualan Terbesar', 'Data Tidak Tersedia')}
    """
    
    popup = folium.Popup(popup_info, max_width=300, min_width=200)  # Set fixed size for easier reading
    tooltip = folium.Tooltip(row['Provinsi'], sticky=True)  # Tooltip that stays open while hovering
    
    folium.Marker(
        location=[row['geometry'].centroid.y, row['geometry'].centroid.x],
        popup=popup,
        tooltip=tooltip
    ).add_to(marker_cluster)

# Feature to add route between provinces
st.subheader("Buat Jalur Antar Provinsi Berdasarkan Pembelian dan Penjualan Terbesar")

# Dropdown selection for route
start_province = st.selectbox("Pilih Provinsi Asal (Pembelian Terbesar):", merged['Provinsi'].unique())
end_province = st.selectbox("Pilih Provinsi Tujuan (Penjualan Terbesar):", merged['Provinsi'].unique())

# Add route if both provinces are selected
if st.button("Tampilkan Jalur"):
    start_location = merged[merged['Provinsi'] == start_province]
    end_location = merged[merged['Provinsi'] == end_province]
    
    if not start_location.empty and not end_location.empty:
        start_coords = [start_location['geometry'].centroid.y.values[0], start_location['geometry'].centroid.x.values[0]]
        end_coords = [end_location['geometry'].centroid.y.values[0], end_location['geometry'].centroid.x.values[0]]
        
        # Draw line on map
        folium.PolyLine(
            locations=[start_coords, end_coords],
            color="blue",
            weight=5,
            opacity=0.7,
            tooltip=f"Jalur dari {start_province} ke {end_province}"
        ).add_to(m)

# Render Map in Streamlit
st.subheader("Peta Provinsi dan Perdagangan")
st_data = st_folium(m, width=700, height=500)
