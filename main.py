from google.transit import gtfs_realtime_pb2
import requests


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
    for entity in feed.entity:
        if entity.HasField('trip_update'):
            print(entity.trip_update)


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
                f' lon: {entity.vehicle.position.longitude} speed : {entity.vehicle.position.speed}')


def download_trip_updates_pb():
    feed = gtfs_realtime_pb2.FeedMessage()
    response = requests.get(
        '   https://www.ztm.poznan.pl/pl/dla-deweloperow/getGtfsRtFile/?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.'
        'eyJpc3MiOiJ0ZXN0Mi56dG0ucG96bmFuLnBsIiwiY29kZSI6MSwibG9naW4iOiJtaFRvcm8iLCJ0aW1lc3RhbXAiOjE1MTM5NDQ4MTJ9.'
        'ND6_VN06FZxRfgVylJghAoKp4zZv6_yZVBu_1-yahlo&file=trip_updates.pb')
    feed.ParseFromString(response.content)
    for entity in feed.entity:
        # if entity.HasField('trip_update'):
        print(entity)


# download_feeds_pb()
# download_trip_updates_pb()
download_vehicle_positions_pb()
