import folium
import webbrowser

import main

my_map = folium.Map(
    location=[52.388980865478516, 16.89756965637207],
    zoom_start=12
)
tram_data = main.create_data_frame_from_tram_data(main.get_tram_data())


def show_trams_on_map(filter):
    vehicles_late=0
    vehicles_sum=0
    filter = filter
    valid_id = range(0, 100000)
    if filter == 'double-sided':
        valid_id = range(900, 999)
    elif filter == 'siemens':
        valid_id = range(501, 515)
    elif filter == 'all':
        pass

    for _, tram in tram_data.iterrows():
        if int(tram['id']) in valid_id:
            tram_id = int(tram['id'])
            route_id = int(tram['route_id'])
            delay = int(tram['delay'])
            speed = int(tram['speed'])
            if delay > 120:
                vehicles_late += 1
                icon = folium.Icon(color='red', icon="subway", prefix='fa')
            elif delay < -120:
                vehicles_sum += 1
                icon = folium.Icon(color='green', icon="subway", prefix='fa')
            else:
                vehicles_sum += 1
                icon = folium.Icon(color='blue', icon="subway", prefix='fa')
            folium.Marker(
                location=[tram['lat'], tram['lon']],
                popup=int(tram['id']),
                tooltip=f'id: {tram_id}, route: {route_id}, delay: {delay}, speed: {speed}',
                icon=icon

            ).add_to(my_map)
    print(f'vehicles late: {(vehicles_late/vehicles_sum)*100} %')
    my_map.save("map.html")
    webbrowser.open("map.html")


show_trams_on_map('all')
#show_trams_on_map('double-sided')
#show_trams_on_map('siemens')
