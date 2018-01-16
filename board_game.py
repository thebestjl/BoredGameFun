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
        #self.__report('Piece ' + p.get_symbol() + ' is destroyed!')
        index = self.pieces.index(p)
        del self.pieces[index]



class piece():
  def __init__(self, symbol, hp, coords, dims):
    self.__symbol = symbol
    self.__hp = hp
    self.coords = coords
    self.dims = dims
    self.__game_pieces = ['x', 't', 'o']


  def update_hp(self):
    if self.__hp > 0:
      self.__hp -= 1


  def get_hp(self):
    return self.__hp


  def get_symbol(self):
    return self.__symbol


  def get_coords(self):
    return self.coords


  def update_coords(self, coords):
    self.coords = coords
  
  
  def __str__(self):
    ret = 'Symbol: ' + self.__symbol + ' HP: ' + str(self.__hp) + ' Coordinates: ' + str(self.coords)
    return ret
  
  
  def __repr__(self):
    ret = 'Symbol: ' + self.__symbol + ' HP: ' + str(self.__hp) + ' Coordinates: ' + str(self.coords)
    return ret

  
  #MOVEMENT RULES
  def move_nw(self, opp_pieces, multimove = False):
    new_coords = [(self.get_coords()[0] - 1) % self.dims[0], (self.get_coords()[1] - 1) % self.dims[1]]
    for p in opp_pieces:
      if p.get_coords()[0] == new_coords[0] and p.get_coords()[1] == new_coords[1]:
        return False
    
    while (multimove and new_coords[0] - 1 >= 0 and new_coords[1] - 1 >= 0):
      for p in opp_pieces:
        if p.get_coords()[0] == new_coords[0] - 1 and p.get_coords()[1] == new_coords[1] - 1:
          multimove = False
          break
        
      new_coords = [(new_coords[0] - 1) % self.dims[0], (new_coords[1] - 1) % self.dims[1]]
      
    self.coords = new_coords
    return True


  def move_sw(self, opp_pieces, multimove = False):
    new_coords = [(self.get_coords()[0] + 1) % self.dims[0], (self.get_coords()[1] - 1) % self.dims[1]]
    
    for p in opp_pieces:
      if p.get_coords()[0] == new_coords[0] and p.get_coords()[1] == new_coords[1]:
        return False
    
    while (multimove and new_coords[0] + 1 < self.dims[0] and new_coords[1] - 1 >= 0):
      for p in opp_pieces:
        if p.get_coords()[0] == new_coords[0] + 1 and p.get_coords()[1] == new_coords[1] - 1:
          multimove = False
          break
        
      new_coords = [(new_coords[0] + 1) % self.dims[0], (new_coords[1] - 1) % self.dims[1]]
    
    self.coords = new_coords
    return True

  
  def move_se(self, opp_pieces, multimove = False):
    new_coords = [(self.get_coords()[0] + 1) % self.dims[0], (self.get_coords()[1] + 1) % self.dims[1]]
    
    for p in opp_pieces:
      if p.get_coords()[0] == new_coords[0] and p.get_coords()[1] == new_coords[1]:
        return False
    
    while (multimove and new_coords[0] + 1 < self.dims[0] and new_coords[1] + 1 < self.dims[1]):
      for p in opp_pieces:
        if p.get_coords()[0] == new_coords[0] + 1 and p.get_coords()[1] == new_coords[1] + 1:
          multimove = False
          break
        
      new_coords = [(new_coords[0] + 1) % self.dims[0], (new_coords[1] + 1) % self.dims[1]]

    self.coords = new_coords
    return True


  def move_ne(self, opp_pieces, multimove = False):
    new_coords = [(self.get_coords()[0] - 1) % self.dims[0], (self.get_coords()[1] + 1) % self.dims[1]]

    for p in opp_pieces:
      if p.get_coords()[0] == new_coords[0] and p.get_coords()[1] == new_coords[1]:
        return False
    
    while (multimove and new_coords[0] - 1 >= 0 and new_coords[1] + 1 < self.dims[1]):
      for p in opp_pieces:
        if p.get_coords()[0] == new_coords[0] - 1 and p.get_coords()[1] == new_coords[1] + 1:
          multimove = False
          break
        
      new_coords = [(new_coords[0] - 1) % self.dims[0], (new_coords[1] + 1) % self.dims[1]]
      
    self.coords = new_coords
    return True


  def move_n(self, opp_pieces, multimove = False):
    new_coords = [(self.get_coords()[0]  - 1) % self.dims[0], (self.get_coords()[1]) % self.dims[1]]
    for p in opp_pieces:
      if p.get_coords()[0] == new_coords[0] and p.get_coords()[1] == new_coords[1]:
        return False
    
    while (multimove and new_coords[0] - 1 >= 0):
      for p in opp_pieces:
        if p.get_coords()[0] == new_coords[0] - 1 and p.get_coords()[1] == new_coords[1]:
          multimove = False
          break
        
      new_coords[0] = (new_coords[0] - 1) % self.dims[0]
      
    self.coords = new_coords
    return True

  def move_w(self, opp_pieces, multimove = False):
    new_coords = [(self.get_coords()[0]) % self.dims[0], (self.get_coords()[1] - 1) % self.dims[1]]
    
    for p in opp_pieces:
      if p.get_coords()[0] == new_coords[0] and p.get_coords()[1] == new_coords[1]:
        return False
    
    while (multimove and new_coords[1] - 1 >= 0):
      for p in opp_pieces:
        if p.get_coords()[0] == new_coords[0] and p.get_coords()[1] == new_coords[1] - 1:
          multimove = False
          break
        
      new_coords[1] = (new_coords[1] - 1) % self.dims[1]
      
    self.coords = new_coords
    return True


  def move_s(self, opp_pieces, multimove = False):
    new_coords = [(self.get_coords()[0] + 1) % self.dims[0], (self.get_coords()[1]) % self.dims[1]]
    
    for p in opp_pieces:
      if p.get_coords()[0] == new_coords[0] and p.get_coords()[1] == new_coords[1]:
        return False
      
    while (multimove and new_coords[0] + 1 < self.dims[0]):
      for p in opp_pieces:
        if p.get_coords()[0] == new_coords[0] + 1 and p.get_coords()[1] == new_coords[1]:
          multimove = False
          break
        
      new_coords[0] = (new_coords[0] + 1) % self.dims[0]
      
    self.coords = new_coords
    return True


  def move_e(self, opp_pieces, multimove = False):
    new_coords = [(self.get_coords()[0]) % self.dims[0], (self.get_coords()[1] + 1) % self.dims[1]]
    
    for p in opp_pieces:
      if p.get_coords()[0] == new_coords[0] and p.get_coords()[1] == new_coords[1]:
        return False
      
    while (multimove and new_coords[1] + 1 < self.dims[1]):
      for p in opp_pieces:
        if p.get_coords()[0] == new_coords[0] and p.get_coords()[1] == new_coords[1] + 1:
          multimove = False
          break
        
      new_coords[1] = (new_coords[1] + 1) % self.dims[1]
      
    self.coords = new_coords
    return True

 
  def move(self, direction, opp_pieces):
    raise NotImplementedError('Method ''move'' must be implemented for piece ' \
      + self.__symbol + ' before calling.')


  def ai_attack_pos(self, this_player, opp_pieces):
    raise NotImplementedError('Method ''ai_attack_pos'' must be implemented for piece ' \
      + self.__symbol + ' before calling.')
  


