import requests
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import re
from geopy.exc import GeocoderUnavailable
import time
import os

def fetch_endodontists_by_city_state(city, state):
    base_url = "https://npiregistry.cms.hhs.gov/api/"
    params = {
        "version": "2.1",
        "enumeration_type": "NPI-1",
        "taxonomy_description": "Endodontic",
        "city": city,
        "state": state,
        "limit": 1000
    }
    
    response = requests.get(base_url, params=params)
    data = response.json()
    if not data.get('results'):
        return None
    
    firstname = []
    lastname = []
    address_1 = []
    address_2 = []
    city_list = []
    state_list = []
    zip_code = []
    desc = []

    for i in range(len(data['results'])):
        firstname.append(data['results'][i]['basic']['first_name'])
        lastname.append(data['results'][i]['basic']['last_name'])
        address_1.append(data['results'][i]['addresses'][0]['address_1'].lower())
        try:
            address_2.append(data['results'][i]['addresses'][0]['address_2'].lower())
        except KeyError:
            address_2.append('')  # Use empty string if address_2 is missing
        city_list.append(data['results'][i]['addresses'][0]['city'].lower())
        state_list.append(data['results'][i]['addresses'][0]['state'].lower())
        zip_code.append(data['results'][i]['addresses'][0]['postal_code'][:5])
        desc.append(data['results'][i]['taxonomies'][0]['desc'].lower())

    df = pd.DataFrame({
    
        'firstname': firstname,
        'lastname': lastname,
        'address_1': address_1, 
        'address_2': address_2, 
        'city': city_list, 
        'state': state_list, 
        'zip_code': zip_code, 
        'desc': desc  
    }).astype({

    'firstname': 'string',
    'lastname': 'string',
    'address_1': 'string',
    'address_2': 'string',
    'city': 'string',
    'state': 'string',
    'zip_code': 'string',  # using string to preserve leading zeroes
    'desc': 'string'
    })

    

    df = df[(df['city']==city.lower()) & (df['state']==state.lower())]
       

    return df
 
def geocode_with_retry(address, retries=3):
    geolocator = Nominatim(user_agent="myGeocoder", timeout=10)
    attempts = 0
    while attempts < retries:
        try:
            location = geolocator.geocode(address)
            if location:
                return location.latitude, location.longitude
            else:
                return None, None
        except Exception as e:
            attempts += 1
            time.sleep(2)
    return None, None
            
def aggregate_location_data(df):
    df['clean_address_1'] = df['address_1'].apply(
        lambda x: re.sub(r'\s*(ste|suite|apt|unit|bldg|fl)\s*\w+', '', str(x), flags=re.IGNORECASE))

    df['full_address'] = df['clean_address_1']  + ', ' + df['city'] + ', ' + df['state'] + ', ' + df['zip_code'] + ', ' + 'USA'

    for address in df['full_address']:
        latitude, longitude = geocode_with_retry(address)
        if latitude and longitude:
            df.loc[df['full_address'] == address, 'latitude'] = latitude
            df.loc[df['full_address'] == address, 'longitude'] = longitude
        else:
            df.loc[df['full_address'] == address, 'latitude'] = None
            df.loc[df['full_address'] == address, 'longitude'] = None
    return df

def get_rent_data(zipcode_list:list):
    columns_to_use = ['zipcode', 'studio', 'one_bedroom', 'two_bedroom', 'three_bedroom']
    column_dtypes = {
    'zipcode': 'string',
    'studio': 'string',
    'one_bedroom': 'string',
    'two_bedroom': 'string',
    'three_bedroom': 'string'
    }

    df = pd.read_csv('https://raw.githubusercontent.com/vathanahim/endo_workplace_insights/refs/heads/main/data/rent_data.csv', usecols =columns_to_use, dtype=column_dtypes )
    df = df[df['zipcode'].isin(zipcode_list)]

    return df

def get_population_data(city, state):
    try:
        df = pd.read_csv('data/uscities.csv.zip', compression='zip', usecols=['city', 'state_id', 'population'])
        # Convert the relevant columns to lowercase
        df['city'] = df['city'].str.lower()
        df['state_id'] = df['state_id'].str.lower()
        population = df[(df['city'] == city.lower()) & (df['state_id'] == state.lower())]['population'].values[0]
        return population
    except Exception as e:
        print(f"Error getting population data: {str(e)}")
        return None

