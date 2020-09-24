# ComputerCraft-Data-Storage
This project converts real-life videos and images to an ASCII (text) format, so they can be viewed within the terminal of Minecraft's ComputerCraft mod.

## Examples

If you click on the image below, you'll see that it's made up of only text characters.
![Alt Text](https://i.imgur.com/t04CTfR.png)

The gif below has been heavily compressed by Giphy, but it's also made up of only text characters.
![Alt Text](https://media.giphy.com/media/l50uTz68nIUC1suQzi/giphy.gif)

These large, colored pixels are also just characters, but the original character font has been heavily modified.
![Alt Text](https://i.imgur.com/jAkjwAJ.png)

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
If you head to `%appdata%/.technic/tekkit/bin` (Windows) and unzip `minecraft.jar`, you'll find this image at `font/default.png`:

![Alt Text](https://i.imgur.com/QEpIybU.png)

This image is the font that Minecraft uses to display text. ComputerCraft also uses this font for its terminal text, so by carefully editing this image, it's possible to assign each of the 94 usable characters in ComputerCraft to any RGB color.
![Alt Text](https://i.imgur.com/WLWlmiw.png)

Changing this font does have the downside of making *everything* inside of Minecraft unreadable, so it's advised to switch back to the regular font when you're done viewing the videos/images.
![Alt Text](https://i.imgur.com/SLRf9GX.png)

### How the 94 RGB colors have been picked

At first, a particle simulation was used where 94 particles repelled each other, and wherever the particles ended up in the 3D space would determine the RGB color of that particle. I couldn't get that to work completely as the particles didn't approach the maximum distances between each other, so I scrapped that concept. I will probably retry this concept in the future, as I suspect it could be the fastest approach, and it should create the best palette of 94 colors.

Then, the palette was generated with a JavaScript program that generates a set of 94 random colors. It then checks the "score" of the palette by looking for the smallest distance between all combinations of two pairs of colors, with the logic being that if the smallest distance is really large, the palette consists of a lot of visually unique colors. This program had O(N^2) complexity, which could have been optimized with a k-d tree to do nearest-neighbour searches with.

## Getting Started

* Install all of the dependencies.
* Change your directory to the folder `asciify` and run `node server.js`, this will start a server.
* ComputerCraft will now be able to send that server some URLs of videos/images to convert, along with any other custom metadata like the name, author, etc. This will all be handled and hidden from the user by the BackWardsOS program for ComputerCraft, which will be published and linked in this repository in the future.
* BackWardsOS will then be able to request ASCII videos/images from the server and view them.

## Dependencies

* Run `pip install -r requirements.txt` to install all the Python dependencies automatically.
* Run `npm install` to install all the JavaScript dependencies automatically.
