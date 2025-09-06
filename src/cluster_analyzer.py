
import sys
import folium
from folium import plugins
import pandas as pd
from geopy.distance import geodesic
from tabulate import tabulate
import googlemaps
import os

# Update CSV with Address Lat/Lon columns
def add_address_lat_lon_columns(df):
    if 'FullAddress' not in df.columns:
        full_addresses = []
        for _,row in df.iterrows():
            full_addresses.append((str(row['Address']) + ", " + str(row['City']) + ", " + str(row['State']) + str(" 0") + str(row['Zip'])).replace(",,",","))
        df['FullAddress'] = full_addresses
    gmaps = googlemaps.Client(key=os.getenv('GOOGLE_MAP_API_KEY'))
    if 'Lat' not in df.columns or 'Lon' not in df.columns:
        latitudes = []
        longitudes = []
        for address in df['FullAddress']:
            try:
                print(f"Geocoding({0}): {address}")
                location = gmaps.geocode(address)[0]['geometry']['location']
                latitudes.append(location['lat'] if location else None)
                longitudes.append(location['lng'] if location else None)
            except Exception as e:
                print(f"Error geocoding {address}: {e}")
                latitudes.append(None)
                longitudes.append(None)
        df['Lat'] = latitudes
        df['Lon'] = longitudes    
    return df    

def update_csv_with_lat_lon(df=pd.read_csv('data/parishioners.csv'), filename='data/parishioner-address.csv'):
    df = add_address_lat_lon_columns(df)
    
    df.to_csv(filename, index=False)
    return df


# Check if within radius
def within_radius(row, center, radius_miles=10):
    point = (row['Lat'], row['Lon'])
    return geodesic(center, point).miles <= radius_miles

# Print addresses within 10 miles of each address
def print_within_10(df=pd.read_csv('data/parishioner-address.csv')):
    with open('output/clusters.txt', 'w') as f:
        sys.stdout = f
        for _, row in df.iterrows():
            df_within_10 = df[df.apply(within_radius, axis=1, center=(row['Lat'], row['Lon']))]
            print(f"Addresses within 10 miles of Family: {row['AdultFirstNames']} \nAddress: {row['FullAddress']}")
            print(tabulate(df_within_10[['AdultFirstNames', 'FullAddress']], headers=['index','Family', 'Address'])) 
        f.close()
        sys.stdout = sys.__stdout__

# Generate clustered map
def generate_clusters(df=pd.read_csv('data/parishioner-address.csv')):
    # Create a map centered on the average latitude and longitude
    map_obj = folium.Map(location=[df['Lat'].mean(), df['Lon'].mean()], zoom_start=10)
    marker_cluster = plugins.MarkerCluster().add_to(map_obj)
    for _, row in df.iterrows():
        print(row['AdultFirstNames'],row['FullAddress'], row['Lat'], row['Lon'])
        html=f"""
        <div style="font-family: Arial; font-size: 14px;">
        <div style="background-color: #2596be; color:white; font-weight:300; font-size: 14px; padding:4px;">{row['AdultFirstNames']}</div>
        <b>Address:</b> {row['FullAddress']}<br>
        </div>
        """
        iframe = folium.IFrame(html=html, width=300, height=95)
        popup = folium.Popup(iframe, max_width=300, max_height=95)
        folium.Marker(location=[row['Lat'], row['Lon']], popup=popup).add_to(marker_cluster)
    map_obj.save('output/address_clusters.html') 

def main():
    args = sys.argv[1:] 
    if len(args) > 0 and args[0] == 'map':
        generate_clusters()
    elif len(args) > 0 and args[0] == 'cluster':
        print_within_10()
    elif len(args) > 0 and args[0] == 'update':
        update_csv_with_lat_lon()
    else:
        print("\n\nUsage: python src/cluster_analyzer.py map|cluster|update")
        print("map - generates an HTML map with clustered addresses. See output/address_clusters.html\n")
        print("cluster - prints addresses within 10 miles of each address. See output/clusters.txt\n")  
        print("update - updates parishioners.csv with Lat/Lon columns and saves to data/parishioner-address.csv\n\n")

# Using the special variable 
# __name__
if __name__=="__main__":
    main()
