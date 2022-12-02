
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

    return file_data
    

def group_by_elf(calorie_data:list) ->dict:
    elf_data = {} 
    value_data = {}

    elf_idx = 0
    _current_val = 0
    for value in calorie_data:
        if value:
            value = int(value)
            _current_val += value
        else:
            value_data.setdefault(_current_val, [] ).append(elf_idx)
            elf_data[elf_idx] = _current_val
            _current_val = 0
            elf_idx += 1

    return elf_data, value_data 
            

def locate_top_elf(elf_data:dict, value_data:dict):
    """
    Given the elf data we find first the top value, secondly the elf(s) that might have that value
    """

    top_value = sorted(list(value_data.keys()))
    top_value = top_value[-1]

    top_elf = value_data[top_value]
    return top_elf, top_value


if __name__ == "__main__":
    file_path = pathlib.Path(__file__)
    folder_path = pathlib.Path(file_path.parent, 'elf_calorie_data.txt')
    calorie_data = load_data_file(folder_path.as_posix())

    elf_data, value_data = group_by_elf(calorie_data.split('\n'))
    top_elf, top_value = locate_top_elf(elf_data, value_data)
    print('Elf {} has {} calories of candy.'.format(top_elf, top_value))


