# .pypal File Syntax Guide
.pypal files are used for Pyxil palettes
the syntax goes as follows:
```
-- use "--" for comments

-- first is the dimensions line, in the format of [x]-[y]
-- this MUST be the first line of every .pypal file(ignoring comments)
-- it tells the palette reader how store and show the palette
4-4
-- then the rest of the file is color definitions, in the format of [red], [blue], [green]
255, 255, 255
0, 0, 0
-- etc, etc
```