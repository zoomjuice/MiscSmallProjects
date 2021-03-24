from os import system, name


def cls():
    system('cls' if name == 'nt' else 'clear')
    return


def move_disk(from_tower, to_tower):
    print(from_tower)
    print(to_tower)
    if len(from_tower) == 0:
        raise ValueError('This tower has no disks!')
    elif len(to_tower) != 0 and from_tower[-1] > to_tower[-1]:
        raise ValueError('You can\'t place a larger disk on top of a smaller disk')
    else:
        to_tower.append(from_tower.pop())


def select_tower(message):
    while True:
        ret_val = input(message)
        if ret_val in towers.keys():
            return ret_val
        else:
            continue


intro_string = """
╔═════════════════════════════════════════════════════════════════════════╗
║                 ╔════════════════════════════════════╗                  ║
║                 ║                                    ║                  ║
║                 ║  █   █   ███   █   █  █████  █████ ║                  ║
║                 ║  █   █  █   █  ██  █  █   █    █   ║                  ║
║                 ║  █████  █████  █ █ █  █   █    █   ║                  ║
║                 ║  █   █  █   █  █  ██  █   █    █   ║                  ║
║                 ║  █   █  █   █  █   █  █████  █████ ║                  ║
║                 ║  ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾ ║                  ║
║                 ║       |          |          |      ║                  ║
║                 ║      █|█         |          |      ║                  ║
║                 ║     ██|██        |          |      ║                  ║
║                 ║    ███|███       |          |      ║                  ║
║                 ║   ████|████      |          |      ║                  ║
║                 ║  ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾ ║                  ║
║                 ╚════════════════════════════════════╝                  ║
║                                                                         ║
║ Welcome to Towers of Hanoi! Your goal is to move all the disks from the ║
║ first tower to either of the other towers. The rules are simple:        ║
║     1.) You may only move the disk from the top of a tower              ║
║     2.) You may not place a larger disk on top of a smaller one         ║
╚═════════════════════════════════════════════════════════════════════════╝
"""
intro_status = 'Let\'s begin.'

while True:
    cls()
    print(intro_string)
    print(intro_status + '\n')
    tower_size = None
    try:
        tower_size = int(input('How many disks would you like to play with?: '))
    except ValueError:
        intro_status = 'Sorry, I didn\'t understand that. Please try again.'
        continue

    if tower_size <= 1:
        intro_status = 'You must have at least 3 disks in your tower. Please choose a new number.'
        continue
    elif tower_size > 100:
        intro_status = 'Nice try, but I\'m not going to let you trigger an overflow.'
        continue
    elif tower_size > 10:
        min_moves = 2**tower_size - 1
        if min_moves > 1_000_000:
            intro_status = 'Your game would take at least {:.2e} moves to solve, try a smaller tower.'.format(min_moves)
            continue
        else:
            intro_status = 'Your game would take at least {m} moves to solve, try a smaller tower.'.format(m=min_moves)
            continue
    else:
        break

tower_1 = [i for i in range(tower_size, 0, -1)]
tower_2 = []
tower_3 = []
filled = [i for i in range(tower_size, 0, -1)]
towers = {'1': tower_1, '2': tower_2, '3': tower_3}


def build_towers():
    t1_pad = tower_1[:] + [0] * (len(filled) - len(tower_1))
    t2_pad = tower_2[:] + [0] * (len(filled) - len(tower_2))
    t3_pad = tower_3[:] + [0] * (len(filled) - len(tower_3))
    tower_art = ''
    for i in range(1, len(filled) + 1):
        t1_art = ' ' * (len(filled) - t1_pad[-i]) + '█' * t1_pad[-i] + '|' + '█' * t1_pad[-i] + ' ' * (len(filled) - t1_pad[-i])
        t2_art = ' ' * (len(filled) - t2_pad[-i]) + '█' * t2_pad[-i] + '|' + '█' * t2_pad[-i] + ' ' * (len(filled) - t2_pad[-i])
        t3_art = ' ' * (len(filled) - t3_pad[-i]) + '█' * t3_pad[-i] + '|' + '█' * t3_pad[-i] + ' ' * (len(filled) - t3_pad[-i])
        tower_art += t1_art + t2_art + t3_art + '\n'
    print(tower_art)


while True:
    build_towers()

    # make a tower selection function
    src = select_tower('Move from which tower? (1, 2, 3): ')
    dst = select_tower('Move to which tower? (1, 2, 3): ')

    try:
        move_disk(towers.get(src), towers.get(dst))
        cls()
    except ValueError as e:
        cls()
        print(str(e))
        continue

    if tower_3 == filled or tower_2 == filled:
        print('You win!')
        break
