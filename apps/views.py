# Python modules
from typing import Any, List, Callable
from timezonefinder import TimezoneFinder
from datetime import datetime
import pytz
from geopy.geocoders import Nominatim

# Django modules
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt


def hello_view(
    request: HttpRequest,
    *args: tuple[Any, ...],
    **kwargs: dict[str, Any]
) -> HttpResponse:
    """
    Return a simple HTML page.

    Parameters:
        request: HttpRequest
            The request object.
        *args: list
            Additional positional arguments.
        **kwargs: dict
            Additional keyword arguments.
    
    Returns:
        HttpResponse
            Rendered HTML page with a name in the context.
    """

    return render(
        request=request,
        template_name="index.html",
        context={"name": "Dias", "names": []},
        status=200
    )

def users_info(
        request: HttpRequest,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any],
) -> HttpResponse:
    """
    Return a HTML page with user informatiom.

    Parameters:
        request: HttpRequest
            The request object.
        *args: list
            Additional positional arguments.
        **kwargs: dict
            Additional keyword arguments.
    
    Returns:
        HttpResponse
            Rendered HTML page with user information(name, age) in the context.
    """
    
    return render(
        request=request,
        template_name="users.html",
        context={"users": [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25},
            {"name": "Charlie", "age": 35},
        ]},
        status=200,
    )

def city_time(
        request: HttpRequest,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any],
) -> HttpResponse:
    """
    Return a HTML page with current time in different cities.

    Parameters:
        request: HttpRequest
            The request object.
        *args: list
            Additional positional arguments.
        **kwargs: dict
            Additional keyword arguments.

    Returns:
        HttpResponse
            Rendered HTML page with real time in different cities in the context.
    """

    city_names: List[str] = ['New York', 'London', 'Tokyo', 'Sydney', 'Almaty']
    cities_info: List[dict[str, Any]] = []
    
    for city_name in city_names:
        # Get coordinates from city name
        geolocator = Nominatim(user_agent="city_time_view")
        location = geolocator.geocode(city_name)
        
        if location:
            lat, lon = location.latitude, location.longitude
            
            # Get timezone using latitude and longitude
            tz_finder = TimezoneFinder()
            timezone_str = tz_finder.timezone_at(lng=lon, lat=lat)
            
            if timezone_str:
                # Get current time in that timezone
                timezone = pytz.timezone(timezone_str)
                city_time = datetime.now(timezone)
                
                cities_info.append({
                    city_name: city_time.strftime('%Y-%m-%d %H:%M:%S')
                })
            else:
                print(f"Could not find the timezone for {city_name}")
        else:
            print(f"City {city_name} not found.")
        
    return render(
        request=request,
        template_name="city_time.html",
        context={"city_times": cities_info},
        status=200,
    )

@csrf_exempt
def counter(
        request: HttpRequest,
        *args: tuple[Any, ...],
        **kwargs: dict[str, Any],
) -> HttpResponse:
    """
    Return a HTML page with a counter value.

    Parameters:
        request: HttpRequest
            The request object.
        *args: list
            Additional positional arguments.
        **kwargs: dict
            Additional keyword arguments.

    Returns:
        HttpResponse
            Rendered HTML page with a value that can be incremented or decremented in the context.
    """
    class Counter:
        count = 0

        def increment(self):
            self.count += 1
            return ''

        def decrement(self):
            self.count -= 1
            return ''

        def double(self):
            self.count *= 2
            return ''
   
    counter_value = Counter()

    return render(
        request=request,
        template_name="counter.html",
        context={"counter": counter_value},
        status=200,
    )
