'''This is boiler plate code to copy paste into new days.'''
import pathlib
import re

DIRECTORY_DATA = {}
FILE_DATA_RE_PATTERN = re.compile(r'(?P<size>\d+) (?P<file>.+)')

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


def parse_directory_change(instruction, current_dir):
    """
    This looks for info after 'cd' and uses pathlib to build up a path and resolve to
    a useful directory.
    """

    instruction = instruction[5:]

    if '/' in instruction:
        current_dir = pathlib.Path('\\')
    else:
        current_dir = current_dir.joinpath(instruction)
    current_dir = current_dir.resolve()
    return current_dir


def parse_directory_data(line, current_directory):
    """
    Look at lines that aren't cd or dir, and parse out the contents
    """

    if not 'dir' in line:
        file_dict = FILE_DATA_RE_PATTERN.search(line)
        if file_dict:
            return( int(file_dict.groupdict()['size']), file_dict.groupdict()['file'])
    return(0,'')


def get_folder_sizes(directory_data):
    """
    This loops over all the directories and finds files and their sizes using a regular expression.
    We return a new dictionary with this information
    """

    directory_sizes = {}
    for path in directory_data:
        directory_size = directory_sizes.setdefault(path.resolve(), 0)
        for s, f in directory_data[path]:
            if s != 0:
                directory_size += s
            directory_sizes[path.resolve()] = directory_size

        _local_path = path.resolve()
        while _local_path.parents:
            _local_path = _local_path.parent

            _resolved_local_path = _local_path.resolve()

            current_size = directory_sizes.setdefault(_resolved_local_path, 0)
            current_size += directory_size
            directory_sizes[_resolved_local_path] = current_size

    return directory_sizes


def per_line_parse(file_lines):
    """
    Figure out what the line of the input is doing, either cd, ls or is directory information
    """

    current_directory = pathlib.Path()
    for line in file_lines:
        if '$' in line and '$ cd' in line:
            current_directory = parse_directory_change(line, current_directory)
            current_dir_data = DIRECTORY_DATA.setdefault(current_directory, [])

        # in this case since neither the above is matched we are
        # assuming data for the directory
        elif '$' not in line:
            file_data = parse_directory_data(line, current_directory)
            current_dir_data.append(file_data)
            print(current_directory.resolve(), file_data)

    # loop over the located directories and add child folders to parent folders
    directory_sizes = get_folder_sizes(DIRECTORY_DATA)

    return directory_sizes


if __name__ == "__main__":

    file_name = 'elf_space_race_data.txt'
    # file_name = 'temp_space_race.txt'
    file_path = pathlib.Path(__file__)
    folder_path = pathlib.Path(file_path.parent, file_name)
    file_data = load_data_file(folder_path.as_posix()).split('\n')

    directory_sizes = per_line_parse(file_data)
    dirs_total = 0
    dir_size_limit = 100000
    for dir in directory_sizes:
        if directory_sizes[dir] <= dir_size_limit:
            dirs_total += directory_sizes[dir]
    print('Folders under {0} totals {1}'.format(dir_size_limit, dirs_total))

    file_system_size    = 70000000
    needed_unused_space = 30000000

    total_space_used = directory_sizes[pathlib.Path('\\').resolve()]
    empty_space_on_disk = file_system_size - total_space_used
    clean_up_size = needed_unused_space - empty_space_on_disk
    print('Need to find directory of at least {} size'.format(clean_up_size))

    potential_sizes = []
    for dir in directory_sizes:
        if directory_sizes[dir] > clean_up_size:
           potential_sizes.append(directory_sizes[dir])
    potential_sizes.sort()
    print('This directory size can be removed {}'.format(potential_sizes[0]))


