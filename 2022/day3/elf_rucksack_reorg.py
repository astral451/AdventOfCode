
import pathlib

PRIORITY_INDEX = [
    'a','b','c','d','e','f','g','h','i','j','k','l','m',
    'n','o','p','q','r','s','t','u','v','w','x','y','z'
]

PRIORITY_INDEX.extend([v.title() for v in PRIORITY_INDEX])

def split_inventory(inventory):
    
    inventory_size = len(inventory)
    half_size = int(inventory_size / 2)
    comp_01 = inventory[:half_size]
    comp_02 = inventory[half_size:]
    
    return comp_01, comp_02
    

def get_common_items(comp_1, comp_2):
    return set(comp_1).intersection(set(comp_2))


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

    return file_data


def get_priority(items):
    value = 0
    for i in items:
        value += PRIORITY_INDEX.index(i) + 1
    
    return value


def find_badge_in_rucksacks(rucksacks:list):
    first_set = set(rucksacks.pop(0))
    for new_set in rucksacks:
        first_set = first_set.intersection(set(new_set))
    
    return first_set


if __name__ == "__main__":
    file_name = 'elf_rucksack_reorg_data.txt'
    #file_name = 'temp_rucksack_data.txt'
    file_path = pathlib.Path(__file__)
    folder_path = pathlib.Path(file_path.parent, file_name)
    inventory_data = load_data_file(folder_path.as_posix()).split('\n')

    total_priority = 0
    elf_badge_index = -1 #starting value is -1 so we can hit the first mod
    elf_badge_groups = {}
    for idx, rucksack in enumerate(inventory_data):

        if idx % 3 == 0:
            elf_badge_index += 1
        elf_badge_group_data = elf_badge_groups.setdefault(elf_badge_index, 
            {
                'rucksacks' : [],
                'badge_item' : ''
            } 
        )
        elf_badge_group_data['rucksacks'].append(rucksack)

        compartments = split_inventory(rucksack)
        shared_items = get_common_items(*compartments)

        priority = get_priority(shared_items)
        total_priority += priority

        print(shared_items, priority)

    print('Puzzle 1 Total Priority : {}'.format(total_priority))

    total_badge_priority = 0
    for key in elf_badge_groups:
        badge_item = find_badge_in_rucksacks(elf_badge_groups[key]['rucksacks'])
        badge_priority = get_priority(badge_item)
        total_badge_priority += badge_priority
    
    print('Badge Priority : {}'.format(total_badge_priority))
    # Now group the elves together.


