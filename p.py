import csv
from os import listdir
from os.path import isfile, join
from datetime import datetime, timedelta
import math
import numpy as np
import pandas as pd


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
for year in range(2001, 2025):
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
            max_pressure = -math.inf
            min_pressure = math.inf
            global_radiation = 0.0
            temperature = 0.0
            ponto_de_orvalho = 0.0
            max_temperature = -math.inf
            min_temperature = math.inf
            max_ponto_de_orvalho = -math.inf
            min_ponto_de_orvalho = math.inf
            max_humidity = -math.inf
            min_humidity = math.inf
            humidity = 0.0
            wind_dir = 0.0
            wind_max = -math.inf
            wind_vel = 0.0
            next_day_rainfall = 0.0

            err_rainfall = 0
            err_pressure = 0
            err_max_pressure = 0
            err_min_pressure = 0
            err_global_radiation = 0
            err_temperature = 0
            err_ponto_de_orvalho = 0
            err_max_temperature = 0
            err_min_temperature = 0
            err_max_ponto_de_orvalho = 0
            err_min_ponto_de_orvalho = 0
            err_max_humidity = 0
            err_min_humidity = 0
            err_humidity = 0
            err_wind_dir = 0
            err_wind_max = 0
            err_wind_vel = 0
            err_next_day_rainfall = 0

            for row in data[key]:
                rainfall += 0 if row[RAINFALL] == '' or row[RAINFALL] == '-9999' else float(row[RAINFALL].replace(',','.'))
                pressure +=  0 if row[PRESSURE] == '' or row[PRESSURE] == '-9999' else float(row[PRESSURE].replace(',','.'))
                max_pressure = max_pressure if row[MAX_PRESSURE] == '' or row[MAX_PRESSURE] == '-9999' else max(max_pressure, float(row[MAX_PRESSURE].replace(',','.')))
                min_pressure = min_pressure if row[MIN_PRESSURE] == '' or row[MIN_PRESSURE] == '-9999' else min(min_pressure, float(row[MIN_PRESSURE].replace(',','.')))
                global_radiation += 0 if row[GLOBAL_RADIATION] == '' or row[GLOBAL_RADIATION] == '-9999' else float(row[GLOBAL_RADIATION].replace(',','.'))
                temperature += 0 if row[TEMPERATURE] == '' or row[TEMPERATURE] == '-9999' else float(row[TEMPERATURE].replace(',','.'))
                ponto_de_orvalho += 0 if row[PONTO_DE_ORVALHO] == '' or row[PONTO_DE_ORVALHO] == '-9999' else float(row[PONTO_DE_ORVALHO].replace(',','.'))
                max_temperature = max_temperature if row[MAX_TEMPERATURE] == '' or row[MAX_TEMPERATURE] == '-9999' else max(max_temperature, float(row[MAX_TEMPERATURE].replace(',','.')))
                min_temperature = min_temperature if row[MIN_TEMPERATURE] == '' or row[MIN_TEMPERATURE] == '-9999' else min(min_temperature, float(row[MIN_TEMPERATURE].replace(',','.')))
                max_ponto_de_orvalho = max_ponto_de_orvalho if row[MAX_PONTO_DE_ORVALHO] == '' or row[MAX_PONTO_DE_ORVALHO] == '-9999' else max(max_ponto_de_orvalho, float(row[MAX_PONTO_DE_ORVALHO].replace(',','.')))
                min_ponto_de_orvalho = min_ponto_de_orvalho if row[MIN_PONTO_DE_ORVALHO] == '' or row[MIN_PONTO_DE_ORVALHO] == '-9999' else min(min_ponto_de_orvalho, float(row[MIN_PONTO_DE_ORVALHO].replace(',','.')))
                max_humidity = max_humidity if row[MAX_HUMIDITY] == '' or row[MAX_HUMIDITY] == '-9999' else max(max_humidity, float(row[MAX_HUMIDITY].replace(',','.')))
                min_humidity = min_humidity if row[MIN_HUMIDITY] == '' or row[MIN_HUMIDITY] == '-9999' else min(min_humidity, float(row[MIN_HUMIDITY].replace(',','.')))
                humidity += 0 if row[HUMIDITY] == '' or row[HUMIDITY] == '-9999' else float(row[HUMIDITY].replace(',','.'))
                wind_dir += 0 if row[WIND_DIR] == '' or row[WIND_DIR] == '-9999' else float(row[WIND_DIR].replace(',','.'))
                wind_max = wind_max if row[WIND_MAX] == '' or row[WIND_MAX] == '-9999' else max(wind_max, float(row[WIND_MAX].replace(',','.')))
                wind_vel += 0 if row[WIND_VEL] == '' or row[WIND_VEL] == '-9999' else float(row[WIND_VEL].replace(',','.'))

                err_rainfall += 1 if row[RAINFALL] == '' or row[RAINFALL] == '-9999' else 0
                err_pressure += 1 if row[PRESSURE] == '' or row[PRESSURE] == '-9999' else 0
                err_max_pressure += 1 if row[MAX_PRESSURE] == '' or row[MAX_PRESSURE] == '-9999' else 0
                err_min_pressure += 1 if row[MIN_PRESSURE] == '' or row[MIN_PRESSURE] == '-9999' else 0
                err_global_radiation += 1 if row[GLOBAL_RADIATION] == '' or row[GLOBAL_RADIATION] == '-9999' else 0
                err_temperature += 1 if row[TEMPERATURE] == '' or row[TEMPERATURE] == '-9999' else 0
                err_ponto_de_orvalho += 1 if row[PONTO_DE_ORVALHO] == '' or row[PONTO_DE_ORVALHO] == '-9999' else 0
                err_max_temperature += 1 if row[MAX_TEMPERATURE] == '' or row[MAX_TEMPERATURE] == '-9999' else 0
                err_min_temperature += 1 if row[MIN_TEMPERATURE] == '' or row[MIN_TEMPERATURE] == '-9999' else 0
                err_max_ponto_de_orvalho += 1 if row[MAX_PONTO_DE_ORVALHO] == '' or row[MAX_PONTO_DE_ORVALHO] == '-9999' else 0
                err_min_ponto_de_orvalho += 1 if row[MIN_PONTO_DE_ORVALHO] == '' or row[MIN_PONTO_DE_ORVALHO] == '-9999' else 0
                err_max_humidity += 1 if row[MAX_HUMIDITY] == '' or row[MAX_HUMIDITY] == '-9999' else 0
                err_min_humidity += 1 if row[MIN_HUMIDITY] == '' or row[MIN_HUMIDITY] == '-9999' else 0
                err_humidity += 1 if row[HUMIDITY] == '' or row[HUMIDITY] == '-9999' else 0
                err_wind_dir += 1 if row[WIND_DIR] == '' or row[WIND_DIR] == '-9999' else 0
                err_wind_max += 1 if row[WIND_MAX] == '' or row[WIND_MAX] == '-9999' else 0
                err_wind_vel += 1 if row[WIND_VEL] == '' or row[WIND_VEL] == '-9999' else 0

            next_day = get_next_day(key)
            if data.get(next_day) == None:
                err_next_day_rainfall = 1
            else:
                for row in data[next_day]:
                    next_day_rainfall += 0 if row[RAINFALL] == '' or row[RAINFALL] == '-9999' else float(row[RAINFALL].replace(',','.'))
                    err_next_day_rainfall += 1 if  row[RAINFALL] == '' or row[RAINFALL] == '-9999' else 0          

            parsed_data.append({
                "Precipitacao Total": pd.NA if err_rainfall == len(data[key]) else rainfall,
                "Vai Chover Amanha":  pd.NA if err_next_day_rainfall == len(data[key]) else ('Sim' if next_day_rainfall >= 1 else 'Nao'),
                "Pressao Media": pd.NA if err_pressure == len(data[key]) else pressure / (len(data[key]) - err_pressure),
                "Pressao Maxima": max_pressure if (len(data[key]) - err_max_pressure) != 0 else pd.NA,
                "Pressao Minima": min_pressure if (len(data[key]) - err_min_pressure) != 0 else pd.NA,
                "Radiacao Global": pd.NA if err_global_radiation == len(data[key]) else global_radiation / (len(data[key]) - err_global_radiation),
                "Temperatura Media": pd.NA if err_temperature == len(data[key]) else temperature / (len(data[key]) - err_temperature),
                "Temperatura Orvalho Media": pd.NA if err_ponto_de_orvalho == len(data[key]) else ponto_de_orvalho / (len(data[key]) - err_ponto_de_orvalho),
                "Temperatura Maxima": max_temperature if (len(data[key]) - err_max_temperature) != 0 else pd.NA,
                "Temperatura Minima": min_temperature if (len(data[key]) - err_min_temperature) != 0 else pd.NA,
                "Temperatura Orvalho Maxima": max_ponto_de_orvalho if (len(data[key]) - err_max_ponto_de_orvalho) != 0 else pd.NA,
                "Temperatura Orvalho Minima": min_ponto_de_orvalho if (len(data[key]) - err_min_ponto_de_orvalho) != 0 else pd.NA,
                "Umidade Maxima": max_humidity if (len(data[key]) - err_max_humidity) != 0 else pd.NA,
                "Umidade Minima": min_humidity if (len(data[key]) - err_min_humidity) != 0 else pd.NA,
                "Umidade Media": pd.NA if err_humidity == len(data[key]) else humidity / (len(data[key]) - err_humidity),
                "Direcao Vento": pd.NA if err_wind_dir == len(data[key]) else wind_dir / (len(data[key]) - err_wind_dir),
                "Rajada Maxima de Vento": wind_max if (len(data[key]) - err_wind_max) != 0 else pd.NA,
                "Vento Velocidade Media": pd.NA if err_wind_vel == len(data[key]) else wind_vel / (len(data[key]) - err_wind_vel),
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