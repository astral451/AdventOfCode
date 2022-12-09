
# For this to work be sure to add AOC_SESSION environment variable with the cookie session_id
#from aocd.models import Puzzle
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
 
# A : Rock
# B : Paper
# C : Scissors
# X : Rock 1
# Y : Paper 2
# Z : Scissors 3
# 0 : lose
# 3 : draw
# 6 : win

ASSUMED_VALUES = {
    'A' : [1, 'Rock'],
    'B' : [2, 'Paper'],
    'C' : [3, 'Scissors'],
    'X' : [1, 'Rock'],
    'Y' : [2, 'Paper'],
    'Z' : [3, 'Scissors'],
    'Rock' : 'Scissors',
    'Scissors' : 'Paper',
    'Paper' : 'Rock',
    'Win' : 6,
    'Lose' : 0,
    'Draw' : 3 
}

VALUES_DATA = {
    'Rock'      : 1,
    'Scissors'  : 3,
    'Paper'     : 2,
    'Win'       : 6,
    'Lose'      : 0,
    'Draw'      : 3 
}

PLAYSTYLE_PART2 = {
    'A' : 'Rock',
    'B' : 'Paper',
    'C' : 'Scissors',
    'X' : 'Lose',
    'Y' : 'Draw',
    'Z' : 'Win',
    # Opponent Hand : [ Losing Throw, Winning Throw ]
    'Rock' : ['Scissors', 'Paper'],
    'Scissors' : ['Paper', 'Rock'],
    'Paper' : ['Rock', 'Scissors'],
}


def process_hand_corrected(line):
    print(line)
    opponent, you = line.split(' ') 

    opponent_hand = PLAYSTYLE_PART2[opponent]
    opponent_value = VALUES_DATA[opponent_hand]

    your_status = PLAYSTYLE_PART2[you]

    opponent_score = 0
    your_score = 0 

    if your_status == 'Draw':
        your_value = opponent_value
        your_hand = opponent_hand
        opponent_score = opponent_value + VALUES_DATA['Draw']
        your_score = your_value + VALUES_DATA['Draw']

    elif your_status == 'Win':
        your_hand = PLAYSTYLE_PART2[opponent_hand][1]
        your_value = VALUES_DATA[your_hand]
        your_status = 'Win'
        opponent_score = opponent_value + VALUES_DATA['Lose']
        your_score = your_value + VALUES_DATA['Win']

    else:
        your_hand = PLAYSTYLE_PART2[opponent_hand][0]
        your_value = VALUES_DATA[your_hand]
        opponent_score = opponent_value + VALUES_DATA['Win']
        your_score = your_value + VALUES_DATA['Lose']

    print('They threw {}, you threw {}, you {}'.format(opponent_hand,your_hand,your_status))
    print('opponent_score {}, your_score {}'.format(opponent_score, your_score))
    return opponent_score, your_score  


def process_hand_assumed(line):
    
    print(line)
    opponent, you = line.split(' ') 
    
    opponent_value, opponent_hand = ASSUMED_VALUES[opponent] 
    your_value, your_hand = ASSUMED_VALUES[you] 

    opponent_score = 0
    your_score = 0 
    your_status = ''

    if opponent_hand == your_hand:
        your_status = 'Draw'
        opponent_score = opponent_value + ASSUMED_VALUES['Draw']
        your_score = your_value + ASSUMED_VALUES['Draw']

    elif your_hand == ASSUMED_VALUES[opponent_hand]:
        your_status = 'Lose'
        opponent_score = opponent_value + ASSUMED_VALUES['Win']
        your_score = your_value + ASSUMED_VALUES['Lose']

    else:
        your_status = 'Win'
        opponent_score = opponent_value + ASSUMED_VALUES['Lose']
        your_score = your_value + ASSUMED_VALUES['Win']

    print('They threw {}, you threw {}, you {}'.format(opponent_hand,your_hand,your_status))
    print('opponent_score {}, your_score {}'.format(opponent_score, your_score))
    return opponent_score, your_score  
    

if __name__ == "__main__":
    file_path = pathlib.Path(__file__)
    folder_path = pathlib.Path(file_path.parent, 'elf_rps_strategy_data.txt')
    #folder_path = pathlib.Path(file_path.parent, 'temp_strat_data.txt')
 
    data_file = load_data_file(folder_path.as_posix())
    data_hands = data_file.split('\n')
    your_score = 0
    opponent_score = 0 
    for hand in data_hands:
        if hand:
            #op_sc, yr_sc = process_hand_assumed(hand)
            op_sc, yr_sc = process_hand_corrected(hand)
            your_score += yr_sc
            opponent_score += op_sc
            
    print('Your Score was {}'.format(your_score))
