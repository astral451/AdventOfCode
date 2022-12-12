import re
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


class Monkey():
    def __init__(self, name, items, operation, test):
        self.name = name
        self.items = items
        self.operation = operation
        self.test = test
        self.true_monkey = None
        self.false_monkey = None

        
    def set_true_monkey(self, monkey):
        self.true_monkey = monkey
    

    def set_false_monkey(self, monkey):
        self.false_monkey = monkey


def process_monkeys(monkey_data):
    
    re_operation = re.compile(r'(old|\d) ([\+\-\*\/]) (old|\d)')

    monkey_idx = 0
    for idx, line in enumerate(monkey_data):
        if 'Monkey' in line:
            _t, name = line.split(' ')
            name = name.replace(':', '')

            item_line = monkey_data[idx+1]
            words, items = item_line.split(':')
            items = [int(i.strip()) for i in items.split(',')]

            operation_line = monkey_data[idx+2]
            _t, operation = operation_line.split('=')
            searched = re_operation.search(operation)

            test_line = monkey_data[idx+3]
            _t, div = test_line.split('by')

            true_line = monkey_data[idx+4]
            _t, monkey = true_line.split('monkey' )

            false_line = monkey_data[idx+5]
            _t, monkey = true_line.split('monkey' )

            print('test')


if __name__ == "__main__":

    file_name = 'money_middle_data.txt'
    file_name = 'temp_monkey_middle.txt'
    file_path = pathlib.Path(__file__)
    folder_path = pathlib.Path(file_path.parent, file_name)
    monkey_data = load_data_file(folder_path.as_posix()).split('\n')

    process_monkeys(monkey_data)
