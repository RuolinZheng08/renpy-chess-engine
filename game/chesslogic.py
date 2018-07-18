# Configurations for chess gui
X_MIN = 280
X_MAX = 1000
Y_MIN = 0
Y_MAX = 720

X_OFFSET = 280
LOC_SIZE = 90

# Configurations for chess logic
NUM_ROW = 8
NUM_COL = 8
FILE = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H')
RANK = (1, 2, 3, 4, 5, 6, 7, 8)
PIECE_TYPE = ('Pawn', 'Bishop', 'Knight', 'Rook', 'King', 'Queen')
PLAYER = ('Black', 'White')
PROMOTE_TO = ('Queen', 'Rook', 'Bishop', 'Knight')

BLACK_PIECES = ('P', 'R', 'B', 'N', 'K', 'Q')
WHITE_PIECES = ('p', 'r', 'b', 'n', 'k', 'q')
SHORT_HAND = {'P' : 'Pawn', 'R' : 'Rook', 'B' : 'Bishop', 'N' : 'Knight', 'K' : 'King', 'Q' : 'Queen'}

RBQ_DIST = 8
KING_DIST = 1
PAWN_INITIAL_RANK = {'White' : 2, 'Black' : 7}
ROOK_VECTOR = ((1, 0), (-1, 0), (0, 1), (0, -1))
BISHOP_VECTOR = ((1, 1), (-1, -1), (-1, 1), (1, -1))
QUEEN_VECTOR = ROOK_VECTOR + BISHOP_VECTOR
KING_VECTOR = QUEEN_VECTOR
KNIGHT_VECTOR = ((1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1))
PAWN_VECTOR = {'White' : ((0, 1), (-1, 1), (1, 1)), 'Black' : ((0, -1), (-1, -1), (1, -1))}
PIECES_VECTOR = {'Rook' : ROOK_VECTOR, 'Bishop' : BISHOP_VECTOR, 'Queen' : QUEEN_VECTOR, 'King' : KING_VECTOR, 'Knight' : KNIGHT_VECTOR, 'Pawn' : PAWN_VECTOR}

STARTING_BOARD_STR = ('RNBQKBNR', 'PPPPPPPP', '--------', '--------', '--------', '--------', 'pppppppp', 'rnbqkbnr')

###############################################################################
# Class definitions

class Loc(object):
  '''
  the location denoted by file and rank on a chessboard
  Attributes:
      file (str)
      rank (int)
  '''
  def __init__(self, file, rank):
    assert file in FILE and rank in RANK
    self.file = file
    self.rank = rank
  def __str__(self):
    return '({}, {})'.format(self.file, self.rank)
  def __eq__(self, other):
    return self.file == other.file and self.rank == other.rank

class Piece(object):
  '''
  the piece characterized by its type and color for a chessgame
  Attributes:
      piece_type (str)
      player (str)
  Methods:
      short_hand_notation(self)
      get_vector(self)
  '''
  def __init__(self, piece_type, player):
    self.piece_type = piece_type
    self.player = player
  def __str__(self):
    return '({} {})'.format(self.piece_type, self.player)
  def __eq__(self, other):
    return self.piece_type == other.piece_type and self.player == other.player

  def short_hand_notation(self):
    if self.piece_type == 'Knight':
      initial = 'N'
    else:
      initial = self.piece_type[0]
    if self.player == 'Black':
      return initial
    else:
      return initial.lower()
  def get_vector(self, capture=False):
    '''
    returns the move vectors of all types except Pawn
    Args:
        None
    Returns:
        vectors (tuple of tuple)
    '''
    assert self.piece_type in PIECES_VECTOR.keys()
    if self.piece_type == 'Pawn':
      if capture:
        return PIECES_VECTOR['Pawn'][self.player][1:]
      else:
        return PIECES_VECTOR['Pawn'][self.player][0]
    return PIECES_VECTOR[self.piece_type]

