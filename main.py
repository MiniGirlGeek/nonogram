from flask import Flask, request, render_template
#import svgwrite
app = Flask(__name__)

svgtemplate = '''
<svg id="puzzle_template" width="{0}" height="{1}">
	{2}
</svg>
 '''

recttemplate = '''
	<rect x="{0}"  y="{1}" width="{2}" height={2} stroke="#000000" fill="white"></rect>
	{3}
'''

texttemplate = '''
	<text x="{0}" y="{1}" font-family="Verdana" font-size="10" fill="black" text-anchor="middle">{2}</text>
	{3}
'''

def draw_grid(data):
	rowval = data[0][:]
	rowdat = data[0][:]
	rowval.sort(key=lambda x: len(x))
	colval = data[1][:]
	coldat = data[1][:]
	print(coldat)
	colval.sort(key=lambda x: len(x))
	rowvallen = len(rowval[-1])
	colvallen = len(colval[-1])
	print(coldat)
	width = (int(request.form['width']) + rowvallen) * int(request.form['length'])
	height = (int(request.form['height']) + colvallen) * int(request.form['length'])
	grid = svgtemplate.format(width, height, '{0}')
	i = 0

	startx = 0
	starty = 0
	xpos = startx
	ypos = starty

	#display column values
	startx = rowvallen * int(request.form['length'])
	xpos = startx
	starty = colvallen * int(request.form['length'])
	ypos = starty
	for y in range(colvallen):
		for x in range(int(request.form['width'])):
			try:
				text = texttemplate.format(xpos + (int(request.form['length']) / 2),
										   ypos + 12,
										   coldat[x][y], '{0}')
				rect = recttemplate.format(xpos, ypos, int(request.form['length']), text)
				grid = grid.format(rect, '{0}')
			except:
				pass
			xpos += int(request.form['length'])
		xpos = startx
		ypos -= int(request.form['length'])

	#display row values
	startx = int(request.form['length'])
	xpos = startx
	starty = (colvallen + 1) * int(request.form['length'])
	ypos = starty
	for y in range(rowvallen):
		for x in range(int(request.form['width'])):
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

def draw_puzzle(inp):
	i = 0
	grid = []
	colvalues = []
	rowvalues = []

	#converting the data from the javascript backi into a 2D list
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


@app.route('/', methods=['GET', 'POST'])
def hello_world():
	if request.method == 'POST':
		return draw_puzzle(request.form['data'])
	else:
		return render_template('index.html')
