# Pyxil
A pixel art program made with Pygame<br>
Inspired by [picoCAD](https://johanpeitz.itch.io/picocad), [Px Editor](https://dafluffypotato.itch.io/px-editor), and [Aseprite](https://www.aseprite.org)

# Features
* Simple to use interface(barely)
* Free(although Px Editor is also free and it's actually well made)
* Open-source, and free to change and edit(refer to Licensing below for more information)
* better than Aseprite(not really, that's a joke; if you want an ACTUAL art editor of the pixel kind that's high quality, go with Aseprite)
* Actively supported by me because passion go brrrrrr(can't wait for that to stop)

## Controls
Refer to [the controls](./controls.md)

## Palettes
Pyxil uses palettes for coloring<br>
Pyxil palette files use the extension .pypal, and while they *are* in plain text, I don't recommend manually making them, since It's just lines of numbers(but if you do(because you're insane), refer to the [syntax guide](./pypal_syntax_guide.md))<br>
I made a tool to convert the colors of an image to a pyxil palette, [this](./image_to_pypal.py) Python file<br>
To use it, simply do "python3 image_to_pypal.py [path/to/image]"(or if it's an executable, do "./image_to_pypal [path/to/image]")<br>
To use any Pyxil palettes you have, put them in the "palettes" folder
The three palettes that come built-in are:
* Pypalette, made by me specifically for Pyxil
* BR-12, also made by me, it's just all the primary, secondary, and trinary colors
* and PICO-8's palette

Btw, **Pyxil and it's palettes do not support transparency**<br>
I don't want to code a complex color system, so it will stay that way



## Pronunciation
"Pyxil" is pronounced "py-zil", "piks-zil", or "pikes-zil"<br>
(your house will be over-run by isopods if you pronounce it any other way)


## Other Stuff
If you have any problems with Pixil, leave a issue<br>
If you want a video explaination, refer to [this video](https://www.youtube.com/watch?v=dQw4w9WgXcQ)

the PICO-8 palette does not belong to me, it belongs to PICO-8 and whoever made it


## Licensing
This repository is licensed under the Apache 2.0 license([file](./LICENSE))
<!--td;tr of the license:
* -->

   Copyright 2024 Nuclear Pasta

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.