# so you wanna deploy hm?

1. First, [get your credentials](#getting-credentials).
   
2. Click this nice button:

   [![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fpoopsicles%2Freadme-now-playing&env=FIREBASE_CREDS,CLIENT_ID,CLIENT_SECRET,REDIRECT_URL,SCOPES&envDescription=API%20Keys%20needed%20for%20correct%20functioning&envLink=https%3A%2F%2Fgithub.com%2Fpoopsicles%2Freadme-now-playing%2Fblob%2Fmain%2FDEPLOYING.md&project-name=github-spotify-readme&repository-name=github-spotify-readme-self-deploy)

3. Use the following environment variables:

   - `FIREBASE_CREDS`: Your Firestore Base64 secret
   - `CLIENT_ID`: Your Spotify app client ID
   - `CLIENT_SECRET`: Your Spotify app client secret
   - `REDIRECT_URL`: Make this `https://localhost:5000/callback/q` for now, we'll fix it later
   - `SCOPES`: Make this `user-read-playback-state user-read-currently-playing user-read-recently-played user-top-read`

3. Click the "Continue to Dashboard" button.

4. Copy the URL - it's the first thing under "Domains".

5. Hop over to Settings > Environment Variables and change the `REDIRECT_URL` to `<URL you just copied>/callback/q` e.g. if your URL is `https://github-spotify.vercel.app/`, you're going to add `https://github-spotify.vercel.app/callback/q`

6. Change the redirect URL for your Spotify app to this value too by going to the [Dashboard](https://developer.spotify.com/dashboard), selecting your app > Settings > Edit > Redirect URIs and clicking "Save" when you're done.

7. Now, go back to Deployments > Three-dot menu > Redeploy > Use existing build cache > Redeploy.

8. Enjoy! Now check out the [docs](README.md/#how-to-use) for more info.

## Getting credentials

### Firestore

1. Make a new Firebase project (call it whatever you want), and a Cloud Firestore.
  
   Google has instructions [here](https://firebase.google.com/docs/firestore/quickstart).

   You want to choose "Production mode" when it asks, as well as a region geographically close to you.

2. Go to the [console](https://console.firebase.google.com/) if it doesn't pop up, and select your project.
   
3. Click the gear icon in the top left > Project settings > Service accounts > Generate new private key.

4. Now we need to convert the `.json` file we just downloaded to Base64:

   - You can use an online service like [base64encode.org](https://www.base64encode.org/).

   - Or your terminal, if you're familiar:

     ```sh
     $ jq -r '. | @base64' ~/Downloads/github-spotify-readme-firebase-adminsdk.json # *nix

     $ # TODO add ex. for pwsh
     ```

5. Keep this Base64 string, this is our Firebase credential.

### Spotify

1. Go to https://developer.spotify.com/dashboard/create and make an app.

   - For the redirect URI, make it `https://localhost:5000/callback/q` for now, we'll change it later
   - Tick just "Web API" under "Which API/SDKs are you planning to use?"

2. Copy your client ID and secret, we'll need these next.

