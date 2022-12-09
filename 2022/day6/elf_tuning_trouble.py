"""
This solution does one extra calculation per chunk MARKER_LENGTH to see if we have
sequential characters so we can advance past them without processing them twice.
nppd doesn't need to look at ppdx so we just move to pdx.
"""
import pathlib


MARKER_LENGTH = 4
MESSAGE_LENGTH = 14

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


def get_next_advancement_point(chunk, marker_length):
    """
    Look at the chunk and find the next space to jump to.  This looks
    within the chunk for simultaneous characters and jumps past them.
    """

    if len(set(chunk)) == marker_length:
        return 0
    elif len(set(chunk)) == 1:
        return 4
    else:
        # the reason for this else is to discover repeated and sequential characters.
        # when we see nppd, we can skip over to the second p to avoid the whole loop.
        # in the case of zzzz, we can skip to the very end and not waste time.
        advance_size = 1  # at least we move forward 1
        for i in range(marker_length- 1):
            if len(set(chunk[i:i+2])) == 1:
                advance_size = i + 1

        return advance_size


def process_signal_for_first_marker(signal, marker_length):
    """
    The Main function to process signal strings.  Pass in the full string and the length
    that needs to be unique characters.
    """

    first_marker_found = False
    signal_length = len(signal)

    idx = 0
    while not first_marker_found:

        if idx+marker_length<= signal_length:
            chunk = signal[idx:idx+marker_length]
            next_adv_pnt = get_next_advancement_point(chunk, marker_length)
            if not next_adv_pnt: # equivalant to 0
                first_marker_found = True
            idx += next_adv_pnt
        else:
            first_marker_found = True

    found_marker_string = signal[idx:idx+marker_length]

    return idx, found_marker_string


if __name__ == "__main__":

    file_name = 'elf_tuning_trouble_data.txt'
    # file_name = 'temp_tuning_trouble.txt'
    file_path = pathlib.Path(__file__)
    folder_path = pathlib.Path(file_path.parent, file_name)
    tuning_signal = load_data_file(folder_path.as_posix()).split('\n')

    print(tuning_signal)

    for signal in tuning_signal:
        first_marker_idx, marker_string = process_signal_for_first_marker(signal, MARKER_LENGTH)
        print('Characters processed : {}'.format(first_marker_idx))
        print('marker characters : {}'.format(marker_string))

        message_signal = signal[first_marker_idx:]
        message_end_idx, message = process_signal_for_first_marker(signal, MESSAGE_LENGTH)
        print('Message Characters Processed : {}'.format(message_end_idx+MESSAGE_LENGTH))