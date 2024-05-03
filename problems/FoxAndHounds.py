'''FoxAndHounds.py
("Fox and Hounds" game)
A SOLUZION problem formulation, originally for SZ001.py,
which supported multi-client sessions.
 (Originally working as of 28-April-2017.)

Adapted for Int_Solv_Client_4b, on March 20, 2024.
 Roles declarations used with SZ001 are removed here,
so the two players (for the Fox and Hounds) should simply
take turns at the same computer, as prompted in the
state display.

'''
#<METADATA>
SOLUZION_VERSION = "4.0"
PROBLEM_NAME = "Fox and Hounds"
PROBLEM_VERSION = "4.0"
PROBLEM_AUTHORS = ['S. Tanimoto']
PROBLEM_CREATION_DATE = "20-MAR-2024"

PROBLEM_DESC=\
 '''The game of <b>"Fox and Hounds"</b> problem is a traditional game
played on a checkerboard, using four white checkers and one black checker.
One player playes the four white "geese" and the other player plays
the black "fox".  Like checkers, only black squares are used on the
checkerboard.  The four geese are lined up on one side of the board
and the fox is on a black square on the opposite side.  The object
of the game is different for the fox than for the geese.  The fox
must "get past" the geese and make it to the other side of the board
(where the geese start).  The geese have the goal of trapping the
fox, boxing him in so he can't move.  Although the geese have an
advantage in numbers, they have two limitations: (1) each hound
can only move forward (diagonally, as in checkers), whereas the
fox can move forward or backward (like a king in checkers);
(2) only one of the geeze can move in any given turn.
Unlike checkers, there is no capturing, no becoming a kind, and
no jumping.  The fox loses if he has no available moves.
The fox gets to move first.

More information about this and related "fox games" can be
found at this web page:
https://en.wikipedia.org/wiki/Fox_games

The operator names in this implementation refer to positions on
the board using the numbering scheme shown below:
 - 1 - 2 - 3 - 4
 5 - 6 - 7 - 8 -
 - 9 -10 -11 -12
13 -14 -15 -16 -
 -17 -18 -18 -20
21 -22 -23 -24 -
 -25 -26 -27 -28
29 -30 -31 -32 -
'''
#</METADATA>

#<COMMON_DATA>
#</COMMON_DATA>
WHITE_SQ = 0
BLACK_SQ = 1
FOX = 2
HOUND = 3
SYMBOLS = ['-','#','F','H']
#<COMMON_CODE>
DEBUG=False

class State():
  def __init__(self):
    print("Creating the initial state.")
    self.foxCoords=[0,3]
    self.coordsOfHounds=[[7,0],[7,2],[7,4],[7,6]]
    self.foxsTurn=False

  def copy(self):
    news = State()
    news.foxCoords = self.foxCoords
    news.coordsOfHounds = self.coordsOfHounds
    news.foxsTurn = self.foxsTurn
    return news
      
  def __str__(self):
    ''' Produces a textual description of a state.
        Might not be needed in normal operation with GUIs.'''
    arr = self.toArray()
    txt = '\n'
    for row in arr:
       for sq in row:
         txt += SYMBOLS[sq]+' '
       txt += "\n"
    if self.foxsTurn:
       txt += "Fox's Turn"
    else:
       txt += "Hounds's Turn"
    return txt

  def toArray(self):
    arr = []
    for i in range(8):
      row = 8*[WHITE_SQ]
      for j in range(8):
        if (i+j)%2 == 1: row[j] = BLACK_SQ
      arr.append(row)
    foxrow, foxcol = self.foxCoords
    arr[foxrow][foxcol]=FOX
    try:
     for (houndrow, houndcol) in self.coordsOfHounds:
      arr[houndrow][houndcol]=HOUND
     return arr
    except:
     return arr

  def __eq__(self, s):
    if self.foxsTurn != s.foxsTurn: return False
    if self.foxCoords[0] != s.foxCoords[0]: return False
    if self.foxCoords[1] != s.foxCoords[1]: return False
    gself = self.coordsOfHounds
    gother = s.coordsOfHounds
    for i in range(4):
        if gself[i][0] != gother[i][0]: return False
        if gself[i][1] != gother[i][1]: return False
    return True

  def __hash__(self):
    return (self.__str__()).__hash__()

  def is_goal(self):
    """There are 2 ways for the Fox to win.  This implementatioon
    only checks for ONE (#1) of them:
     1. The fox reaches the opposite row.
     2. The hounds have no moves left.
    In case 2. The game will typically stop, but the game
    master program might not explain why. """
    foxrow,foxcol = self.foxCoords
    if foxrow==7:
      self.win_msg = "The Fox wins!"
      return True

    # Now test whether the geese have won...
    # Count the number of moves for fox.
    arr = self.toArray()
    n_moves_for_fox = 0    
    for d in DIRECTIONS:
        drow,dcol = deltas_from_direction(d)
        newrow = foxrow+drow
        newcol = foxcol+dcol
        if newrow < 0: continue
        if newrow > 7: continue
        if newcol < 0: continue
        if newcol > 7: continue
        if arr[newrow][newcol]==HOUND: continue
        return False  # Fox still has a move; game not over.

    self.win_msg = "The Hounds win!"
    return True
  
  def goal_message(self):
      return self.win_msg

