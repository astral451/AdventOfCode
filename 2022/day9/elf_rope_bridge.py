import pathlib
import math


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


def parse_instructions(file_data):
    instructions = []
    for line in file_data:
        if line:
            dir, distance = line.split(' ')
            distance = int(distance)
            instructions.append([dir, distance])

    return instructions

ROPE_ASCII = [' ', '.', ':', '-', '=', '+', '*', '#', '%', '@']

class Rope_Simulation():
    def __init__(self, number_of_knots):
        self.head_pos = [0, 0]
        self.head_positions = dict()
        self.head_positions[tuple(self.head_pos)] = 1
        
        self.rope_pos = [[0, 0] for i in range(number_of_knots)]
        self.knot_positions = list()
        for k in self.rope_pos:
            pos_dict = { tuple([0,0]) : 1 } 
            self.knot_positions.append(pos_dict)
            

        self.vectors = {
            'R' : tuple([ 0,  1]),
            'L' : tuple([ 0, -1]),
            'U' : tuple([-1,  0]),
            'D' : tuple([ 1,  0]),
            # the corners for use by tail
            'RU': tuple([-1,  1]),
            'RD': tuple([ 1,  1]),
            'LU': tuple([-1, -1]),
            'LD': tuple([ 1, -1])
        }


    def _get_direction_of_travel(self, vector):
        dx, dy = vector
        dx = max(min(dx, 1), -1)
        dy = max(min(dy, 1), -1)

        return tuple([dx,dy])


    def _print_positions(self):
        vec, dist = self._head_to_tail_vector()
        print(self.head_pos, self.tail_pos, vec, dist)


    def _print_stored_positions(self):
        file_string = ''
        low_corner = [0,0]
        high_corner = [0,0]

        for k in self.knot_positions:
            for p in k:
                low_corner[0] = min(p[0],low_corner[0])
                low_corner[1] = min(p[1],low_corner[1]) 
                high_corner[0] = max(p[0], high_corner[0])
                high_corner[1] = max(p[1], high_corner[1])

        #this offset of adding one, gets to the last row in the print
        high_corner[0] += 1
        high_corner[1] += 1

        for i in range(low_corner[0],high_corner[0]):
            dots = ''
            for j in range(low_corner[1],high_corner[1]):
                address = tuple([i,j])
                dot = 0 
                for p in self.knot_positions:
                    if address in p:
                        dot += 1 
                        dot = min(9, dot)
                dot = ROPE_ASCII[dot]
                # if dot == 0:
                #     dot = ' '
                # else:
                #     dot = ROPE_ASCII[dot]
                dots += dot 
            print(dots)
            file_string += dots 
            file_string += '\n'
        return file_string


    def _translate_in_direction(self, unit_vector, distance, pawn_idx=0):

        _obj = self.rope_pos[pawn_idx]

        x = _obj[0] + unit_vector[0]
        y = _obj[1] + unit_vector[1]
        _obj = [x, y]

        self.rope_pos[pawn_idx] = _obj
        _idx = tuple(self.rope_pos[pawn_idx])
        stored_pos = self.knot_positions[pawn_idx].setdefault(_idx, 0)
        stored_pos += 1
        self.knot_positions[pawn_idx][_idx] = stored_pos


    def _head_to_tail_vector(self, h_idx, t_idx):
        hx, hy = self.rope_pos[h_idx]
        tx, ty = self.rope_pos[t_idx]
        vx = hx - tx
        vy = hy - ty
        distance = math.sqrt(math.pow(vx, 2) + math.pow(vy,2))
        return tuple([vx, vy]), distance


    def _translate_rope(self):
        for i in range(1,len(self.rope_pos)):
            vector, distance = self._head_to_tail_vector(i-1, i)
            if distance > math.sqrt(2):
                # this means it's just beyond the diagonal we care about
                direction_of_travel = self._get_direction_of_travel(vector)
                self._translate_in_direction(direction_of_travel, 1, pawn_idx=i)


    def move_head(self, direction, distance):
        for i in range(distance):

            direction_tuple = self.vectors[direction] * distance
            self._translate_in_direction(direction_tuple, 1)
            self._translate_rope()
            # self._print_positions()


if __name__ == "__main__":

    file_name = 'elf_rope_bridge_data.txt'
    # file_name = 'temp_elf_rope_bridge_larger.txt'
    file_path = pathlib.Path(__file__)
    folder_path = pathlib.Path(file_path.parent, file_name)
    file_data = load_data_file(folder_path.as_posix()).split('\n')

    all_instructions = parse_instructions(file_data)
    rs = Rope_Simulation(10)

    for inst in all_instructions:
        direction = inst[0]
        distance =  inst[1]

        rs.move_head(direction, distance)
    # fun novelty to write this out to disk
    file_name = pathlib.Path(pathlib.Path(__file__).parent.resolve(), 'path_output.txt')
    with open(file_name, 'w') as fio:
        fio.write(rs._print_stored_positions())

    print('count:{}'.format(len(rs.knot_positions[-1].keys())))
