import sched, time
import copy
from sense_hat import SenseHat
sense = SenseHat()


global scheduler
global pl_rotations
global pl_hoffsets

class block(object):
    def __init__(self, shape):
        self._shape = shape
        self._state = shape
        self._pl_hoffset = 0
        self._gm_voffset = 0
        self._color = (0,255,0)
        
    def __iter__(self):
        return iter(self._state)
        
    def advance_block(self):
        new_state = []
        for y,x in self._state:
            new_state.append((y+1,x))
        self._state = new_state
    
        #self._state = [(pixel[1],pixel[0]) for pixel in self._state]
    
#    def get_miny_perx():
#        dict_pixel = {}
#        for pixel in self._state:
#            if dict_pixel.exists()
#            dict_pixcel
    
    def turn_block(self):
        new_block = []
        for y, x in _state:
            new_block.append((x,-y))
        min_x = 0
        min_y = 0
        for y, x in new_block:
            if x < min_x:
                min_x = x
            if y < min_y:
                min_y = y
        x_offset = min_x * -1
        y_offset = min_y * -1
        updated_block = []
        for y, x in new_block:
            updated_block.append((y+y_offset,x+x_offset))
        self._state = updated_block
    

class board(object):
    def __init__(self):
        self._ROWS = 8
        self._COLS = 8
        self._HOFFSET = 3
        self._board = [[(255,255,255) for y in range(self._ROWS)] for x in range(self._COLS)]
        self._state = [[(255,255,255) for y in range(self._ROWS)] for x in range(self._COLS)]
        self._boolboard = [[0 for y in range(self._ROWS)] for x in range(self._COLS)]
        self._boolstate = [[0 for y in range(self._ROWS)] for x in range(self._COLS)]
    
    def register_game(self, game):
        self._game = game
    
    def initialize(self):
        self.draw()      

    def is_terminal(self,block):
        for y,x in block:
            if y == self._ROWS-1:
                return True
            if y < self._ROWS:
                if self._boolstate[y+1][x] == 1:
                    return True
        return False
    
    def is_tetris_state(self, block):

        return False
    
    def set_block(self, block):
        print("Setting Block to Board")
        self._board = copy.deepcopy(self._state)
        self._boolboard = copy.deepcopy(self._boolstate)
        for pixel in block:
            y,x = pixel
            self._board[y][x] = block._color
            self._boolboard[y][x] = 1
        
        # if block has hit floor then make it permanent else schedule next advance
        if self.is_terminal(block):
            self.update_state()
            self._game.schedule_new_block()
        else:
            self._game.schedule_update_block(block)

        if self.is_tetris_state(block):
            pass
        self.draw()
        
    def tetris(self):
        pass
        
    def update_state(self):
        self._state = copy.deepcopy(self._board)
        self._boolstate = copy.deepcopy(self._boolboard)
        
    
    def draw(self):
        for i in range(len(self._board)):
            for j in range(len(self._board[i])):
                sense.set_pixel(i,j, self._board[j][i])

class game(object):
    def __init__(self, board):
        print("Initialize game")
        self._board = board
        self._time_delay = 2
        self._scheduler = sched.scheduler(time.time, time.sleep)
        self._board.register_game(self)
        self._scheduler.enter(self._time_delay,1,self.intialize_game)
        self._scheduler.run()
        
    def intialize_game(self):
        self._board.initialize()
        self.schedule_new_block()
   
    def schedule_new_block(self):
        print("Generating new block")
        block = self.generate_block()
        print("Scheduling first block update")
        self._scheduler.enter(self._time_delay,1,self.set_board_block, kwargs={'block': block})

    def schedule_update_block(self, block):
        print("Advancing block one step")
        block.advance_block()
        self._scheduler.enter(self._time_delay,1,self.set_board_block, kwargs={'block': block})

    def set_board_block(self, block):
        self._board.set_block(block)

    def generate_block(self):
        jblock = [(0,0),(1,0),(1,1),(1,2)]
        new_block = block(jblock)
        return new_block

b = board()
g = game(b)