class Move(object):
  '''
  the movement of a piece and its effect in a chessgame
  Attributes:
      src (Loc object)
      dst (Loc object)
      moved (Piece object)
      captured (U (None, Piece object))
      promote_to (U (None, str))
  '''
  def __init__(self, src, dst, moved, captured=None, promote_to=None):
    if promote_to:
      assert promote_to in PROMOTE_TO
    self.src = src
    self.dst = dst
    self.moved = moved
    self.captured = captured
    self.promote_to = promote_to
  def __str__(self):
    return 'Move: {} {}->{} captured {} promoted-to {}'.format(self.moved, self.src, self.dst, str(self.captured), str(self.promote_to))
  def __eq__(self, other):
    '''two Moves are equivalent if they have equal string representation'''
    return self.src == other.src and self.dst == other.dst and self.moved == other.moved and self.captured == other.captured and self.promote_to == other.promote_to
    
class Board(list):
  '''
  the chess board inherited from python list class, 8 lists of 8 optional Piece objects nested in an outer list
  Attributes:
      None
  Methods:
      get_at_loc(self, loc)
      update_loc(self, loc, square)
      occupied_by(self, loc)
  '''
  def __str__(self):
    none_repr = lambda l: [str(elm).ljust(14) for elm in l]
    return '\n'.join(' '.join(none_repr(row)) for row in self)

  # Board operations
  def get_at_loc(self, loc):
    '''
    Args: loc (Loc object)
    Returns: square (U (Piece object, None))
    '''
    row, col = index_from_loc(loc)
    return self[row][col]
  def update_loc(self, loc, square):
    '''
    Args: loc (Loc object), square (U (Piece object, None))
    Returns: None
    '''
    row, col = index_from_loc(loc)
    self[row][col] = square
  def occupied_by(self, loc):
    '''
    Args: lov (Loc object)
    Returns: U (player (str), None)
    '''
    piece = self.get_at_loc(loc)
    if piece:
      return piece.player
    else:
      return None

