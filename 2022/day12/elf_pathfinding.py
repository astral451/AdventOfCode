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


def create_grid(heatmap):
    start_cell = [0,0]
    end_cell = [0,0]
    
    grid = []
    number_grid = []
    for idx, line in enumerate(heatmap):
        line = list(line)
        n_line = []
        if 'S' in line:
            h_idx = line.index('S')
            start_cell =[idx, h_idx]
        if 'E' in line:
            h_idx = line.index('E')
            end_cell = [idx, h_idx]
        for letter in line:
            n_line.append(letter_indexs.index(letter))
        number_grid.append(n_line)
        grid.append(line)

    return grid, number_grid, start_cell, end_cell


if __name__ == "__main__":

    file_name = 'elf_pathfinding_data.txt'
    file_name = 'temp_pathfinding.txt'
    file_path = pathlib.Path(__file__)
    folder_path = pathlib.Path(file_path.parent, file_name)
    heatmap = load_data_file(folder_path.as_posix()).split('\n')

    grid, num_grid, start, end = create_grid(heatmap)
    print(grid, num_grid, start, end)