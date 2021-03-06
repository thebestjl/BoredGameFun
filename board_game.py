#TODO: Allow both players to both move and attack in the same turn.
#   x is only piece that can both move and attack

#TODO: Allow customizable piece selection and placement.

#TODO: Allow varied board sizes.

#TODO: Add randomly varying attack strength. Will require larger health pools.

from random import randint



class player():
  def __init__(self, pieces):
    self.pieces = pieces


  def get_pieces(self):
    return self.pieces


  def get_pieces_remaining(self):
    return len(self.pieces)


  def remove_pieces(self):
    for p in self.pieces:
      if p.get_hp() == 0:
        index = self.pieces.index(p)
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
    self.__mute = False
    self.__is_ai = is_ai
    
    if height != None:
      self.__board_height = height
    else:
      self.__board_height = 5
      
    if width < 3:
      self.__board_width = 5
    else:
      self.__board_width = width
      
    self.__board = []
    self.__game_pieces = ['x', 't', 'o']
    p1_x = piece(self.__game_pieces[0], 2, [self.__board_height - 1, 1])
    p1_t = piece(self.__game_pieces[1], 4, [self.__board_height - 1, 2])
    p1_o = piece(self.__game_pieces[2], 3, [self.__board_height - 1, 3])
    p1 = player([p1_x, p1_t, p1_o])
    
    p2_x = piece(self.__game_pieces[0].upper(), 2, [0, 3])
    p2_t = piece(self.__game_pieces[1].upper(), 4, [0, 2])
    p2_o = piece(self.__game_pieces[2].upper(), 3, [0, 1])
    p2 = player([p2_x, p2_t, p2_o])
    
    self.__players = [p1, p2]
    self.__turns_left = 20
    self.__update_board()


  def __turn(self, this_player):
    bk = False
    while not bk:
      cur_player = self.__players[this_player - 1]
      if this_player == 1:
        self.__report('Player 1:')
      else:
        self.__report('Player 2:')
        
      piece_select_str = 'Choose your move by typing the piece''s symbol or type ''help'': '
      for i in range(cur_player.get_pieces_remaining()):
        piece_select_str += '\n\t' + cur_player.get_pieces()[i].get_symbol()
      
      piece_select_str += ':\n'
      piece_select = input(piece_select_str)
      
      if piece_select.strip().lower() == 'help':
        help_str = 'Press the index assigned to select a piece or perform the action, type ''hp'' to see the hp for each piece, ''skip'' to skip your turn, or type ''board'' to display the board.'
        self.__report(help_str)
      elif piece_select.strip().lower() == 'hp':
        self.__display_hp()
      elif piece_select.strip().lower() == 'board':
        self.__print_board()
      elif piece_select.strip().lower() == 'skip':
        bk = True
      else:
        for i in range(cur_player.get_pieces_remaining()):
          if piece_select.lower() == cur_player.get_pieces()[i].get_symbol().lower():
            if self.__parse_action(this_player, i):
              bk = True
              break
                              
        self.__report('Invalid input.')


  def __parse_action(self, this_player, index):
    cur_player = self.__players[this_player - 1]
    ret_bool = False
    
    if cur_player.get_pieces()[index].get_symbol().lower() == self.__game_pieces[0]:
      move_select = input('\t7 or Q for northwest\n\t1 or Z for southwest\n\t3 or C for southeast\n\t9 or E for northeast\n\t5 or S to attack\n')
      
      if [str(5), 's', 'S'].count(move_select) > 0:
        ret_bool = self.__attack(this_player, index)
      elif ['7', '1', '3', '9', 'q', 'Q', 'z', 'Z', 'c', 'C', 'e', 'E'].count(move_select) > 0:
        ret_bool = self.__move_x(this_player, move_select, index)

    elif cur_player.get_pieces()[index].get_symbol().lower() == self.__game_pieces[1]:
      move_select = input('\t7 or Q for northwest\n\t1 or Z for southwest\n\t3 or C for southeast\n\t9 ' \
        + 'or E for northeast\n\t8 or W for north\n\t4 or A for west\n\t2 or X for south\n\t6 or D for east\n\t5 or S to attack\n')
      
      if [str(5), 's', 'S'].count(move_select) > 0:
        ret_bool = self.__attack(this_player, index)
      elif ['7', '1', '3', '9', '8', '4', '2', '6', 'q', 'Q', 'z', 'Z', 'c', 'C', 'e', 'E', 'w', 'W', 'a', 'A', 'x', 'X', 'd', 'D'].count(move_select) > 0:
        ret_bool = self.__move_t(this_player, move_select, index)
      
    elif cur_player.get_pieces()[index].get_symbol().lower() == self.__game_pieces[2]:
      move_select = input('\t8 or W for north\n\t4 or A for west\n\t2 or X for south\n\t6 or D for east\n\t5 or S to attack\n')
    
      if [str(5), 's', 'S'].count(move_select) > 0:
        ret_bool = self.__attack(this_player, index)
      elif ['8', '4', '2', '6', 'w', 'W', 'a', 'A', 'x', 'X', 'd', 'D'].count(move_select) > 0:
        ret_bool = self.__move_o(this_player, move_select, index)
        
    self.__report('Inccorrect input, try again!')
    return ret_bool


  #Attack Function
  def __attack(self, this_player, index):
    hit = False
    direction = (-1) ** this_player
    other_player = self.__players[this_player % 2]
    
    cur_piece = self.__players[this_player - 1].get_pieces()[index]
    cur_piece_coords = cur_piece.get_coords()[:]
    opp_pieces = other_player.get_pieces()
    
    for p in opp_pieces:
      opp_coords = p.get_coords()[:]
      if cur_piece_coords[0] + direction == opp_coords[0] and cur_piece_coords[1] == opp_coords[1]:
        p.update_hp()
        hit = True
        
        if p.get_hp() == 0:
          self.__report('Piece ' + p.get_symbol() + ' is destroyed.')
          other_player.remove_pieces()
    
    if not hit:
      self.__report('Failed to hit.')
    
    return hit


  #Movement rules
  def __move_x(self, this_player, direction, index):
    if direction == '7' or direction.lower() == 'q':
      return self.__move_nw(this_player, index)
    elif direction == '1' or direction.lower() == 'z':
      return self.__move_sw(this_player, index)
    elif direction == '3' or direction.lower() == 'c':
      return self.__move_se(this_player, index)
    elif direction == '9' or direction.lower() == 'e':
      return self.__move_ne(this_player, index)
    else:
      self.__report('Incorrect input choice. Try again.')
      return False


  def __move_t(self, this_player, direction, index):
    ret_bool = False
    if direction == '7' or direction.lower() == 'q':
      ret_bool = self.__move_nw(this_player, index, True)
    elif direction == '1' or direction.lower() == 'z':
      ret_bool = self.__move_sw(this_player, index, True)
    elif direction == '3' or direction.lower() == 'c':
      ret_bool = self.__move_se(this_player, index, True)
    elif direction == '9' or direction.lower() == 'e':
      ret_bool = self.__move_ne(this_player, index, True)
    elif direction == '8' or direction.lower() == 'w':
      ret_bool = self.__move_n(this_player, index, True)
    elif direction == '4' or direction.lower() == 'a':
      ret_bool = self.__move_w(this_player, index, True)
    elif direction == '2' or direction.lower() == 'x':
      ret_bool = self.__move_s(this_player, index, True)
    elif direction == '6' or direction.lower() == 'd':
      ret_bool = self.__move_e(this_player, index, True)
    else:
      self.__report('Incorrect input choice. Try again.')
    
    return ret_bool


  def __move_o(self, this_player, direction, index):
    if direction == '8' or direction.lower() == 'w':
      return self.__move_n(this_player, index)
    elif direction == '4' or direction.lower() == 'a':
      return self.__move_w(this_player, index)
    elif direction == '2' or direction.lower() == 'x':
      return self.__move_s(this_player, index)
    elif direction == '6' or direction.lower() == 'd':
      return self.__move_e(this_player, index)
    else:
      self.__report('Incorrect input choice. Try again.')
      return False


  #Directional functions
  def __move_nw(self, this_player, index, multimove = False):
    cur_piece_coords = self.__players[this_player - 1].get_pieces()[index].get_coords()[:]
    opp_pieces = self.__players[this_player % 2].get_pieces()
    new_coords = [(cur_piece_coords[0] - 1) % self.__board_height, (cur_piece_coords[1] - 1) % self.__board_width]
    cur_player = self.__players[this_player - 1]
    
    for p in opp_pieces:
      if p.get_coords()[0] == new_coords[0] and p.get_coords()[1] == new_coords[1]:
        self.__report('Error: blocked by opponent.')
        return False
    
    while (multimove and new_coords[0] - 1 >= 0 and new_coords[1] - 1 >= 0):
      for p in opp_pieces:
        if p.get_coords()[0] == new_coords[0] - 1 and p.get_coords()[1] == new_coords[1] - 1:
          cur_player.get_pieces()[index].update_coords(new_coords)
          return True
        
      new_coords = [(new_coords[0] - 1) % self.__board_height, (new_coords[1] - 1) % self.__board_width]
      
    cur_player.get_pieces()[index].update_coords(new_coords)
    return True


  def __move_sw(self, this_player, index, multimove = False):
    cur_piece_coords = self.__players[this_player - 1].get_pieces()[index].get_coords()[:]
    opp_pieces = self.__players[this_player % 2].get_pieces()
    new_coords = [(cur_piece_coords[0] + 1) % self.__board_height, (cur_piece_coords[1] - 1) % self.__board_width]
    cur_player = self.__players[this_player - 1]
    
    for p in opp_pieces:
      if p.get_coords()[0] == new_coords[0] and p.get_coords()[1] == new_coords[1]:
        self.__report('Error: blocked by opponent.')
        return False
    
    while (multimove and new_coords[0] + 1 < self.__board_height and new_coords[1] - 1 >= 0):
      for p in opp_pieces:
        if p.get_coords()[0] == new_coords[0] + 1 and p.get_coords()[1] == new_coords[1] - 1:
          cur_player.get_pieces()[index].update_coords(new_coords)
          return True
        
      new_coords = [(new_coords[0] + 1) % self.__board_height, (new_coords[1] - 1) % self.__board_width]
      
    cur_player.get_pieces()[index].update_coords(new_coords)
    return True
  
  
  def __move_se(self, this_player, index, multimove = False):
    cur_piece_coords = self.__players[this_player - 1].get_pieces()[index].get_coords()[:]
    opp_pieces = self.__players[this_player % 2].get_pieces()
    new_coords = [(cur_piece_coords[0] + 1) % self.__board_height, (cur_piece_coords[1] + 1) % self.__board_width]
    cur_player = self.__players[this_player - 1]
    
    for p in opp_pieces:
      if p.get_coords()[0] == new_coords[0] and p.get_coords()[1] == new_coords[1]:
        self.__report('Error: blocked by opponent.')
        return False
    
    while (multimove and new_coords[0] + 1 < self.__board_height and new_coords[1] + 1 < self.__board_width):
      for p in opp_pieces:
        if p.get_coords()[0] == new_coords[0] + 1 and p.get_coords()[1] == new_coords[1] + 1:
          cur_player.get_pieces()[index].update_coords(new_coords)
          return True
        
      new_coords = [(new_coords[0] + 1) % self.__board_height, (new_coords[1] + 1) % self.__board_width]

    cur_player.get_pieces()[index].update_coords(new_coords)
    return True


  def __move_ne(self, this_player, index, multimove = False):
    cur_piece_coords = self.__players[this_player - 1].get_pieces()[index].get_coords()[:]
    opp_pieces = self.__players[this_player % 2].get_pieces()
    new_coords = [(cur_piece_coords[0] - 1) % self.__board_height, (cur_piece_coords[1] + 1) % self.__board_width]
    cur_player = self.__players[this_player - 1]
    
    for p in opp_pieces:
      if p.get_coords()[0] == new_coords[0] and p.get_coords()[1] == new_coords[1]:
        self.__report('Error: blocked by opponent.')
        return False
    
    while (multimove and new_coords[0] - 1 >= 0 and new_coords[1] + 1 < self.__board_width):
      for p in opp_pieces:
        if p.get_coords()[0] == new_coords[0] - 1 and p.get_coords()[1] == new_coords[1] + 1:
          cur_player.get_pieces()[index].update_coords(new_coords)
          return True
        
      new_coords = [(new_coords[0] - 1) % self.__board_height, (new_coords[1] + 1) % self.__board_width]
      
    cur_player.get_pieces()[index].update_coords(new_coords)
    return True


  def __move_n(self, this_player, index, multimove = False):
    cur_piece_coords = self.__players[this_player - 1].get_pieces()[index].get_coords()[:]
    opp_pieces = self.__players[this_player % 2].get_pieces()
    cur_player = self.__players[this_player - 1]
    new_coords = [(cur_piece_coords[0]  - 1) % self.__board_height, (cur_piece_coords[1]) % self.__board_width]
    
    for p in opp_pieces:
      if p.get_coords()[0] == new_coords[0] and p.get_coords()[1] == new_coords[1]:
        self.__report('Error: blocked by opponent.')
        return False
    
    while (multimove and new_coords[0] - 1 >= 0):
      for p in opp_pieces:
        if p.get_coords()[0] == new_coords[0] - 1 and p.get_coords()[1] == new_coords[1]:
          cur_player.get_pieces()[index].update_coords(new_coords)
          return True
        
      new_coords[0] = (new_coords[0] - 1) % self.__board_height
      
    cur_player.get_pieces()[index].update_coords(new_coords)
    return True


  def __move_w(self, this_player, index, multimove = False):
    cur_piece_coords = self.__players[this_player - 1].get_pieces()[index].get_coords()[:]
    opp_pieces = self.__players[this_player % 2].get_pieces()
    cur_player = self.__players[this_player - 1]
    new_coords = [(cur_piece_coords[0]) % self.__board_height, (cur_piece_coords[1] - 1) % self.__board_width]
    
    for p in opp_pieces:
      if p.get_coords()[0] == new_coords[0] and p.get_coords()[1] == new_coords[1]:
        self.__report('Error: blocked by opponent.')
        return False
    
    while (multimove and new_coords[1] - 1 >= 0):
      for p in opp_pieces:
        if p.get_coords()[0] == new_coords[0] and p.get_coords()[1] == new_coords[1] - 1:
          cur_player.get_pieces()[index].update_coords(new_coords)
          return True
        
      new_coords[1] = (new_coords[1] - 1) % self.__board_width
      
    cur_player.get_pieces()[index].update_coords(new_coords)
    return True


  def __move_s(self, this_player, index, multimove = False):
    cur_piece_coords = self.__players[this_player - 1].get_pieces()[index].get_coords()[:]
    opp_pieces = self.__players[this_player % 2].get_pieces()
    cur_player = self.__players[this_player - 1]
    new_coords = [(cur_piece_coords[0] + 1) % self.__board_height, (cur_piece_coords[1]) % self.__board_width]
    
    for p in opp_pieces:
      if p.get_coords()[0] == new_coords[0] and p.get_coords()[1] == new_coords[1]:
        self.__report('Error: blocked by opponent.')
        return False
      
    while (multimove and new_coords[0] + 1 < self.__board_height):
      for p in opp_pieces:
        if p.get_coords()[0] == new_coords[0] + 1 and p.get_coords()[1] == new_coords[1]:
          cur_player.get_pieces()[index].update_coords(new_coords)
          return True
        
      new_coords[0] = (new_coords[0] + 1) % self.__board_height
      
    cur_player.get_pieces()[index].update_coords(new_coords)
    return True


  def __move_e(self, this_player, index, multimove = False):
    cur_piece_coords = self.__players[this_player - 1].get_pieces()[index].get_coords()[:]
    opp_pieces = self.__players[this_player % 2].get_pieces()
    cur_player = self.__players[this_player - 1]
    new_coords = [(cur_piece_coords[0]) % self.__board_height, (cur_piece_coords[1] + 1) % self.__board_width]
    
    for p in opp_pieces:
      if p.get_coords()[0] == new_coords[0] and p.get_coords()[1] == new_coords[1]:
        self.__report('Error: blocked by opponent.')
        return False
      
    while (multimove and new_coords[1] + 1 < self.__board_width):
      for p in opp_pieces:
        if p.get_coords()[0] == new_coords[0] and p.get_coords()[1] == new_coords[1] + 1:
          cur_player.get_pieces()[index].update_coords(new_coords)
          return True
        
      new_coords[1] = (new_coords[1] + 1) % self.__board_width
      
    cur_player.get_pieces()[index].update_coords(new_coords)
    return True
  
  
  #Helper functions
  def __update_board(self):
    self.__board = []
    for i in range(self.__board_height):
      self.__board.append([' ' for j in range(self.__board_width)])
        
    p1_pieces = self.__players[0].get_pieces()
    for i in range(self.__players[0].get_pieces_remaining()):
      x = p1_pieces[i].get_coords()[0]
      y = p1_pieces[i].get_coords()[1]
      self.__board[x][y] = p1_pieces[i].get_symbol()
      
    p2_pieces = self.__players[1].get_pieces()
    for i in range(self.__players[1].get_pieces_remaining()):
      x = p2_pieces[i].get_coords()[0]
      y = p2_pieces[i].get_coords()[1]
      self.__board[x][y] = p2_pieces[i].get_symbol()


  def __display_hp(self):
    hp_str = 'Player 1 HP:\n'
    for i in range(self.__players[0].get_pieces_remaining()):
      cur_piece = self.__players[0].get_pieces()[i]
      hp_str += '\t' + cur_piece.get_symbol() + ' has ' + str(cur_piece.get_hp()) + ' remaining.\n'
      hp_str += '\t  ' + cur_piece.get_symbol() + ' located at: ' + str(cur_piece.get_coords()[:]) + '\n'
    
    hp_str += '\nPlayer 2 HP:\n'
    for i in range(self.__players[1].get_pieces_remaining()):
      cur_piece = self.__players[1].get_pieces()[i]
      hp_str += '\t' + cur_piece.get_symbol() + ' has ' + str(cur_piece.get_hp()) + ' remaining.\n'
      hp_str += '\t  ' + cur_piece.get_symbol() + ' located at: ' + str(cur_piece.get_coords()[:]) + '\n'
    
    self.__report(hp_str)


  def __print_board(self):
    board_str = '\n'
    for i in range(self.__board_height):
      board_str += '|'.join([self.__board[i][j] for j in range(self.__board_width)]) + '\n'
      if i < self.__board_height - 1:
        board_str += ' '.join(['_' for j in range(self.__board_width)]) + '\n'
      
    self.__report(board_str)


  def __damage_all_pieces(self):
    for p in self.__players[0].get_pieces():
      p.update_hp()
    
    for p in self.__players[1].get_pieces():
      p.update_hp()
      
    self.__players[0].remove_pieces()
    self.__players[1].remove_pieces()


  def __print_winner(self):
    if self.__players[0].get_pieces_remaining() == 0 and self.__players[1].get_pieces_remaining() == 0:  
      self.__report('This should never happen... Draws are boring.')
      return 2
    elif self.__players[0].get_pieces_remaining() == 0 and self.__players[1].get_pieces_remaining() > 0:
      self.__report('PLAYER 2 WINS THE GAME')
      return 1
    elif self.__players[0].get_pieces_remaining() > 0 and self.__players[1].get_pieces_remaining() == 0:
      self.__report('PLAYER 1 WINS THE GAME')
      return 0
    else:
      self.__report('WHO KNOWS?')
      return 3


  def __dbug(self, dbug_lst):
    print('*****DEBUG STATEMENT*****')
    for item in dbug_lst:
      print('\t' + str(item))
      
    print('*****DEBUG STATEMENT*****')
    
  def __report(self, rep_str):
    if not self.__mute:
      print(rep_str)


  #AI!
  def __turn_ai(self, this_player, mute = True):
    bk = False
    if this_player == 1:
      plyr_str = 'Player 1'
    else:
      plyr_str = 'Player 2'
      
    while not bk:
      self.__report(plyr_str + ':')
  
      if self.__ai_attack(this_player):
        plyr_str = plyr_str + ' attacked!'
        bk = True
      elif self.__ai_move_to_attack(this_player):
        plyr_str = plyr_str + ' moved to attack position!'
        bk = True
      else:
        plyr_str = plyr_str + ' flailed helplessly!'
        while not bk:
          bk = self.__ai_move(this_player)
        
      self.__report(plyr_str)


  def __ai_attack(self, this_player):
    cur_player = self.__players[this_player - 1]
    other_player = self.__players[this_player % 2]
    direction = (-1) ** this_player

    dfndr = None
    for i in range(cur_player.get_pieces_remaining()):
      cur_piece_attk_coords = cur_player.get_pieces()[i].get_coords()[:]
      cur_piece_attk_coords[0] = (cur_piece_attk_coords[0] + direction) % self.__board_height
      for j in range(other_player.get_pieces_remaining()):
        if other_player.get_pieces()[j].get_coords()[:] == cur_piece_attk_coords \
          and (dfndr is None or other_player.get_pieces()[j].get_hp() < other_player.get_pieces()[dfndr].get_hp()):
          dfndr = j
          
          

    if dfndr is not None:
      other_player.get_pieces()[dfndr].update_hp()
      other_player.remove_pieces()
      return True

    return False


  def __ai_move_to_attack(self, this_player):
    cur_player = self.__players[this_player - 1]
    other_player = self.__players[this_player % 2]
    direction = (-1) ** this_player

    o_p_coords = []
    for o_p in other_player.get_pieces():
      o_p_coords.append(o_p.get_coords()[:])

    for c_p in cur_player.get_pieces():
      if c_p.get_symbol().strip().lower() == self.__game_pieces[0] \
        and self.__ai_move_to_attack_x(direction, c_p, o_p_coords): #x
        return True
      elif c_p.get_symbol().strip().lower() == self.__game_pieces[1] \
        and self.__ai_move_to_attack_t(direction, c_p, o_p_coords): #t
        return True
      elif c_p.get_symbol().strip().lower() == self.__game_pieces[2] \
        and self.__ai_move_to_attack_o(direction, c_p, o_p_coords): #o
        return True

    return False


  def __ai_move_to_attack_x(self, direction, c_p, o_p_coords):
    c_p_c = c_p.get_coords()[:]
    #sw
    x_coords = [(c_p_c[0] + 1) % self.__board_height, (c_p_c[1] - 1) % self.__board_width]
    ox_coords = [(x_coords[0] + direction) % self.__board_height, x_coords[1]]
    if o_p_coords.count(x_coords) == 0 and o_p_coords.count(ox_coords) >= 1:
      c_p.update_coords(x_coords)
      return True
    
    #nw
    x_coords = [(c_p_c[0] - 1) % self.__board_height, (c_p_c[1] - 1) % self.__board_width]
    ox_coords = [(x_coords[0] + direction) % self.__board_height, x_coords[1]]
    if o_p_coords.count(x_coords) == 0 and o_p_coords.count(ox_coords) >= 1:
      c_p.update_coords(x_coords)
      return True
    
    #se
    x_coords = [(c_p_c[0] + 1) % self.__board_height, (c_p_c[1] + 1) % self.__board_width]
    ox_coords = [(x_coords[0] + direction) % self.__board_height, x_coords[1]]
    if o_p_coords.count(x_coords) == 0 and o_p_coords.count(ox_coords) >= 1:
      c_p.update_coords(x_coords)
      return True

    #ne
    x_coords = [(c_p_c[0] - 1) % self.__board_height, (c_p_c[1] + 1) % self.__board_width]
    ox_coords = [(x_coords[0] + direction) % self.__board_height, x_coords[1]]
    if o_p_coords.count(x_coords) == 0 and o_p_coords.count(ox_coords) >= 1:
      c_p.update_coords(x_coords)
      return True
      
    return False
  

  def __ai_move_to_attack_t(self, direction, c_p, o_p_coords):
    #sw
    t_coords = c_p.get_coords()[:]
    moved = False
    while o_p_coords.count([(t_coords[0] + 1) % self.__board_height, (t_coords[1] - 1) % self.__board_width]) == 0 \
      and t_coords[0] + 1 != self.__board_height \
      and  t_coords[1] - 1 != 0:
      t_coords = [(t_coords[0] + 1) % self.__board_height, (t_coords[1] - 1) % self.__board_width]
      moved = True
    
    ot_coords = [(t_coords[0] + direction) % self.__board_height, t_coords[1]]
    if o_p_coords.count(ot_coords) >= 1 and moved:
      c_p.update_coords(t_coords)
      return True
    
    #nw
    t_coords = c_p.get_coords()[:]
    moved = False
    while o_p_coords.count([(t_coords[0] - 1) % self.__board_height, (t_coords[1] - 1) % self.__board_width]) == 0 \
      and t_coords[0] - 1 != 0 \
      and  t_coords[1] - 1 != 0:
      t_coords = [(t_coords[0] - 1) % self.__board_height, (t_coords[1] - 1) % self.__board_width]
      moved = True
    
    ot_coords = [(t_coords[0] + direction) % self.__board_height, t_coords[1]]
    if o_p_coords.count(ot_coords) >= 1 and moved:
      c_p.update_coords(t_coords)
      return True
      
    #se
    t_coords = c_p.get_coords()[:]
    moved = False
    while o_p_coords.count([(t_coords[0] + 1) % self.__board_height, (t_coords[1] + 1) % self.__board_width]) == 0 \
      and t_coords[0] + 1 != self.__board_height \
      and  t_coords[1] + 1 != self.__board_width:
      t_coords = [(t_coords[0] + 1) % self.__board_height, (t_coords[1] + 1) % self.__board_width]
      moved = True
    
    ot_coords = [(t_coords[0] + direction) % self.__board_height, t_coords[1]]
    if o_p_coords.count(ot_coords) >= 1 and moved:
      c_p.update_coords(t_coords)
      return True
    
    #ne
    t_coords = c_p.get_coords()[:]
    moved = False
    while o_p_coords.count([(t_coords[0] - 1) % self.__board_height, (t_coords[1] + 1) % self.__board_width]) == 0 \
      and t_coords[0] - 1 != 0 \
      and  t_coords[1] + 1 != self.__board_width:
      t_coords = [(t_coords[0] - 1) % self.__board_height, (t_coords[1] + 1) % self.__board_width]
      moved = True
    
    ot_coords = [(t_coords[0] + direction) % self.__board_height, t_coords[1]]
    if o_p_coords.count(ot_coords) >= 1 and moved:
      c_p.update_coords(t_coords)
      return True

    #s
    t_coords = c_p.get_coords()[:]
    moved = False
    while o_p_coords.count([(t_coords[0] + 1) % self.__board_height, t_coords[1]]) == 0 \
      and t_coords[0] + 1 != self.__board_height:
      t_coords = [(t_coords[0] + 1) % self.__board_height, t_coords[1]]
      moved = True

    ot_coords = [(t_coords[0] + direction) % self.__board_height, t_coords[1]]
    if o_p_coords.count(ot_coords) >= 1 and moved:
      c_p.update_coords(t_coords)
      return True
      
    #n
    t_coords = c_p.get_coords()[:]
    moved = False
    while o_p_coords.count([(t_coords[0] - 1) % self.__board_height, t_coords[1]]) == 0 \
      and t_coords[0] - 1 != 0:
      t_coords = [(t_coords[0] - 1) % self.__board_height, t_coords[1]]
      moved = True

    ot_coords = [(t_coords[0] + direction) % self.__board_height, t_coords[1]]
    if o_p_coords.count(ot_coords) >= 1 and moved:
      c_p.update_coords(t_coords)
      return True
    
    #w
    t_coords = c_p.get_coords()[:]
    moved = False
    while o_p_coords.count([t_coords[0], (t_coords[1] - 1) % self.__board_width]) == 0 \
      and t_coords[1] - 1 != 0:
      t_coords = [t_coords[0], (t_coords[1] - 1) % self.__board_width]
      moved = True
    
    ot_coords = [(t_coords[0] + direction) % self.__board_height, t_coords[1]]
    if o_p_coords.count(ot_coords) >= 1 and moved:
      c_p.update_coords(t_coords)
      return True
    
    #e
    t_coords = c_p.get_coords()[:]
    moved = False
    while o_p_coords.count([t_coords[0], (t_coords[1] + 1) % self.__board_width]) == 0 \
      and t_coords[1] + 1 != self.__board_width:
      t_coords = [t_coords[0], (t_coords[1] + 1) % self.__board_width]
      moved = True
    
    ot_coords = [(t_coords[0] + direction) % self.__board_height, t_coords[1]]
    if o_p_coords.count(ot_coords) >= 1 and moved:
      c_p.update_coords(t_coords)
      return True
  
    return False


  def __ai_move_to_attack_o(self, direction, c_p, o_p_coords):
    c_p_c = c_p.get_coords()[:]
    #w
    o_coords = [c_p_c[0], (c_p_c[1] - 1) % self.__board_width]
    oo_coords = [(o_coords[0] + direction) % self.__board_height, o_coords[1]]
    if o_p_coords.count(o_coords)  == 0 and o_p_coords.count(oo_coords) >= 1:
      c_p.update_coords(o_coords)
      return True
    
    #e
    o_coords = [c_p_c[0], (c_p_c[1] + 1) % self.__board_width]
    oo_coords = [(o_coords[0] + direction) % self.__board_height, o_coords[1]]
    if o_p_coords.count(o_coords) == 0 and o_p_coords.count(oo_coords) >= 1:
      c_p.update_coords(o_coords)
      return True
    
    #s
    o_coords = [(c_p_c[0] + 1) % self.__board_height, c_p_c[1]]
    oo_coords = [(o_coords[0] + direction) % self.__board_height, o_coords[1]]
    if o_p_coords.count(o_coords) == 0 and o_p_coords.count(oo_coords) >= 1:
      c_p.update_coords(o_coords)
      return True
    
    #n
    o_coords = [(c_p_c[0] - 1) % self.__board_height, c_p_c[1]]
    oo_coords = [(o_coords[0] + direction) % self.__board_height, o_coords[1]]
    if o_p_coords.count(o_coords) == 0 and o_p_coords.count(oo_coords) >= 1:
      c_p.update_coords(o_coords)
      return True
    
    return False


  def __ai_move(self, this_player):
    piece_to_move = randint(0, self.__players[this_player - 1].get_pieces_remaining() - 1)

    if self.__game_pieces[piece_to_move] == 'o':
      return self.__ai_move_o(this_player, piece_to_move)
    elif self.__game_pieces[piece_to_move] == 't':
      return self.__ai_move_t(this_player, piece_to_move)
    elif self.__game_pieces[piece_to_move] == 'x':
      return self.__ai_move_x(this_player, piece_to_move)
    else:
      return False


  def __ai_move_o(self, this_player, index):
    direction = randint(0, 3)
    if direction == 0:
      return self.__move_n(this_player, index)
    elif direction == 1:
      return self.__move_w(this_player, index)
    elif direction == 2:
      return self.__move_s(this_player, index)
    elif direction == 3:
      return self.__move_e(this_player, index)
    
    return False


  def __ai_move_t(self, this_player, index):
    direction = randint(0, 7)
    ret_bool = False
    
    if direction == 0:
      ret_bool = self.__move_n(this_player, index, True)
    elif direction == 1:
      ret_bool = self.__move_w(this_player, index, True)
    elif direction == 2:
      ret_bool = self.__move_s(this_player, index, True)
    elif direction == 3:
      ret_bool = self.__move_e(this_player, index, True)
    elif direction == 4:
      ret_bool = self.__move_nw(this_player, index, True)
    elif direction == 5:
      ret_bool = self.__move_ne(this_player, index, True)
    elif direction == 6:
      ret_bool = self.__move_sw(this_player, index, True)
    elif direction == 7:
      ret_bool = self.__move_se(this_player, index, True)
    
    return ret_bool


  def __ai_move_x(self, this_player, index):
    direction = randint(0, 3)
    if direction == 0:
      return self.__move_nw(this_player, index)
    elif direction == 1:
      return self.__move_ne(this_player, index)
    elif direction == 2:
      return self.__move_sw(this_player, index)
    elif direction == 3:
      return self.__move_se(this_player, index)


  #Driver function
  def play_game(self, mute = False):
    self.__mute = mute
    
    while not (self.__players[0].get_pieces_remaining() <= 0 or self.__players[1].get_pieces_remaining() <= 0):
      self.__report('Turns left: ' + str(self.__turns_left))
      self.__update_board()
      self.__print_board()
      
      self.__turn(1)
      
      if self.__players[1].get_pieces_remaining() == 0:
        break
        
      self.__update_board()
      self.__print_board()
      
      if not self.__is_ai:
        self.__turn(2)
      else:
        self.__turn_ai(2, True)
      
      if self.__players[0].get_pieces_remaining() == 0:
        break
      
      if self.__turns_left > 0:
        self.__turns_left -= 1
      else:
        self.__damage_all_pieces()
    
    return self.__print_winner()


  def play_game_ai(self, mute = False):
    self.__mute = mute
    while not (self.__players[0].get_pieces_remaining() <= 0 or self.__players[1].get_pieces_remaining() <= 0):
      self.__report('Turns left: ' + str(self.__turns_left))
      
      self.__update_board()
      self.__print_board()
      
      self.__turn_ai(1)
      self.__display_hp()
      
      if self.__players[1].get_pieces_remaining() == 0:
        break
      
      self.__update_board()
      self.__print_board()
      
      self.__turn_ai(2)
      self.__display_hp()
      
      if self.__players[0].get_pieces_remaining() == 0:
        break
      
      if self.__turns_left > 0:
        self.__turns_left -= 1
      else:
        self.__damage_all_pieces()
        
    return self.__print_winner()



def robot_fight(num_games, mute = True):
  winners = [0, 0, 0, 0]
  for i in range(num_games):
    bg = board_game()
    winners[bg.play_game_ai(mute)] += 1
    
  print(winners)
  print('Player 1 wins: ' + str(winners[0] * 100.0 / num_games) + '% of games')
  print('Player 2 wins: ' + str(winners[1] * 100.0 / num_games) + '% of games')
  print('Draws: ' + str(winners[2] * 100.0 / num_games) + '% of games')
  print('Uhohs...: ' + str(winners[3] * 100.0 / num_games) + '% of games')
  
  
board_game(True).play_game()
#robot_fight(1000)