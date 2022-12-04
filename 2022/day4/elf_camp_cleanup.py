
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

def split_and_get_ranges(pair):
    elf_1, elf_2 = pair.split(',')

    # get the range inputs, remember range to 4 only reaches 3, so we add one more
    elf_1_a, elf_1_b = [int(i) for i in elf_1.split('-')] 
    elf_1_b += 1
    elf_section_range_1 = list(range(elf_1_a, elf_1_b))

    elf_2_a, elf_2_b = [int(i) for i in elf_2.split('-')]
    elf_2_b += 1
    elf_section_range_2 = list(range(elf_2_a, elf_2_b))
    
    return elf_section_range_1, elf_section_range_2


if __name__ == "__main__":
    file_name = 'elf_camp_cleanup_data.txt'
    #file_name = 'temp_camp_cleanup_data.txt'
    file_path = pathlib.Path(__file__)
    folder_path = pathlib.Path(file_path.parent, file_name)
    sections = load_data_file(folder_path.as_posix()).split('\n')

    overlapping_data = {}
    for idx, section in enumerate(sections):
        if not section:
            continue
        section_ranges = split_and_get_ranges(section)

        section_intersections = set(section_ranges[0]).intersection(section_ranges[1])
        if len(section_intersections) == min(len(section_ranges[0]),len(section_ranges[1])):
            overlapping_data[idx] = {
                'section' : section,
                'ranges'  : section_ranges
            }
            print(section, section_ranges, section_intersections)
    
    print('Number of sections with complete overlap {}'.format(len(overlapping_data.keys())))





