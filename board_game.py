class player():
  def __init__(self, pieces):
    self.pieces = pieces
    
  def get_pieces(self):
    return self.pieces
    
  def get_pieces_remaining(self):
    return len(self.pieces)
    
  def remove_pieces(self):
    to_remove = []
    for i in range (self.get_pieces_remaining()):
      if self.pieces[i].get_hp() == 0:
        to_remove.append(i)
    
    for i in range(len(to_remove) - 1, -1, -1):
      del self.pieces[to_remove[i]]



class piece():
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
  #add board_small and board_displayed where displayed has lines and small is just pieces. Build displayed from small.
  def __init__(self, height = None, width = 0):
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
    
    #Eventually, let player choose which pieces to use and vary total number based on board size
    p1_o = piece(self.game_pieces[0], 2, [self.board_height - 1, 1])
    p1_t = piece(self.game_pieces[1], 4, [self.board_height - 1, 2])
    p1_x = piece(self.game_pieces[2], 3, [self.board_height - 1, 3])
    
    p2_o = piece(self.game_pieces[0].upper(), 2, [0, 3])
    p2_t = piece(self.game_pieces[1].upper(), 4, [0, 2])
    p2_x = piece(self.game_pieces[2].upper(), 3, [0, 1])
    
    self.p1 = player([p1_o, p1_t, p1_x])
    self.p2 = player([p2_o, p2_t, p2_x])

    self.update_board()
  
  def turn(self, this_player):
    cur_player = self.get_players(this_player)[0]
    if this_player == 1:
      print('Player 1:')
    else:
      print('Player 2:')
      
    piece_select_str = 'Choose your move or type ''help'': '
    for i in range(cur_player.get_pieces_remaining()):
      piece_select_str += '\n\t' + str(i) + ' for ' + cur_player.get_pieces()[i].get_symbol()
    
    piece_select_str += ':\n'
    piece_select = input(piece_select_str)
    
    if piece_select.strip().lower() == 'help':
      help_str = 'Press the index assigned to select a piece or perform the action, type ''hp'' to see the hp for each piece, or type ''board'' to display the board.'
      print(help_str)
    elif piece_select.strip().lower() == 'hp':
      self.display_hp()
    elif piece_select.strip().lower() == 'board':
      self.print_board()
    else:
      i = 0
      for i in range(cur_player.get_pieces_remaining()):
        if piece_select == str(i):
          self.parse_action(this_player, i)
          self.update_board()
          return
        
      print('Invalid input.')
      
    self.turn(this_player)
    
  def parse_action(self, this_player, index):
    cur_player = self.get_players(this_player)[0]
    
    if cur_player.get_pieces()[index].get_symbol().lower() == self.game_pieces[0]:
      move_select = input('1 for northwest\n2 for southwest\n3 for southeast\n4 for northeast\n5 to attack:\n')
      
      if move_select == str(5):
        self.attack(this_player, index)
        return
      elif ['1', '2', '3', '4'].count(move_select) > 0:
        self.move_o(this_player, int(move_select), index)
        return
      else:
        self.parse_action(this_player, input('Incorrect input. Try again: '))

    elif cur_player.get_pieces()[index].get_symbol().lower() == self.game_pieces[1]:
      move_select = input('Press 1 for northwest\n2 for southwest\n3 for southeast\n4 for northeast\n5 for north\n6 for west\n7 for south\n8 for east\n9 to attack:\n')
      
      if move_select == str(9):
        self.attack(this_player, index)
        return
      elif ['1', '2', '3', '4', '5', '6', '7', '8'].count(move_select) > 0:
        self.move_t(this_player, int(move_select), index)
        return
      else:
        self.parse_action(this_player, input('Incorrect input. Try again: '))
    
    elif cur_player.get_pieces()[index].get_symbol().lower() == self.game_pieces[2]:
      move_select = input('Press 1 for north\n2 for west\n3 for south\n4 for east\n5 to attack:\n')
    
      if move_select == str(5):
        self.attack(this_player, index)
        return
      elif ['1', '2', '3', '4'].count(move_select) > 0:
        self.move_x(this_player, int(move_select), index)
        return
      else:
        self.parse_action(this_player, input('Incorrect input. Try again: '))
    
    self.parse_action(cur_player, input('Incorrect input. Try again: '))
    
  """
  --Attack Function
  """
  def attack(self, this_player, index):
    players = self.get_players(this_player)
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
    
    for i in range(other_player.get_pieces_remaining()):
      opp_coords = opp_pieces[i].get_coords()
      if cur_piece_coords[0] + movement == opp_coords[0] and cur_piece_coords[1] == opp_coords[1]:
        other_player.get_pieces()[i].update_hp()
        if other_player.get_pieces()[i].get_hp() == 0:
          print('Piece ' + other_player.get_pieces()[i].get_symbol() + ' is destroyed.')
          other_player.remove_pieces()
      
      self.update_players(this_player, cur_player, other_player)
    else:
      print('Failed to hit.')
  
  """
  ---Movement rules
  """
  def move_o(self, this_player, direction, index):
    if direction == 1:
      self.move_nw(this_player, index)
    elif direction == 2:
      self.move_sw(this_player, index)
    elif direction == 3:
      self.move_se(this_player, index)
    else:
      self.move_ne(this_player, index)
    
  def move_t(self, this_player, direction, index):
    if direction == 1:
      self.move_nw(this_player, index, True)
    elif direction == 2:
      self.move_sw(this_player, index, True)
    elif direction == 3:
      self.move_se(this_player, index, True)
    elif direction == 4:
      self.move_ne(this_player, index, True)
    elif direction == 5:
      self.move_n(this_player, index, True)
    elif direction == 6:
      self.move_w(this_player, index, True)
    elif direction == 7:
      self.move_se(this_player, index, True)
    else:
      self.move_e(this_player, index, True)
      
  def move_x(self, this_player, direction, index):
    if direction == 1:
      self.move_n(this_player, index)
    elif direction == 2:
      self.move_w(this_player, index)
    elif direction == 3:
      self.move_s(this_player, index)
    else:
      self.move_e(this_player, index)
    
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
        return
    
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
        return
    
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
        return
    
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
        return
    
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
        return
    
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
        return
    
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
        return
      
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
        return
      
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
      
  """
  ---Driver function
  """
  def play_game(self):
    while not (self.p1.get_pieces_remaining() <= 0 or self.p2.get_pieces_remaining() <= 0):
      self.print_board()
      
      self.turn(1)
      if self.p2.get_pieces_remaining() == 0:
        print('PLAYER 1 WINS THE GAME')
        return
      self.print_board()
      self.turn(2)
      if self.p1.get_pieces_remaining() == 0:
        print('PLAYER 2 WINS THE GAME')
        return
      
    print('This should never happen...')

bg = board_game()
bg.play_game()