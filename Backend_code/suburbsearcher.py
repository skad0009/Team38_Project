import requests
import pandas as pd
import mysql.connector
from mysql.connector import errorcode
import folium
#Set the connection 
config = {
  'host':'db-infotoad.mysql.database.azure.com',
  'user':'infotoad38admin',
  'password':'cO52LFKBwNYrmXVJvbdM',
  'database':'dbtoad',
  'client_flags': [mysql.connector.ClientFlag.SSL],
  'ssl_ca': '/Users/pavneetheer/Downloads/DigiCertGlobalRootCA.crt.pem'
}

conn = mysql.connector.connect(**config)


cursor=conn.cursor()
suburb= input("Enter your suburb")
Suburb=suburb.title()

Query= """ SELECT Latitude, Longitude, Year
FROM data where 
Suburb = %s;
"""
cursor.execute(Query, (Suburb,))

results = cursor.fetchall()


#Center of the map 
mymap = folium.Map(location=[-25.2744,133.7751], zoom_start=6)

#Make a dictionary 
total={}
#Go over the results 

for result in results:
    #The following is the result
    Latitude, Longitude, Year = result
    occurence= f"{Latitude}_{Longitude}_{Year}"
    # Increase the count of occurrences for the marker
    total[occurence] = total.get(occurence, 0) + 1
    #Pop up text says the year and the poccurences 
    text = f"Year: {Year} \n Occurrences: {total[occurence]}"
    popup = folium.Popup(text, parse_html=True)
    #Markers are created based on location and longitude and a pop is created for the particular location
    folium.CircleMarker(location=[Latitude, Longitude],radius=2, color='Red',  fill=True,fill_color="Red",popup=popup).add_to(mymap)

# Save the map to an HTML file
mymap.save("suburb_map.html")