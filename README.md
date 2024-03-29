# Spotify x GitHub - Readme Cards

Cool looking cards for your [GitHub README](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-github-profile/customizing-your-profile/managing-your-profile-readme) that show your currently playing song on Spotify.

## How to use?

Unfortunately, due to Spotify [not allowing quota extensions](https://github.com/totallynotadi/now-playing-cards/issues/3) for the API, running this is a bit more involved than the usual click-and-deploy route...

Refer to [DEPLOYING.md](DEPLOYING.md) for more details.

For local build instructions, you want [BUILDING.md](BUILDING.md).

Use your personal URL like so: `![](https://now-playing-cards.vercel.app/now-playing/q?uid=YOUR_USER_ID)` and paste your user ID from the last step instead of `YOUR USER ID`.

**OPTIONAL:** For more custom styling, refer to the parameters below.

## URL Parameters

| Parameters | Description                                                                        | Options                                                                          |
| :--------: | ---------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- |
|    size    | Size of the cards to be displayed.                                                 | `small`, `med` (default), `large`                                                |
|   theme    | Color theme of the card displayed.                                                 | `light`, `dark` (default), `colorblock` (extract colors from the song cover art) |
|  bg-color  | custom **background** color for the card (is ignored if a theme is also specified) | CSS compatible hex string in the format `#RRGGBB` or `#RRGGBBAA`                 |
| text-color | custom **text** color for the card (also ignored if a theme is specified too)      | CSS compatible hex string in the format `#RRGGBB` or `#RRGGBBAA`                 |

## Demos

The cards come in various sizes and styles, which can also be customized by passing the above parameters to the URL. You can mix and match many options to your liking and there's more of them coming soon. Here's some examples.

<!-- ### Waves -->

| ![spotify-github-profile](https://now-playing-cards.vercel.app/now-playing/q?uid=bwygdf3k5na8cdy8ek3ofoteq&size=large&theme=extract) | ![spotify-github-profile](https://now-playing-cards.vercel.app/now-playing/q?uid=bwygdf3k5na8cdy8ek3ofoteq&size=med&theme=light) | ![spotify-github-profile](https://now-playing-cards.vercel.app/now-playing/q?uid=bwygdf3k5na8cdy8ek3ofoteq&size=small&theme=dark) |
| :----------------------------------------------------------------------------------------------------------------------------------: | :------------------------------------------------------------------------------------------------------------------------------: | :-------------------------------------------------------------------------------------------------------------------------------: |
|                                       size: `large`<br />theme: `colorblock`<br />bar: `waves`                                       |                                        size: `med`<br />theme: `light`<br />bar: `waves`                                         |                                        size: `small`<br />theme: `dark`<br />bar: `waves`                                         |

<!-- ### Progress Indicator -->

| ![spotify-github-profile](https://now-playing-cards.vercel.app/now-playing/q?uid=bwygdf3k5na8cdy8ek3ofoteq&size=large&theme=light) | ![spotify-github-profile](https://now-playing-cards.vercel.app/now-playing/q?uid=bwygdf3k5na8cdy8ek3ofoteq&size=med&theme=dark) | ![spotify-github-profile](https://now-playing-cards.vercel.app/now-playing/q?uid=bwygdf3k5na8cdy8ek3ofoteq&size=small&theme=extract) |
| :--------------------------------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------------------------------: | :----------------------------------------------------------------------------------------------------------------------------------: |
|                                     size: `large`<br />theme: `light`<br />bar: `progress-bar`                                     |                                     size: `med`<br />theme: `dark`<br />bar: `progress-bar`                                     |                                   size: `small`<br />theme: `colorblock`<br />bar: `progress-bar`                                    |

## Roadmap

TODO:

- [ ] add landscape cards
- [ ] make more themes
- [ ] add endpoints for top artists/tracks
- [ ] make self-hosting easier, maybe move to Vercel KV store?
- [ ] bring back progress bars & waves
- [ ] actually add docs
- [ ] cache readme pics, they take too long to load
- [ ] ~~turn on strict typechecking~~ no

<details>
  <summary><b>Landscape cards</b></summary>

  The portrait oriented cards tend to occupy a lot of **vertical** space, so having one of them at the end or in the middle of your profile readme would look kinda wierd.
  so besides not having to left/right align the cards against some other content for space, horizontal cards make much more sense in terms of using the space better.
  This is an example SVG implementation of such layout, will implement the daynamic data fetching soon and then this can be used.
  <br />
  ![spotify-github-profile](docs/card_landscape_large.svg)
</details>

<details>
  <summary><b>Top tracks / artists card</b></summary>

  an separate endpoint (`/top`) for cards showing a list of a user's top artist (at `/top/artsits`) or top tracks (`/top/tracks`).

  will create a design on figma and an svg implementation of it before setting up dynamic data and the corresponding endpoints.
</details>

<details>
  <summary><b>more themes</b></summary>

  more themes for card backgrounds besides the ones available now (dark, light and colorblock)

* **gradient**

    extracts the dominant colors from the album cover art, but instead of a flat color fill, the background will have a gradient fill, between the extracted color and black (as the `gradient-dark` theme) or between the extracted color and white (as `gradient-light`)
* **blurred covert art background**

    having the blurred version of the cover art as the card background. Again, could have a black or white tints on top of the blur (for text legibility) and call them `blur-dark` or `blur-light` themes.

</details>

<!-- ![spotify-github-profile](https://now-playing-cards.vercel.app/now-playing/q?uid=bwygdf3k5na8cdy8ek3ofoteq&size=small&background=dark&test=true) -->
<!-- ![spotify-github-profile](https://now-playing-cards.vercel.app/now-playing/q?uid=bwygdf3k5na8cdy8ek3ofoteq&size=small&background=dark) -->
<!-- ![spotify-github-profil](https://now-playing-cards.vercel.app/now-playing/q?uid=bwygdf3k5na8cdy8ek3ofoteq&size=small) -->
<!-- ![testing svg rendering in github markdown](docs/card_small.svg) -->

## Contribution

Any and every contribution is welcomed and appreciated.
