import draw

def turn_into_template(data, width, height):
    '''takes the 2D array and creates puzzle data from it'''
    row_data = get_row_data_from(data, width)
    col_data = get_col_data_from(data, height)
    return [row_data, col_data]
    #return(draw.grid((row_data, col_data), width, height))

def get_row_data_from(data, width):
    '''reads the data left to right for each row'''
    row_data = []
    for y in enumerate(data):
        for x in enumerate(y[1]):
            row_data.append(data[y[0]][x[0]])
    return find_groups(row_data, width)

def get_col_data_from(data, height):
    '''reads the data top to bottom for each column'''
    col_data = []
    for x in enumerate(data[0]):
        for y in enumerate(data):
            col_data.append(data[y[0]][x[0]])
    return find_groups(col_data, height)

def find_groups(data, splitval):
    '''finds groups of 1's in the input data'''
    groups = []
    i = 0
    first = True
    for item in data:
        if i % splitval == 0:
            if first:
                count = 0
                group = []
                first = False
            else:
                if count != 0:
                    group.append(count)
                    count = 0
                if group != []:
                    groups.append(group)
                    group = []
                else:
                    groups.append([0])
        if item == 1:
            count += 1
        elif count != 0:
            group.append(count)
            count = 0
        i += 1
    if count != 0:
        group.append(count)
    if group != []:
        groups.append(group)
    else:
        groups.append([0])
    return groups

def process(data, width, height):
    '''takes the data recieved from the POST method and reconstructs an 2D array from it'''
    i = 0
    grid = []
    for y in range(height):
        row = []
        for x in range(width):
            row.append(int(data[i*2]))
            i += 1
        grid.append(row)
    return grid
