from math import inf
from os import system, name

tower_size = int(input('How many disks would you like to play with?: '))
tower_1 = [inf] + [i for i in range(tower_size, 0, -1)]
tower_2 = [inf]
tower_3 = [inf]
filled = [inf] + [i for i in range(tower_size, 0, -1)]
towers = [None, tower_1, tower_2, tower_3]

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


while True:
    print('Tower 1:', tower_1[1:])
    print('Tower 2:', tower_2[1:])
    print('Tower 3:', tower_3[1:])

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
