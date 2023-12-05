# [Spotify-Spotipy Saving Data]

This repository is an experimental project for collecting data from Spotify, into another database for further usage. 

# Instruction 

## Setup API server

1. Install dependencies

```sh
$ cd ./spotify-api

# Create Virtual Environment
$ python3 -m virtualenv .venv
$ source ./.venv/bin/activate

# Install dependencies
$ pip3 install -r requirements.txt
```

2. Setup development server

```sh
# Create Docker network
docker network create -d bridge spotify-net
```



# Requirement

- [ ] 1. Total time I have listen spotify from past, given date, or a year until present.
- [ ] 2. What songs have I listened over the past, given date, or a year until present.
  - [ ]     2.1 The top song, how many time have I listened to it, and how long is that?
- [ ] 3. Detail of genre I have listen from the past, given date, or a year until present.
  - [ ]     3.1 Proportion of genre
  - [ ]     3.2 What genre played the most and the least, and rank them.
- [ ] 4. Similar to 3.) but Artist
- [ ] 5. How many songs have I added to Favorite from given period to present.
- [ ] 6. The duration I spent listening to particular Artist. Album as well would be great.
- [ ] 7. Record the summary of each month using the above requirements.

# Roughly developmental steps

- [x] 1. Do auth(things)
   - authen -> authorize
   - store token in session (somehow)
   - refresh access token
- [x] 2. Function calling to Spotify API service
- [x] 3. Learn Docker-compose more
- [x] 4. Manage to fetch data
- [ ] 5. Transform the data and save to file
  - I will save the raw files first, and think about normalization later when needed to store in the relational db
- [ ] 6. Store the data, maybe on cloud
- [ ] 7. Get the genre data for each track, use Genre from Artist data
- [ ] 8. Transform JSON to tabular format. 
- [ ] 9. Design schema for storing the historical top tracks/artists with their corresponding details (Genre, etc)
- [ ] 10. Get not-quite near-real-time of Current_playback state, maybe run every 3 minutes?, so that I can record the history more accurate.
