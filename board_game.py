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
    print('A move happened for ' + self.symbol)
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
    
    self.players = [self.p1, self.p2]
    
    self.turns_left = 20

    self.update_board()
  
  
  def turn(self, this_player):
    cur_player = self.players[this_player - 1]
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
      return False
    elif piece_select.strip().lower() == 'hp':
      self.display_hp()
      return False
    elif piece_select.strip().lower() == 'board':
      self.print_board()
      return False
    elif piece_select.strip().lower() == 'skip':
      return True
    else:
      for i in range(cur_player.get_pieces_remaining()):
        if piece_select.lower() == cur_player.get_pieces()[i].get_symbol().lower():
          return self.parse_action(this_player, i)
                            
      print('Invalid input.')
      
    return False
    
    
  def parse_action(self, this_player, index):
    cur_player = self.players[this_player - 1]
    if cur_player.get_pieces()[index].get_symbol().lower() == self.game_pieces[0]:
      move_select = input('\t7 or Q for northwest\n\t1 or Z for southwest\n\t3 or C for southeast\n\t9 or E for northeast\n\t5 or S to attack\n')
      
      if [str(5), 's', 'S'].count(move_select) > 0:
        return self.attack(this_player, index)
      elif ['7', '1', '3', '9', 'q', 'Q', 'z', 'Z', 'c', 'C', 'e', 'E'].count(move_select) > 0:
        return self.move_x(this_player, move_select, index)
      else:
        print('Inccorrect input, try again!')
        return False 

    elif cur_player.get_pieces()[index].get_symbol().lower() == self.game_pieces[1]:
      move_select = input('\t7 or Q for northwest\n\t1 or Z for southwest\n\t3 or C for southeast\n\t9 or E for northeast\n\t8 or W for north\n\t4 or A for west\n\t2 or X for south\n\t6 or D for east\n\t5 or S to attack\n')
      
      if [str(5), 's', 'S'].count(move_select) > 0:
        return self.attack(this_player, index)
      elif ['7', '1', '3', '9', '8', '4', '2', '6', 'q', 'Q', 'z', 'Z', 'c', 'C', 'e', 'E', 'w', 'W', 'a', 'A', 'x', 'X', 'd', 'D'].count(move_select) > 0:
        return self.move_t(this_player, move_select, index)
      else:
        print('Inccorrect input, try again!')
        return False
      
    elif cur_player.get_pieces()[index].get_symbol().lower() == self.game_pieces[2]:
      move_select = input('\t8 or W for north\n\t4 or A for west\n\t2 or X for south\n\t6 or D for east\n\t5 or S to attack\n')
    
      if [str(5), 's', 'S'].count(move_select) > 0:
        return self.attack(this_player, index)
      elif ['8', '4', '2', '6', 'w', 'W', 'a', 'A', 'x', 'X', 'd', 'D'].count(move_select) > 0:
        return self.move_o(this_player, move_select, index)
      else:
        print('Inccorrect input, try again!')
        return False
        
    print('Inccorrect input, try again!')
    return False
    
    
    
  """
  --Attack Function
  """
  def attack(self, this_player, index):
    hit = False
    movement = 0
    if this_player == 1:
      movement = -1
    else:
      movement = 1
    
    other_player = self.players[this_player % 2]
    
    cur_piece = self.players[this_player - 1].get_pieces()[index]
    cur_piece_coords = cur_piece.get_coords()[:]
    opp_pieces = other_player.get_pieces()
    
    for p in opp_pieces:
      opp_coords = p.get_coords()[:]
      if cur_piece_coords[0] + movement == opp_coords[0] and cur_piece_coords[1] == opp_coords[1]:
        p.update_hp()
        hit = True
        
        if p.get_hp() == 0:
          print('Piece ' + p.get_symbol() + ' is destroyed.')
          other_player.remove_pieces()
  
    if not hit:
      print('Failed to hit.')
  
    return hit
  
  """
  ---Movement rules
  """
  def move_x(self, this_player, direction, index):
    if direction == '7' or direction.lower() == 'q':
      return self.move_nw(this_player, index)
    elif direction == '1' or direction.lower() == 'z':
      return self.move_sw(this_player, index)
    elif direction == '3' or direction.lower() == 'c':
      return self.move_se(this_player, index)
    elif direction == '9' or direction.lower() == 'e':
      return self.move_ne(this_player, index)
    else:
      print('Incorrect input choice. Try again.')
      return False
    
    
  def move_t(self, this_player, direction, index):
    if direction == '7' or direction.lower() == 'q':
      return self.move_nw(this_player, index, True)
    elif direction == '1' or direction.lower() == 'z':
      return self.move_sw(this_player, index, True)
    elif direction == '3' or direction.lower() == 'c':
      return self.move_se(this_player, index, True)
    elif direction == '9' or direction.lower() == 'e':
      return self.move_ne(this_player, index, True)
    elif direction == '8' or direction.lower() == 'w':
      return self.move_n(this_player, index, True)
    elif direction == '4' or direction.lower() == 'a':
      return self.move_w(this_player, index, True)
    elif direction == '2' or direction.lower() == 'x':
      return self.move_s(this_player, index, True)
    elif direction == '6' or direction.lower() == 'd':
      return self.move_e(this_player, index, True)
    else:
      print('Incorrect input choice. Try again.')
      return False
      
      
  def move_o(self, this_player, direction, index):
    if direction == '8' or direction.lower() == 'w':
      return self.move_n(this_player, index)
    elif direction == '4' or direction.lower() == 'a':
      return self.move_w(this_player, index)
    elif direction == '2' or direction.lower() == 'x':
      return self.move_s(this_player, index)
    elif direction == '6' or direction.lower() == 'd':
      return self.move_e(this_player, index)
    else:
      print('Incorrect input choice. Try again.')
      return False
    
    
  """
  --Directional functions
  """
  def move_nw(self, this_player, index, multimove = False):
    cur_piece_coords = self.players[this_player - 1].get_pieces()[index].get_coords()[:]
    opp_pieces = self.players[this_player % 2].get_pieces()
    new_coords = [(cur_piece_coords[0] - 1) % self.board_height, (cur_piece_coords[1] - 1) % self.board_width]
    cur_player = self.players[this_player - 1]
    
    for p in opp_pieces:
      if p.get_coords()[0] == new_coords[0] and p.get_coords()[1] == new_coords[1]:
        print('Error: blocked by opponent.')
        return False
    
    while (multimove and new_coords[0] - 1 >= 0 and new_coords[1] - 1 >= 0):
      for p in opp_pieces:
        if p.get_coords()[0] == new_coords[0] - 1 and p.get_coords()[1] == new_coords[1] - 1:
          cur_player.get_pieces()[index].update_coords(new_coords)
          return True
        
      new_coords = [(new_coords[0] - 1) % self.board_height, (new_coords[1] - 1) % self.board_width]
      
    cur_player.get_pieces()[index].update_coords(new_coords)
    return True
    
    
  def move_sw(self, this_player, index, multimove = False):
    cur_piece_coords = self.players[this_player - 1].get_pieces()[index].get_coords()[:]
    opp_pieces = self.players[this_player % 2].get_pieces()
    new_coords = [(cur_piece_coords[0] + 1) % self.board_height, (cur_piece_coords[1] - 1) % self.board_width]
    cur_player = self.players[this_player - 1]
    
    for p in opp_pieces:
      if p.get_coords()[0] == new_coords[0] and p.get_coords()[1] == new_coords[1]:
        print('Error: blocked by opponent.')
        return False
    
    while (multimove and new_coords[0] + 1 < self.board_height and new_coords[1] - 1 >= 0):
      for p in opp_pieces:
        if p.get_coords()[0] == new_coords[0] + 1 and p.get_coords()[1] == new_coords[1] - 1:
          cur_player.get_pieces()[index].update_coords(new_coords)
          return True
        
      new_coords = [(new_coords[0] + 1) % self.board_height, (new_coords[1] - 1) % self.board_width]
      
    cur_player.get_pieces()[index].update_coords(new_coords)
    return True
  
  
  def move_se(self, this_player, index, multimove = False):
    cur_piece_coords = self.players[this_player - 1].get_pieces()[index].get_coords()[:]
    opp_pieces = self.players[this_player % 2].get_pieces()
    new_coords = [(cur_piece_coords[0] + 1) % self.board_height, (cur_piece_coords[1] + 1) % self.board_width]
    cur_player = self.players[this_player - 1]
    
    for p in opp_pieces:
      if p.get_coords()[0] == new_coords[0] and p.get_coords()[1] == new_coords[1]:
        print('Error: blocked by opponent.')
        return False
    
    while (multimove and new_coords[0] + 1 < self.board_height and new_coords[1] + 1 < self.board_width):
      for p in opp_pieces:
        if p.get_coords()[0] == new_coords[0] + 1 and p.get_coords()[1] == new_coords[1] + 1:
          cur_player.get_pieces()[index].update_coords(new_coords)
          return True
        
      new_coords = [(new_coords[0] + 1) % self.board_height, (new_coords[1] + 1) % self.board_width]

    cur_player.get_pieces()[index].update_coords(new_coords)
    return True
    
    
  def move_ne(self, this_player, index, multimove = False):
    cur_piece_coords = self.players[this_player - 1].get_pieces()[index].get_coords()[:]
    opp_pieces = self.players[this_player % 2].get_pieces()
    new_coords = [(cur_piece_coords[0] - 1) % self.board_height, (cur_piece_coords[1] + 1) % self.board_width]
    cur_player = self.players[this_player - 1]
    
    for p in opp_pieces:
      if p.get_coords()[0] == new_coords[0] and p.get_coords()[1] == new_coords[1]:
        print('Error: blocked by opponent.')
        return False
    
    while (multimove and new_coords[0] - 1 >= 0 and new_coords[1] + 1 < self.board_width):
      for p in opp_pieces:
        if p.get_coords()[0] == new_coords[0] - 1 and p.get_coords()[1] == new_coords[1] + 1:
          cur_player.get_pieces()[index].update_coords(new_coords)
          return True
        
      new_coords = [(new_coords[0] - 1) % self.board_height, (new_coords[1] + 1) % self.board_width]
      
    cur_player.get_pieces()[index].update_coords(new_coords)
    return True
    
    
  def move_n(self, this_player, index, multimove = False):
    cur_piece_coords = self.players[this_player - 1].get_pieces()[index].get_coords()[:]
    opp_pieces = self.players[this_player % 2].get_pieces()
    cur_player = self.players[this_player - 1]
    new_coords = [(cur_piece_coords[0]  - 1) % self.board_height, (cur_piece_coords[1]) % self.board_width]
    
    for p in opp_pieces:
      if p.get_coords()[0] == new_coords[0] and p.get_coords()[1] == new_coords[1]:
        print('Error: blocked by opponent.')
        return False
    
    while (multimove and new_coords[0] - 1 >= 0):
      for p in opp_pieces:
        if p.get_coords()[0] == new_coords[0] - 1 and p.get_coords()[1] == new_coords[1]:
          cur_player.get_pieces()[index].update_coords(new_coords)
          return True
        
      new_coords[0] = (new_coords[0] - 1) % self.board_height
      
    cur_player.get_pieces()[index].update_coords(new_coords)
    return True
    
    
  def move_w(self, this_player, index, multimove = False):
    cur_piece_coords = self.players[this_player - 1].get_pieces()[index].get_coords()[:]
    opp_pieces = self.players[this_player % 2].get_pieces()
    cur_player = self.players[this_player - 1]
    new_coords = [(cur_piece_coords[0]) % self.board_height, (cur_piece_coords[1] - 1) % self.board_width]
    
    for p in opp_pieces:
      if p.get_coords()[0] == new_coords[0] and p.get_coords()[1] == new_coords[1]:
        print('Error: blocked by opponent.')
        return False
    
    while (multimove and new_coords[1] - 1 >= 0):
      for p in opp_pieces:
        if p.get_coords()[0] == new_coords[0] and p.get_coords()[1] == new_coords[1] - 1:
          cur_player.get_pieces()[index].update_coords(new_coords)
          return True
        
      new_coords[1] = (new_coords[1] - 1) % self.board_width
      
    cur_player.get_pieces()[index].update_coords(new_coords)
    return True
    
    
  def move_s(self, this_player, index, multimove = False):
    cur_piece_coords = self.players[this_player - 1].get_pieces()[index].get_coords()[:]
    opp_pieces = self.players[this_player % 2].get_pieces()
    cur_player = self.players[this_player - 1]
    new_coords = [(cur_piece_coords[0] + 1) % self.board_height, (cur_piece_coords[1]) % self.board_width]
    
    for p in opp_pieces:
      if p.get_coords()[0] == new_coords[0] and p.get_coords()[1] == new_coords[1]:
        print('Error: blocked by opponent.')
        return False
      
    while (multimove and new_coords[0] + 1 < self.board_height):
      for p in opp_pieces:
        if p.get_coords()[0] == new_coords[0] + 1 and p.get_coords()[1] == new_coords[1]:
          cur_player.get_pieces()[index].update_coords(new_coords)
          return True
        
      new_coords[0] = (new_coords[0] + 1) % self.board_height
      
    cur_player.get_pieces()[index].update_coords(new_coords)
    return True
    
    
  def move_e(self, this_player, index, multimove = False):
    cur_piece_coords = self.players[this_player - 1].get_pieces()[index].get_coords()[:]
    opp_pieces = self.players[this_player % 2].get_pieces()
    cur_player = self.players[this_player - 1]
    new_coords = [(cur_piece_coords[0]) % self.board_height, (cur_piece_coords[1] + 1) % self.board_width]
    
    for p in opp_pieces:
      if p.get_coords()[0] == new_coords[0] and p.get_coords()[1] == new_coords[1]:
        print('Error: blocked by opponent.')
        return False
      
    while (multimove and new_coords[1] + 1 < self.board_width):
      for p in opp_pieces:
        if p.get_coords()[0] == new_coords[0] and p.get_coords()[1] == new_coords[1] + 1:
          cur_player.get_pieces()[index].update_coords(new_coords)
          return True
        
      new_coords[1] = (new_coords[1] + 1) % self.board_width
      
    cur_player.get_pieces()[index].update_coords(new_coords)
    return True
  
  
  """
  ---Helper functions
  """
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
      hp_str += '\t  ' + cur_piece.get_symbol() + ' located at: ' + str(cur_piece.get_coords()[:]) + '\n'
    
    hp_str += '\nPlayer 2 HP:\n'
    for i in range(self.p2.get_pieces_remaining()):
      cur_piece = self.p2.get_pieces()[i]
      hp_str += '\t' + cur_piece.get_symbol() + ' has ' + str(cur_piece.get_hp()) + ' remaining.\n'
      hp_str += '\t  ' + cur_piece.get_symbol() + ' located at: ' + str(cur_piece.get_coords()[:]) + '\n'
    
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
    for p in self.p1.get_pieces():
      p.update_hp()
    
    for p in self.p2.get_pieces():
      p.update_hp()
      
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
      return True
    elif self.ai_move_to_attack(this_player):
      print(plyr_str + ' moved to attack position!')
      return True
    elif self.ai_move(this_player):
      return True

    return False
    

  def ai_attack(self, this_player):
    print('AI planning to attack')
    cur_player = self.players[this_player - 1]
    other_player = self.players[this_player % 2]

    if this_player == 1:
      direction = -1
    else:
      direction = 1

    dfndr = None
    for i in range(cur_player.get_pieces_remaining()):
      cur_piece_attk_coords = cur_player.get_pieces()[i].get_coords()[:]
      cur_piece_attk_coords[0] = (cur_piece_attk_coords[0] + direction) % self.board_height
      for j in range(other_player.get_pieces_remaining()):
        if other_player.get_pieces()[j].get_coords()[:] == cur_piece_attk_coords \
          and (dfndr is None or other_player.get_pieces()[j].get_hp() < other_player.get_pieces()[dfndr].get_hp()):
          dfndr = j

    if dfndr is not None:
      other_player.get_pieces()[dfndr].update_hp()
      other_player.remove_pieces()
      print('AI Did attack')
      return True

    return False


  def ai_move_to_attack(self, this_player):
    print('AI Did Not Attack. AI Will Attempt Attack Formation')
    cur_player = self.players[this_player - 1]
    other_player = self.players[this_player % 2]

    if this_player == 1:
      direction = -1
    else:
      direction = 1

    o_p_coords = []
    for o_p in other_player.get_pieces():
      o_p_coords.append(o_p.get_coords()[:])

    for c_p in cur_player.get_pieces():
      c_p_c = c_p.get_coords()[:]
      for o_p in other_player.get_pieces():
        if c_p.get_symbol().strip().lower() == self.game_pieces[0]: #x
          #nw/sw
          x_coords = [(c_p_c[0] + direction) % self.board_height, (c_p_c[1] - 1) % self.board_width]
          ox_coords = [(c_p_c[0] + 2 * direction) % self.board_height, (c_p_c[1] - 1) % self.board_width]
          if o_p_coords.count(x_coords) == 0 and ox_coords == o_p.get_coords()[:]:
            c_p.update_coords(x_coords)
            print ('AI-x moved nw/sw to attack position')
            return True
          
          #ne/se
          x_coords = [(c_p_c[0] + direction) % self.board_height, (c_p_c[1] + 1) % self.board_width]
          ox_coords = [(c_p_c[0] + 2 * direction) % self.board_height, (c_p_c[1] + 1) % self.board_width]
          if o_p_coords.count(x_coords) == 0 and ox_coords == o_p.get_coords()[:]:
            c_p.update_coords(x_coords)
            print ('AI-x moved ne/se to attack position')
            return True

        elif c_p.get_symbol().strip().lower() == self.game_pieces[1]: #t
          #nw/sw
          t_coords = c_p.get_coords()[:]
          moved = False
          while o_p_coords.count([(t_coords[0] + direction) % self.board_height, (t_coords[1] - 1) % self.board_width]) == 0 \
            and t_coords[0] + direction != self.board_height \
            and t_coords[0] + direction != 0 \
            and  t_coords[1] - 1 != 0:
            t_coords = [(t_coords[0] + direction) % self.board_height, (t_coords[1] - 1) % self.board_width]
            moved = True
          
          ot_coords = [(t_coords[0] + direction) % self.board_height, t_coords[1]]
          if o_p_coords.count(ot_coords) >= 1 and moved:
            c_p.update_coords(t_coords)
            print ('AI-t moved nw/sw to attack position')
            return True
          
          #ne/se
          t_coords = c_p.get_coords()[:]
          moved = False
          while o_p_coords.count([(t_coords[0] + direction) % self.board_height, (t_coords[1] + 1) % self.board_width]) == 0 \
            and t_coords[0] + direction != self.board_height \
            and t_coords[0] + direction != 0 \
            and  t_coords[1] + 1 != self.board_width:
            t_coords = [(t_coords[0] + direction) % self.board_height, (t_coords[1] + 1) % self.board_width]
            moved = True
          
          ot_coords = [(t_coords[0] + direction) % self.board_height, t_coords[1]]
          if o_p_coords.count(ot_coords) >= 1 and moved:
            c_p.update_coords(t_coords)
            print ('AI-t moved ne/se to attack position')
            return True

          #n/s
          t_coords = c_p.get_coords()[:]
          moved = False
          while o_p_coords.count([(t_coords[0] + direction) % self.board_height, t_coords[1]]) == 0 \
            and t_coords[0] + direction != self.board_height \
            and t_coords[0] + direction != 0:
            t_coords = [(t_coords[0] + direction) % self.board_height, t_coords[1]]
            moved = True

          ot_coords = [(t_coords[0] + direction) % self.board_height, t_coords[1]]
          if o_p_coords.count(ot_coords) >= 1 and moved:
            c_p.update_coords(t_coords)
            print ('AI-t moved n/s to attack position')
            return True
          
          #w
          t_coords = c_p.get_coords()[:]
          moved = False
          while o_p_coords.count([t_coords[0], (t_coords[1] - 1) % self.board_width]) == 0 \
            and t_coords[1] - 1 != 0:
            t_coords = [t_coords[0], (t_coords[1] - 1) % self.board_width]
            moved = True
          
          ot_coords = [(t_coords[0] + direction) % self.board_height, t_coords[1]]
          if o_p_coords.count(ot_coords) >= 1 and moved:
            c_p.update_coords(t_coords)
            print ('AI-t moved w to attack position')
            return True
          
          #e
          t_coords = c_p.get_coords()[:]
          moved = False
          while o_p_coords.count([t_coords[0], (t_coords[1] + 1) % self.board_width]) == 0 \
            and t_coords[1] + 1 != self.board_width:
            t_coords = [t_coords[0], (t_coords[1] + 1) % self.board_width]
            moved = True
          
          ot_coords = [(t_coords[0] + direction) % self.board_height, t_coords[1]]
          if o_p_coords.count(ot_coords) >= 1 and moved:
            c_p.update_coords(t_coords)
            print ('AI-t moved e to attack position')
            return True

        elif c_p.get_symbol().strip().lower() == self.game_pieces[2]: #o
          #w
          o_coords = [c_p_c[0], (c_p_c[1] - 1) % self.board_width]
          oo_coords = [(c_p_c[0] + direction) % self.board_height, (c_p_c[1] - 1) % self.board_width]
          if o_p_coords.count(o_coords)  == 0 and oo_coords == o_p.get_coords()[:]:
            c_p.update_coords(o_coords)
            print ('AI-o moved w to attack position')
            return True
          
          #e
          o_coords = [c_p_c[0], (c_p_c[1] + 1) % self.board_width]
          oo_coords = [(c_p_c[0] + direction) % self.board_height, (c_p_c[1] + 1) % self.board_width]
          if o_p_coords.count(o_coords) == 0 and oo_coords == o_p.get_coords()[:]:
            c_p.update_coords(o_coords)
            print ('AI-o moved e to attack position')
            return True
          
          #n/s
          o_coords = [(c_p_c[0] + direction) % self.board_height, c_p_c[1]]
          oo_coords = [(c_p_c[0] + 2 * direction) % self.board_height, c_p_c[1] + 1]
          if o_p_coords.count(o_coords) == 0 and oo_coords == o_p.get_coords()[:]:
            c_p.update_coords(o_coords)
            print ('AI-o moved n/s to attack position')
            return True

      return False



  def ai_move(self, this_player):
    print('Nothing to attack, AI will just move someone.')
    piece_to_move = randint(0, 2)

    if self.game_pieces[piece_to_move] == 'o':
      direction = randint(0, 3)

      if direction == 0:
        print('AI-o moved n')
        return self.move_n(this_player, piece_to_move)
      elif direction == 1:
        print('AI-o moved w')
        return self.move_w(this_player, piece_to_move)
      elif direction == 2:
        print('AI-o moved s')
        return self.move_s(this_player, piece_to_move)
      elif direction == 3:
        print('AI-o moved e')
        return self.move_e(this_player, piece_to_move)

    elif self.game_pieces[piece_to_move] == 't':
      direction = randint(0, 7)

      if direction == 0:
        print('AI-t moved n')
        return self.move_n(this_player, piece_to_move, True)
      elif direction == 1:
        print('AI-t moved w')
        return self.move_w(this_player, piece_to_move, True)
      elif direction == 2:
        print('AI-t moved s')
        return self.move_s(this_player, piece_to_move, True)
      elif direction == 3:
        print('AI-t moved e')
        return self.move_e(this_player, piece_to_move, True)
      elif direction == 4:
        print('AI-t moved nw')
        return self.move_nw(this_player, piece_to_move, True)
      elif direction == 5:
        print('AI-t moved ne')
        return self.move_ne(this_player, piece_to_move, True)
      elif direction == 6:
        print('AI-t moved sw')
        return self.move_sw(this_player, piece_to_move, True)
      elif direction == 7:
        print('AI-t moved se')
        return self.move_se(this_player, piece_to_move, True)

    elif self.game_pieces[piece_to_move] == 'x':
      direction = randint(0, 3)

      if direction == 0:
        print('AI-x moved nw')
        return self.move_nw(this_player, piece_to_move)
      elif direction == 1:
        print('AI-x moved ne')
        return self.move_ne(this_player, piece_to_move)
      elif direction == 2:
        print('AI-x moved sw')
        return self.move_sw(this_player, piece_to_move)
      elif direction == 3:
        print('AI-x moved se')
        return self.move_se(this_player, piece_to_move)

    else:
      return False
    
      
  """
  ---Driver function
  """
  def play_game(self):
    while not (self.p1.get_pieces_remaining() <= 0 or self.p2.get_pieces_remaining() <= 0):
      print('Turns left: ' + str(self.turns_left))
      print()
      self.print_board()
      while self.turn(1) == False:
        pass
      if self.p2.get_pieces_remaining() == 0:
        print('PLAYER 1 WINS THE GAME')
        return
        
      self.update_board()
      
      print()
      self.print_board()
      if not self.is_ai:
        while self.turn(2) == False:
          pass
      else:
        while self.turn_ai(2) == False:
          pass
      
      self.update_board()
        
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


bg = board_game(True)
bg.play_game()