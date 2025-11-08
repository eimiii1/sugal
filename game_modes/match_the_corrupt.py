import random
import os
import time
from cards import cards

HIDDEN_CARD = """
#:.....  ...  .     . . ...:#
...:..... . .   . ..  ..   ..
....  :.. .. . . .:::...:....
..:..:. .  ....:..      .....
...... .   .::. . ....   . ..
.. . . ...:.. .. ::+@#.   ..:
. .  . .:..    ..@=.=@:.  ..:
.  . ..:.   ..-*@%@#::...  .:
. . ..:   ..:#@+:.....:.   .:
.. .:.    .:..=%%.  .=: . .:.
. .:..   ..%@@@+.  .=-.  ....
...... ..:..-......=:..  ....
..:.  .:+%#@%-.  .=:....... .
.:.   :@%*-:.. .:+.  . ...  .
..  .:=:-=#: .:=-.  . .:.  ..
:.. .%%%*=...--...   .:.    .
:  .=...--..:.    ..:.. .   .
:  . .. . .   .  ..:.. .... .
:. .           ..:.   . .....
.:. .      ....:. .  ..:..:..
..:..    ..::....    ... .... 
.  ...::... .. .    .:...:. .
*..........................:#
""".splitlines() 

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_grid(cards_to_display, show_cards, rows, cols):
    card_lines = []
    for i, card in enumerate(cards_to_display):
        if show_cards[i]:
            card_lines.append(card['card'].splitlines())
        else:
            card_lines.append(HIDDEN_CARD)

    max_height = max(len(lines) for lines in card_lines)
    for lines in card_lines:
        while len(lines) < max_height:
            lines.append(" " * len(lines[0]))

    for r in range(rows):
        row_cards = card_lines[r*cols:(r+1)*cols]
        for line_index in range(max_height):
            print("   ".join(card[line_index] for card in row_cards))
        print()

def match_the_corrupt(money):
    levels = [
        {"num_unique": 4, "rows": 2, "cols": 4, "base_time": 60, "memorize_time": 5},
        {"num_unique": 6, "rows": 3, "cols": 4, "base_time": 90, "memorize_time": 10},
        {"num_unique": 8, "rows": 4, "cols": 4, "base_time": 120, "memorize_time": 15},
    ]

    for level_idx, level in enumerate(levels, start=1):
        num_unique = level["num_unique"]
        rows, cols = level["rows"], level["cols"]
        total_cards = num_unique * 2

        selected_cards = random.sample(cards, num_unique)
        paired_cards = selected_cards * 2
        random.shuffle(paired_cards)

        clear_console()
        print(f"Level {level_idx}: Memorize the cards!")
        display_grid(paired_cards, show_cards=[True]*total_cards, rows=rows, cols=cols)
        time.sleep(level["memorize_time"])  # increased per level

        # 2. Flip all to hidden
        clear_console()
        print(f"Level {level_idx}: Cards are hidden! Match the pairs.")
        show_flags = [False] * total_cards
        matched = [False] * total_cards

        start_time = time.time()
        total_time = level["base_time"]

        while not all(matched):
            elapsed = time.time() - start_time
            remaining = total_time - elapsed
            if remaining <= 0:
                print("Time's up!")
                break

            print(f"Time left: {int(remaining)} seconds")
            display_grid(paired_cards, show_cards=show_flags, rows=rows, cols=cols)

            try:
                idx1, idx2 = map(int, input(f"Select two cards (1-{total_cards}): ").split())
                idx1 -= 1
                idx2 -= 1
                if idx1 == idx2 or matched[idx1] or matched[idx2]:
                    print("Invalid selection. Choose two different hidden cards.")
                    time.sleep(1)
                    clear_console()
                    continue
            except:
                print("Invalid input. Enter two numbers separated by space.")
                time.sleep(1)
                clear_console()
                continue

            show_flags[idx1] = True
            show_flags[idx2] = True
            clear_console()
            display_grid(paired_cards, show_cards=show_flags, rows=rows, cols=cols)

            if paired_cards[idx1]['name'] == paired_cards[idx2]['name']:
                print("Matched!")
                matched[idx1] = matched[idx2] = True
                total_time += 5
                money += 10
            else:
                print("Not a match!")
                total_time -= 5  # penalty
                time.sleep(1)
                show_flags[idx1] = show_flags[idx2] = False

            time.sleep(1)
            clear_console()

        print(f"Level {level_idx} complete!")

    print("All levels complete!")
    return money