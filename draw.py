svgtemplate = '''
<svg id="puzzle_template" width="{0}" height="{1}">
	{2}
</svg>
<script src="../static/scripts/main.js"></script>
 '''

recttemplate = '''
	<rect x="{0}"  y="{1}" width="{2}" height={2} stroke="#000000" fill="AliceBlue"></rect>
	{3}
'''

texttemplate = '''
	<text x="{0}" y="{1}" font-family="Verdana" font-size="10" fill="black" text-anchor="middle">{2}</text>
	{3}
'''

celltemplate = '''
	<rect x="{0}"  y="{1}" width="{2}" height={2} stroke="#000000" style="cursor:pointer;" fill="white" onmousedown="colourChange(this)"></rect>
	{3}
'''

def grid(data, width, height):
    row_data = data[0][:]
    col_data = data[1][:]

    row_data.sort(key=lambda x: len(x))
    col_data.sort(key=lambda x: len(x))

    largest_x = len(row_data[-1])
    largest_y = len(col_data[-1])

    row_data = data[0][:]
    col_data = data[1][:]

    grid = svgtemplate.format(15 * (width + largest_x), 15 * (height+largest_y), '{0}')

    #draw column data
    startx = largest_x * 15
    starty = 0
    x = startx
    y = starty
    i = 0
    for row in range(largest_y):
        xpos = 0
        for col in range(width):
            try:
                offset = 15 * (largest_y - len(col_data[xpos]))
                text = texttemplate.format(x + 7.5, y + 10 + offset, col_data[xpos][i], '{0}')
                rect = recttemplate.format(x, y + offset, 15, text)
                grid = grid.format(rect)
            except:
                pass
            x += 15
            xpos += 1
        x = startx
        y += 15
        i += 1

    #draw row data
    startx = 0
    starty = largest_y * 15
    x = startx
    y = starty
    i = 0
    for col in range(largest_x):
        ypos = 0
        for row in range(height):
            try:
                offset = 15 * (largest_x - len(row_data[ypos]))
                text = texttemplate.format(x + 7.5 + offset, y + 10, row_data[ypos][i], '{0}')
                rect = recttemplate.format(x + offset, y, 15, text)
                grid = grid.format(rect)
            except IndexError:
                pass
            y += 15
            ypos += 1
        y = starty
        x += 15
        i += 1

    #draw grid
    startx = largest_x * 15
    starty = largest_y * 15
    x = startx
    y = starty
    for row in range(height):
        for col in range(width):
            cell = celltemplate.format(x, y, 15, '{0}')
            grid = grid.format(cell)
            x += 15
        y += 15
        x = startx
    grid = grid.format('')
    return grid
