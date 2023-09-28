get py-env or pyenv-win

https://github.com/pyenv-win/pyenv-win

run pyenv install 3.9.13

set virtualenvs.prefer-active-python in poetry to true

pyenv local 3.9.13
poetry install

go to https://developer.spotify.com/dashboard/create
make an app
for redirect uri, for now make it  https://localhost:5000/callback/q
copy your client id and secret