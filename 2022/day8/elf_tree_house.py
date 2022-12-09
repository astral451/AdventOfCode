import pathlib


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


def grid_from_data(all_tree_data):
    """
    Create a grid from the incoming numbers    
    """

    data_grid_width = len(all_tree_data[0])
    data_grid_height = len(all_tree_data)
    total_grid_count = data_grid_width * data_grid_height
    data_grid = []
    for i in range(data_grid_height):
        data_grid.append([int(i) for i in list(all_tree_data[i])])

    return data_grid, total_grid_count, data_grid_height, data_grid_width


def check_vertical_values(tree_data, h_range, w_range, h_idx, w_idx):
    """
    Moves through the vertical access from the grid position.  This will be expensive
    in large grids as it does not early out once a block is found. It could be
    better.    
    """

    tree_height = tree_data[h_idx][w_idx]
    neg_vis = True
    pos_vis = True
    visiblilty = []
    for h in h_range:
        if h == h_idx:
            visiblilty.append(-1) # this is THE tree
        else:
            if tree_data[h][w_idx] >= tree_height:
                visiblilty.append(0)
                if h <= h_idx:
                    neg_vis = False
                else:
                    pos_vis = False
            else:
                visiblilty.append(1)

    return visiblilty, neg_vis, pos_vis


def check_horizontal_values(tree_data, h_range, w_range, h_idx, w_idx):
    """
    A complete copy of _vertical_ version.  I really don't like this and want
    to genericize it.  All I'm doing is swapping which element I loop over 
    """

    tree_height = tree_data[h_idx][w_idx]
    neg_vis = True
    pos_vis = True
    visiblilty = []
    for w in w_range:
        if w == w_idx:
            visiblilty.append(-1) # this is THE tree
        else:
            if tree_data[h_idx][w] >= tree_height:
                visiblilty.append(0)
                if w <= w_idx:
                    neg_vis = False
                else:
                    pos_vis = False
            else:
                visiblilty.append(1)

    return visiblilty, neg_vis, pos_vis


def look_for_visible_trees(tree_data, height, width):
    """
    Looks through the interior trees looking for the parts of the forest
    with visibility.  It skips the perimeter 
    """

    central_core_height_indexs = range(1, height - 1)
    central_core_width_indexs = range(1, width - 1)
    hidden_tree_count = 0
    hidden_tree_data = [[[] for y in range(width)] for x in range(height)]

    for h_idx in central_core_height_indexs:
        for w_idx in central_core_width_indexs:
            h_data, u_vis, d_vis = check_vertical_values(
                tree_data,
                range(height),
                range(width),
                h_idx,
                w_idx
            )
            w_data, l_vis, r_vis = check_horizontal_values(
                tree_data,
                range(height),
                range(width),
                h_idx,
                w_idx
            )
            hidden_tree_data[h_idx][w_idx] = (h_data, w_data)
            if any([u_vis, d_vis, l_vis, r_vis]):
                print(h_idx, w_idx, 'Is visible')
            else:
                hidden_tree_count += 1
                print(h_idx, w_idx, 'Is Hidden')

    return hidden_tree_count, hidden_tree_data


def calculate_scenic_score(tree_data, height, width, h_idx, w_idx):
    """
    In this method that covers one item within the whole grid, this will
    work through each items looking up down left right for trees at or below
    the starting height. This uses reverse ranges to count outwards from
    the central tree.  Once it hits a block it quits
    """

    up_range = range(h_idx, -1, -1)
    down_range = range(h_idx, height)
    left_range = range(w_idx, -1, -1)
    right_range = range(w_idx, width)

    current_tree_height = tree_data[h_idx][w_idx]
    scenic_scores = []
    for h_range in [up_range, down_range]:
        count = 0
        for h in h_range:
            if h == h_idx:
                continue
            count += 1
            if tree_data[h][w_idx] >= current_tree_height:
                break
        scenic_scores.append(count)

    for w_range in [left_range, right_range]:
        count = 0
        for w in w_range:
            if w == w_idx:
                continue
            count += 1
            if tree_data[h_idx][w] >= current_tree_height:
                break
        scenic_scores.append(count)


    score_total = 1
    for score in scenic_scores:
        score_total *= score
    print(current_tree_height, scenic_scores, score_total)
    return score_total


def get_scenic_score(tree_data, h_size, w_size):
    """
    A wrapper for the actual work.  Essentially just the outside x,y for loop
    """

    score_data = [[1 for j in range(w_size)] for i in range(h_size)]
    h_range = range(h_size)
    w_range = range(w_size)
    for h_idx in h_range:
        for w_idx in w_range:
            score_data[h_idx][w_idx] = calculate_scenic_score(tree_data, h_size, w_size, h_idx, w_idx)

    for row in score_data:
        print(row)

    return score_data


if __name__ == "__main__":

    file_name = 'elf_tree_house_data.txt'
    # file_name = 'temp_tree_house.txt'
    file_path = pathlib.Path(__file__)
    folder_path = pathlib.Path(file_path.parent, file_name)
    tree_data = load_data_file(folder_path.as_posix()).split('\n')[:-1]

    tree_grid, total_trees, g_height, g_width = grid_from_data(tree_data)
    hidden_tree_count, hidden_tree_data = look_for_visible_trees(tree_grid, g_height, g_width)
    print(f'Visible trees : {total_trees-hidden_tree_count}')

    all_scores = get_scenic_score(tree_grid, g_height, g_width)
    top_score = 0
    for row in all_scores:
        top_score = max(top_score, max(row))
    print(f'Top score in all trees is {top_score}')
