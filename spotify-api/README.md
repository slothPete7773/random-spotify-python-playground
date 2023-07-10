# Spotify API Server

## TODO: Instruction

- setup env
- instantiate server
- first time authen, authorize, and retrieve access token

## TODO: API Doc

View interactive API doc at [http://localhost:8000/docs](http://localhost:8000/docs)

- DONE: GET /login
    
    Request to authenticate, then request for authorization from user

- DONE: GET /spotify-api/v1/me

    Request to get user info

- DONE: GET /spotify-api/v1/me/top/tracks

    Request to get top tracks of user's history

- DONE: GET /spotify-api/v1/me/top/artists

    Request to get top artists of user's history

- DONE: POST /spotify-api/v1/artists

- DONE: POST /spotify-api/v1/tracks

- TODO: POST /spotify-api/v1/albums

- TODO: GET /spotify-api/v1/album/genre

    Request to get the genre respective to the Album

- TODO: GET /spotify-api/v1/artist/genre

    Request to get the genre respective to the Artist, in case that the Album does not have `genre` value
    