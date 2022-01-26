from datetime import datetime
from typing import Tuple


class Station:
	def __init__(self, data, status):
		self.id: str  = data[0]
		self.name: str = data[1]
		self.capacity: int = int(data[2])
		self.location: Tuple[float, float] = (float(data[3]), float(data[4]))
		self.status: Station_Status = Station_Status(status)
	
class Station_Status:
	def __init__(self, data):
		self.is_deployed: bool = data[1] == '1'
		self.is_renting: bool = data[2] == '1'
		self.is_returning: bool = data[3] == '1'
		self.last_reported: datetime = datetime.fromtimestamp(int(data[4]))
		self.available_bikes: int = int(data[5])
		self.available_ebikes: int = int(data[6])
		# L'attribut  `num_bikes_available_mechanical` est inutile
		# Il est égal à la différence de `available_bikes` et `available_ebikes`
		self.available_docks: int = int(data[8])

# Ouverture des fichiers CSV
raw_stations = open('station_information.csv').readlines()
raw_status = open('station_status.csv').readlines()

# Créations de toutes les instances de Station
stations = []
for i in range(1,len(raw_stations)):
	station_entry = raw_stations[i][:-1].split(';')
	status_entry = raw_status[i][:-1].split(';')
	stations.append(Station(station_entry, status_entry))

## Question a
print('\n== Question (a) ==\n')
not_deployed_count = 0
for station in stations:
	if not station.status.is_deployed:
		not_deployed_count+=1

percentage = not_deployed_count/len(stations) * 100
print(f'{round(percentage, 2)}% des stations ne sont pas déployées.')

## Question b
print('\n== Question (b) ==\n')
print('Stations dont le nom contient \'Lecourbe\' : ')
for station in stations:
	if 'Lecourbe' in station.name:
		print(station.name)

## Question c
print('\n== Question (c) ==\n')
lowest_lat = 90
lowest_name = ''
for station in stations:
	if station.location[0] < lowest_lat:
		lowest_lat = station.location[0]
		lowest_name = station.name
print(f'La station la plus au sud est la station {lowest_name}')

## Question d
print('\n== Question (d) ==\n')
most_available = 0
most_available_name = ''
for station in stations:
	if station.status.available_bikes > most_available:
		most_available = station.status.available_bikes
		most_available_name = station.name

print(f'Station avec le plus grand nombre de vélos disponibles : {most_available_name}')

## Question e
print('\n== Question (e) ==\n')
print('Stations dont le nombre de vélos disponibles est supérieur au nombre de bornettes : ')
for station in stations:
	if station.status.available_bikes > station.capacity:
		print(station.name)