class ChessGame(object):
  '''
  the chessgame which consists of a board and history, a list of moves in chronological order
  Attributes:
      board (Board object)
      history (list of Move object)
  Methods:
      moves_piece(self, loc)
      moves_player(self)
      in_check(self)
      legal_move(self)
      checkmate(self)
      stalemate(self)
      apply_move(self)
      undo_move(self)
  '''
  def __init__(self, board_str=None):
    if board_str:
      self.board = board_from_strings(board_str)
    else:
      self.board = board_from_strings(STARTING_BOARD_STR)
    self.history = []
  def __str__(self):
    return '###Board###\n{}\n###History###\n{}\n'.format(self.board, self.history)
  
  # ChessGame operations

  def promotion(self):
    pass
  def castling(self):
    pass
  def en_passant(self):
    pass

  def moves_piece(self, loc):
    '''returns a list of moves available to the piece identified by the loc'''
    piece = self.board.get_at_loc(loc)
    moves_piece_list_raw = []
    moves_piece_list = []
    if piece:
      if piece.piece_type == 'Rook' or piece.piece_type == 'Bishop' or piece.piece_type == 'Queen':
        moves_piece_list_raw = self.moves_along_vectors(loc, piece, piece.get_vector(), RBQ_DIST)
      elif piece.piece_type == 'King':
        moves_piece_list_raw = self.moves_along_vectors(loc, piece, piece.get_vector(), KING_DIST)
      elif piece.piece_type == 'Knight':
        moves_piece_list_raw = self.moves_knight(loc, piece)
      elif piece.piece_type == 'Pawn':
        moves_piece_list_raw = self.moves_pawn(loc, piece)
      # removes from list if the move puts king into check
      for move in moves_piece_list_raw:
        # updates board without modifying history
        self.board.update_loc(move.src, None)
        self.board.update_loc(move.dst, move.moved)
        if not self.in_check():
          moves_piece_list.append(move)
        # restores board
        self.board.update_loc(move.src, move.moved)
        self.board.update_loc(move.dst, move.captured)
    return moves_piece_list

  def moves_player(self):
    '''returns a list of moves available to the current player'''
    moves_list_player = []
    player_locs = self.get_player_pieces_loc()
    for loc in player_locs:
      moves_list_player += self.moves_piece(loc)
    return moves_list_player

  def in_check(self): 
    '''
    True if with player's king unmoved, opponent's next move can capture king
    Args: None
    Returns: bool (Boolean)
    '''
    opponent = opponent_color(self.whose_turn())
    king_loc = self.get_player_king_loc()
    assert king_loc
    if self.threatened_along_vectors(king_loc, Piece('Rook', opponent), RBQ_DIST):
      return True
    elif self.threatened_along_vectors(king_loc, Piece('Bishop', opponent), RBQ_DIST):
      return True
    elif self.threatened_along_vectors(king_loc, Piece('Queen', opponent), RBQ_DIST):
      return True
    elif self.threatened_along_vectors(king_loc, Piece('King', opponent), KING_DIST):
      return True
    elif self.threatened_by_knight(king_loc, Piece('Knight', opponent)):
      return True
    elif self.threatened_by_pawn(king_loc, Piece('Pawn', opponent)):
      return True
    return False

  def legal_move(self, move):
    '''
    True if the move is in the player's move list
    Args: move (Move object)
    Returns: bool (Boolean)
    '''
    available_moves = self.moves_player()
    for available_move in available_moves:
      if available_move == move:
        return True
    return False

  def checkmate(self):
    '''True if player is in check and has no available move'''
    if self.moves_player() == [] and self.in_check() == True:
      return True

  def stalemate(self):
    '''True if player is not in check but has no available move'''
    if self.moves_player() == [] and self.in_check() == False:
      return True

  def apply_move(self, move):
    '''
    Args: move (Move object)
    Returns: bool (Boolean)
    '''
    if self.legal_move(move):
      # remove from src
      self.board.update_loc(move.src, None)
      # move to dst, replace piece if any
      self.board.update_loc(move.dst, move.moved)
      # append to history
      self.history.append(move)
      return True
    else:
      return False

  def undo_move(self):
    '''
    undo the last move in history
    Args: move (Move object)
    Returns: bool (Boolean)
    '''
    if self.history == []:
      return False
    prev_move = self.history[-1]
    assert self.board.occupied_by(prev_move.src) is None
    # move back to src
    self.board.update_loc(prev_move.src, prev_move.moved)
    # remove from dst, restore piece if any
    self.board.update_loc(prev_move.dst, prev_move.captured)
    # remove last move from history
    self.history = self.history[:-1]
    return True


  # Helpers
  def whose_turn(self):
    '''Returns: player (str)'''
    if self.history == []:
      return 'White'
    else:
      return opponent_color(self.history[-1].moved.player)
  def get_player_king_loc(self):
    '''
    Args: None
    Returns: loc (Loc object)
    '''
    player = self.whose_turn()
    for row in range(0, NUM_ROW):
      for col in range(0, NUM_COL):
        square = self.board[row][col]
        if square and square.piece_type == 'King' and square.player == player:
          return loc_from_index(row, col)
    return None
  def get_player_pieces_loc(self):
    '''
    Args: None
    Returns: player_locs (list of Piece objects)
    '''
    player_locs = []
    for row in range(0, NUM_ROW):
      for col in range(0, NUM_COL):
        square = self.board[row][col]
        if square and square.player == self.whose_turn():
          player_locs.append(loc_from_index(row, col))
    return player_locs

  # Helpers for moves_piece()
  def moves_along(self, loc, vector, max_dist):
    '''
    returns a list of unblocked, legal moves in the vector direction within max distance from current loc
    Args:
        loc (Loc object)
        vector (tuple)
        max_dist (int)
    Returns:
        moves_along_list (list of Move objects)
    '''
    moves_along_list = []
    moved = self.board.get_at_loc(loc)
    for dist in range(1, max_dist+1):
      scaled_vector = tuple(i * dist for i in vector)
      dst = loc_add_vector(loc, scaled_vector)
      # dst is on board
      if dst != None:
        on_loc = self.board.get_at_loc(dst)
        # occupied by player's piece
        if on_loc and on_loc.player == self.whose_turn():
          break
        # unoccupied or occupied by opponent
        else:
          move = Move(loc, dst, moved, captured=on_loc)      
          moves_along_list.append(move)
          # captured opponent's piece
          if move.captured != None:
            break
    return moves_along_list
  # for Rook, Bishop, Queen, King
  def moves_along_vectors(self, loc, piece, vector_list, max_dist):
    '''
    returns a list of unblocked, legal moves in all vector directions within max distance from current loc
    Args:
        loc (Loc object)
        vector_list (a list of tuple)
        max_dist (int)
    Returns:
        moves_list_vectors (list of Move objects)
    '''
    moves_list_vectors = []
    for vector in piece.get_vector():
      moves_along_vector = self.moves_along(loc, vector, max_dist)
      moves_list_vectors.extend(moves_along_vector)
    return moves_list_vectors

  def moves_knight(self, loc, knight):
    '''
    Args: loc (Loc object), knight (Piece object)
    Returns: moves_knight (list)
    '''
    moves_list_knight = []
    for vector in knight.get_vector():
      dst = loc_add_vector(loc, vector)
      if dst != None:
        if self.board.occupied_by(dst) != knight.player:
          dst_piece = self.board.get_at_loc(dst)
          move = Move(loc, dst, knight, captured=dst_piece)
          moves_list_knight.append(move)
    return moves_list_knight

  def moves_pawn(self, loc, pawn):
    '''
    pawn may move 2 steps or 1 step forward at initial loc; moves 1 step forward or captures horizontally
    '''
    moves_list_pawn = []
    move_vector = pawn.get_vector()
    initial_move_vector = tuple(i * 2 for i in move_vector)
    capture_vector_list = pawn.get_vector(capture=True)
    # regular move case, move available if no piece on dst
    dst = loc_add_vector(loc, move_vector)
    if dst != None:
      on_loc = self.board.get_at_loc(dst)
      if on_loc is None:
        move = Move(loc, dst, pawn)
        moves_list_pawn.append(move)
        # pawn at initial loc
        if loc.rank == PAWN_INITIAL_RANK[pawn.player]:
          dst = loc_add_vector(loc, initial_move_vector)
          if dst != None:
            on_loc = self.board.get_at_loc(dst)
            if on_loc is None:
              move = Move(loc, dst, pawn)
              moves_list_pawn.append(move)
    # regular capture case
    for capture_vector in capture_vector_list:
      dst = loc_add_vector(loc, capture_vector)
      if dst != None:
        on_loc = self.board.get_at_loc(dst)
        if on_loc and on_loc.player != pawn.player:
          move = Move(loc, dst, pawn, captured=on_loc)
          moves_list_pawn.append(move)
    return moves_list_pawn

  # Helpers for in_check()
  # for Rook, Bishop, Queen, King
  def threatened_along_vectors(self, loc, attacker, max_dist):
    '''
    returns True if the king is threatened by attacker along the its path
    Args:
        loc (Loc object)
        attacker (Piece object)
        max_dist (int)
    Returns:
        bool (Boolean)
    '''
    king = self.board.get_at_loc(loc)
    assert king and king.piece_type == 'King' and king.player == self.whose_turn()
    for vector in attacker.get_vector():   
      for dist in range(1, max_dist+1):
        scaled_vector = tuple(i * dist for i in vector)
        src = loc_add_vector(loc, scaled_vector)
        # src is on board
        if src != None:
          on_loc = self.board.get_at_loc(src)
          if on_loc:
            # if attack path blocked by player's own piece, check other paths
            if on_loc.player == self.whose_turn():
              break
            # if attack path blocked by opponent's piece
            elif on_loc.player == opponent_color(self.whose_turn()):
              # non-attacker, check other paths
              if on_loc.piece_type != attacker.piece_type:
                break
              # attack, return True
              else:
                return True
    return False

  def threatened_by_knight(self, loc, knight):
    for vector in knight.get_vector():
      src = loc_add_vector(loc, vector)
      if src != None: 
        on_loc = self.board.get_at_loc(src)
        if on_loc and on_loc == knight:
          return True
    return False

  def threatened_by_pawn(self, loc, pawn):
    for vector in pawn.get_vector(capture=True):
      attack_vector = tuple(-i for i in vector)
      src = loc_add_vector(loc, attack_vector)
      if src != None: 
        on_loc = self.board.get_at_loc(src)
        if on_loc and on_loc == pawn:
          return True
    return False

