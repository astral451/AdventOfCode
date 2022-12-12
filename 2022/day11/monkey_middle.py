import re
import pathlib

MONKEYS = {}

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


class Item:
    def __init__(self, value):
        self.value = value

    def calculate_worry(self, arg1, operator, arg2, divided=0, mod=0):
        if arg1 == 'old':
            a_1 = self.value
        else:
            a_1 = int(arg1)

        if arg2 == 'old':
            a_2 = self.value
        else:
            a_2 = int(arg2)

        if operator == '-':
            value = a_1 - a_2
        elif operator == '+':
            value = a_1 + a_2
        elif operator == '*':
            value = a_1 * a_2
        elif operator == '/':
            value = a_1 / a_2

        if divided != 0:
            value = int(value / float(divided))

        if mod > 0:
            value = value % mod

        self.value = value

class Monkey:
    def __init__(self, name, items, operations, test):
        self.name = name
        self.items = items
        self.operations = operations
        self.test = test
        self.true_monkey = None
        self.false_monkey = None

        self.inspection_times = 0

        
    def set_true_monkey(self, monkey):
        self.true_monkey = monkey
    

    def set_false_monkey(self, monkey):
        self.false_monkey = monkey


    def test_value(self, item_value):
        self.inspection_times += 1
        if item_value%self.test == 0:
            return self.true_monkey
        else:
            return self.false_monkey


def process_monkeys(monkey_data):
    
    re_operation = re.compile(r'(old|\d+) ([\+\-\*\/]) (old|\d+)')

    monkey_idx = 0
    for idx, line in enumerate(monkey_data):
        if 'Monkey' in line:
            _t, name = line.split(' ')
            name = name.replace(':', '')

            item_line = monkey_data[idx+1]
            words, items = item_line.split(':')
            items = [Item(int(i.strip())) for i in items.split(',')]

            operation_line = monkey_data[idx+2]
            _t, operation = operation_line.split('=')
            searched = re_operation.search(operation)
            arg1 = searched.group(1)
            operator = searched.group(2)
            arg2 = searched.group(3)

            test_line = monkey_data[idx+3]
            _t, div = test_line.split('by ')
            div = int(div)

            # make monkey
            new_monkey = Monkey(
               name,
               items,
                [arg1, operator, arg2],
                div
            )

            true_line = monkey_data[idx+4]
            _t, monkey = true_line.split('monkey ')
            monkey = monkey
            new_monkey.set_true_monkey(monkey)

            false_line = monkey_data[idx+5]
            _t, monkey = false_line.split('monkey ')
            monkey = monkey
            new_monkey.set_false_monkey(monkey)

            MONKEYS[new_monkey.name] = new_monkey


def pass_item_to_monkey(item, monkey_idx2):

    MONKEYS[monkey_idx2].items.append(item)


if __name__ == "__main__":

    file_name = 'money_middle_data.txt'
    file_name = 'temp_monkey_middle.txt'
    file_path = pathlib.Path(__file__)
    folder_path = pathlib.Path(file_path.parent, file_name)
    monkey_data = load_data_file(folder_path.as_posix()).split('\n')

    process_monkeys(monkey_data)

    _ranges = range(1000,11000,1000)
    range_to_test = [0, 20] + list(_ranges)
    for idx in range(0, 10000):
        for m_idx in MONKEYS:
            monkey = MONKEYS[m_idx]
            monkey_items = monkey.items
            monkey.items = []
            for item in monkey_items:
                # item.calculate_worry(*monkey.operations, divided=monkey.inspection_times) #, mod=int(m_idx)+1)
                item.calculate_worry(*monkey.operations, divided=0, mod=monkey.inspection_times) #, mod=int(m_idx)+1)
                pass_to_monkey_idx = monkey.test_value(item.value)
                pass_item_to_monkey(item, pass_to_monkey_idx)


        if idx in range_to_test:
            inspections = [(m.name,m.inspection_times) for m in MONKEYS.values()]
            print(inspections)


    inspections = sorted([(m.name,m.inspection_times) for m in MONKEYS.values()],reverse=True, key=lambda x:x[0])
    print(inspections)
    print(inspections[0][1] * inspections[1][1])

