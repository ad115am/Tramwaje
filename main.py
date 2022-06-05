from google.transit import gtfs_realtime_pb2
import requests
import pandas as pd

trams_dataframe = pd.DataFrame()
def get_only_trams(vehicle_id):
    if 1 < vehicle_id < 999:
        return True


def download_feeds_pb():
    feed = gtfs_realtime_pb2.FeedMessage()
    response = requests.get(
        'https://www.ztm.poznan.pl/pl/dla-deweloperow/getGtfsRtFile/?token='
        'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJ0ZXN0Mi56dG0ucG96bmFuLnBsIiwiY29kZSI6MSwibG9naW4iOiJtaFRvcm8i'
        'LCJ0aW1lc3RhbXAiOjE1MTM5NDQ4MTJ9.ND6_VN06FZxRfgVylJghAoKp4zZv6_yZVBu_1-yahlo&file=feeds.pb')
    feed.ParseFromString(response.content)
    print('feeds_pb start')
    for entity in feed.entity:
        print(entity)



def download_vehicle_positions_pb():
    feed = gtfs_realtime_pb2.FeedMessage()
    response = requests.get(
        'https://www.ztm.poznan.pl/pl/dla-deweloperow/getGtfsRtFile/?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9'
        '.eyJpc3MiOiJ0ZXN0Mi56dG0ucG96bmFuLnBsIiwiY29kZSI6MSwibG9naW4iOiJtaFRvcm8iLCJ0aW1lc3RhbXAiOjE1MTM5NDQ4MTJ9.'
        'ND6_VN06FZxRfgVylJghAoKp4zZv6_yZVBu_1-yahlo&file=vehicle_positions.pb')
    feed.ParseFromString(response.content)
    # print(feed.entity)
    # print(type(feed.entity))
    # a = str(feed.entity)
    # print(a)
    for entity in feed.entity:
        # if entity.HasField('trip_update'):
        if get_only_trams(int(entity.vehicle.vehicle.id)):
            print(
                f'id: {entity.vehicle.vehicle.id} route_id: {entity.vehicle.trip.route_id} lat: {entity.vehicle.position.latitude}'
                f' lon: {entity.vehicle.position.longitude} speed: {round(entity.vehicle.position.speed*3.6)} km/h')


def download_trip_updates_pb():
    feed = gtfs_realtime_pb2.FeedMessage()
    response = requests.get(
        '   https://www.ztm.poznan.pl/pl/dla-deweloperow/getGtfsRtFile/?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.'
        'eyJpc3MiOiJ0ZXN0Mi56dG0ucG96bmFuLnBsIiwiY29kZSI6MSwibG9naW4iOiJtaFRvcm8iLCJ0aW1lc3RhbXAiOjE1MTM5NDQ4MTJ9.'
        'ND6_VN06FZxRfgVylJghAoKp4zZv6_yZVBu_1-yahlo&file=trip_updates.pb')
    feed.ParseFromString(response.content)
    for entity in feed.entity:
        # if entity.HasField('trip_update'):
        if get_only_trams(int(entity.trip_update.vehicle.id)):
            print(
                f'id: {entity.trip_update.vehicle.id} route_id: {entity.trip_update.trip.route_id} '
                f'stop sequence: {entity.trip_update.stop_time_update[0].stop_sequence} delay: {entity.trip_update.stop_time_update[0].arrival.delay}')




def create_trams_dataframe():
    pass
#download_feeds_pb()
download_trip_updates_pb()
#download_vehicle_positions_pb()