class piece_t(piece):
  def __init__(self, coords, dims, to_upper = False):
    sym = 't'
    if to_upper:
      sym = sym.upper()
      
    piece.__init__(self, sym, 4, coords, dims)


  def move(self, direction, opp_pieces):
    ret_bool = False
    
    if direction == '7' or direction.lower() == 'q':
      ret_bool = self.move_nw(opp_pieces, True)
    elif direction == '1' or direction.lower() == 'z':
      ret_bool = self.move_sw(opp_pieces, True)
      print('t moved sw!')
    elif direction == '3' or direction.lower() == 'c':
      ret_bool = self.move_se(opp_pieces, True)
    elif direction == '9' or direction.lower() == 'e':
      ret_bool = self.move_ne(opp_pieces, True)
    elif direction == '8' or direction.lower() == 'w':
      ret_bool = self.move_n(opp_pieces, True)
    elif direction == '4' or direction.lower() == 'a':
      ret_bool = self.move_w(opp_pieces, True)
    elif direction == '2' or direction.lower() == 'x':
      ret_bool = self.move_s(opp_pieces, True)
    elif direction == '6' or direction.lower() == 'd':
      ret_bool = self.move_e(opp_pieces, True)
    
    return ret_bool
    
  
  def ai_attack_pos(self, this_player, opp_pieces):
    direction = (-1) ** this_player
    o_p_coords = []
    for p in opp_pieces:
      o_p_coords.append(p)
    
    #sw
    t_coords = self.get_coords()[:]
    if self.move_sw(opp_pieces, True):
      ot_coords = [(self.get_coords()[0] + direction) % self.dims[0], self.get_coords()[1]]
      if o_p_coords.count(ot_coords) >= 1:
        return True
      else:
        self.coords = t_coords
    
    #nw
    t_coords = self.get_coords()[:]
    if self.move_nw(opp_pieces, True):
      ot_coords = [(self.get_coords()[0] + direction) % self.dims[0], self.get_coords()[1]]
      if o_p_coords.count(ot_coords) >= 1:
        return True
      else:
        self.coords = t_coords
      
    #se
    t_coords = self.get_coords()[:]
    if self.move_se(opp_pieces, True):
      ot_coords = [(self.get_coords()[0] + direction) % self.dims[0], self.get_coords()[1]]
      if o_p_coords.count(ot_coords) >= 1:
        return True
      else:
        self.coords = t_coords
        
    return False


  def t_se(direction, opp_pieces, o_p_coords):
    t_coords = self.get_coords()[:]
    if self.move_se(opp_pieces, True):
      ot_coords = [(self.get_coords()[0] + direction) % self.dims[0], self.get_coords()[1]]
      if o_p_coords.count(ot_coords) >= 1:
        return True
      else:
        self.coords = t_coords
        
    return False

  def t_ne(direction, opp_pieces, o_p_coords):
    t_coords = self.get_coords()[:]
    if self.move_ne(opp_pieces, True):
      ot_coords = [(self.get_coords()[0] + direction) % self.dims[0], self.get_coords()[1]]
      if o_p_coords.count(ot_coords) >= 1:
        return True
      else:
        self.coords = t_coords
        
    return False
  
  
  def t_south(self, direction, opp_pieces, o_p_coords):
    t_coords = self.get_coords()[:]
    if self.move_s(opp_pieces, True):
      ot_coords = [(self.get_coords()[0] + direction) % self.dims[0], self.get_coords()[1]]
      if o_p_coords.count(ot_coords) >= 1:
        return True
      else:
        self.coords = t_coords
        
    return False


  def t_north(self, direction, opp_pieces, o_p_coords):
    t_coords = self.get_coords()[:]
    if self.move_n(opp_pieces, True):
      ot_coords = [(self.get_coords()[0] + direction) % self.dims[0], self.get_coords()[1]]
      if o_p_coords.count(ot_coords) >= 1:
        return True
      else:
        self.coords = t_coords
        
    return False


  def t_west(self, direction, opp_pieces, o_p_coords):
    t_coords = self.get_coords()[:]
    if self.move_w(opp_pieces, True):
      ot_coords = [(self.get_coords()[0] + direction) % self.dims[0], self.get_coords()[1]]
      if o_p_coords.count(ot_coords) >= 1:
        return True
      else:
        self.coords = t_coords
    
    return False


  def t_east(self, direction, opp_pieces, o_p_coords):
    t_coords = self.get_coords()[:]
    if self.move_e(opp_pieces, True):
      ot_coords = [(self.get_coords()[0] + direction) % self.dims[0], self.get_coords()[1]]
      if o_p_coords.count(ot_coords) >= 1:
        return True
      else:
        self.coords = t_coords
  
    return False



