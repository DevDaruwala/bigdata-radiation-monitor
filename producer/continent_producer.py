import json
import time
import reverse_geocoder as rg # for extra feature if we want to use it later
import pycountry # because I want country name insted of country code 

# I am defining content for the using it later in key value feature in kafka
def map_to_continent(lat, lon):
    lat = float(lat)
    lon = float(lon)

    if -35 <= lat <= 37 and -17 <= lon <= 51:
        return "Africa"
    elif 35 <= lat <= 71 and -10 <= lon <= 40:
        return "Europe"
    elif -55 <= lat <= 12 and -80 <= lon <= -35:
        return "South America"
    elif 15 <= lat <= 70 and -170 <= lon <= -50:
        return "North America"
    elif -47 <= lat <= -10 and 110 <= lon <= 180:
        return "Oceania"
    elif -34 <= lat <= 60 and 60 <= lon <= 150:
        return "Asia"
    elif lat <= -60:
        return "Antarctica"
    else:
        return "Unknown"
    
from kafka import KafkaProducer
producer = KafkaProducer(bootstrap_servers='localhost:9092')

with open('/media/dev/Expansion/Big_data/Small_file.csv', 'r') as f:

    header = f.readline()
    columns = header.strip().split(',')
    for line in f:
        # Split the line into columns
        value = line.strip().split(',')
        data_dict = dict(zip(columns, value))
       
         # now we will define capture time here to later use in flink(event_time and watermark)
        capture_time = data_dict.get('Captured Time')

        #now here I will extract lat and lon for the key value feature
        lat = data_dict.get('Latitude')
        lon = data_dict.get('Longitude')
        continent = map_to_continent(lat, lon)
        data_dict['continent'] = continent

        # Just as metadata if we want to use it as extra feature going ahead and little bit of my curiosity
        try:
            geo_result = rg.search((float(lat), float(lon)))[0]  # returns dict with 'cc', 'name', etc.
            country_code = geo_result['cc']
            country = pycountry.countries.get(alpha_2=country_code)
            data_dict['country'] = country.name if country else "Unknown"
            data_dict['city'] = geo_result['name']
        except:
            data_dict['country'] = "Unknown"
            data_dict['city'] = "Unknown"

        #------------------------------------------------------------------------------------

        message = json.dumps(data_dict).encode('utf-8') #we converted in to jason till here 

        key = continent.encode('utf-8')

        # Send the message to Kafka
        producer.send('radiation-stream', key=key, value=message)
        producer.flush()
        print(f"Sent to Kafka | Key: {continent} | Message: {data_dict}")
        time.sleep(1)
