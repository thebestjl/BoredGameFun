#TODO: Allow incorrect attack selections to try again. Done?

#TODO: Allow customizable piece selection and placement.

#TODO: Allow varied board sizes.

#TODO: Add randomly varying attack strength. Will require larger health pools.

#TODO: Add incredibly basic AI that will determine if a piece is in attack position and prioritize attacking the lowest health target.
# Possibly even flee once it gets to low health. If no piece is in attack position, then select a piece that's close (within two spaces)
# to an opponent and move in their direction. Otherwise, move randomly.

#TODO: Allow multiple pieces to attack at once? Can't decide.

from random import *

class player():
  def __init__(self, pieces):
    self.pieces = pieces
    
    
  def get_pieces(self):
    return self.pieces
    
    
  def get_pieces_remaining(self):
    return len(self.pieces)
    
    
  def remove_pieces(self):
    for piece in self.pieces:
      if piece.get_hp() == 0:
        index = self.pieces.index(piece)
        del self.pieces[index]


class piece():
  #TODO: HARDCODE SYMBOL TO HP MAP
  def __init__(self, symbol, hp, coords):
    self.symbol = symbol
    self.hp = hp
    self.coords = coords
    
    
  def update_hp(self):
    if self.hp > 0:
      self.hp -= 1
      
      
  def get_hp(self):
    return self.hp
    
    
  def get_symbol(self):
    return self.symbol
    
    
  def get_coords(self):
    return self.coords
    
    
  def update_coords(self, coords):
    self.coords = coords
  
  
  def __str__(self):
    ret = 'Symbol: ' + self.symbol + ' HP: ' + str(self.hp) + ' Coordinates: ' + str(self.coords)
    return ret
  
  
  def __repr__(self):
    ret = 'Symbol: ' + self.symbol + ' HP: ' + str(self.hp) + ' Coordinates: ' + str(self.coords)
    return ret
    
    

