from flask import Flask, request, render_template
app = Flask(__name__)

def switch(grid):
	new_grid = []
	for y in range(len(grid)):
		row = []
		for x in range(len(grid[y])):
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
	
	return str((rowvalues, colvalues))


@app.route('/', methods=['GET', 'POST'])
def hello_world():
	if request.method == 'POST':
		return draw_puzzle(request.form['data'])
	else:
		return render_template('index.html')
