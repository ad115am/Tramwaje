import folium
import pandas as pd
import webbrowser
my_map = folium.Map(
    location=[52.388980865478516,16.89756965637207]
)
marker1 = folium.Marker(location=[52.388980865478516,16.89756965637207]).add_to(my_map)


print(my_map)
my_map.save("map.html")
webbrowser.open("map.html")