class piece_o(piece):
  def __init__(self, coords, dims, to_upper = False):
    sym = 'o'
    if to_upper:
      sym = sym.upper()

    piece.__init__(self, sym, 3, coords, dims)


  def move(self, direction, opp_pieces):
    if direction == '8' or direction.lower() == 'w':
      return self.move_n(opp_pieces)
    elif direction == '4' or direction.lower() == 'a':
      return self.move_w(opp_pieces)
    elif direction == '2' or direction.lower() == 'x':
      return self.move_s(opp_pieces)
    elif direction == '6' or direction.lower() == 'd':
      return self.move_e(opp_pieces)
    else:
      return False
      
  def ai_attack_pos(self, this_player, opp_pieces):
    c_p_c = self.get_coords()[:]
    direction = (-1) ** this_player
    o_p_coords = []
    for p in opp_pieces:
      o_p_coords.append(p)
      
    #w
    o_coords = [c_p_c[0], (c_p_c[1] - 1) % self.dims[1]]
    oo_coords = [(o_coords[0] + direction) % self.dims[0], o_coords[1]]
    if o_p_coords.count(o_coords)  == 0 and o_p_coords.count(oo_coords) >= 1:
      self.coords = o_coords
      return True
    
    #e
    o_coords = [c_p_c[0], (c_p_c[1] + 1) % self.dims[1]]
    oo_coords = [(o_coords[0] + direction) % self.dims[0], o_coords[1]]
    if o_p_coords.count(o_coords) == 0 and o_p_coords.count(oo_coords) >= 1:
      self.coords = o_coords
      return True
    
    #s
    o_coords = [(c_p_c[0] + 1) % self.dims[0], c_p_c[1]]
    oo_coords = [(o_coords[0] + direction) % self.dims[0], o_coords[1]]
    if o_p_coords.count(o_coords) == 0 and o_p_coords.count(oo_coords) >= 1:
      self.coords = o_coords
      return True
    
    #n
    o_coords = [(c_p_c[0] - 1) % self.dims[0], c_p_c[1]]
    oo_coords = [(o_coords[0] + direction) % self.dims[0], o_coords[1]]
    if o_p_coords.count(o_coords) == 0 and o_p_coords.count(oo_coords) >= 1:
      self.coords = o_coords
      return True
    
    return False



