# The script of the game goes in this file.

# The game starts here.

label start:
    $ ai_mode = False

    "Welcome to the Ren'Py Chess Game!"

    label opponent_selection:
        menu:
            "Please select the game mode."

            "Player vs. Self":
                $ ai_mode = False
            "Player vs. Computer":
                $ ai_mode = True
    window hide
    # Minigame starts below
    call screen minigame(ai_mode)

    if ai_mode:
        if _return == 'player':
            "Congratulations! You won!"
        else:
            "Better luck next time!"

    menu:
        "Do you want to play another round of chess?"

        "Yes":
            jump opponent_selection
        "No":
            "Okay, see you next time! Bye!"
            return