class board_game():
  def __init__(self, is_ai = False, height = None, width = 0):
    
    self.is_ai = is_ai
    
    if height != None:
      self.board_height = height
    else:
      self.board_height = 5
      
    if width < 3:
      self.board_width = 5
    else:
      self.board_width = width
      
    self.board = []
    
    self.game_pieces = ['x', 't', 'o']
    
    p1_o = piece(self.game_pieces[0], 2, [self.board_height - 1, 1])
    p1_t = piece(self.game_pieces[1], 4, [self.board_height - 1, 2])
    p1_x = piece(self.game_pieces[2], 3, [self.board_height - 1, 3])
    
    p2_o = piece(self.game_pieces[0].upper(), 2, [0, 3])
    p2_t = piece(self.game_pieces[1].upper(), 4, [0, 2])
    p2_x = piece(self.game_pieces[2].upper(), 3, [0, 1])
    
    self.p1 = player([p1_o, p1_t, p1_x])
    self.p2 = player([p2_o, p2_t, p2_x])
    
    self.turns_left = 20

    self.update_board()
  
  
  def turn(self, this_player):
    cur_player = self.get_players(this_player)[0]
    if this_player == 1:
      print('Player 1:')
    else:
      print('Player 2:')
      
    piece_select_str = 'Choose your move by typing the piece''s symbol or type ''help'': '
    for i in range(cur_player.get_pieces_remaining()):
      piece_select_str += '\n\t' + cur_player.get_pieces()[i].get_symbol()
    
    piece_select_str += ':\n'
    piece_select = input(piece_select_str)
    
    if piece_select.strip().lower() == 'help':
      help_str = 'Press the index assigned to select a piece or perform the action, type ''hp'' to see the hp for each piece, ''skip'' to skip your turn, or type ''board'' to display the board.'
      print(help_str)
    elif piece_select.strip().lower() == 'hp':
      self.display_hp()
    elif piece_select.strip().lower() == 'board':
      self.print_board()
    elif piece_select.strip().lower() == 'skip':
      return
    else:
      for i in range(cur_player.get_pieces_remaining()):
        if piece_select.lower() == cur_player.get_pieces()[i].get_symbol().lower():
          self.parse_action(this_player, i)
          self.update_board()
          return
        
      print('Invalid input.')
      
    self.turn(this_player)
    
    
  def parse_action(self, this_player, index):
    cur_player = self.get_players(this_player)[0]
    
    if cur_player.get_pieces()[index].get_symbol().lower() == self.game_pieces[0]:
      move_select = input('\t7 or Q for northwest\n\t1 or Z for southwest\n\t3 or C for southeast\n\t9 or E for northeast\n\t5 or S to attack\n')
      
      if [str(5), 's', 'S'].count(move_select) > 0:
        self.attack(this_player, index)
        return
      elif ['7', '1', '3', '9', 'q', 'Q', 'z', 'Z', 'c', 'C', 'e', 'E'].count(move_select) > 0:
        self.move_o(this_player, move_select, index)
        return
      else:
        print('Inccorrect input, try again!')
        self.parse_action(this_player, index)
        return

    elif cur_player.get_pieces()[index].get_symbol().lower() == self.game_pieces[1]:
      move_select = input('\t7 or Q for northwest\n\t1 or Z for southwest\n\t3 or C for southeast\n\t9 or E for northeast\n\t8 or W for north\n\t4 or A for west\n\t2 or X for south\n\t6 or D for east\n\t5 or S to attack\n')
      
      if move_select == str(5) or move_select == 's' or move_select == 'S':
        self.attack(this_player, index)
        return
      elif ['7', '1', '3', '9', '8', '4', '2', '6', 'q', 'Q', 'z', 'Z', 'c', 'C', 'e', 'E', 'w', 'W', 'a', 'A', 'x', 'X', 'd', 'D'].count(move_select) > 0:
        self.move_t(this_player, move_select, index)
        return
      else:
        print('Inccorrect input, try again!')
        self.parse_action(this_player, index)
        return
      
    elif cur_player.get_pieces()[index].get_symbol().lower() == self.game_pieces[2]:
      move_select = input('\t8 or W for north\n\t4 or A for west\n\t2 or X for south\n\t6 or D for east\n\t5 or S to attack\n')
    
      if move_select == str(5):
        self.attack(this_player, index)
        return
      elif ['8', '4', '2', '6', 'w', 'W', 'a', 'A', 'x', 'X', 'd', 'D'].count(move_select) > 0:
        self.move_x(this_player, move_select, index)
        return
      else:
        print('Inccorrect input, try again!')
        self.parse_action(this_player, index)
        return
        
    print('Inccorrect input, try again!')
    self.parse_action(this_player, index)
    return
    
    
  """
  --Attack Function
  """
  def attack(self, this_player, index):
    players = self.get_players(this_player)
    hit = False
    movement = 0
    if this_player == 1:
      movement = -1
    else:
      movement = 1
    
      
    cur_player = players[0]
    other_player = players[1]
    
    cur_piece = cur_player.get_pieces()[index]
    cur_piece_coords = cur_piece.get_coords()
    opp_pieces = other_player.get_pieces()
    
    for piece in other_player.get_pieces():
      opp_coords = piece.get_coords()
      if cur_piece_coords[0] + movement == opp_coords[0] and cur_piece_coords[1] == opp_coords[1]:
        piece.update_hp()
        hit = True
        
        if piece.get_hp() == 0:
          print('Piece ' + piece.get_symbol() + ' is destroyed.')
          other_player.remove_pieces()
          
      self.update_players(this_player, cur_player, other_player)
  
    if not hit:
      print('Failed to hit.')
  
  
  """
  ---Movement rules
  """
  def move_o(self, this_player, direction, index):
    if direction == '7' or direction.lower() == 'q':
      self.move_nw(this_player, index)
    elif direction == '1' or direction.lower() == 'z':
      self.move_sw(this_player, index)
    elif direction == '3' or direction.lower() == 'c':
      self.move_se(this_player, index)
    elif direction == '9' or direction.lower() == 'e':
      self.move_ne(this_player, index)
    else:
      print('Incorrect input choice. Try again.')
      self.parse_action(this_player, index)
    
    
  def move_t(self, this_player, direction, index):
    if direction == '7' or direction.lower() == 'q':
      self.move_nw(this_player, index, True)
    elif direction == '1' or direction.lower() == 'z':
      self.move_sw(this_player, index, True)
    elif direction == '3' or direction.lower() == 'c':
      self.move_se(this_player, index, True)
    elif direction == '9' or direction.lower() == 'e':
      self.move_ne(this_player, index, True)
    elif direction == '8' or direction.lower() == 'w':
      self.move_n(this_player, index, True)
    elif direction == '4' or direction.lower() == 'a':
      self.move_w(this_player, index, True)
    elif direction == '2' or direction.lower() == 'x':
      self.move_s(this_player, index, True)
    elif direction == '6' or direction.lower() == 'd':
      self.move_e(this_player, index, True)
    else:
      print('Incorrect input choice. Try again.')
      self.parse_action(this_player, index)
      
      
  def move_x(self, this_player, direction, index):
    if direction == '8' or direction.lower() == 'w':
      self.move_n(this_player, index)
    elif direction == '4' or direction.lower() == 'a':
      self.move_w(this_player, index)
    elif direction == '2' or direction.lower() == 'x':
      self.move_s(this_player, index)
    elif direction == '6' or direction.lower() == 'd':
      self.move_e(this_player, index)
    else:
      print('Incorrect input choice. Try again.')
      self.parse_action(this_player, index)
    
    
  """
  --Directional functions
  """
  def move_nw(self, this_player, index, multimove = False):
    players = self.get_players(this_player)
    cur_piece_coords = players[0].get_pieces()[index].get_coords()
    opp_pieces = players[1].get_pieces()
    new_coords = [(cur_piece_coords[0] - 1) % self.board_height, (cur_piece_coords[1] - 1) % self.board_width]
    
    for p in opp_pieces:
      if p.get_coords()[0] == new_coords[0] and p.get_coords()[1] == new_coords[1]:
        print('Error: blocked by opponent.')
        return self.parse_action(this_player, index)
    
    while (multimove and new_coords[0] - 1 >= 0 and new_coords[1] - 1 >= 0):
      for p in opp_pieces:
        if p.get_coords()[0] == new_coords[0] - 1 and p.get_coords()[1] == new_coords[1] - 1:
          players[0].get_pieces()[index].update_coords(new_coords)
          return
        
      new_coords = [(new_coords[0] - 1) % self.board_height, (new_coords[1] - 1) % self.board_width]
      
    players[0].get_pieces()[index].update_coords(new_coords)
    self.update_players(this_player, players[0], players[1])
    
    
  def move_sw(self, this_player, index, multimove = False):
    players = self.get_players(this_player)
    cur_piece_coords = players[0].get_pieces()[index].get_coords()
    opp_pieces = players[1].get_pieces()
    new_coords = [(cur_piece_coords[0] + 1) % self.board_height, (cur_piece_coords[1] - 1) % self.board_width]
    
    for p in opp_pieces:
      if p.get_coords()[0] == new_coords[0] and p.get_coords()[1] == new_coords[1]:
        print('Error: blocked by opponent.')
        return self.parse_action(this_player, index)
    
    while (multimove and new_coords[0] + 1 < self.board_height and new_coords[1] - 1 >= 0):
      for p in opp_pieces:
        if p.get_coords()[0] == new_coords[0] + 1 and p.get_coords()[1] == new_coords[1] - 1:
          players[0].get_pieces()[index].update_coords(new_coords)
          return
        
      new_coords = [(new_coords[0] + 1) % self.board_height, (new_coords[1] - 1) % self.board_width]
      
    players[0].get_pieces()[index].update_coords(new_coords)
    self.update_players(this_player, players[0], players[1])
  
  
  def move_se(self, this_player, index, multimove = False):
    players = self.get_players(this_player)
    cur_piece_coords = players[0].get_pieces()[index].get_coords()
    opp_pieces = players[1].get_pieces()
    new_coords = [(cur_piece_coords[0] + 1) % self.board_height, (cur_piece_coords[1] + 1) % self.board_width]
    
    for p in opp_pieces:
      if p.get_coords()[0] == new_coords[0] and p.get_coords()[1] == new_coords[1]:
        print('Error: blocked by opponent.')
        return self.parse_action(this_player, index)
    
    while (multimove and new_coords[0] + 1 < self.board_height and new_coords[1] + 1 < self.board_width):
      for p in opp_pieces:
        if p.get_coords()[0] == new_coords[0] + 1 and p.get_coords()[1] == new_coords[1] + 1:
          players[0].get_pieces()[index].update_coords(new_coords)
          return
        
      new_coords = [(new_coords[0] + 1) % self.board_height, (new_coords[1] + 1) % self.board_width]
      
    players[0].get_pieces()[index].update_coords(new_coords)
    self.update_players(this_player, players[0], players[1])
    
    
  def move_ne(self, this_player, index, multimove = False):
    players = self.get_players(this_player)
    cur_piece_coords = players[0].get_pieces()[index].get_coords()
    opp_pieces = players[1].get_pieces()
    new_coords = [(cur_piece_coords[0] - 1) % self.board_height, (cur_piece_coords[1] + 1) % self.board_width]
    
    for p in opp_pieces:
      if p.get_coords()[0] == new_coords[0] and p.get_coords()[1] == new_coords[1]:
        print('Error: blocked by opponent.')
        return self.parse_action(this_player, index)
    
    while (multimove and new_coords[0] - 1 >= 0 and new_coords[1] + 1 < self.board_width):
      for p in opp_pieces:
        if p.get_coords()[0] == new_coords[0] - 1 and p.get_coords()[1] == new_coords[1] + 1:
          players[0].get_pieces()[index].update_coords(new_coords)
          return
        
      new_coords = [(new_coords[0] - 1) % self.board_height, (new_coords[1] + 1) % self.board_width]
      
    players[0].get_pieces()[index].update_coords(new_coords)
    self.update_players(this_player, players[0], players[1])
    
    
  def move_n(self, this_player, index, multimove = False):
    players = self.get_players(this_player)
    cur_piece_coords = players[0].get_pieces()[index].get_coords()
    opp_pieces = players[1].get_pieces()
    new_coords = [(cur_piece_coords[0]  - 1) % self.board_height, (cur_piece_coords[1]) % self.board_width]
    
    for p in opp_pieces:
      if p.get_coords()[0] == new_coords[0] and p.get_coords()[1] == new_coords[1]:
        print('Error: blocked by opponent.')
        return self.parse_action(this_player, index)
    
    while (multimove and new_coords[0] - 1 >= 0):
      for p in opp_pieces:
        if p.get_coords()[0] == new_coords[0] - 1 and p.get_coords()[1] == new_coords[1]:
          players[0].get_pieces()[index].update_coords(new_coords)
          return
        
      new_coords[0] = (new_coords[0] - 1) % self.board_height
      
    players[0].get_pieces()[index].update_coords(new_coords)
    self.update_players(this_player, players[0], players[1])
    
    
  def move_w(self, this_player, index, multimove = False):
    players = self.get_players(this_player)
    cur_piece_coords = players[0].get_pieces()[index].get_coords()
    opp_pieces = players[1].get_pieces()
    new_coords = [(cur_piece_coords[0]) % self.board_height, (cur_piece_coords[1] - 1) % self.board_width]
    
    for p in opp_pieces:
      if p.get_coords()[0] == new_coords[0] and p.get_coords()[1] == new_coords[1]:
        print('Error: blocked by opponent.')
        return self.parse_action(this_player, index)
    
    while (multimove and new_coords[1] - 1 >= 0):
      for p in opp_pieces:
        if p.get_coords()[0] == new_coords[0] and p.get_coords()[1] == new_coords[1] - 1:
          players[0].get_pieces()[index].update_coords(new_coords)
          return
        
      new_coords[1] = (new_coords[1] - 1) % self.board_width
      
    players[0].get_pieces()[index].update_coords(new_coords)
    self.update_players(this_player, players[0], players[1])
    
    
  def move_s(self, this_player, index, multimove = False):
    players = self.get_players(this_player)
    cur_piece_coords = players[0].get_pieces()[index].get_coords()
    opp_pieces = players[1].get_pieces()
    new_coords = [(cur_piece_coords[0] + 1) % self.board_height, (cur_piece_coords[1]) % self.board_width]
    
    for p in opp_pieces:
      if p.get_coords()[0] == new_coords[0] and p.get_coords()[1] == new_coords[1]:
        print('Error: blocked by opponent.')
        return self.parse_action(this_player, index)
      
    while (multimove and new_coords[0] + 1 < self.board_height):
      for p in opp_pieces:
        if p.get_coords()[0] == new_coords[0] + 1 and p.get_coords()[1] == new_coords[1]:
          players[0].get_pieces()[index].update_coords(new_coords)
          return
        
      new_coords[0] = (new_coords[0] + 1) % self.board_height
      
    players[0].get_pieces()[index].update_coords(new_coords)
    self.update_players(this_player, players[0], players[1])
    
    
  def move_e(self, this_player, index, multimove = False):
    players = self.get_players(this_player)
    cur_piece_coords = players[0].get_pieces()[index].get_coords()
    opp_pieces = players[1].get_pieces()
    new_coords = [(cur_piece_coords[0]) % self.board_height, (cur_piece_coords[1] + 1) % self.board_width]
    
    for p in opp_pieces:
      if p.get_coords()[0] == new_coords[0] and p.get_coords()[1] == new_coords[1]:
        print('Error: blocked by opponent.')
        return self.parse_action(this_player, index)
      
    while (multimove and new_coords[1] + 1 < self.board_width):
      for p in opp_pieces:
        if p.get_coords()[0] == new_coords[0] and p.get_coords()[1] == new_coords[1] + 1:
          players[0].get_pieces()[index].update_coords(new_coords)
          return
        
      new_coords[1] = (new_coords[1] + 1) % self.board_width
      
    players[0].get_pieces()[index].update_coords(new_coords)
    self.update_players(this_player, players[0], players[1])
  
  
  """
  ---Helper functions
  """
  def get_players(self, this_player):
    if this_player == 1:
      return [self.p1, self.p2]
    else:
      return [self.p2, self.p1]
  
  
  def update_players(self, this_player, cur_player, other_player):
    if this_player == 1:
      self.p1 = cur_player
      self.p2 = other_player
    else:
      self.p2 = cur_player
      self.p1 = other_player
  
  
  def update_board(self):
    self.board = []
    for i in range(self.board_height):
      self.board.append([])
      for j in range(self.board_width):
        self.board[i].append(' ')
        
    p1_pieces = self.p1.get_pieces()
    for i in range(self.p1.get_pieces_remaining()):
      x = p1_pieces[i].get_coords()[0]
      y = p1_pieces[i].get_coords()[1]
      self.board[x][y] = p1_pieces[i].get_symbol()
      
    p2_pieces = self.p2.get_pieces()
    for i in range(self.p2.get_pieces_remaining()):
      x = p2_pieces[i].get_coords()[0]
      y = p2_pieces[i].get_coords()[1]
      self.board[x][y] = p2_pieces[i].get_symbol()
      
      
  def display_hp(self):
    hp_str = 'Player 1 HP:\n'
    for i in range(self.p1.get_pieces_remaining()):
      cur_piece = self.p1.get_pieces()[i]
      hp_str += '\t' + cur_piece.get_symbol() + ' has ' + str(cur_piece.get_hp()) + ' remaining.\n'
    
    hp_str += '\nPlayer 2 HP:\n'
    for i in range(self.p2.get_pieces_remaining()):
      cur_piece = self.p2.get_pieces()[i]
      hp_str += '\t' + cur_piece.get_symbol() + ' has ' + str(cur_piece.get_hp()) + ' remaining.\n'
    
    hp_str += '\nPlayer 1 has ' + str(self.p1.get_pieces_remaining()) + ' pieces remaining.\n'
    hp_str += '\nPlayer 2 has ' + str(self.p2.get_pieces_remaining()) + ' pieces remaining.\n'
    
    print(hp_str)


  def print_board(self):
    board_str = ''
    for i in range(self.board_height):
      for j in range(self.board_width):
        if j == self.board_width - 1:
          board_str += self.board[i][j] + '\n'
          if i < self.board_height - 1:
            for k in range(self.board_width * 2):
              if k % 2 == 0:
                board_str += '_'
              else:
                board_str += ' '
            board_str += '\n'
        else:
          board_str += self.board[i][j]
          board_str += '|'
      
    print(board_str)
    
    
  def damage_all_pieces(self):
    for piece in self.p1.get_pieces():
      piece.update_hp()
    
    for piece in self.p2.get_pieces():
      piece.update_hp()
      
    self.p1.remove_pieces()
    self.p2.remove_pieces()
     
  """
  ---AI!
  """
  def turn_ai(self, this_player = 2):
    if this_player == 1:
      plyr_str = 'Player 1'
    else:
      plyr_str = 'Player 2'
    
    print(plyr_str + ':')

    if self.ai_attack(this_player):
      print(plyr_str + ' attacked!')
      return
    elif self.ai_move_to_attack(this_player):
      return
    else self.ai_move(this_player):
      return
    

  def ai_attack(self, this_player, piece):
    players = self.get_players(this_player)
    cur_player = players[0]
    other_player = players[1]

    if this_player == 1:
      direction = -1
    else:
      direction = 1

    opp_hp = 1000
    dfndr = -1
    for i in range(cur_player.get_pieces_remaining()):
      cur_piece_attk_coords = cur_player.get_pieces().get_coords()
      cur_piece_attk_coords[0] = (cur_piece_attk_coords[0] + direction) % self.board_height
      for j in range(other_player.get_pieces_remaining()):
        if other_player.get_pieces()[j].get_coords() == cur_piece_attk_coords and other_player.get_pieces()[j].get_hp() < opp_hp:
          dfndr = j
          opp_hp = other_player.get_pieces()[j].get_hp()

    if attkr > -1 and dfndr > -1:
      other_player.get_pieces()[dfndr].update_hp()
      other_player.remove_pieces()
      return True

    return False


  def ai_move_to_attack(self, this_player):
    players = self.get_players(this_player)
    cur_player = players[0]
    other_player = players[1]

    if this_player == 1:
      direction = -1
    else:
      direction = 1

    o_p_coords = []
    for o_p in other_player.get_pieces():
      o_p_coords.append(o_p.get_coords())

    for c_p in cur_player.get_pieces():
      c_p_c = c_p.get_coords()
      for o_p in other_player.get_pieces():
        if c_p.get_symbol().strip().lower() == self.game_pieces[0]: #o
          o_coords = [(c_p_c[0] + direction) % self.board_height, (c_p_c[1] - 1) % self.board_width]
          oo_coords = o_coords = [(c_p_c[0] + 2 * direction) % self.board_height, (c_p_c[1] - 1) % self.board_width]
          if o_p_coords.count(o_coords) == 0 and oo_coords == o_p.get_coords():
            c_p.update_coords(o_coords)
            return True

          o_coords = [(c_p_c[0] + direction) % self.board_height, (c_p_c[1] + 1) % self.board_width]
          oo_coords = o_coords = [(c_p_c[0] + 2 * direction) % self.board_height, (c_p_c[1] + 1) % self.board_width]
          if o_p_coords.count(o_coords) == 0 and oo_coords == o_p.get_coords():
            c_p.update_coords(o_coords)
            return True

        elif c_p.get_symbol().strip().lower() == self.game_pieces[1]: #t
          t_coords = c_p.get_coords()
          moved = False
          while o_p_coords.count([(t_coords[0] + direction) % self.board_height, (t_coords[1] - 1) % self.board_width]) == 0 and t_coords[0] + direction != self.board_height and t_coords[0] + direction != 0 and  t_coords[1] - 1 != 0:
            t_coords = [(t_coords[0] + direction) % self.board_height, (t_coords[1] - 1) % self.board_width]
            moved = True
          
          ot_coords = [(t_coords[0] + direction) % self.board_height, t_coords[1]]
          if o_p_coords.count(ot_coords) >= 1 and moved:
            c_p.update_coords(t_coords)
            return True
          
          t_coords = c_p.get_coords()
          moved = False
          while o_p_coords.count([(t_coords[0] + direction) % self.board_height, (t_coords[1] + 1) % self.board_width]) == 0 and t_coords[0] + direction != self.board_height and t_coords[0] + direction != 0 and  t_coords[1] + 1 != self.board_width:
            t_coords = [(t_coords[0] + direction) % self.board_height, (t_coords[1] + 1) % self.board_width]
            moved = True
          
          ot_coords = [(t_coords[0] + direction) % self.board_height, t_coords[1]]
          if o_p_coords.count(ot_coords) >= 1 and moved:
            c_p.update_coords(t_coords)
            return True

          t_coords = c_p.get_coords()
          moved = False
          while o_p_coords.count([(t_coords[0] + direction) % self.board_height, t_coords[1]]) == 0 and t_coords[0] + direction != self.board_height and t_coords[0] + direction != 0:
            t_coords = [(t_coords[0] + direction) % self.board_height, t_coords[1]]
            moved = True

          ot_coords = [(t_coords[0] + direction) % self.board_height, t_coords[1]]
          if o_p_coords.count(ot_coords) >= 1 and moved:
            c_p.update_coords(t_coords)
            return True

          t_coords = c_p.get_coords()
          moved = False
          while o_p_coords.count([t_coords[0], (t_coords[1] - 1) % self.board_width]) == 0 and t_coords[1] - 1 != 0:
            t_coords = [t_coords[0], (t_coords[1] - 1) % self.board_width]
            moved = True
          
          ot_coords = [(t_coords[0] + direction) % self.board_height, t_coords[1]]
          if o_p_coords.count(ot_coords) >= 1 and moved:
            c_p.update_coords(t_coords)
            return True

          t_coords = c_p.get_coords()
          moved = False
          while o_p_coords.count([t_coords[0], (t_coords[1] + 1) % self.board_width]) == 0 and t_coords[1] + 1 != self.board_width:
            t_coords = [t_coords[0], (t_coords[1] + 1) % self.board_width]
            moved = True
          
          ot_coords = [(t_coords[0] + direction) % self.board_height, t_coords[1]]
          if o_p_coords.count(ot_coords) >= 1 and moved:
            c_p.update_coords(t_coords)
            return True

        elif c_p.get_symbol().strip().lower() == self.game_pieces[2]: #x
          x_coords = [c_p_c[0], (c_p_c[1] - 1) % self.board_width]
          ox_coords = [(c_p_c[0] + direction) % self.board_height, (c_p_c[1] - 1) % self.board_width]
          if o_p_coords.count(x_coords)  == 0 and ox_coords == o_p.get_coords():
            c_p.update_coords(x_coords)
            return True
          
          x_coords = [c_p_c[0], (c_p_c[1] + 1) % self.board_width]
          ox_coords = [(c_p_c[0] + direction) % self.board_height, (c_p_c[1] + 1) % self.board_width]
          if o_p_coords.count(x_coords) == 0 and ox_coords == o_p.get_coords():
            c_p.update_coords(x_coords)
            return True
          
          x_coords = [(c_p_c[0] + direction) % board_height, c_p_c[1]]
          ox_coords = [(c_p_c[0] + 2 * direction) % self.board_height, c_p_c[1] + 1]
          if o_p_coords.count(x_coords) == 0 and ox_coords == o_p.get_coords():
            c_p.update_coords(x_coords)
            return True

      return False




  def ai_move(self, this_player):
    pass
    
    
  
  #     for i in range(cur_player.get_pieces_remaining()):
  #       if piece_select.lower() == cur_player.get_pieces()[i].get_symbol().lower():
  #         self.parse_action(this_player, i)
  #         self.update_board()
  #         return
        
  #     print('Invalid input.')
      
  #   self.turn(this_player)

  # def parse_action(self, this_player, index):
  #   cur_player = self.get_players(this_player)[0]
    
  #   if cur_player.get_pieces()[index].get_symbol().lower() == self.game_pieces[0]:
  #     move_select = input('\t7 or Q for northwest\n\t1 or Z for southwest\n\t3 or C for southeast\n\t9 or E for northeast\n\t5 or S to attack\n')
      
  #     if [str(5), 's', 'S'].count(move_select) > 0:
  #       self.attack(this_player, index)
  #       return
  #     elif ['7', '1', '3', '9', 'q', 'Q', 'z', 'Z', 'c', 'C', 'e', 'E'].count(move_select) > 0:
  #       self.move_o(this_player, move_select, index)
  #       return
  #     else:
  #       print('Inccorrect input, try again!')
  #       self.parse_action(this_player, index)
  #       return

  #   elif cur_player.get_pieces()[index].get_symbol().lower() == self.game_pieces[1]:
  #     move_select = input('\t7 or Q for northwest\n\t1 or Z for southwest\n\t3 or C for southeast\n\t9 or E for northeast\n\t8 or W for north\n\t4 or A for west\n\t2 or X for south\n\t6 or D for east\n\t5 or S to attack\n')
      
  #     if move_select == str(5) or move_select == 's' or move_select == 'S':
  #       self.attack(this_player, index)
  #       return
  #     elif ['7', '1', '3', '9', '8', '4', '2', '6', 'q', 'Q', 'z', 'Z', 'c', 'C', 'e', 'E', 'w', 'W', 'a', 'A', 'x', 'X', 'd', 'D'].count(move_select) > 0:
  #       self.move_t(this_player, move_select, index)
  #       return
  #     else:
  #       print('Inccorrect input, try again!')
  #       self.parse_action(this_player, index)
  #       return
      
  #   elif cur_player.get_pieces()[index].get_symbol().lower() == self.game_pieces[2]:
  #     move_select = input('\t8 or W for north\n\t4 or A for west\n\t2 or X for south\n\t6 or D for east\n\t5 or S to attack\n')
    
  #     if move_select == str(5):
  #       self.attack(this_player, index)
  #       return
  #     elif ['8', '4', '2', '6', 'w', 'W', 'a', 'A', 'x', 'X', 'd', 'D'].count(move_select) > 0:
  #       self.move_x(this_player, move_select, index)
  #       return
  #     else:
  #       print('Inccorrect input, try again!')
  #       self.parse_action(this_player, index)
  #       return
        
  #   print('Inccorrect input, try again!')
  #   self.parse_action(this_player, index)
  #   return

  # def attack(self, this_player, index):
  #   players = self.get_players(this_player)
  #   hit = False
  #   movement = 0
  #   if this_player == 1:
  #     movement = -1
  #   else:
  #     movement = 1
    
  #   cur_player = players[0]
  #   other_player = players[1]
    
  #   cur_piece = cur_player.get_pieces()[index]
  #   cur_piece_coords = cur_piece.get_coords()
  #   opp_pieces = other_player.get_pieces()
    
  #   for piece in other_player.get_pieces():
  #     opp_coords = piece.get_coords()
  #     if cur_piece_coords[0] + movement == opp_coords[0] and cur_piece_coords[1] == opp_coords[1]:
  #       piece.update_hp()
  #       hit = True
        
  #       if piece.get_hp() == 0:
  #         print('Piece ' + piece.get_symbol() + ' is destroyed.')
  #         other_player.remove_pieces()
          
  #     self.update_players(this_player, cur_player, other_player)
  
  #   if not hit:
  #     print('Failed to hit.')
      
      
      
  """
  ---Driver function
  """
  def play_game(self):
    while not (self.p1.get_pieces_remaining() <= 0 or self.p2.get_pieces_remaining() <= 0):
      print('Turns left: ' + str(self.turns_left))
      print()
      self.print_board()
      self.turn(1)
      if self.p2.get_pieces_remaining() == 0:
        print('PLAYER 1 WINS THE GAME')
        return
      
      print()
      self.print_board()
      if not self.is_ai:
        self.turn(2)
      else:
        self.turn_ai()
        
      if self.p1.get_pieces_remaining() == 0:
        print('PLAYER 2 WINS THE GAME')
        return
        
      if self.turns_left > 0:
        self.turns_left -= 1
      else:
        self.damage_all_pieces()
    
    if self.p1.get_pieces_remaining() == 0 and self.p2.get_pieces_remaining() == 0:  
      print('This should never happen... Draws are boring.')
    elif self.p1.get_pieces_remaining() == 0 and self.p2.get_pieces_remaining() > 0:
      print('PLAYER 2 WINS THE GAME')
    elif self.p1.get_pieces_remaining() > 0 and self.p2.get_pieces_remaining() == 0:
      print('PLAYER 1 WINS THE GAME')
    else:
      print('WHO KNOWS?')



bg = board_game()
bg.play_game()