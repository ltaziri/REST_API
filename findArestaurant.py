from geocode import getGeocodeLocation
import json
import httplib2

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

foursquare_client_id = "JK1O0Z0DI4C4AEXOI5UI45IBCNXOU4BACNBQEUCASXGRCVCO"
foursquare_client_secret = "QHBHG0JZD3Z2PC200QGN2SLSQHEOXQS5LQPLHQ1HMXHAZDQH"


def findARestaurant(mealType,location):

    #1. Use getGeocodeLocation to get the latitude and longitude coordinates of the location string.
    coordinates = getGeocodeLocation(location);

    lat = str(coordinates[0])
    lon = str(coordinates[1])
        
    #2.  Use foursquare API to find a nearby restaurant with the latitude, longitude, and mealType strings.
    #HINT: format for url will be something like https://api.foursquare.com/v2/venues/search?client_id=CLIENT_ID&client_secret=CLIENT_SECRET&v=20130815&ll=40.7,-74&query=sushi
    url = ('https://api.foursquare.com/v2/venues/search?client_id=%s&client_secret=%s&v=20130815&ll=%s,%s&query=%s'% (foursquare_client_id, foursquare_client_secret, lat, lon, mealType))
    h = httplib2.Http()
    result = json.loads(h.request(url,'GET')[1])
        
    #3. Grab the first restaurant
    restaurant = result['response']['venues'][0]
    # print restaurant['location']['formattedAddress'][0]

    restaurant_id = restaurant['id']

    #4. Get a  300x300 picture of the restaurant using the venue_id (you can change this by altering the 300x300 value in the URL or replacing it with 'orginal' to get the original picture
    photo_url = ('https://api.foursquare.com/v2/venues/%s/photos?client_id=%s&client_secret=%s&v=20130815' % (restaurant_id, foursquare_client_id, foursquare_client_secret))
    photos = json.loads(h.request(photo_url,'GET')[1])

    #5. Grab the first image
    #6. If no image is available, insert default a image url

    count = photos['response']['photos']['count']

    if count == 0:
        photo = 'http://www.pizzahut-tt.com/wp-content/uploads/2013/06/pizza-hut-trinidad-and-tobago-pepperoni-lovers-pizza.png'
    else:
        photo = photos['response']['photos']['items'][0]['prefix']+"300x500"+photos['response']['photos']['items'][0]['suffix']

    result_dict = {}
    result_dict['name'] = restaurant['name']
    result_dict['address'] = restaurant['location']['formattedAddress'][0]
    result_dict['photo'] = photo
    
    #7. Return a dictionary containing the restaurant name, address, and image url  
    print result_dict['name']
    print result_dict['address']
    print result_dict['photo']
    return result_dict


if __name__ == '__main__':
    findARestaurant("Pizza", "Tokyo, Japan")
    findARestaurant("Tacos", "Jakarta, Indonesia")
    findARestaurant("Tapas", "Maputo, Mozambique")
    findARestaurant("Falafel", "Cairo, Egypt")
    findARestaurant("Spaghetti", "New Delhi, India")
    findARestaurant("Cappuccino", "Geneva, Switzerland")
    findARestaurant("Sushi", "Los Angeles, California")
    findARestaurant("Steak", "La Paz, Bolivia")
    findARestaurant("Gyros", "Sydney Australia")