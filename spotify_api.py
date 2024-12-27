import requests

CLIENT_ID = '2ab9d0c5ed804559b17a2b08496a4b82'
CLIENT_SECRET = '6aa848ae5f984ec5bd920b29f08d6b73'

auth_url = 'https://accounts.spotify.com/api/token'

auth_response = requests.post(auth_url, {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
})

access_token = auth_response.json()['access_token']
headers = {
    'Authorization': f'Bearer {access_token}'}
print('access token generated successfully')

search_url = 'https://api.spotify.com/v1/search'
params = {'q': 'track:Blinding Lights artist:The Weeknd', 'type': 'track', 'limit': 1}
response =  requests.get(search_url, headers=headers, params=params)
print(response.json())

track = response.json()['tracks']['items'][0]
track_info = {
    'Track Name': track['name'],
    'Artist Name': track['artists'][0]['name'],
    'Album Name': track['album']['name'],
    'Release Date': track['album']['release_date'],
    'Popularity': track['popularity'],
    'Duration (ms)': track['duration_ms'],
    'Spotify Track ID': track['id'],
    'Spotify URL': track['external_urls']['spotify'],  
}

print(track_info)

import pandas as pd
play_history = pd.read_csv('clean_play_history.csv')

spotify_data = []

for index, row in play_history.iterrows():
    track_name = row['Track ``Description']
    artist_name = row['Artist Name']
    params = {
        'q': f'track:{track_name} artist:{artist_name}',
        'type': 'track',
        'limit': 1
    }
    response = requests.get(search_url, headers=headers, params=params) 
    data = response.json()
    
    if data['tracks']['items']: 
        track = data['tracks']['items'][0]
        track_info = {
            'Track Name': track['name'],
            'Artist Name': track['artists'][0]['name'],
            'Album Name': track['album']['name'],
            'Release Date': track['album']['release_date'],
            'Popularity': track['popularity'],
            'Duration (ms)': track['duration_ms'],
            'Spotify Track ID': track['id'],
            'Spotify URL': track['external_urls']['spotify'],
        }
        spotify_data.append(track_info)
    else:
        print(f"No track found for {track_name} by {artist_name}")
        
spotify_df = pd.DataFrame(spotify_data)
spotify_df.to_csv('spotify_metadata.csv', index=False)

artist_id = track['artists'][0]['id']
artist_url = f'https://api.spotify.com/v1/artists/{artist_id}'
artist_response = requests.get(artist_url, headers=headers) 
artist_data = artist_response.json()

genres = artist_data['genres']