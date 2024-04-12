# Controls

## load-up console
To disable the console, add a file named "skipinitconsole.txt" next to the executable/python file
This file can also hold some configs<br>
Example:
```
screenxy: 768, 768
startingpixelscale: 6
canvassize: 16, 16
startingpalette: pypalette
output: /Users/[user]/pictures/pixelart
```

## Editor
**Please note, black(0, 0, 0 in RGB and #000000 in hex) is treated as completely transparent when exporting, so use 1, 1, 1(or #010101) instead**

### Non-Exclusive
* Escape: quit/exit Pyxil
<!--* G: toggle showing a grid
* H: toggle showing that classic dark grey-light grey checker pattern-->
* G: toggle showing that classic dark grey-light grey checker pattern
* M: toggle between mouse mode and keyboard mode(defaults to mouse mode)
<!--* R: toggle showing the color channel diplay in the top-left
* C: toggle visually showing the current color as a colored square
* Semicolon/Apostrophe: change the currently selected color channel(red, green, or blue); the color channels are shown in the top-left corner
* Up/Down Arrows: shift the currently selected color channel up/down by 1, respectively
    * hold Left or Right Shift to shift it by 5, instead
* Left/Right Arrows: shift the currently selected color channel down/up by 10, respectively
    * hold Left or Right Shift to shift it by 50, instead-->
* B: switch between the white and black background(defaults to black)
* Up/Down/Left/Right Arrows: switch the selected color from the current palette
* P: open the palette selection screen(not yet implemented)
* Backspace: set the current pixel to black
* Control + S: export what you currently have on the canvas as a .png or a .jpg

### Keyboard Mode Exclusive
* W/A/S/D: move brush
* Space: paint pixel
* Q: select the current pixel's color to paint with(eye dropper tool/color picker)

### Mouse Mode Exclusive
* Brush follows mouse
* Left Mouse: paint pixel
* Right Mouse: set the current pixel to black
* Middle Mouse: select the current pixel's color to paint with(eye dropper tool/color picker)
<!--* Hovering over the rgb values and scrolling: raise/lower rgb values-->
* Mouse Scroll: zoom in/out
* Left or Right Shift + Mouse Scroll: move the canvas horizontally
* Left or Right Control + Mouse Scroll: move the canvas Vertically