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



class Rope_Simulation():
    def __init__(self):
        self.head_pos = [0, 0]
        self.head_positions = dict()
        self.head_positions[tuple(self.head_pos)] = 1
        self.tail_pos = [0, 0]
        self.tail_positions = dict()
        self.tail_positions[tuple(self.tail_pos)] = 1

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
        min_head = [0,0]
        max_head = [0,0]
        min_tail = [0,0]
        max_tail = [0,0]

        for x, y in self.head_positions:
            min_head[0] = min(x, min_head[0])
            min_head[1] = min(y, min_head[1])
            max_head[0] = max(x, max_head[0])
            max_head[1] = max(y, max_head[1])
        for x, y in self.tail_positions:
            min_tail[0] = min(x, min_tail[0])
            min_tail[1] = min(y, min_tail[1])
            max_tail[0] = max(x, max_tail[0])
            max_tail[1] = max(y, max_tail[1])

        for i in range(min_head[0],max_head[0]):
            dots = ''
            for j in range(min_head[1],max_head[1]):
                address = tuple([i,j])
                if address in self.tail_positions:
                    dots += '#'
                else:
                    dots += '.'
            print(dots)


    def _translate_in_direction(self, unit_vector, distance, pawn='head'):

        if pawn == 'head':
            _obj = self.head_pos
        else:
            _obj = self.tail_pos

        x = _obj[0] + unit_vector[0]
        y = _obj[1] + unit_vector[1]
        _obj = [x, y]
        if pawn == 'head':
            self.head_pos = _obj
            _idx = tuple(self.head_pos)
            stored_pos = self.head_positions.setdefault(_idx, 0)
            stored_pos += 1
            self.head_positions[_idx] = stored_pos
        else:
            self.tail_pos = _obj
            _idx = tuple(self.tail_pos)
            stored_pos = self.tail_positions.setdefault(_idx, 0)
            stored_pos += 1
            self.tail_positions[_idx] = stored_pos


    def _head_to_tail_vector(self):
        hx, hy = self.head_pos
        tx, ty = self.tail_pos
        vx = hx - tx
        vy = hy - ty
        distance = math.sqrt(math.pow(vx, 2) + math.pow(vy,2))
        return tuple([vx, vy]), distance


    def _translate_tail(self):
        vector, distance = self._head_to_tail_vector()
        if distance > math.sqrt(2):
            # this means it's just beyond the diagonal we care about
            direction_of_travel = self._get_direction_of_travel(vector)
            self._translate_in_direction(direction_of_travel, 1, pawn='tail')


    def move_head(self, direction, distance):
        for i in range(distance):

            direction_tuple = self.vectors[direction] * distance
            self._translate_in_direction(direction_tuple, 1)
            self._translate_tail()
            # self._print_positions()


if __name__ == "__main__":

    file_name = 'elf_rope_bridge_data.txt'
    # file_name = 'temp_elf_rope_bridge.txt'
    file_path = pathlib.Path(__file__)
    folder_path = pathlib.Path(file_path.parent, file_name)
    file_data = load_data_file(folder_path.as_posix()).split('\n')

    all_instructions = parse_instructions(file_data)
    rs = Rope_Simulation()

    for inst in all_instructions:
        direction = inst[0]
        distance =  inst[1]

        rs.move_head(direction, distance)
    rs._print_stored_positions()
    print('count:{}'.format(len(rs.tail_positions.keys())))
