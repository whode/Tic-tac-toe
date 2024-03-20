import random

class TicTacToe:
    FREE_CELL = 0
    HUMAN_X = 1
    COMPUTER_O = 2
    
    def __init__(self, area_size = 3):
        self.pole = tuple(tuple(Cell() for j in range(area_size)) for i in range(area_size))
        self._area_size = area_size
        self._count = area_size * area_size
        
    def verify_coords(self, coords):
        return all(0 <= i <= self._area_size - 1 and type(i) is int for i in coords) and len(coords) == 2
        
    def __getitem__(self, item):
        if not self.verify_coords(item):
            raise IndexError('Invalid indices')
        return self.pole[item[0]][item[1]]
    
    def __setitem__(self, key, value):
        if not self.verify_coords(key):
            raise IndexError('Invalid indices')
        pole = [[i for i in row] for row in self.pole]
        pole[key[0]][key[1]] = Cell(value)
        self.pole = tuple(tuple(i for i in row) for row in pole)
        
    def __bool__(self):
        return bool(self._count)
        
    def reset(self):
        self.__init__()
        
    def show(self):
        print('   ' + ' '.join(map(str, range(self._area_size))))
        for i in range(self._area_size):
            print(i, end = ' ')
            print('|', end = '')
            print(*self.pole[i], sep = '|', end = '')
            print('|')
    
    def make_coords(self, coords_string):
        if len(coords_string) != 2:
            return False
        try:
            coords = tuple(map(int, (coords_string[0], coords_string[1])))
            if self.verify_coords(coords):
                return coords
            else:
                return False
        except:
            return False
            
    def human_go(self):
        user_input = input('Enter the coordinates of the cell: ')
        if not user_input:
            self._count = 0
            return False
        coords = self.make_coords(user_input)
        while True:
            if not coords:
                print('Coordinates entered incorrectly!')
            elif not self[coords]:
                print('This cell is already occupied!')
            else:
                break
            user_input = input('Enter the coordinates of the cell: ')
            if not user_input:
                self._count = 0
                return False
            coords = self.make_coords(user_input)
        self[coords] = self.HUMAN_X
        self._count -= 1
        return True
            
    def computer_go(self):
        while True:
            coords = random.randint(0, self._area_size - 1), random.randint(0, self._area_size - 1)
            if self[coords]:
                self[coords] = self.COMPUTER_O
                break
        self._count -= 1
        return True
    
    def is_someone_win(self, value):
        for i in range(self._area_size):
            if all(self[i, j] == value for j in range(self._area_size)):
                return True
            if all(self[j, i] == value for j in range(self._area_size)):
                return True
        if all(self[i, i] == value for i in range(self._area_size)):
            return True
        if all(self[i, j] == value for i, j in zip(range(self._area_size), range(self._area_size - 1, -1, -1))):
            return True
        return False
    
    @property
    def is_human_win(self):
        status = self.is_someone_win(self.HUMAN_X)
        if status:
            self._count = 0
            return True
        else:
            return False
    
    @property
    def is_computer_win(self):
        status = self.is_someone_win(self.COMPUTER_O)
        if status:
            self._count = 0
            return True
        else:
            return False
    
    @property
    def is_draw(self):
        return not self.is_human_win and not self.is_computer_win

class Cell:
    def __init__(self, value = TicTacToe.FREE_CELL):
        self.value = value
        
    def __bool__(self):
        return not self.value
    
    def __repr__(self):
        if self.value == TicTacToe.FREE_CELL:
            return ' '
        elif self.value == TicTacToe.HUMAN_X:
            return 'x'
        else:
            return 'o'
        
    def __eq__(self, other):
        return self.value == other

def make_size(size_string):
    if size_string.isdigit() and 2 < int(size_string) < 11:
        return int(size_string)
    else:
        False

while True:
    user_input = input('Choose the size of the board from 3 to 10, or press Enter to quit: ')
    if not user_input:
        break
    f = False
    while True:
        area_size = make_size(user_input)
        if area_size:
            break
        print('The board size is incorrect!')
        user_input = input('Choose the size of the board from 3 to 10, or press Enter to quit: ')
        if not user_input:
            f = True
            break
    if f:
        break
            
    game = TicTacToe(area_size)
    print('Game on! Enter the coordinates of the points without spaces. If you want to quit the game, just press Enter.')
    step_game = random.randint(0, 1)
    if step_game:
        status = game.computer_go()
        game.show()
    else:
        game.show()
        status = game.human_go()
    if not status:
        print('Game over.')
    
    step_game += 1

    while game:
        status = [game.human_go, game.computer_go][step_game % 2]()
        if not status:
            print('Game over.')
            break
        if step_game % 2:
            game.show()
        if game.is_human_win:
            game.show()
            print('You win!')
        elif game.is_computer_win:
            print('Computer won :(')
        step_game += 1

    if game.is_draw and status:
        print('Draw!')
        
    game.reset()
    
    status = input('Do you want to start a new game? (Y/N): ').lower()
    if status != 'y':
        break
