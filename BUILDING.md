# Prerequisites

- [Poetry](https://python-poetry.org/docs/#installing-with-the-official-installer), used for managing dependencies, including Python versions.
- [Pyenv](https://github.com/pyenv/pyenv#installation) or [pyenv-win](https://github.com/pyenv-win/pyenv-win/blob/master/docs/installation.md#powershell), for managing Python versions themselves (why? because Vercel wants v3.9, so that's what we'll work with too). 

  Don't forget to [_Set up your shell environment for Pyenv_](https://github.com/pyenv/pyenv#set-up-your-shell-environment-for-pyenv) if you're using the original version.

# Setup

0. Clone the repo and switch to its directory:

   ```sh
   $ git clone https://github.com/poopsicles/readme-now-playing
   $ cd readme-now-playing
   ```

1. First, we get the latest Python 3.9, as of writing that's [3.9.18](https://peps.python.org/pep-0596/):

   ```sh
   $ pyenv install 3.9.18
   ```
 
   - Set it as your default Python version for this project and install the dependencies:
 
   ```sh
   $ pyenv local 3.9.18
   $ poetry install
   ```

2. Copy [`example.env`](example.env) to `.env` and fill it in with [your credentials](DEPLOYING.md#getting-credentials):
   
   ```sh
   $ cp example.env .env
   $ hx .env
   $ cat .env
   FIREBASE_CREDS=bmV2ZXJnb25uYWdpdmV5b3V1cAo=
   CLIENT_ID=bmV2ZXJnb25uYWxldHlvdWRvd24K
   CLIENT_SECRET=bmV2ZXJnb25uYXR1cm5hcm91bmRhbmRkZXNlcnR5b3UK
   REDIRECT_URL=https://localhost:5000/callback/q
   SCOPES=user-read-playback-state user-read-currently-playing user-read-recently-played user-top-read
   ```
  
3. Run the app with Poetry:

   ```sh
   $ poetry run python3 api/index.py
    * Serving Flask app 'index'
    * Debug mode: on
   WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
    * Running on https://localhost:5000
   Press CTRL+C to quit
    * Restarting with stat
    * Debugger is active!
    ...
   ```

You can update dependencies with Poetry:

```sh
$ poetry update
```

As well as emit a `requirements.txt` which Vercel seems to like (you might need to [install the poetry-plugin-export plugin](https://python-poetry.org/docs/plugins/#using-plugins)):

```sh
$ poetry export --without-hashes -f requirements.txt --output requirements.txt
```
