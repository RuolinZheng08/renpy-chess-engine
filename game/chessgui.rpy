# The Ren'Py Chess Game
# Updated 07/19/2018

# Author: Ruolin Zheng
# GitHub: RuolinZheng08

# This code belongs in the Public Domain.
# Feel free to re-use and / or modify in free or commercial products.

###############################################################################

label chessgui:

    init python:

        from chesslogic import *
        from chessai import *

        class ChessDisplayable(renpy.Displayable):
            '''
            the ChessDisplayable class which inherits from renpy.Displayable
            '''
            def __init__(self, chess_ai=None):
                renpy.Displayable.__init__(self)

                # Objects and logic
                self.chessgame = ChessGame()
                if chess_ai:
                    self.chessai = ChessAI()
                else:
                    self.chessai = None
                self.player_move = None
                self.ai_move = None
                self.moves_list_piece = []
                self.winner = None

                # Blit positions
                self.hover_coord = None
                self.src_coord = None
                self.dst_coord = None

                # Displayables
                self.pieces_image = {}
                self.pieces_image_constructor()
                self.hover_image = Solid('#00ff0050', xsize=LOC_SIZE, ysize=LOC_SIZE)
                self.clicked_image = Solid('#0a82ff88', xsize=LOC_SIZE, ysize=LOC_SIZE)
                self.moves_image = Solid('#45b8ff88', xsize=LOC_SIZE, ysize=LOC_SIZE)
                self.player_text = Text("Whose turn: White", color='#fff', size=26)
                self.status_text = Text("")

            def render(self, width, height, st, at):

                # Render objects
                # images
                pieces_image_render = self.pieces_render_constructor(width, height, st, at)
                hover_image_render = renpy.render(self.hover_image, width, height, st, at)
                clicked_image_render = renpy.render(self.clicked_image, width, height, st, at)
                moves_image_render = renpy.render(self.moves_image, width, height, st, at)
                # texts
                player_text_render = renpy.render(self.player_text, width, height, st, at)
                status_text_render = renpy.render(self.status_text, width, height, st, at)

                # Main render and blit
                render = renpy.Render(width, height)
                render.blit(player_text_render, (1020, 10))
                render.blit(status_text_render, (1020, 40))
                if self.hover_coord:
                    render.blit(hover_image_render, self.hover_coord)
                if self.src_coord:
                    render.blit(clicked_image_render, self.src_coord)
                self.board_to_image(pieces_image_render, render)
                self.moves_to_image(moves_image_render, render)

                return render

            def event(self, ev, x, y, st):
                import pygame

                # Player vs.Player or Player's turn in Player vs. AI

                if self.chessai == None or \
                (self.chessai and self.chessgame.whose_turn() == 'White'):

                    # Handle mouse motion inside frame
                    if X_MIN < x < X_MAX:
                        # Hover
                        if ev.type == pygame.MOUSEMOTION:
                            self.hover_coord = cursor_round(x, y)
                            renpy.redraw(self, 0)
                            
                        # Click
                        if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                            # First click
                            if self.src_coord is None:
                                self.src_coord = cursor_round(x, y)
                                src_loc = loc_from_cursor(self.src_coord)
                                # Redraw if piece present and is player's turn, reset if None
                                piece = self.chessgame.board.get_at_loc(src_loc)
                                if piece and piece.player == self.chessgame.whose_turn():
                                    self.moves_list_piece = self.chessgame.moves_piece(src_loc)
                                    renpy.redraw(self, 0)
                                else:
                                    self.src_coord = None
                            # Second click
                            else:
                                self.dst_coord = cursor_round(x, y)
                                self.player_move = self.move_constructor()
                                ret = self.chessgame.apply_move(self.player_move)
                                if ret:
                                    # Deactivate highlight for AI's turn
                                    self.hover_coord = None
                                    self.player_text = Text("Whose turn: %s" % self.chessgame.whose_turn(), color='#fff', size=26)
                                    renpy.redraw(self, 0)
                                # Reset two clicks and moves list
                                self.src_coord, self.dst_coord = None, None
                                self.moves_list_piece = []
                # AI's turn in Player vs.AI:
                if self.chessai and self.chessgame.whose_turn() == 'Black':
                    ai_move = self.chessai.pick_move(self.chessgame)
                    if ai_move:
                        self.chessgame.apply_move(ai_move)
                    self.player_text = Text("Whose turn: %s" % self.chessgame.whose_turn(), color='#fff', size=26)
                    renpy.redraw(self, 0)
                        
                # Handle key
                keys = pygame.key.get_pressed()
                # undoing moves
                num_moves = len(self.chessgame.history)
                if num_moves != 0:
                    if keys[pygame.K_LEFT]:
                        renpy.notify("You can undo a move by pressing <-")
                        # undo one move in Player vs. Self
                        if not self.chessai:
                            self.chessgame.undo_move()
                        # undo two moves in Player vs. Computer
                        else:
                            if not num_moves & 0x1:
                                self.chessgame.undo_move()
                                self.chessgame.undo_move()
                        renpy.redraw(self, 0)

                # Status texts and End Game condition
                if self.chessgame.in_check():
                    self.status_text = Text("In Check: %s" % self.chessgame.whose_turn(), color='#fff', size=26)
                else:
                    self.status_text = Text("")

                if self.chessgame.stalemate():
                    self.player_text = Text("Stalemate", color='#fff', size=26)
                    self.status_text = Text("Winner: None", color='#fff', size=26)
                    self.winner = 'draw'
                    renpy.redraw(self, 0)

                if self.chessgame.checkmate():
                    winner = opponent_color(self.chessgame.whose_turn())
                    self.winner = winner
                    self.player_text = Text("Checkmate", color='#fff', size=26)
                    self.status_text = Text("Winner: %s" % winner, color='#fff', size=26)
                    renpy.redraw(self, 0)


                # Exits when user clicks anywhere on the screen
                if self.winner:
                    self.hover_coord = None
                    self.moves_list_piece = []
                    renpy.redraw(self, 0)
                    renpy.notify("Exiting Chess Game, the Winner is %s" % winner)

            def visit(self):
                return [ self.player_text, self.status_text ]

            ###############################################################################
            # Self-defined functions
            def board_to_image(self, pieces_render, render):
                '''
                blits the squares on board into render
                Args:
                    pieces_render (dict {piece : Render object})
                    render (Render object)
                Returns:
                    None
                '''
                for row in range(0, NUM_ROW):
                    for col in range(0, NUM_COL):
                        square = self.chessgame.board[row][col]
                        if square:
                            render_obj = pieces_render[square.short_hand_notation()]
                            render_coord = cursor_from_index(row, col)
                            render.blit(render_obj, render_coord)

            def moves_to_image(self, moves_render, render):
                '''
                blits the squares the selected piece can move to into render
                Args:
                    moves_render (Render object)
                    render (Render object)
                Returns:
                    None
                '''
                for move in self.moves_list_piece:
                    dst = move.dst
                    dst_coord = cursor_from_loc(dst)
                    render.blit(moves_render, dst_coord)

            # Self-defined helpers
            def pieces_image_constructor(self):
                '''
                constructs Image objects and a mapping dict
                Args:
                    None
                Returns:
                    None
                '''
                for black_piece in BLACK_PIECES:
                    image_path = './images/pieces_image/' + SHORT_HAND[black_piece].lower() + '_black.png'
                    image_obj = Image(image_path)
                    self.pieces_image[black_piece] = image_obj
                for white_piece in WHITE_PIECES:
                    image_path = './images/pieces_image/' + SHORT_HAND[white_piece.upper()].lower() + '_white.png'
                    image_obj = Image(image_path)
                    self.pieces_image[white_piece] = image_obj

            def pieces_render_constructor(self, width, height, st, at):
                '''
                constructs Render objects and a mapping dict
                Args:
                    None
                Returns:
                    pieces_render (dict {piece : Render object})
                '''
                pieces_render = {}
                for black_piece in BLACK_PIECES:
                    render_obj = renpy.render(self.pieces_image[black_piece], width, height, st, at)
                    pieces_render[black_piece] = render_obj
                for white_piece in WHITE_PIECES:
                    render_obj = renpy.render(self.pieces_image[white_piece], width, height, st, at)
                    pieces_render[white_piece] = render_obj
                return pieces_render

            def move_constructor(self):
                assert self.src_coord and self.dst_coord
                src_loc = loc_from_cursor(self.src_coord)
                dst_loc = loc_from_cursor(self.dst_coord)
                moved = self.chessgame.board.get_at_loc(src_loc)
                captured = self.chessgame.board.get_at_loc(dst_loc)
                return Move(src_loc, dst_loc, moved, captured, None)
                

                