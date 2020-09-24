# ComputerCraft-Data-Storage
This project converts real-life videos and images to an ASCII (text) format, so they can be viewed within the terminal of Minecraft's ComputerCraft mod.

## Examples

If you click on the image below, you'll see that it's made up of only text characters.
![Alt Text](https://i.imgur.com/t04CTfR.png)

The gif below has been heavily compressed by Giphy, but it's also made up of only text characters!
![Alt Text](https://media.giphy.com/media/l50uTz68nIUC1suQzi/giphy.gif)

## Explanation

The ASCII files only use these 20 characters:

` `, `.`, `'`, `:`, `-`, `!`, `/`, `(`, `=`, `%`, `1`, `C`, `3`, `$`, `2`, `5`, `A`, `0`, `#`, `@`

They have been sorted by the number of pixels each character has with ComputerCraft's terminal font.

Since there are only 20 characters with a unique number of pixels, the other 74 available characters aren't useful for conversion.

## Getting Started

* `animations` holds data files that can be requested using HTTPS by ComputerCraft.
* `python/main.py` can be run to add desired data files to `animations`.

## Dependencies

Run `pip install -r requirements.txt` to install all the dependencies automatically.
