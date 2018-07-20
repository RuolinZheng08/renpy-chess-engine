# The Ren'Py Chess Game
# Updated 07/19/2018

# Author: Ruolin Zheng
# GitHub: RuolinZheng08

# This code belongs in the Public Domain.
# Feel free to re-use and / or modify in free or commercial products.

###############################################################################

# Chess AI for chess gui
# Reference: 
# http://blog.mbuffett.com/creating-a-basic-chess-ai-using-python/
# https://medium.freecodecamp.org/simple-chess-ai-step-by-step-1d55a9266977
# https://byanofsky.com/2017/07/06/building-a-simple-chess-ai/

from chesslogic import Piece, Move, opponent_color
import random

###############################################################################
# Configurations for Board Value Calculations
# White pieces controlled by player have positive values while Black pieces controlled by AI have negative values 
PIECE_VALUES = {'Pawn' : 1, 'Knight' : 3, 'Bishop' : 3, 'Rook' : 5, 'Queen' : 9, 'King' : 999}

###############################################################################
# Class definitions

class MoveNode(object):
  '''
  move node objects that records the value of a given move
  Attributes:
      move (Move object)
      value (U (int, None))
  '''
  def __init__(self, move=None, value=None):
    self.move = move
    self.value = value
    self.children = []

class ChessAI(object):
  '''
  a minimal chess ai that opts for the current most-valued capturing move without taking into consideration any subsequent moves
  Attributes:
      None
  '''
  def pick_move(self, chessgame):
    '''
    construct a list of most-valued move nodes and randomly return one
    Args:
        chessgame (ChessGame object)
    Returns:
        best_value_move (Move object)
    '''
    root = self.generate_move_tree(chessgame)
    # traversing the tree to construct a list of most-valued moves
    best_value_moves = []
    best_value = None
    for move_node in root.children:
      # initialize
      if best_value == None:
        best_value = move_node.value
        best_value_moves.append(move_node.move)
      # append if equal
      elif move_node.value == best_value:
        best_value_moves.append(move_node.move)
      # clear the old list and update best_value if greater
      elif move_node.value > best_value:
        best_value = move_node.value
        best_value_moves = []
        best_value_moves.append(move_node.move)

    # AI is checkmated and has no available move
    if best_value_moves == []:
      return None
    else:
      return random.choice(best_value_moves)

  def generate_move_tree(self, chessgame):
    root = MoveNode()
    ai_legal_moves = chessgame.moves_player()

    # depth one
    assert chessgame.whose_turn() == 'Black'
    for ai_move in ai_legal_moves:
      parent_move_value = get_move_value(ai_move)
      ai_move_node = MoveNode(ai_move, parent_move_value)
      root.children.append(ai_move_node)

      # depth two
      chessgame.apply_move(ai_move)
      assert chessgame.whose_turn() == 'White'
      self.populate_children(ai_move_node, chessgame)
      chessgame.undo_move()
      # optimize move value
      ai_move_node.value = self.optimize_move_value(ai_move_node)

    return root

  def populate_children(self, parent_move_node, chessgame):
    child_legal_moves = chessgame.moves_player()
    parent_move_value = parent_move_node.value
    for child_move in child_legal_moves:
      child_move_value = parent_move_value + get_move_value(child_move)
      child_move_node = MoveNode(child_move, child_move_value)
      parent_move_node.children.append(child_move_node)

  def optimize_move_value(self, parent_move_node):
    # Player is checkmated and has no available move
    if parent_move_node.children == []:
      checkmate_move = Move(None, None, Piece('King', opponent_color(parent_move_node.move.moved.player)))
      assert checkmate_move.moved.player == 'White'
      return get_move_value(checkmate_move)
    else:
      return min([child.value for child in parent_move_node.children])

###############################################################################
# Helper functions
def get_move_value(move):
  '''
  returns the value of the given move, positive for capturing White pieces and negative for capturing Black pieces
  Args: move (Move object)  Returns: move_value (int)
  '''
  if move.captured:
    # positive for capturing White, player's pieces
    if move.captured.player == 'White':
      move_value = PIECE_VALUES[move.captured.piece_type]
    # negative for capturing Black, AI's pieces
    else:
      move_value = ~PIECE_VALUES[move.captured.piece_type] + 0x1
  else:
    move_value = 0
  return move_value
