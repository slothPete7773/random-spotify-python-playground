# [Spotify-Spotipy Saving Data]

This repository is an experimental project for collecting data from Spotify, into another database for further usage. 

The data that got pulled are as the following:

1. Still in consideration...

 # Roughly developmental steps

 1. DONE: Do auth(things)
    - authen -> authorize
    - store token in session (somehow)
    - refresh access token
 2. DONE: Function calling to Spotify API service
 3. DONE: Manage to fetch data
 4. TODO: Transform the data and save to file
       
       - I will save the raw files first, and think about normalization later when needed to store in the relational db

 5. TODO: Store the data, maybe on cloud
 6. TODO: Get the genre data for each track, use Genre from Artist data
 7. PLAN: Think about what to analyse, compare, and visualize from the historical top tracks/artists data.
 