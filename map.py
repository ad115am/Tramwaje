import folium
import webbrowser

import main

my_map = folium.Map(
    location=[52.388980865478516,16.89756965637207],
    zoom_start=12
)
tram_data=main.create_data_frame_from_tram_data(main.get_tram_data())
def show_trams_on_map(filter):
    filter=filter
    valid_id= range(0,1000)
    print(filter)
    if filter== 'double-sided':
        valid_id = range(900,999)
    elif filter == 'siemens':
        valid_id = range(501, 515)
    elif filter == 'all':
        pass




    for _,tram in tram_data.iterrows():
        if int(tram['id']) in valid_id:
            print(valid_id)
            tram_id = int(tram['id'])
            route_id = int(tram['route_id'])
            delay = int(tram['delay'])
            speed = int(tram['speed'])
            icon_size=(50,50)
            if delay > 120:
                icon = folium.Icon(color='red',icon="subway",prefix='fa')
            elif delay<-120:
                icon = folium.Icon(color='green', icon="subway", prefix='fa')
            else:
                icon = folium.Icon(color='blue',icon="subway",prefix='fa')
            folium.Marker(
                location=[tram['lat'],tram['lon']],
                popup=int(tram['id']),
                tooltip=f'id: {tram_id}, route: {route_id}, delay: {delay}, speed: {speed}',
                icon=icon


            ).add_to(my_map)
    print(my_map)
    my_map.save("map.html")
    webbrowser.open("map.html")
#marker1 = folium.Marker(location=[52.388980865478516,16.89756965637207]).add_to(my_map)

# a=[]
# b=main.create_data_frame_from_tram_data(main.get_tram_data())
# print(b.at[0,'lat'])
show_trams_on_map('all')
#show_trams_on_map('double-sided')
#show_trams_on_map('siemens')