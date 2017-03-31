def puzz_temp(data, width, height):
	svgtemplate = '''
	<svg id="puzzle_temp" width="{0}" height="{1}">
	<defs>
  		<pattern id="cross" patternUnits="userSpaceOnUse" width="15" height="15">
    	<image xlink:href="/static/images/cross.svg" x="0" y="0" width="15" height="15" />
  	</pattern>
	</defs>
	{2}
	</svg>
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
	<rect x="{0}"  y="{1}" width="{2}" height={2} id="[{3},{4}]"stroke="#000000" style="cursor:pointer;" fill="white" onmousedown="colourChange(this)"></rect>
	{5}
	'''
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
				text = texttemplate.format(x + 7.5, y + 11 + offset, col_data[xpos][i], '{0}')
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
			cell = celltemplate.format(x, y, 15, col, row, '{0}')
			grid = grid.format(cell)
			x += 15
		y += 15
		x = startx
	grid = grid.format('')
	print('done')
	return grid


def puzzle_prev(puzz_index, puzz_no, puzz_id, data, width, height):
	svgtemplate = '''
	<div class="gallery">
	<a href="{0}"><button>previous</button></a>
	<a href="/solve/{1}">
	<div class="puzzle_frame" width="{2}" height="{3}">
	<svg class="puzzle_template" width="{2}" height="{3}" style="vertical-align:middle;">
	{4}
	</svg>
	</div>
	</a>
	<a href="{5}"><button>next</button></a>
	</div>
	'''

	celltemplate = '''
	<rect x="{0}"  y="{1}" width="{2}" height={2} stroke="#000000" style="cursor:pointer;" fill="white"></rect>
	{3}
	'''

	row_data = data[0][:]
	col_data = data[1][:]

	grid = svgtemplate.format((puzz_index - 1) % puzz_no, puzz_id, 15 * width, 15 * height, '{0}', (puzz_index + 1) % puzz_no)


	#draw grid
	startx = 0
	starty = 0
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
