import random
from collections import deque
import itertools



class Board(object):
    def __init__(self, board):
        self.board = board

    def is_solved(self):
        return self.board[0] == deque(['A','K','Q','_'])

    def display_board(self):
        print reduce(lambda a,x: [a[0] + x[0]], self.board)[0]

    def move_piece_left(self, loc):
        self.board[(loc-1)%3].appendleft(self.board[loc].popleft())

    def move_piece_right(self, loc):
        self.board[(loc+1)%3].appendleft(self.board[loc].popleft())

    def get_board_length(self):
        return len([x for x in self.board if len(x) > 1])

    #location or -1
    def get_card_pos(self, card):
        return reduce(lambda a,x: [a[0] + x[0]], self.board)[0].find(card)

class Solver(object):
    def __init__(self, board):
        self.board = board

    def is_not_solved(self):
        return not self.board.is_solved()

    def get_locations(self):
        return {x:self.board.get_card_pos(x) if self.board.get_card_pos(x) >= 0
                else None for x in ['A','K','Q']}

    def solver_logic(self):
        #self.board.display_board()
        board_length = self.board.get_board_length()
        board_loc = self.get_locations()
        if board_length == 3:
            if board_loc['Q'] == 0 and board_loc['K'] == 1:
                self.board.move_piece_left(board_loc['K'])
            else:
                self.board.move_piece_left((board_loc['Q']-1)%3)
            #if board_loc['Q'] == 0: #or board_loc['K'] == 0:
            #    self.board.move_piece_left(board_loc['K'])
            #else:
            #    self.board.move_piece_right(board_loc['A'])
        elif board_length == 2:
            if board_loc['K'] == 0 and board_loc['A'] == 2:
                self.board.move_piece_right(2)
            else:
                self.board.move_piece_left((self.board.get_card_pos('_') + 1) % 3)
            #if board_loc['Q'] == 1:
            #    self.board.move_piece_right(board_loc['Q'])
            #elif board_loc['Q'] == 2 and self.board.get_card_pos('_') == 0:
            #    self.board.move_piece_right(board_loc['Q'])
            #elif board_loc['K'] >= 1:
            #    self.board.move_piece_left(board_loc['K'])
            #elif board_loc['A'] >= 0:
            #    self.board.move_piece_right(board_loc['A'])
        else:
            if self.board.is_solved():
                return True
            elif board_loc['Q'] >= 0:
                self.board.move_piece_right(board_loc['Q'])
            elif board_loc['K'] >= 0:
                self.board.move_piece_right(board_loc['K'])
                #self.board.move_piece_left(board_loc['K'])
            else:
                self.board.move_piece_right(board_loc['A'])





def run_program(locations):
    print locations
    board = Board(locations)
    s = Solver(board)
    for x in xrange(25):
        if s.solver_logic():
            print 'Solved'
            return True
    return False

def gen_random_tests():
    board = (deque(['_']),deque(['_']),deque(['_']))
    cards = ['A','K','Q']
    random.shuffle(cards)
    for x in xrange(3):
        x = random.randint(0,2)
        board[x].appendleft(cards.pop())
    return board

def gen_all_tests():
    boards = reduce(lambda a,x :a+x,
                    map(make_boards, itertools.permutations(['A','K','Q'],3)))
    return boards

def make_boards(perm):
    boards = make_threes(perm)
    boards += make_flat(perm)
    boards += make_twos(perm)
    return boards

def make_threes(perm):
    boards = []
    for x in xrange(3):
        board = (deque(['_']),deque(['_']),deque(['_']))
        for y in perm:
            board[x].appendleft(y)
        boards.append(board)
    return boards

def make_flat(perm):
    return [tuple(map(lambda x:deque([x,'_']), perm))]

def make_twos(perm):
    boards = []
    for x in xrange(3):
        board = (deque(['_']),deque(['_']),deque(['_']))
        board[x].appendleft(perm[0])
        board[x].appendleft(perm[1])
        board[(x+1)%3].appendleft(perm[2])
        boards.append(board)
    return boards

if __name__ == '__main__':
    for test in gen_all_tests():
        result = run_program(test)
        if not result:
            print 'FAIL'
