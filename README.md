# ComputerCraft-Data-Storage
This is a project for viewing regular video and image files as ASCII within Minecraft's ComputerCraft mod.

## Examples

If you click on the image below, you'll see that it's made up of only text characters.
![Alt Text](https://i.imgur.com/t04CTfR.png)

The gif below has been heavily compressed by giphy, but it's also made up of only text characters!
![Alt Text](https://media.giphy.com/media/l50uTz68nIUC1suQzi/giphy.gif)

## Explanation

If you include the space character, only 20 unique characters are used by these ASCII files:

` `, `.`, `'`, `:`, `-`, `!`, `/`, `(`, `=`, `%`, `1`, `C`, `3`, `$`, `2`, `5`, `A`, `0`, `#`, `@`

They have been sorted by the number of pixels each character fills on the screen with ComputerCraft's font.
Since there are only 20 unique numbers of pixels per character, all the other characters were 'identical' and have been omitted.

## Getting Started

* `animations` holds data files that can be requested using HTTPS by ComputerCraft.
* `python/main.py` can be run to add desired data files to `animations`.

## Dependencies

Run `pip install -r requirements.txt` to install all the dependencies automatically.