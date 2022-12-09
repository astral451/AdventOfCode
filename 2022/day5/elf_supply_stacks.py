import pathlib
import re

CONTAINER_SYMBOL_SIZE = 3 # number of symbols, including []
INSTRUCTIONS_PATTERN = r'move (?P<count>\d+) from (?P<s1>\d+) to (?P<s2>\d+)'


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


def split_layout_and_instructions(diagram):
    container_layer = []
    hull_layer = []
    instructions = []

    _reached_the_hull = False
    all_digits = set(list(range(0,9)))


    for line in diagram:
        if not _reached_the_hull:
            if '[' not in line:
                hull_layer = line
                _reached_the_hull = True
                print('reached the hull')
                continue
            else:
                container_layer.append(line)
        if _reached_the_hull:
            if line:
                instructions.append(line)

    return container_layer, hull_layer, instructions


def process_container_layers(container_layers, hull_layer, stacks):
    stack_piles = [ [] for x in stacks ]
    for layer in container_layers:

        for i, s in enumerate(stacks):

            index = hull_layer.index(str(s))
            if len(layer) < index:
                continue
                # print('skip layer')
                # stack_piles[i].append('')
            else:
                value = layer[index] if layer[index] != ' ' else ''
                if value:
                    stack_piles[i].append(value)

    return stack_piles

def perform_instruction_on_containers_9000(stack_piles, instruction_code):
    count = int(instruction_code['count'])
    s1 = int(instruction_code['s1']) - 1
    s2 = int(instruction_code['s2']) - 1

    crane_arm_stack = []
    for c in range(count):
        stack_piles[s2].insert(0, stack_piles[s1].pop(0))

    print(stack_piles)

def perform_instruction_on_containers_9001(stack_piles, instruction_code):
    count = int(instruction_code['count'])
    s1 = int(instruction_code['s1']) - 1
    s2 = int(instruction_code['s2']) - 1

    crane_arm_stack = stack_piles[s1][:count]
    new_pile = crane_arm_stack + stack_piles[s2]
    stack_piles[s2] = new_pile
    for c in range(count):
        stack_piles[s1].pop(0)

    print(stack_piles)



def run_instructions_on_containers(stack_piles, instructions):

    instruction_re = re.compile(INSTRUCTIONS_PATTERN)
    instruction_code = []
    for instruction in instructions:
        inst_parsed = instruction_re.search(instruction)
        instruction_code.append(inst_parsed.groupdict())

    for instruction in instruction_code:
        perform_instruction_on_containers_9001(stack_piles, instruction)

    return stack_piles


def get_top_most_per_stack(stack_piles):
    final_top = ''
    for stack in stack_piles:
        final_top += stack[0]
    return final_top


if __name__ == "__main__":

    file_name = 'elf_supply_stack_data.txt'
    # file_name = 'temp_supply_stacks.txt'
    file_path = pathlib.Path(__file__)
    folder_path = pathlib.Path(file_path.parent, file_name)
    sections = load_data_file(folder_path.as_posix()).split('\n')

    container_layer, hull_layer, instructions = split_layout_and_instructions(sections)
    # convert the hull layer to integers representing stacks
    stacks = [int(x) for x in filter(None, hull_layer.split(' '))]

    stack_piles = process_container_layers(container_layer, hull_layer, stacks)
    new_stack_piles = run_instructions_on_containers(stack_piles, instructions)
    top_most = get_top_most_per_stack(new_stack_piles)
    print(top_most)
