import csv
from os import listdir
from os.path import isfile, join
from datetime import datetime, timedelta

def parse_date(date_str):
    formats_to_try = ['%Y-%m-%d', '%Y/%m/%d']
    for fmt in formats_to_try:
        try:
            return datetime.strptime(date_str, fmt).strftime('%Y-%m-%d')
        except ValueError:
            continue

def get_next_day(date_str):
    formats_to_try = ['%Y-%m-%d', '%Y/%m/%d']
    for fmt in formats_to_try:
        try:
            date = datetime.strptime(date_str, fmt)
            next_day = date + timedelta(days=1)
            return next_day.strftime(fmt)
        except ValueError:
            continue

def parse_hour(hour_str):
    hours = hour_str[:2]
    return int(hours)
    

DATE = 0
HOUR = 1
RAINFALL = 2
PRESSURE = 3
MAX_PRESSURE = 4
MIN_PRESSURE = 5
GLOBAL_RADIATION = 6
TEMPERATURE = 7
PONTO_DE_ORVALHO = 8
MAX_TEMPERATURE = 9
MIN_TEMPERATURE = 10
MAX_PONTO_DE_ORVALHO = 11
MIN_PONTO_DE_ORVALHO = 12
MAX_HUMIDITY = 13
MIN_HUMIDITY = 14
HUMIDITY = 15
WIND_DIR = 16
WIND_MAX = 17
WIND_VEL = 18

CITY = 2
COD = 3
LAT = 4
LONG = 5

data_dict = {}
for year in range(2001, 2024):
   file_names = [f for f in listdir(str(year)) if isfile(join(str(year), f)) and f.endswith(".CSV")]
   for file_name in file_names:
        with open(str(year) + '/' + file_name) as csvfile:
            reader = csv.reader(csvfile, delimiter=';')

            city = ""
            cod = ""
            lat = ""
            long = ""

            counter = 0
            for row in reader:
                if counter < 8:
                    if counter == CITY:
                        city = row[1]
                    elif counter == COD:
                        cod = row[1]
                    elif counter == LAT:
                        lat = row[1].replace(',','.')
                    elif counter == LONG:
                        long = row[1].replace(',','.')
                    counter += 1
                else:
                    break

            if data_dict.get(cod) == None:
                data_dict[cod] = {}
            data = data_dict.get(cod)

            for row in reader:
                if data.get(row[DATE]) == None:
                    data[row[DATE]] = {}
                row[HOUR] = parse_hour(row[HOUR])
                data[row[DATE]][row[HOUR]] = row
            data["meta"] = {"city": city, "cod": cod, "lat": lat, "long": long}
            data_dict[cod] = data

            csvfile.close()

parsed_data_dict = {}
for data in data_dict.values():
    parsed_data = {}
    parsed_data["meta"] = data["meta"]
    for key in data.keys():
        if key != "meta":
            parsed_data[key] = []
            next_day = get_next_day(key)
            for row_key in data[key].keys():
                if row_key < 23 and data[key].get(row_key+1) != None:
                    next_row = data[key][row_key+1]
                    new_row = data[key][row_key].copy()
                    new_row[MAX_PRESSURE] = new_row[MAX_PRESSURE]
                    new_row[MIN_PRESSURE] = new_row[MIN_PRESSURE]
                    new_row[MAX_HUMIDITY] = new_row[MAX_HUMIDITY]
                    new_row[MIN_HUMIDITY] = new_row[MIN_HUMIDITY]
                    new_row[MAX_TEMPERATURE] = new_row[MAX_TEMPERATURE]
                    new_row[MIN_TEMPERATURE] = new_row[MIN_TEMPERATURE]
                    new_row[MAX_PONTO_DE_ORVALHO] = new_row[MAX_PONTO_DE_ORVALHO]
                    new_row[MAX_PONTO_DE_ORVALHO] = new_row[MAX_PONTO_DE_ORVALHO]
                    parsed_data[key].append(new_row)
                elif row_key == 23 and data.get(next_day) != None and data[next_day].get(0) != None:
                    next_row = data[next_day][0]
                    new_row = data[key][row_key].copy()

                    parsed_data[key].append(new_row)
    parsed_data_dict[parsed_data["meta"]["cod"]] = parsed_data

            

