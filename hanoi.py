"""
TODO:
    - Refactor build_towers()
    - Add art and screen consistency to gameplay portion
    - Show users their number of moves vs. perfect play
    - Don't automatically exit on completion
    - Add support for INI files?
"""

from os import system, name


# Clear screen
def cls():
    system('cls' if name == 'nt' else 'clear')
    return


# Verify validity of and perform user's chosen move
def move_disk(from_tower, to_tower):
    if len(from_tower) == 0:  # Make sure user isn't moving from an empty tower
        raise ValueError('This tower has no disks!')
    elif len(to_tower) != 0 and from_tower[-1] > to_tower[-1]:
        raise ValueError('You can\'t place a larger disk on top of a smaller disk')
    else:
        to_tower.append(from_tower.pop())


# Repeatedly ask user to select tower until a valid selection is made
def select_tower(message):
    while True:
        ret_val = input(message)
        if ret_val in towers.keys():
            return ret_val
        else:
            print('Invalid tower. Please try again.')
            continue


# Calculate padding and disk sizes, then draw towers
def build_towers():
    tower_art = ''

    # Zero-pad towers to uniform length of completed tower, plus one empty space on top for the center rod
    t1_pad = tower_1.copy() + [0] * (len(filled) - len(tower_1) + 1)
    t2_pad = tower_2.copy() + [0] * (len(filled) - len(tower_2) + 1)
    t3_pad = tower_3.copy() + [0] * (len(filled) - len(tower_3) + 1)

    # Add 1 to range since it stops before the end number, add another 1 for an empty space on top of the tower
    for i in range(1, len(filled) + 2):
        # Build left side of each tower's current layer
        t1_left_side = str(' ' * (len(filled) - t1_pad[-i]) + '█' * t1_pad[-i])
        t2_left_side = str(' ' * (len(filled) - t2_pad[-i]) + '█' * t2_pad[-i])
        t3_left_side = str(' ' * (len(filled) - t3_pad[-i]) + '█' * t3_pad[-i])
        # Append center rod followed by the reverse image of the left side to make the right
        t1_art = t1_left_side + '|' + t1_left_side[::-1]
        t2_art = t2_left_side + '|' + t2_left_side[::-1]
        t3_art = t3_left_side + '|' + t3_left_side[::-1]
        # Combine each tower segment into a layer and add it to the final string
        tower_art += t1_art + t2_art + t3_art + '\n'
    print(tower_art)


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
    # Maintain consistent screen display while user is selecting tower sizes
    cls()
    print(intro_string)
    print(intro_status + '\n')
    tower_size = None

    try:
        tower_size = int(input('How many disks would you like to play with?: '))
    except ValueError:
        intro_status = 'Sorry, I didn\'t understand that. Please try again.'
        continue

    # Make sure the user selects a reasonably sized tower
    if tower_size <= 2:
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

# Initialize towers with disks ordered from largest to smallest based on user's selected tower size
tower_1 = [i for i in range(tower_size, 0, -1)]
tower_2 = []
tower_3 = []

# Generate completed tower to check against for win condition
filled = tower_1.copy()

# Tower selection during gameplay
towers = {'1': tower_1, '2': tower_2, '3': tower_3}

while True:
    cls()
    build_towers()

    # Get move from player
    src = select_tower('Move from which tower? (1, 2, 3): ')
    dst = select_tower('Move to which tower? (1, 2, 3): ')

    # Execute player's move
    try:
        move_disk(towers.get(src), towers.get(dst))
        cls()
    except ValueError as e:
        cls()
        print(str(e))
        continue

    # Check to see if either of the initially empty towers now has a full tower
    if tower_3 == filled or tower_2 == filled:
        print('You win!')
        break
