# The Ren'Py Chess Game
# Updated 07/19/2018

# Author: Ruolin Zheng
# GitHub: RuolinZheng08

# This code belongs in the Public Domain.
# Feel free to re-use and / or modify in free or commercial products.

###############################################################################

# The script of the game goes in this file.

# The game starts here.

label start:
    $ ai_mode = False
    $ winner = None

    "Welcome to the Ren'Py Chess Game!"

    label opponent_selection:
        menu:
            "Please select the game mode."

            "Player vs. Self":
                $ ai_mode = False
            "Player vs. Computer":
                $ ai_mode = True
                # Player plays White by default
                $ player_color = 'White'
                $ computer_color = 'Black'

    window hide

    # Start chess game
    call screen minigame(ai_mode)
    # End chess game
    $ winner = _return

    if ai_mode:
        if winner == player_color:
            "Congratulations! You won!"
        elif winner == computer_color:
            "The computer defeated you. Better luck next time!"
        elif winner == 'draw':
            "The game ended in a draw. See if you can win the next time!"
    else:
        if winner != 'draw':
            "The winner is [winner]! Congratulations!"
        else:
            "The game ended in a draw."

    menu:
        "Do you want to play another round of chess?"

        "Yes":
            jump opponent_selection
        "No":
            "Okay, see you next time! Bye!"
            return
