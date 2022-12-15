import pathlib

letter_indexs = 'SabcdefghijklmnopqrstuvwxyzE'



def load_data_file(file_path):
    """
    Pull in the file data from file_path and return the contents.  None if not found.

    Args:
        file_path (str): The path to the file to import

    Returns:
        str: The String return of the file.
    """

    file_data = None
    data_path = pathlib.Path(file_path)

    if data_path.exists():
        with open(file_path) as fio:
           file_data = fio.read()
    else:
        print('file path {} missing'.format(file_path))

    return file_data




class Grid:
    def __init__(self):
        self.grid = []
        self.number_grid = []
        self.start_cell = None
        self.end_cell = None
        self.visited_cells = {}

        self.directions = ['UP', 'LEFT', 'DOWN', 'RIGHT']


    def create_grid(self, heatmap):
        
        for idx, line in enumerate(heatmap):
            line = list(line)
            n_line = []
            if 'S' in line:
                h_idx = line.index('S')
                self.start_cell = [idx, h_idx]
            if 'E' in line:
                h_idx = line.index('E')
                self.end_cell = [idx, h_idx]
            for letter in line:
                n_line.append(letter_indexs.index(letter))
            self.number_grid.append(n_line)
            self.grid.append(line)


    def find_local_neighbors(self, address):
        x_neg = [(address[0]-1), address[1]] 
        x_pos = [(address[0]+1), address[1]]
        y_neg = [ address[0],   (address[1]+1)] # positive since printing 0 - 1 goes DOWN
        y_pos = [ address[0],   (address[1]-1)] 

        neighbors = []
        for addr in [ y_pos, x_neg, y_neg, x_pos]:
            if addr[0] < 0 or addr[1] < 0:
                neighbors.append([None, None])
                continue
            try:
                neighbors.append([self.number_grid[addr[0]][addr[1]], addr])
            except IndexError as i_err:
                neighbors.append([None, None])
                continue # this isn't a big deal, just not report the neighbor

        return neighbors


    def find_path(self, current_start, path_idx=0):
        start_cell = current_start 
        if start_cell == self.end_cell:
            return
        current_value = self.number_grid[start_cell[0]][start_cell[1]]
        cells = self.visited_cells.setdefault(path_idx, []) 
        cells.append(start_cell)
        self.visited_cells[path_idx] = cells

        local_neighbors = self.find_local_neighbors(start_cell)
        possible_paths = []
        idx =-1
        for value, neighbor in local_neighbors:
            if neighbor and neighbor not in self.visited_cells[path_idx]: # IE it's not None
                _value = self.number_grid[start_cell[0]][start_cell[1]]
                diff = value - _value
                if diff == 1 or diff == 0:
                    idx += 1
                    new_idx = path_idx + idx
                    self.find_path(neighbor, path_idx=new_idx)


        
        
        



if __name__ == "__main__":

    file_name = 'elf_pathfinding_data.txt'
    file_name = 'temp_pathfinding.txt'
    file_path = pathlib.Path(__file__)
    folder_path = pathlib.Path(file_path.parent, file_name)
    heatmap = load_data_file(folder_path.as_posix()).split('\n')

    grid = Grid()
    
    grid.create_grid(heatmap)

    grid.find_path(grid.start_cell)
    print('test')