###############################################################################
# Main functions for logic
def board_from_strings(string_list):
  '''
  create a board based on the given list of eight strings each of eight characters
  Args:
      string_list (list of str)
  Returns:
      board (Board object)
  '''
  assert len(string_list) == 8
  board = Board()
  for string in string_list:
    assert len(string) == 8
    row = []
    for chara in string:
      if chara == '-':
        piece = None
      else:
        # Black
        if chara.isupper():
          assert chara in BLACK_PIECES
          piece_type = SHORT_HAND[chara]
          player = 'Black'
          piece = Piece(piece_type, player)
        # White
        elif chara.islower():
          assert chara in WHITE_PIECES
          piece_type = SHORT_HAND[chara.upper()]
          player = 'White'
          piece = Piece(piece_type, player)
      row.append(piece)
    board.append(row)
  return board

###############################################################################
# Helper functions for gui
def cursor_round(x, y):
  '''
  returns cursor position rounded to the upperleft coordinate of the current loc
  Args:
      x (int)
      y (int)
  Returns:
      (x_round, y_round) (tuple)
  '''
  assert X_MIN <= x <= X_MAX and Y_MIN <= y <= Y_MAX
  x_round = (x - X_OFFSET) / LOC_SIZE * LOC_SIZE + X_OFFSET
  y_round = y / LOC_SIZE * LOC_SIZE
  return (x_round, y_round)

