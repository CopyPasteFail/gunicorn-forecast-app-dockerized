"""
 Title: Python final project
 Author: Omer Reznik
 Description: A helper module for the weather app, handles API calls to weather and location services
 Reviewed by: Ben, Aviad
"""

# for getting coordinates of a city/country
from geopy.geocoders import Nominatim  # not built-in
import requests  # not built-in


def get_long_lat(in_location: str) -> tuple:
    """
    Uses geopy module to retrieve geographical info about the given location
    Note: geolocator.geocode() requires internet connection
    If the operation fails, an exception will be raised

    :param in_location: the location to search for

    :return: the location's latitude, longitude, and full address (in the local language)
    """
    geolocator = Nominatim(user_agent="geoapiExercises")

    result = geolocator.geocode(in_location)

    if result is None:
        raise Exception ("get_long_lat(): geolocator.geocode() returned None "
                         + "(location '"+ in_location + "' couldn't be found)")

    return result.latitude, result.longitude, str(result)


def get_json_from_weather_service(in_lat_long: tuple) -> dict:
    """
    Send an API request to meteo web service
    If the operation fails, an exception will be raised

    :param in_lat_long: a tuple of containing (ints) latitude and longitude

    :return: the received JSON object as a dict
    """
    http_res = requests.get(
        'https://api.open-meteo.com/v1/forecast?latitude=' + str(in_lat_long[0])
        + '&longitude=' + str(in_lat_long[1]) +
        '&daily=temperature_2m_max,temperature_2m_min&timezone=auto')

    if http_res.status_code != 200:
        # if the API request wasn't successful (i.e. the web service returned an error)
        raise Exception ("get_json_from_weather_service(): " +
                         "http request returned: " + str(http_res.status_code))

    json_object_dict = http_res.json()  # convert to dict

    return json_object_dict


def get_weather_forecast(in_location: str) -> list:
    """
    Retrieves the coordinates of the desired location
    and uses the coordinates to get the weather forecast information

    :param in_location: The location of which is the weather forecast is desired

    :return: the location full address, and the 7 day forecast information
    """
    ret_list = []

    long_lat_name = get_long_lat(in_location)  # getting the location coordinates and name
    ret_list.append(long_lat_name[2])  # appending the location name
    weather_dict = get_json_from_weather_service(long_lat_name)
    # if dict.get() fails it returns 'None'
    ret_list.append(weather_dict.get('daily').get("time"))  # appending the dates list
    ret_list.append(weather_dict.get('daily').get("temperature_2m_min"))  # appending min temps list
    ret_list.append(weather_dict.get('daily').get("temperature_2m_max"))  # appending max temps list

    if None in ret_list:
        # when one or more the required details are missing
        raise Exception ("get_weather_forecast(): Received JSON doesn't have the necessary info")

    return ret_list


if __name__ == '__main__':
    """ unit testing """
    try:
        test_list = get_weather_forecast("neverl")
    except Exception as e:
        print(f"caught this: {e}")
    else:
        print (f"test_list = {test_list}")

    try:
        get_json_from_weather_service(("", ""))
    except Exception as e:
        print(f"caught this: {e}")
