from datetime import datetime


class Station:
	def __init__(self, data, status):
		self.id = data[0]
		self.name = data[1]
		self.capacity = int(data[2])
		self.location = (float(data[3]), float(data[4]))
		self.status = Station_Status(status)
	
class Station_Status:
	def __init__(self, data):
		self.is_deployed = data[1] == '1'
		self.is_renting = data[2] == '1'
		self.is_returning = data[3] == '1'
		self.last_reported = datetime.fromtimestamp(int(data[4]))
		self.available_bikes = int(data[5])
		self.available_ebikes = int(data[6])
		self.available_mechanical_bikes = int(data[7])
		self.available_docks = int(data[8])


raw_stations = open('station_information.csv').readlines()
raw_status = open('station_status.csv').readlines()

stations = []

for i in range(1,len(raw_stations)):
	station_entry = raw_stations[i][:-1].split(';')
	status_entry = raw_status[i][:-1].split(';')
	stations.append(Station(station_entry, status_entry))


## Question a
not_deployed_count = 0
for station in stations:
	if not station.status.is_deployed:
		not_deployed_count+=1

percentage = not_deployed_count/len(stations) * 100
print(f'{round(percentage, 2)}% des stations ne sont pas déployées.')

## Question b
print('Stations dont le nom contient Lecourbe: ')
for station in stations:
	if 'Lecourbe' in station.name:
		print(station.name)

## Question c
lowest_lat = 90
lowest_name = ''
for station in stations:
	if station.location[0] < lowest_lat:
		lowest_lat = station.location[0]
		lowest_name = station.name
print(f'Plus petite latitude : {lowest_name}')