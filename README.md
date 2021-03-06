# ComputerCraft-Data-Storage
This project converts real-life videos and images to an ASCII (text) format, so they can be viewed within the terminal of Minecraft's ComputerCraft mod.

## Examples

| ![Alt Text](https://i.imgur.com/t04CTfR.png) |
| :---: |
| If you click on this image you'll see that it's made up of only text characters! |

| ![Alt Text](https://media.giphy.com/media/l50uTz68nIUC1suQzi/giphy.gif) |
| :---: |
| This gif has been heavily compressed by Giphy, but it's also made up of only text characters! |

| ![Alt Text](https://i.imgur.com/jAkjwAJ.png) |
| :---: |
| These large, colored pixels are also just characters, which has been achieved by modifying how characters are drawn to the screen. |

## How do the black-and-white examples work?

This project converts an `RGB pixel` -> `grayscale value` -> `ASCII character`.
These ASCII characters are then drawn on a ComputerCraft terminal.

The ASCII files only use these 20 characters:

` `, `.`, `'`, `:`, `-`, `!`, `/`, `(`, `=`, `%`, `1`, `C`, `3`, `$`, `2`, `5`, `A`, `0`, `#`, `@`

They have been sorted by their brightness, which has been done by counting the number of white pixels each character has in Minecraft's font.

This means the ` ` character has a brightness of 0, and the `@` character has a brightness of 1.

Since there are only 20 characters with a unique number of white pixels, the other 74 available characters are useless.

## How do the colored examples work?

There are 94 available characters in ComputerCraft's terminal, but only 20 of those have a unique number of white pixels.
If you head to `%appdata%/.technic/tekkit/bin` (Windows) and unzip `minecraft.jar`, you'll find this image at `font/default.png` (the transparent background has been made black):

| ![Alt Text](https://i.imgur.com/3ZB6Zom.png) | ![Alt Text](https://i.imgur.com/XYM8UGb.png) |
| :---: | :---: |
| This image is the font that Minecraft uses to display text. | ComputerCraft also uses this font for its terminal text, so it's possible to assign each of the 94 characters that are usable in ComputerCraft to any RGB color. |

| ![Alt Text](https://i.imgur.com/SLRf9GX.png) |
| :---: |
| Changing this font does have the downside of making *everything* inside of Minecraft unreadable, so it's advised to switch back to the regular font when you're done viewing the videos/images. |

### How the 94 RGB colors have been picked

#### v1

At first, a particle simulation was used where 94 particles repelled each other, and wherever the particles ended up in the 3D space would determine the RGB color of that particle. I couldn't get that to work completely as the particles didn't approach the maximum distances between each other, so that concept got scrapped.

| `(color1_r - color2_r) ** 2 + (color1_g - color2_g) ** 2 + (color1_b - color2_b) ** 2` |
| :---: |
| This is the formula for calculating the distance between two colors with the Pythagorean theorem (Euclidean distance). Then, the palette was generated with a JavaScript program that generates a set of 94 random colors. It then calculates the "score" of the palette by looking for the smallest distance between all possible combinations of two colors, with the logic being that if the smallest distance found is larger than that of any other palette, the palette has a lot of variance, which means a lot of visually unique colors. |

#### v2

This program was then rewritten in C, because I assumed the algorithm would execute faster in C, but I haven't benchmarked the JS or C program yet to confirm or deny this. This C program ran on my server for about 8 hours, but I stopped the program after that time because it took 3 hours and millions of randomly generated palettes to find a palette that was slightly better. This program has O(N^2) complexity, which could have been optimized with a k-d tree to do nearest-neighbour searches with, but the chances of this program getting really close to the optimal palette are so incredibly small that it'd be better using a totally different approach anyways.

| ![Alt Text](https://wikimedia.org/api/rest_v1/media/math/render/svg/41684f5a5dd515420fdc46c05f75d2b7efdc6045) ![Alt Text](https://wikimedia.org/api/rest_v1/media/math/render/svg/2e9018b3d7c1c1e622cc8d68a49cf208945bbfb2) |
| :---: |
| These are the equations used to calculate the redmean distance. The [Wikipedia page on Color Difference](https://en.wikipedia.org/wiki/Color_difference#Euclidean) discusses how the human vision isn't equally sensitive to the colors red, green and blue, which means that a simple euclidean distance between two colors isn't accurate to how the humans perceive color differences. The article also discusses many alternative distance functions which can be used to approximate the distance much more accurately. The "redmean" algorithm discussed there seemed like an easy to implement, much better algorithm, so that's what the C palette generator and Python video converter programs currently use for calculating the distance between two colors. |

#### v3?

v1 had the most potential, so I'll probably come back to that concept in the future to give it another shot.

## Dependencies

* Run `pip install -r requirements.txt` to install all the Python dependencies automatically.
* Run `npm install` to install all the JavaScript dependencies automatically.

## Getting Started

* Install all of the dependencies.
* Change your directory to the folder `asciify` and run `node server.js`, this will start a server.
* ComputerCraft will now be able to send that server some URLs of videos/images to convert, along with any other custom metadata like the name, author, etc. This will all be handled and hidden from the user by the BackWardsOS program for ComputerCraft, which will be published and linked in this repository in the future.
* BackWardsOS will then be able to request ASCII videos/images from the server and view them.