parsed_data = []
for data in parsed_data_dict.values():
    for key in data.keys():
        if key != "meta":
            rainfall = 0.0
            pressure = 0.0
            max_pressure = 0.0
            min_pressure = 100000000.0
            global_radiation = 0.0
            temperature = 0.0
            ponto_de_orvalho = 0.0
            max_temperature = 0.0
            min_temperature = 100000000.0
            max_ponto_de_orvalho = 0.0
            min_ponto_de_orvalho = 100000000.0
            max_humidity = 0.0
            min_humidity = 100000000.0
            humidity = 0.0
            wind_dir = 0.0
            wind_max = 0.0
            wind_vel = 0.0
            next_day_rainfall = 0.0

            err_rainfall = False
            err_pressure = False
            err_max_pressure = False
            err_min_pressure = False
            err_global_radiation = False
            err_temperature = False
            err_ponto_de_orvalho = False
            err_max_temperature = False
            err_min_temperature = False
            err_max_ponto_de_orvalho = False
            err_min_ponto_de_orvalho = False
            err_max_humidity = False
            err_min_humidity = False
            err_humidity = False
            err_wind_dir = False
            err_wind_max = False
            err_wind_vel = False
            err_next_day_rainfall = 0.0

            for row in data[key]:
                rainfall += 0 if row[RAINFALL] == '' else float(row[RAINFALL].replace(',','.'))
                pressure +=  0 if row[PRESSURE] == '' else float(row[PRESSURE].replace(',','.'))
                max_pressure = 0 if row[MAX_PRESSURE] == '' else max(max_pressure, float(row[MAX_PRESSURE].replace(',','.')))
                min_pressure = 0 if row[MIN_PRESSURE] == '' else min(min_pressure, float(row[MIN_PRESSURE].replace(',','.')))
                global_radiation += 0 if row[GLOBAL_RADIATION] == '' else float(row[GLOBAL_RADIATION].replace(',','.'))
                temperature += 0 if row[TEMPERATURE] == '' else float(row[TEMPERATURE].replace(',','.'))
                ponto_de_orvalho += 0 if row[PONTO_DE_ORVALHO] == '' else float(row[PONTO_DE_ORVALHO].replace(',','.'))
                max_temperature = 0 if row[MAX_TEMPERATURE] == '' else max(max_temperature, float(row[MAX_TEMPERATURE].replace(',','.')))
                min_temperature = 0 if row[MIN_TEMPERATURE] == '' else min(min_temperature, float(row[MIN_TEMPERATURE].replace(',','.')))
                max_ponto_de_orvalho = 0 if row[MAX_PONTO_DE_ORVALHO] == '' else max(max_ponto_de_orvalho, float(row[MAX_PONTO_DE_ORVALHO].replace(',','.')))
                min_ponto_de_orvalho = 0 if row[MIN_PONTO_DE_ORVALHO] == '' else min(min_ponto_de_orvalho, float(row[MIN_PONTO_DE_ORVALHO].replace(',','.')))
                max_humidity = 0 if row[MAX_HUMIDITY] == '' else max(max_humidity, float(row[MAX_HUMIDITY].replace(',','.')))
                min_humidity = 0 if row[MIN_HUMIDITY] == '' else min(min_humidity, float(row[MIN_HUMIDITY].replace(',','.')))
                humidity += 0 if row[HUMIDITY] == '' else float(row[HUMIDITY].replace(',','.'))
                wind_dir += 0 if row[WIND_DIR] == '' else float(row[WIND_DIR].replace(',','.'))
                wind_max = 0 if row[WIND_MAX] == '' else max(wind_max, float(row[WIND_MAX].replace(',','.')))
                wind_vel += 0 if row[WIND_VEL] == '' else float(row[WIND_VEL].replace(',','.'))
                err_rainfall = err_rainfall or row[RAINFALL] == '' or row[RAINFALL] == '-9999'
                err_pressure = err_pressure or row[PRESSURE] == '' or row[PRESSURE] == '-9999'
                err_max_pressure = err_max_pressure or row[MAX_PRESSURE] == '' or row[MAX_PRESSURE] == '-9999'
                err_min_pressure = err_min_pressure or row[MIN_PRESSURE] == '' or row[MIN_PRESSURE] == '-9999'
                err_global_radiation = err_global_radiation or row[GLOBAL_RADIATION] == '' or row[GLOBAL_RADIATION] == '-9999'
                err_temperature = err_temperature or row[TEMPERATURE] == '' or row[TEMPERATURE] == '-9999'
                err_ponto_de_orvalho = err_ponto_de_orvalho or row[PONTO_DE_ORVALHO] == '' or row[PONTO_DE_ORVALHO] == '-9999'
                err_max_temperature = err_max_temperature or row[MAX_TEMPERATURE] == '' or row[MAX_TEMPERATURE] == '-9999'
                err_min_temperature = err_min_temperature or row[MIN_TEMPERATURE] == '' or row[MIN_TEMPERATURE] == '-9999'
                err_max_ponto_de_orvalho = err_max_ponto_de_orvalho or row[MAX_PONTO_DE_ORVALHO] == '' or row[MAX_PONTO_DE_ORVALHO] == '-9999'
                err_min_ponto_de_orvalho = err_min_ponto_de_orvalho or row[MIN_PONTO_DE_ORVALHO] == '' or row[MIN_PONTO_DE_ORVALHO] == '-9999'
                err_max_humidity = err_max_humidity or row[MAX_HUMIDITY] == '' or row[MAX_HUMIDITY] == '-9999'
                err_min_humidity = err_min_humidity or row[MIN_HUMIDITY] == '' or row[MIN_HUMIDITY] == '-9999'
                err_humidity = err_humidity or row[HUMIDITY] == '' or row[HUMIDITY] == '-9999'
                err_wind_dir = err_wind_dir or row[WIND_DIR] == '' or row[WIND_DIR] == '-9999'
                err_wind_max = err_wind_max or row[WIND_MAX] == '' or row[WIND_MAX] == '-9999'
                err_wind_vel = err_wind_vel or row[WIND_VEL] == '' or row[WIND_VEL] == '-9999'

            next_day = get_next_day(key)
            if data.get(next_day) == None:
                continue

            for row in data[next_day]:
                next_day_rainfall += 0 if row[RAINFALL] == '' else float(row[RAINFALL].replace(',','.'))
                err_next_day_rainfall = err_rainfall or row[RAINFALL] == '' or row[RAINFALL] == '-9999'
            
            if err_rainfall or err_pressure or err_max_pressure or err_min_pressure or err_temperature or err_ponto_de_orvalho or err_max_temperature or err_min_temperature or err_max_ponto_de_orvalho or err_min_ponto_de_orvalho or err_max_humidity or err_min_humidity or err_humidity or err_wind_dir or err_wind_max or err_wind_vel or err_next_day_rainfall:
                continue

            parsed_data.append({
                "Precipitacao Total": rainfall if not err_rainfall else -9999,
                #"next_day_rainfall": next_day_rainfall if not err_next_day_rainfall else -9999,
                "Vai Chover Amanha": 'Sim' if next_day_rainfall >= 1 else 'Nao',
                "Pressao Media": pressure / len(data[key]) if not err_pressure else -9999,
                "Pressao Maxima": max_pressure if not err_max_pressure else -9999,
                "Pressao Minima": min_pressure if not err_min_pressure else -9999,
                #"avg_global_radiation": global_radiation / len(data[key]) if not err_global_radiation else -9999,
                "Temperatura Media": temperature / len(data[key]) if not err_temperature else -9999,
                "Temperatura Orvalho Media": ponto_de_orvalho / len(data[key]) if not err_ponto_de_orvalho else -9999,
                "Temperatura Maxima": max_temperature if not err_max_temperature else -9999,
                "Temperatura Minima": min_temperature if not err_min_temperature else -9999,
                "Temperatura Orvalho Maxima": max_ponto_de_orvalho if not err_max_ponto_de_orvalho else -9999,
                "Temperatura Orvalho Minima": min_ponto_de_orvalho if not err_min_ponto_de_orvalho else -9999,
                "Umidade Maxima": max_humidity if not err_rainfall else -9999,
                "Umidade Minima": min_humidity if not err_rainfall else -9999,
                "Umidade Media": humidity / len(data[key]) if not err_humidity else -9999,
                "Direcao Vento": wind_dir / len(data[key]) if not err_wind_dir else -9999,
                "Rajada Maxima de Vento": wind_max if not err_wind_max else -9999,
                "Vento Velocidade Media": wind_vel / len(data[key]) if not err_wind_vel else -9999,
                "Cidade": data["meta"]["city"],
                "Codigo": data["meta"]["cod"],
                "Latitude": data["meta"]["lat"],
                "Longitude": data["meta"]["long"],
                "Data": parse_date(key),
            })
    
with open('data.csv', 'w', newline='') as file:
    writer = csv.DictWriter(
                file,
                parsed_data[0].keys(),
                delimiter=';')
    writer.writeheader()
    writer.writerows(parsed_data)
    file.close()