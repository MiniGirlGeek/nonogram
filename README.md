# Nonograms Website

For my A-Level computing project I made a website where you could design and solve black and white nonograms aka japenese crosswords. [Examples of nonograms][1] can be found online.


On one part of the website you could specify the size of a grid, and click within in the generated grid to create pixel art.


On the client side the images and puzzles are displayed using svgs. Server side they are stored as arrays in a database. On the server a python script converts image arrays into puzzle arrays. It also converts the puzzle arrays back into svgs to be displayed client side.


[1]: https://en.wikipedia.org/wiki/Nonogram
