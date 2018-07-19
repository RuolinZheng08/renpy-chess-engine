## Chess Game: A Ren'Py Chess Engine

#### About

This repo contains the source code of a basic Chess Engine made with Ren'Py. The main purpose of this project is to demonstrate the integration of a mini-game into a Ren'Py Visual Novel with the help of Ren'Py Displayable.

Within the Ren'Py Chess Game, there are two available gameplay modes, *Player vs. Self* and *Player vs. Computer*. Out of consideration for computation speed and VN players' expectations for a mini-game in a Visual Novel, the Computer chess player is of a minimal chess AI implementation.

#
#### Adapting the Chess Game to other Ren'Py projects


The code for the Ren'Py Chess Game is in the Public Domain and can be used and / or modified in any free or commercial projects.
> **List of core files for the Chess Game:**
> - `images/bg chessboard.png` - the chess board image
> - `images/pieces_image` - the chess pieces images
> - `chesslogic.py`	- the rules and logic behind chess
> - `chessai.py` - the auto-player that evaluates and selects move
> - `chessgui.rpy` - the Renpy Displayable class and methods
> - `screens.rpy` - the mini-game screen holding the Displayable
> - `script.rpy` - the game script that calls the mini-game screen  

##### Instructions
Copy the image files, `chesslogic.py`, `chessai.py` and `chessgui.rpy` into your `game/` directory.  
Paste the following code into specified `.rpy` files.
> In `screens.rpy`  
> Note that ai_mode is a Boolean, for *Player vs. Self*, call `screen minigame(False)` and for *Player vs. Computer*, call `screen minigame(True)` 
```python
## This screen is used for the chess game.
screen minigame(ai_mode):
    default chess = ChessDisplayable(chess_ai=ai_mode)
    add "bg chessboard"
    add chess
``` 


> In `script.rpy` (or any script file in which the chess game should occur)
> Note the way `screen minigame()` is called with the variable `ai_mode`
```python
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
```


##### Customization for different window size  
By Ren'Py default configuration, this code assumes a window size of `1280 * 720`. If a different window size is used, the following changes will need to be made.
> **Files and directories of concern:**
> - `chesslogic.py` - change in configurations
> - `images/bg chessboard.png` - change in size
> - `images/pieces_image` - change in size

`bg chessboard.png` is a `1280 * 720` image, with the `720 * 720` chessboard at the center and two `280 * 720` black paddings on each side. A chessboard customized for your VN window should also position the chessboard at the center of the rectangular image.  
The current chess pieces are of size `81 * 81`, fitting into each `90 * 90` square on the board. Make sure you change the size of these images accordingly to accomodate your window size.  

Then make changes to the following configuration parameters in `chesslogic.py`

> In `chesslogic.py`
``` python
# Configurations for chess gui

# the leftmost coordinate of the chessboard
# (1280 - 720) / 2 = 280
X_MIN = 280 
# the rightmost coordinate of the chessboard
# 1280 - (1280 - 720) / 2 = 1000
X_MAX = 1000
# the top coordinate of the chessboard
Y_MIN = 0
# the bottom coordinate of the chessboard
Y_MAX = 720

# the leftmost coordinate of the chessboard
# (1280 - 720) / 2 = 280
X_OFFSET = 280
# the size of each square on the chessboard
# 720 / 8 = 90
LOC_SIZE = 90
```

##### Customization for different styles
> **Files and directories of concern:**
> - `chessgui.rpy` - changes in displayed text and style
> - `images/bg chessboard.png` - changes in art style
> - `images/pieces_image` - changes in art style

Customize the art of the image files as you wish.  
The following stylistic changes can be made in `chessgui.rpy`.
> In `chessgui.rpy`
```python
# customize the RGBA colors and texts
self.hover_image = Solid('#00ff0050', xsize=LOC_SIZE, ysize=LOC_SIZE)
self.clicked_image = Solid('#0a82ff88', xsize=LOC_SIZE, ysize=LOC_SIZE)
self.moves_image = Solid('#45b8ff88', xsize=LOC_SIZE, ysize=LOC_SIZE)
self.player_text = Text("Whose turn: White", color='#fff', size=26)
self.status_text = Text("")
```
> To add new displayables in `chessgui.rpy`
```python
class ChessDisplayable(renpy.Displayable):

    def __init__(self, chess_ai=None):
        renpy.Displayable.__init__(self)
        ...
        # create new displayables by setting color and text
		self.image_displayable = Solid(color, **properties)
        self.text_displayable = Text(text, **properties)
        ...
        
    def render(self, width, height, st, at):
    	...
        # render new displayables
        image_displayable_render = renpy.render(self.image_displayable, width, height, st, at)
        text_displayable_render = renpy.render(self.text_displayable, width, height, st, at)
        ...
        # blit new displayables onto main render
        # by setting xcoord and ycoord
        render = renpy.Render(width, height)
        render.blit(image_displayable_render, (xcoord_1, ycoord_1))
        render.blit(text_displayable_render, (xcoord_2, ycoord_2))
        ...
        return render
```
  
#
#### Reference
**Chess GUI**
- [Ren'Py Displayables](https://www.renpy.org/doc/html/displayables.html)
- [Ren'Py Creator-Defined Displayables](https://www.renpy.org/doc/html/udd.html)
- [Ren'Py Screens and Screen Language](https://www.renpy.org/doc/html/udd.html)
- [Pong Minigame from the Ren'Py Tutorial](https://github.com/renpy/renpy/blob/master/tutorial/game/indepth_minigame.rpy)

**Chess Logic** 
- UChicago CMSC 151 Project 1 & 2, `chess-logic.rkt` and `chess-gui.rkt`

**Chess AI** 
- [Creating a Basic Chess AI Using Python](http://blog.mbuffett.com/creating-a-basic-chess-ai-using-python/)
- [Simple Chess AI Step by Step](https://medium.freecodecamp.org/simple-chess-ai-step-by-step-1d55a9266977)
- [Building a Simple Chess AI](https://byanofsky.com/2017/07/06/building-a-simple-chess-ai/)

#
#### TODOs
More features that I may find time to do in the future:  
- castling, en passant, promotion
- allowing the player to choose whether to play as `Black` or `White` in *Player vs. Computer*