import pandas as pd
from pathlib import Path
import json
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

path_name = Path(__file__).parent.parent/'data'/'weather_data.json' 
columns_name_to_drop = ['weather', 'weather_icon','sys.type'] 
columns_names_to_rename = {
        "base": "base",
        "visibility": "visibility",
        "dt": "datetime",
        "timezone": "timezone",
        "id": "city_id", 
        "name": "city_name",
        "cod": "code",
        "coord.lon": "longitude",
        "coord.lat": "latitude",
        "main.temp": "temperature",
        "main.feels_like": "feels_like",
        "main.temp_min": "temp_min",
        "main.temp_max": "temp_max",
        "main.pressure": "pressure",
        "main.humidity": "humidity",
        "main.sea_level": "sea_level",
        "main.grnd_level": "grnd_level",
        "wind.speed": "wind_speed",
        "wind.deg": "wind_deg",
        "wind.gust": "wind_gust",
        "clouds.all": "clouds", 
        "sys.type": "sys_type",                 
        "sys.id": "sys_id",                
        "sys.country": "country",                
        "sys.sunrise": "sunrise",                
        "sys.sunset": "sunset",
        # weather_id, weather_main, weather_description 
    }
columns_to_normalize_datetime = ['datetime', 'sunrise', 'sunset']

def create_dataframe(path_name: str) -> pd.DataFrame:
    logging.info(f"Attempting to load data from {path_name} and convert to DataFrame.")
    path = Path(path_name)
    
    if not Path.exists(path):
        logging.error(f"Error: File {path} does not exist.")
        return pd.DataFrame() 
    
    with open(path, encoding='latin-1') as f:
        data = json.load(f)
    df = pd.json_normalize(data)
    logging.info(f"Data successfully loaded from {path} and converted to DataFrame. {len(df)} lines and {len(df.columns)} columns.") 
    return df 

def normalize_weather_columns(df: pd.DataFrame) -> pd.DataFrame:  

    df_weather = pd.json_normalize(df['weather'].apply(lambda x: x[0]))

    df_weather = df_weather.rename(columns={
        'id': 'weather_id',
        'main': 'weather_main',
        'description': 'weather_description',
        'icon': 'weather_icon'
    })

    df = pd.concat([df, df_weather], axis=1)
    logging.info(f"Columns normalized. New columns added: {list(df_weather.columns)}")
    
    return df 

def drop_columns(df: pd.DataFrame,columns_name_to_drop:list[str]) -> pd.DataFrame:
    df =df.drop(columns=columns_name_to_drop)
    logging.info(f"Columns dropped: {columns_name_to_drop} - Remaining columns: {list(df.columns)}")
    return df 

def rename_columns(df: pd.DataFrame,columns_names:dict[str, str]) -> pd.DataFrame:
    df = df.rename(columns=columns_names)
    logging.info(f"Columns renamed: {columns_names} - Remaining columns: {list(df.columns)}")
    return df 

def normalize_datetime_columns(df: pd.DataFrame, columns_to_normalize_datetime:list[str]) -> pd.DataFrame:

   logging.info(f"Normalizing datetime columns: {columns_to_normalize_datetime}")
   for name in columns_to_normalize_datetime:
        df[name] = pd.to_datetime(df[name], unit='s', utc=True).dt.tz_convert('America/Sao_Paulo')
   logging.info(f"Datetime columns normalized: {columns_to_normalize_datetime}")
   return df

def data_transformations():
    logging.info("Starting data transformation process.")
    df = create_dataframe(path_name)
    df = normalize_weather_columns(df)
    df = drop_columns(df, columns_name_to_drop)
    df = rename_columns(df, columns_names_to_rename)
    df = normalize_datetime_columns(df, columns_to_normalize_datetime)
    logging.info(f"Data transformation completed. Final DataFrame has {len(df)} lines and {len(df.columns)} columns.")
    return df