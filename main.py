from google.transit import gtfs_realtime_pb2
import requests
import pandas as pd

trams_dataframe = pd.DataFrame()


def get_only_trams(vehicle_id):
    if 0 < vehicle_id < 999:
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


def download_vehicle_positions_pb_old():
    feed = gtfs_realtime_pb2.FeedMessage()
    response = requests.get(
        'https://www.ztm.poznan.pl/pl/dla-deweloperow/getGtfsRtFile/?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9'
        '.eyJpc3MiOiJ0ZXN0Mi56dG0ucG96bmFuLnBsIiwiY29kZSI6MSwibG9naW4iOiJtaFRvcm8iLCJ0aW1lc3RhbXAiOjE1MTM5NDQ4MTJ9.'
        'ND6_VN06FZxRfgVylJghAoKp4zZv6_yZVBu_1-yahlo&file=vehicle_positions.pb')
    feed.ParseFromString(response.content)

    for entity in feed.entity:
        if get_only_trams(int(entity.vehicle.vehicle.id)):
            print(
                f'id: {entity.vehicle.vehicle.id} route_id: {entity.vehicle.trip.route_id} lat: {entity.vehicle.position.latitude}'
                f' lon: {entity.vehicle.position.longitude} speed: {round(entity.vehicle.position.speed * 3.6)} km/h')


def download_trip_updates_pb_old():
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
                f'stop sequence: {entity.trip_update.stop_time_update[0].stop_sequence} '
                f'delay: {entity.trip_update.stop_time_update[0].arrival.delay}')


def download_vehicle_positions_pb():
    feed = gtfs_realtime_pb2.FeedMessage()
    response = requests.get(
        'https://www.ztm.poznan.pl/pl/dla-deweloperow/getGtfsRtFile/?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9'
        '.eyJpc3MiOiJ0ZXN0Mi56dG0ucG96bmFuLnBsIiwiY29kZSI6MSwibG9naW4iOiJtaFRvcm8iLCJ0aW1lc3RhbXAiOjE1MTM5NDQ4MTJ9.'
        'ND6_VN06FZxRfgVylJghAoKp4zZv6_yZVBu_1-yahlo&file=vehicle_positions.pb')
    return feed, response


def download_trip_updates_pb():
    feed = gtfs_realtime_pb2.FeedMessage()
    response = requests.get(
        '   https://www.ztm.poznan.pl/pl/dla-deweloperow/getGtfsRtFile/?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.'
        'eyJpc3MiOiJ0ZXN0Mi56dG0ucG96bmFuLnBsIiwiY29kZSI6MSwibG9naW4iOiJtaFRvcm8iLCJ0aW1lc3RhbXAiOjE1MTM5NDQ4MTJ9.'
        'ND6_VN06FZxRfgVylJghAoKp4zZv6_yZVBu_1-yahlo&file=trip_updates.pb')
    return feed, response


# to download both at the same time so that the data match
def get_tram_data():
    vehicle_positions_pb_feed, vehicle_positions_pb_response = download_vehicle_positions_pb()
    trip_updates_pb_feed, trip_updates_pb_response = download_trip_updates_pb()
    vehicle_positions_pb_feed.ParseFromString(vehicle_positions_pb_response.content)
    trip_updates_pb_feed.ParseFromString(trip_updates_pb_response.content)
    return vehicle_positions_pb_feed.entity, trip_updates_pb_feed.entity


def create_data_frame_from_tram_data(tram_data):
    vehicle_positions_list = []
    trip_updates_list = []
    for entity in tram_data[0]:
        if get_only_trams(int(entity.vehicle.vehicle.id)):
            vehicle_positions_list.append(
                [int(entity.vehicle.vehicle.id), int(entity.vehicle.trip.route_id), entity.vehicle.position.latitude,
                 entity.vehicle.position.longitude, round(entity.vehicle.position.speed * 3.6)])

    for entity in tram_data[1]:
        if get_only_trams(int(entity.trip_update.vehicle.id)):
            trip_updates_list.append(
                [int(entity.trip_update.vehicle.id), int(entity.trip_update.trip.route_id),
                 entity.trip_update.stop_time_update[0].stop_sequence,
                 entity.trip_update.stop_time_update[0].arrival.delay
                 ])
    vehicle_positions_columns = ["id", "route_id", "lat", "lon", "speed"]
    trip_updates_columns = ["id", "route_id", "stop_seq", "delay"]
    data_frame_vehicle_positions = pd.DataFrame(vehicle_positions_list, columns=vehicle_positions_columns)
    data_frame_trip_updates = pd.DataFrame(trip_updates_list, columns=trip_updates_columns)
    data_frame_merged = data_frame_vehicle_positions.merge(data_frame_trip_updates, how='inner')
    # print(data_frame_vehicle_positions)
    # print(data_frame_trip_updates)
    #print(data_frame_merged.to_string())
    # print(vehicle_positions_list)
    # print(trip_updates_list)
    return (data_frame_merged)


# download_feeds_pb()
# download_trip_updates_pb()
# download_vehicle_positions_pb()
# get_tram_data()
create_data_frame_from_tram_data(get_tram_data())
