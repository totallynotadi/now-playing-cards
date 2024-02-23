get py-env or pyenv-win

https://github.com/pyenv-win/pyenv-win

make sure to follow the init procedures

run pyenv install 3.9.13

set virtualenvs.prefer-active-python in poetry to true

pyenv local 3.9.13
poetry install

go to https://developer.spotify.com/dashboard/create
make an app
for redirect uri, for now make it  https://localhost:5000/callback/q
copy your client id and secret

make a firestore project & a cloud firestore 
https://firebase.google.com/docs/firestore/quickstart

you want to make it in a region close to you
and lets do production mode 

click gear icon > project settings > service accounts > generate new private key
you will downlload a json file

depending on platform, base64 encode the file

```sh
$ jq -r '. | @base64' ~/Downloads/github-spotify-readme-firebase-adminsdk.json
```

copy the result