class piece_x(piece):
  def __init__(self, coords, dims, to_upper = False):
    sym = 'x'
    if to_upper:
      sym = sym.upper()
      
    piece.__init__(self, sym, 2, coords, dims)


  def move(self, direction, opp_pieces):
    if direction == '7' or direction.lower() == 'q':
      return self.move_nw(opp_pieces)
    elif direction == '1' or direction.lower() == 'z':
      return self.move_sw(opp_pieces)
    elif direction == '3' or direction.lower() == 'c':
      return self.move_se(opp_pieces)
    elif direction == '9' or direction.lower() == 'e':
      return self.move_ne(opp_pieces)
    else:
      return False


  def ai_attack_pos(self, this_player, opp_pieces):
    c_p_c = self.get_coords()[:]
    direction = (-1) ** this_player
    o_p_coords = []
    for p in opp_pieces:
      o_p_coords.append(p)
      
    #sw
    x_coords = [(c_p_c[0] + 1) % self.dims[0], (c_p_c[1] - 1) % self.dims[1]]
    ox_coords = [(x_coords[0] + direction) % self.dims[0], x_coords[1]]
    if o_p_coords.count(x_coords) == 0 and o_p_coords.count(ox_coords) >= 1:
      self.coords = x_coords
      return True
    
    #nw
    x_coords = [(c_p_c[0] - 1) % self.dims[0], (c_p_c[1] - 1) % self.dims[1]]
    ox_coords = [(x_coords[0] + direction) % self.dims[0], x_coords[1]]
    if o_p_coords.count(x_coords) == 0 and o_p_coords.count(ox_coords) >= 1:
      self.coords = x_coords
      return True
    
    #se
    x_coords = [(c_p_c[0] + 1) % self.dims[0], (c_p_c[1] + 1) % self.dims[1]]
    ox_coords = [(x_coords[0] + direction) % self.dims[0], x_coords[1]]
    if o_p_coords.count(x_coords) == 0 and o_p_coords.count(ox_coords) >= 1:
      self.coords = x_coords
      return True

    #ne
    x_coords = [(c_p_c[0] - 1) % self.dims[0], (c_p_c[1] + 1) % self.dims[1]]
    ox_coords = [(x_coords[0] + direction) % self.dims[0], x_coords[1]]
    if o_p_coords.count(x_coords) == 0 and o_p_coords.count(ox_coords) >= 1:
      self.coords = x_coords
      return True
      
    return False



