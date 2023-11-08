import pandas as pd

def load_data():

    try:
        path = 'D:/Master BDIA - M2/Data_Viz_Project/MyApp/Data/dataset.csv'
        df = pd.read_csv(path)
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None
    

def preProcess_data(df):

    try:
        # Drop 'Unnamed: 0' column
        df = df.drop('Unnamed: 0', axis=1)
        
        # New column names
        new_columns = {
            'track_id': 'Track ID',
            'artists': 'Artists',
            'album_name': 'Album Name',
            'track_name': 'Track Name',
            'popularity': 'Popularity',
            'duration_ms': 'Duration (ms)',
            'explicit': 'Explicit',
            'danceability': 'Danceability',
            'energy': 'Energy',
            'key': 'Key',
            'loudness': 'Loudness',
            'mode': 'Mode',
            'speechiness': 'Speechiness',
            'acousticness': 'Acousticness',
            'instrumentalness': 'Instrumentalness',
            'liveness': 'Liveness',
            'valence': 'Valence',
            'tempo': 'Tempo',
            'time_signature': 'Time Signature',
            'track_genre': 'Track Genre'
        }

        # Rename columns
        df.rename(columns=new_columns, inplace=True)
        
        return df
    except Exception as e:
        print(f"Error preprocessing data: {e}")
        return None



loaded_data = load_data()
preProcessed_data = preProcess_data(loaded_data)