def cursor_from_index(row, col):
  '''
  returns cursor position rounded to the upperleft coordinate given board indices
  Args:
      row (int)
      col (int)
  Returns:
      (x, y) (tuple)
  '''
  x = LOC_SIZE * col + X_OFFSET
  y = LOC_SIZE * row
  return (x, y)

def cursor_from_loc(loc):
  '''
  returns cursor position rounded to the upperleft coordinate given board indices
  Args:
      loc (Loc object)
  Returns:
      (x, y) (tuple)
  '''
  row = 8 - loc.rank
  col = FILE.index(loc.file)
  x = LOC_SIZE * col + X_OFFSET
  y = LOC_SIZE * row
  return (x, y)

def loc_from_cursor(coord_tuple):
  '''
  Args:
      coord_tuple (tuple)
  Returns:
      loc (Loc object)
  '''
  x, y = coord_tuple
  assert X_MIN <= x <= X_MAX and Y_MIN <= y <= Y_MAX
  x_index = (x - X_OFFSET) / LOC_SIZE
  y_index = 7 - (y / LOC_SIZE)
  return Loc(FILE[x_index], RANK[y_index])

###############################################################################
# Helper functions for logic
def loc_from_index(row, col):
  '''
  returns a Loc object given board indices
  Args:
      row (int)
      col (int)
  Returns:
      loc (Loc object)
  '''
  file = FILE[col]
  rank = 8 - row
  return Loc(file, rank)

def index_from_loc(loc):
  '''
  returns the board index tuple given Loc object
  Args:
      loc (Loc object)
  Returns:
      (row, col) (tuple)
  '''
  row = 8 - loc.rank
  col = FILE.index(loc.file)
  return (row, col)

def opponent_color(player):
  '''
  returns opponent's color given player
  Args:
      player (str)
  Returns:
      opponent (str)
  '''
  assert player in PLAYER
  if player == 'White':
    return 'Black'
  else:
    return 'White'

def loc_add_vector(loc, vector):
  '''
  returns the loc with the vector added, None if off board
  Args:
      loc (Loc object)
      vector (tuple)
  Returns:
      U (loc, None)
  '''
  delta_file, delta_rank = vector
  new_file_index = FILE.index(loc.file) + delta_file
  new_rank = loc.rank + delta_rank
  if new_file_index < 0 or new_file_index >= NUM_COL or new_rank <= 0 or new_rank > NUM_ROW:
    return None
  else:
    return Loc(FILE[new_file_index], new_rank)