class board_game():
  def __init__(self, dims = None):
    self.__mute = False
    
    if dims != None:
      self.__dims = []
      self.__dims[0] = 5 if dims[0] < 3 else dims[0]
      self.__dims[1] = 5 if dims[1] < 3 else dims[1]
    else:
      self.__dims = [5, 5]
      
    self.__board = []
    self.__game_pieces = ['x', 't', 'o']
    p1_x = piece_x([self.__dims[0] - 1, 1], self.__dims)
    p1_t = piece_t([self.__dims[0] - 1, 2], self.__dims)
    p1_o = piece_o([self.__dims[0] - 1, 3], self.__dims)
    p1 = player([p1_x, p1_t, p1_o])
    
    p2_x = piece_x([0, 3], self.__dims, True)
    p2_t = piece_t([0, 2], self.__dims, True)
    p2_o = piece_o([0, 1], self.__dims, True)
    p2 = player([p2_x, p2_t, p2_o])
    
    self.__players = [p1, p2]
    self.__turns_left = 20
    self.__update_board()


  def __turn(self, this_player):
    bk = False
    while not bk:
      cur_player = self.__players[this_player - 1]
      self.__report('Player ' + str(this_player) + ':')

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
      
        if not bk:                      
          self.__report('Invalid input.')


  def __parse_action(self, this_player, index):
    cur_player = self.__players[this_player - 1]
    ret_bool = False
    opp_pieces = self.__players[this_player % 2].get_pieces()
    
    if cur_player.get_pieces()[index].get_symbol().lower() == self.__game_pieces[0]:
      move_select = input('\t7 or Q for northwest\n\t1 or Z for southwest\n\t3 or C for southeast\n\t9 or E for northeast\n\t5 or S to attack\n')
      
      if [str(5), 's', 'S'].count(move_select) > 0:
        ret_bool = self.__attack(this_player, index)
      elif ['7', '1', '3', '9', 'q', 'Q', 'z', 'Z', 'c', 'C', 'e', 'E'].count(move_select) > 0:
        ret_bool = cur_player.get_pieces()[index].move(move_select, opp_pieces)

    elif cur_player.get_pieces()[index].get_symbol().lower() == self.__game_pieces[1]:
      move_select = input('\t7 or Q for northwest\n\t1 or Z for southwest\n\t3 or C for southeast\n\t9 ' \
        + 'or E for northeast\n\t8 or W for north\n\t4 or A for west\n\t2 or X for south\n\t6 or D for east\n\t5 or S to attack\n')
      
      if [str(5), 's', 'S'].count(move_select) > 0:
        ret_bool = self.__attack(this_player, index)
      elif ['7', '1', '3', '9', '8', '4', '2', '6', 'q', 'Q', 'z', 'Z', 'c', 'C', 'e', 'E', 'w', 'W', 'a', 'A', 'x', 'X', 'd', 'D'].count(move_select) > 0:
        ret_bool = cur_player.get_pieces()[index].move(move_select, opp_pieces)
      
    elif cur_player.get_pieces()[index].get_symbol().lower() == self.__game_pieces[2]:
      move_select = input('\t8 or W for north\n\t4 or A for west\n\t2 or X for south\n\t6 or D for east\n\t5 or S to attack\n')
    
      if [str(5), 's', 'S'].count(move_select) > 0:
        ret_bool = self.__attack(this_player, index)
      elif ['8', '4', '2', '6', 'w', 'W', 'a', 'A', 'x', 'X', 'd', 'D'].count(move_select) > 0:
        ret_bool = cur_player.get_pieces()[index].move(move_select, opp_pieces)
    
    if not ret_bool:    
      self.__report('Incorrect input, try again!')
    return ret_bool


  #Helper functions
  def __update_board(self):
    self.__board = []
    for i in range(self.__dims[0]):
      self.__board.append([' ' for j in range(self.__dims[1])])
        
    p1_pieces = self.__players[0].get_pieces()
    for i in range(self.__players[0].get_pieces_remaining()):
      x = p1_pieces[i].coords[0]
      y = p1_pieces[i].coords[1]
      self.__board[x][y] = p1_pieces[i].get_symbol()
      
    p2_pieces = self.__players[1].get_pieces()
    for i in range(self.__players[1].get_pieces_remaining()):
      x = p2_pieces[i].coords[0]
      y = p2_pieces[i].coords[1]
      self.__board[x][y] = p2_pieces[i].get_symbol()


  def __display_hp(self):
    hp_str = 'Player 1 HP:\n'
    for i in range(self.__players[0].get_pieces_remaining()):
      cur_piece = self.__players[0].get_pieces()[i]
      hp_str += '\t' + cur_piece.get_symbol() + ' has ' + str(cur_piece.get_hp()) + ' remaining.\n'
      hp_str += '\t  ' + cur_piece.get_symbol() + ' located at: ' + str(cur_piece.coords[:]) + '\n'
    
    hp_str += '\nPlayer 2 HP:\n'
    for i in range(self.__players[1].get_pieces_remaining()):
      cur_piece = self.__players[1].get_pieces()[i]
      hp_str += '\t' + cur_piece.get_symbol() + ' has ' + str(cur_piece.get_hp()) + ' remaining.\n'
      hp_str += '\t  ' + cur_piece.get_symbol() + ' located at: ' + str(cur_piece.coords[:]) + '\n'
    
    self.__report(hp_str)


  def __print_board(self):
    board_str = '\n'
    for i in range(self.__dims[0]):
      board_str += '|'.join([self.__board[i][j] for j in range(self.__dims[1])]) + '\n'
      if i < self.__dims[0] - 1:
        board_str += ' '.join(['_' for j in range(self.__dims[1])]) + '\n'
      
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
      
      
  #Attack Function
  def __attack(self, this_player, index):
    hit = False
    direction = (-1) ** this_player
    other_player = self.__players[this_player % 2]
    
    cur_piece = self.__players[this_player - 1].get_pieces()[index]
    cur_piece_coords = cur_piece.coords[:]
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


  #AI!
  def __turn_ai(self, this_player):
    if this_player == 1:
      plyr_str = 'Player 1'
    else:
      plyr_str = 'Player 2'
    
    self.__report(plyr_str + ':')
    if self.__ai_attack(this_player):
      plyr_str = plyr_str + ' attacked!'
    elif self.__ai_move_to_attack(this_player):
      plyr_str = plyr_str + ' moved to attack position!'
    else:
      plyr_str = plyr_str + ' flailed helplessly!'
      while not self.__ai_move(this_player):
        pass
    self.__report(plyr_str)


  def __ai_attack(self, this_player):
    cur_player = self.__players[this_player - 1]
    other_player = self.__players[this_player % 2]
    direction = (-1) ** this_player
    dfndr = None
    
    for i in range(cur_player.get_pieces_remaining()):
      cur_piece_attk_coords = cur_player.get_pieces()[i].coords[:]
      cur_piece_attk_coords[0] = (cur_piece_attk_coords[0] + direction) % self.__dims[0]
      for j in range(other_player.get_pieces_remaining()):
        if other_player.get_pieces()[j].coords[:] == cur_piece_attk_coords \
          and (dfndr is None or other_player.get_pieces()[j].get_hp() < other_player.get_pieces()[dfndr].get_hp()):
          dfndr = j
          
    if dfndr is not None:
      other_player.get_pieces()[dfndr].update_hp()
      other_player.remove_pieces()
      return True

    return False


  def __ai_move_to_attack(self, this_player):
    cur_player = self.__players[this_player - 1]

    for i in range(cur_player.get_pieces_remaining()):
      c_p = cur_player.get_pieces()[i]
      if c_p.ai_attack_pos(this_player, self.__players[this_player % 2].get_pieces()):
        return True

    return False


  def __ai_move(self, this_player):
    cur_player = self.__players[this_player - 1]
    cur_piece = cur_player.get_pieces()[randint(0, cur_player.get_pieces_remaining() - 1)]
    direction = (-1) ** this_player
    
    return cur_piece.move(direction, self.__players[this_player % 2].get_pieces())


  #Driver function
  def play_game(self, is_ai_1 = False, is_ai_2 = True, mute = False):
    self.__mute = mute
    
    while not (self.__players[0].get_pieces_remaining() <= 0 or self.__players[1].get_pieces_remaining() <= 0):
      self.__report('Turns left: ' + str(self.__turns_left))
      self.__update_board()
      self.__print_board()
      
      if not is_ai_1:
        self.__turn(1)
      else:
        self.__turn_ai(1)
      
      if self.__players[1].get_pieces_remaining() == 0:
        break
        
      self.__update_board()
      self.__print_board()
      
      if not is_ai_2:
        self.__turn(2)
      else:
        self.__turn_ai(2)
      
      if self.__players[0].get_pieces_remaining() == 0:
        break
      
      if self.__turns_left > 0:
        self.__turns_left -= 1
      else:
        self.__damage_all_pieces()
    
    return self.__print_winner()


  def play_game_ai(self, mute = True):
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
  
  
board_game().play_game()
#robot_fight(1000)