#---------------------

class Precondition():
  def __init__(self, source, direction):
    self.source = source
    self.direction = direction

  def __call__(self, state):
    if state.foxsTurn==False:
      if self.direction in ['SW', 'SE']:
        if DEBUG:
          print("Hounds cannot move backwards.")
        return False
    arr = state.toArray()
    (i,j) = coords_from_square_number(self.source)
    # Piece to move must be at source location.
    source_piece = arr[i][j]
    if (state.foxsTurn and source_piece !=FOX) or \
       ((not state.foxsTurn) and source_piece != HOUND):
      if DEBUG:
        print("The move doesn't have a proper piece at source position.")
        print("Position="+str((i,j))+"; source_piece="+str(source_piece))
      return False 
    (di,dj) = deltas_from_direction(self.direction)
    if i+di < 0 or i+di > 7: 
       if DEBUG:
         print("Would move too high or low.")
       return False
    if j+dj < 0 or j+dj > 7: 
       if DEBUG:
         print("Would move too far left or right.")
       return False
    if arr[i+di][j+dj]==BLACK_SQ: 
       if DEBUG:
         print("Destination is vacant, so OK to make this move.")
       return True
    if DEBUG:
      print("Destination square already occupied:")
      print(state)
    return False

def coords_from_square_number(source):
    row = int((source-1)/4)
    col = 2*((source-1)%4) + (row+1)%2
    return (row, col)

def deltas_from_direction(direc):
    i = DIRECTIONS.index(direc)
    return [[1,-1],[1,1],[-1,-1],[-1,1]][i]

class StateTransf():
  def __init__(self, source, direction):
    self.source = source
    self.direction = direction

  def __call__(self, state):
    arr = state.toArray()
    (i,j) = coords_from_square_number(self.source)
    (di,dj) = deltas_from_direction(self.direction)
    news = state.copy()
    news.foxsTurn = not (news.foxsTurn)
    if news.foxCoords[0]==i and news.foxCoords[1]==j:
       news.foxCoords = [i+di, j+dj]
       return news
    for gp in news.coordsOfHounds:
       if gp[0]==i and gp[1]==j:
          gp[0] = i+di; gp[1] = j+dj
    return news

#</COMMON_CODE>

#<OPERATORS>
from soluzion import Basic_Operator as Operator

SOURCES = list(range(1,33))
DIRECTIONS = ['SW', 'SE', 'NW', 'NE']

OPERATORS = [Operator(
  "Move piece at "+str(source)+" in direction "+direc,
  Precondition(source, direc),
  StateTransf(source, direc))\
     for source in SOURCES for direc in DIRECTIONS]

if DEBUG:
  for o in OPERATORS:
    print(o.name)
#</OPERATORS>

