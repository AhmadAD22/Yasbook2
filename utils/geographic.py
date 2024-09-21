from geopy.distance import geodesic
from auth_login.models import Provider
from provider_details.models import Store
from provider_details.serializers import NearbyFeaturedStoreOrderSerializer

def get_nearest_store(customer_latitude, customer_longitude,store_ids):
    stores = Store.objects.filter(id__in=store_ids)
    store_with_distance = []

    for store in stores:
       provider_latitude =store.provider.latitude
       provider_longitude = store. provider.longitude

       if provider_latitude and provider_longitude:
            provider_location = (provider_latitude, provider_longitude)
            customer_location = (customer_latitude, customer_longitude)
            distance = geodesic(provider_location, customer_location).km
            store_with_distance.append((store, distance))
    store_with_distance.sort(key=lambda x: x[1])  # Sort Stores by distance 
    # return the stors and their distance
    ordered_stors = [{'store':NearbyFeaturedStoreOrderSerializer(store).data,'distance':distance} for store, distance in store_with_distance]
    return ordered_stors

def distance(customer_latitude, customer_longitude,provider_latitude, provider_longitude,):
    if provider_latitude and provider_longitude and customer_latitude and customer_longitude:
            provider_location = (provider_latitude, provider_longitude)
            customer_location = (customer_latitude, customer_longitude)
            distance = geodesic(provider_location, customer_location).kilometers
            return distance
            