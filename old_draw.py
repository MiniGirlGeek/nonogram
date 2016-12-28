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

def draw_grid():
    data = request.form['data']
    #create copies of the row data
    rowval = data[0][:]
    rowdat = data[0][:]

    #sort the row data based on the length of the lists
    rowval.sort(key=lambda x: len(x))

    #create copies of the column data
    colval = data[1][:]
    coldat = data[1][:]

    #sort the column data based on the length of the lists
    colval.sort(key=lambda x: len(x))

    #get the length of the largest lists to work out how large the puzzle template needs to be
    rowvallen = len(rowval[-1])
    colvallen = len(colval[-1])

    #work out the dimensions the grid needs to be
    width = (int(request.form['width']) + rowvallen) * int(request.form['length'])
    height = (int(request.form['height']) + colvallen) * int(request.form['length'])

    #set up the grid using the dimensions calculated
    grid = svgtemplate.format(width, height, '{0}')

    #########################
    # Display column values #
    #########################

    #define the starting x and y positions so that they can be reset later on
    startx = rowvallen * int(request.form['length'])
    starty = (colvallen -1) * int(request.form['length'])

    #set the initial x and y positions
    xpos = startx
    ypos = starty

    rev = False
    for y in range(colvallen):
    	for x in range(int(request.form['width'])):
    		coldat[x][::-1]
    		try:
    			text = texttemplate.format(xpos + (int(request.form['length']) / 2),
    									   ypos + 12,
    									   coldat[x][y], '{0}')
    			rect = recttemplate.format(xpos, ypos, int(request.form['length']), text)
    			grid = grid.format(rect, '{0}')
    		except:
    			pass
    		xpos += int(request.form['length'])
    	rev = False
    	xpos = startx
    	ypos -= int(request.form['length'])

    #display row values
    startx = (rowvallen - 1) * int(request.form['length'])
    xpos = startx
    starty = (colvallen) * int(request.form['length'])
    ypos = starty
    for x in range(int(request.form['width'])):
    	rowdat[x].reverse()
    	for y in range(rowvallen):
    		try:
    			text = texttemplate.format(xpos + (int(request.form['length']) / 2),
    									   ypos + 12,
    									   rowdat[x][y], '{0}')
    			rect = recttemplate.format(xpos, ypos, int(request.form['length']), text)
    			grid = grid.format(rect, '{0}')
    		except:
    			pass
    		xpos -= int(request.form['length'])
    	xpos = startx
    	ypos += int(request.form['length'])

    #draw the grid area
    startx = (rowvallen) * int(request.form['length'])
    xpos = startx
    starty = (colvallen) * int(request.form['length'])
    ypos = starty
    for x in range(int(request.form['width'])):
    	for y in range(int(request.form['height'])):
    		cell = celltemplate.format(xpos, ypos, int(request.form['length']), '{0}')
    		grid = grid.format(cell, '{0}')
    		ypos += int(request.form['length'])
    	xpos += int(request.form['length'])
    	ypos = startx
    return grid



def switch(grid):
    new_grid = []
    width = len(grid)
    height = len(grid[0])
    for y in range(height):
    	row = []
    	for x in range(width):
    		row.append(0)
    	new_grid.append(row)

    for y in range(len(grid)):
    	for x in range(len(grid[y])):
    		new_grid[x][y] = grid[y][x]
    return new_grid

def find_groups(grid):
    values = []
    for y in grid:
    	count = 0
    	rowdata = []
    	for x in y:
    		if x == '1':
    			count += 1
    		else:
    			if count != 0:
    				rowdata.append(count)
    			count = 0
    	if count != 0:
    		rowdata.append(count)
    	values.append(rowdata)

    	for i in range(len(values)):
    		if values[i] == []:
    			values[i] = [0]
    return values

def draw_puzzle():
    inp = request.forms['data']
    i = 0
	grid = []
	colvalues = []
	rowvalues = []

	#converting the data from the javascript back into a 2D list
	data = str(inp).split(',')
	for y in range(int(request.form['height'])):
		row = []
		for x in range(int(request.form['width'])):
			row.append(data[i])
			i += 1
		grid.append(row)

	#work out what the puzzle template numbers will be
	rowvalues = find_groups(grid)
	colvalues = find_groups(switch(grid))

	#create a svg element to return
	return draw_grid((rowvalues, colvalues))
	return str((rowvalues, colvalues))
