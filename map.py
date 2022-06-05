import folium
import pandas as pd
import webbrowser

import main

my_map = folium.Map(
    location=[52.388980865478516,16.89756965637207]
)
tram_data=main.create_data_frame_from_tram_data(main.get_tram_data())
for _,tram in tram_data.iterrows():
    folium.Marker(
        location=[tram['lat'],tram['lon']],
        popup=int(tram['id'])
    ).add_to(my_map)

#marker1 = folium.Marker(location=[52.388980865478516,16.89756965637207]).add_to(my_map)

# a=[]
# b=main.create_data_frame_from_tram_data(main.get_tram_data())
# print(b.at[0,'lat'])
print(my_map)
my_map.save("map.html")
webbrowser.open("map.html")