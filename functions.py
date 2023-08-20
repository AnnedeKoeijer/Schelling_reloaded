def get_neighbors_snake(x,y,grid):
    '''Alternative function to the grid.get_neighborhood function of mesa.
    This functions looks for the neighbors in the surrouding cells but it follows snake/circle path (Instead of going bottom to up per column)
    Functions returns the found neighbors in a list with None values for the cells in which no agent was found'''

    neighbor_list = []

    if len(grid.get_cell_list_contents(((x-1), (y-1)))) > 0:
        neighbor_list += grid.get_cell_list_contents(((x-1), (y-1)))
    else:
        neighbor_list.append(None)

    if len(grid.get_cell_list_contents(((x-1), (y)))) > 0:
        neighbor_list += grid.get_cell_list_contents(((x-1), (y)))
    else:
        neighbor_list.append(None)

    # Makes sure the y+1 value is not a value outside the limits of the grid
    if (y+1) == grid.height:
        neighbor_list += [None, None, None]
    else:
        if len(grid.get_cell_list_contents(((x-1), (y+1)))) > 0:
            neighbor_list += grid.get_cell_list_contents(((x-1), (y+1)))
        else:
            neighbor_list.append(None)

        if len(grid.get_cell_list_contents(((x-1), (y+1)))) > 0:
            neighbor_list += grid.get_cell_list_contents(((x), (y+1)))
        else:
            neighbor_list.append(None)

        # Makes sure the x+1 and y+1 value is not a value outside the limits of the grid
        if (x + 1) == grid.width:
            neighbor_list.append(None)
        else:
            if len(grid.get_cell_list_contents(((x+1), (y+1)))) > 0:
                neighbor_list += grid.get_cell_list_contents(((x+1), (y+1)))
            else:
                neighbor_list.append(None)

    # Makes sure the x+1 value is not a value outside the limits of the grid
    if (x+1) == grid.width:
        neighbor_list += [None, None]
    else:
        if len(grid.get_cell_list_contents(((x+1), (y)))) > 0:
            neighbor_list += grid.get_cell_list_contents(((x+1), (y)))
        else:
            neighbor_list.append(None)

        if len(grid.get_cell_list_contents(((x+1), (y-1)))) > 0:
            neighbor_list += grid.get_cell_list_contents(((x+1), (y-1)))
        else:
            neighbor_list.append(None)

    if len(grid.get_cell_list_contents(((x), (y-1)))) > 0:
        neighbor_list += grid.get_cell_list_contents(((x), (y-1)))
    else:
        neighbor_list.append(None)

    return neighbor_list