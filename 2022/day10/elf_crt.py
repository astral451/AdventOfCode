'''This is boiler plate code to copy paste into new days.'''
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



def cpu_cycles(line_input, signal_queries):
    signal_values_at_queries = []
    value = 1
    cycles = 0

    pause_for = 0

    crt_output = ''

    for _input in line_input:

        if 'noop' in _input:
            pause_for = 1
        elif 'addx' in _input:
            pause_for = 2
        
        for i in range(pause_for):
            pixel_range = [value-1, value, value+1]
            
            # pulling out signal data
            if cycles in SIGNAL_QUERIES:
                signal_values_at_queries.append(cycles * value)
                # print(cycles, value, cycles * value)
            print(cycles, pixel_range)

            cycle_40_mod = cycles % 40 

            if cycle_40_mod == 0 :
                crt_output += '\n'
            if cycle_40_mod in pixel_range:
                crt_output += '#'
            else:
                crt_output += '.'
            cycles += 1

        if 'addx' in _input:
            op, op_val = _input.split(' ')
            value += int(op_val)

    return signal_values_at_queries, crt_output


if __name__ == "__main__":

    file_name = 'elf_crt_data.txt'
    # file_name = 'temp_elf_crt.txt'
    file_path = pathlib.Path(__file__)
    folder_path = pathlib.Path(file_path.parent, file_name)
    sections = load_data_file(folder_path.as_posix()).split('\n')

    SIGNAL_QUERIES = [20,60, 100, 140, 180, 220]
    signal_samples, crt_output = cpu_cycles(sections, SIGNAL_QUERIES)
    print(sum(signal_samples))
    print(crt_output)
