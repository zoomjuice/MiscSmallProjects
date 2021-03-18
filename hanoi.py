from math import inf
from os import system, name


def cls():
    system('cls' if name == 'nt' else 'clear')
    return


def move_disk(from_tower, to_tower):
    if from_tower[-1] == inf:
        raise ValueError('This tower has no disks!')
    elif from_tower[-1] > to_tower[-1]:
        raise ValueError('You can\'t place a larger disk on top of a smaller disk')
    else:
        to_tower.append(from_tower.pop())


welcome_string = """
    Towers of Hanoi rules:
        -
    """

while True:
    tower_size = None
    try:
        tower_size = int(input('How many disks would you like to play with?: '))
    except ValueError:
        print('Sorry, I didn\'t understand that. Are you sure you entered a whole number? Please try again.')
        continue

    if tower_size <= 1:
        print('You must have at least 3 disks in your tower. Please choose a new number.')
        continue
    elif tower_size > 10:
        print('Your game would take at least {m} moves to solve, try a smaller tower.'.format(m=(2**tower_size - 1)))
        continue
    else:
        break

tower_1 = [inf] + [i for i in range(tower_size, 0, -1)]
tower_2 = [inf]
tower_3 = [inf]
filled = [inf] + [i for i in range(tower_size, 0, -1)]
towers = [None, tower_1, tower_2, tower_3]


def build_towers():
    t1_pad = tower_1[1:] + [0] * (len(filled) - len(tower_1) + 1)
    t2_pad = tower_2[1:] + [0] * (len(filled) - len(tower_2) + 1)
    t3_pad = tower_3[1:] + [0] * (len(filled) - len(tower_3) + 1)
    tower_art = ''
    for i in range(1, len(filled) + 1):
        t1_art = ' ' * (len(filled) - t1_pad[-i]) + '█' * t1_pad[-i] + '|' + '█' * t1_pad[-i] + ' ' * (len(filled) - t1_pad[-i])
        t2_art = ' ' * (len(filled) - t2_pad[-i]) + '█' * t2_pad[-i] + '|' + '█' * t2_pad[-i] + ' ' * (len(filled) - t2_pad[-i])
        t3_art = ' ' * (len(filled) - t3_pad[-i]) + '█' * t3_pad[-i] + '|' + '█' * t3_pad[-i] + ' ' * (len(filled) - t3_pad[-i])
        tower_art += t1_art + t2_art + t3_art + '\n'
    print(tower_art)


while True:
    build_towers()

    src = int(input('Move from which tower? (1, 2, 3): '))
    dst = int(input('Move to which tower? (1, 2, 3): '))

    try:
        move_disk(towers[src], towers[dst])
        cls()
    except ValueError as e:
        cls()
        print(str(e))
        continue
    except IndexError as e:
        cls()
        print('Invalid tower')
        continue

    if tower_3 == filled:
        print('You win!')
        break
