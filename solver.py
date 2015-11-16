import random
from collections import deque
import itertools
import copy


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

    def get_locations(self):
        return {x:self.board.get_card_pos(x) if self.board.get_card_pos(x) >= 0
                else None for x in ['A','K','Q']}

    def solver_logic(self):
        #self.board.display_board()
        board_loc = self.get_locations()
        if self.board.get_board_length() == 3:
            if board_loc['Q'] == 0 and board_loc['K'] == 1:
                self.board.move_piece_left(board_loc['K'])
            else:
                self.board.move_piece_left((board_loc['Q']-1)%3)
        elif self.board.get_board_length() == 2:
            if board_loc['K'] == 0 and board_loc['A'] == 2:
                self.board.move_piece_right(2)
            else:
                self.board.move_piece_left((self.board.get_card_pos('_') + 1) % 3)
        else:
            if self.board.is_solved():
                return True
            else:
                top_card = [k for k,v in board_loc.iteritems() if v >= 0][0]
                self.board.move_piece_right(board_loc[top_card])

def run_program(locations):
    #print locations
    board = Board(locations)
    s = Solver(board)
    for x in xrange(100):
        if s.solver_logic():
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

def get_wambo_combos():
    return [[3,0,0],[2,1,0],[1,2,0],[1,1,1]]

def make_boards(perm):
    return reduce(lambda a,x: a+x, (gen_boards(list(perm), combo) for
                                    combo in get_wambo_combos()))

def gen_boards(perm, combo):
    board = [deque(['_']),deque(['_']),deque(['_'])]
    for ind, num_com in enumerate(combo):
        while num_com:
            board[ind].appendleft(perm.pop())
            num_com -= 1
    # if 1,1,1 no need to rotate
    if all(map(lambda x: len(x)==2, board)):
        #return list of board, because later flatten
        return [board]
    return [rotate_boards(board, x) for x in xrange(3)]

def rotate_boards(board, n):
    return board[-n:] + board[:-n]


if __name__ == '__main__':
    for test in gen_all_tests():
        print test
        if run_program(copy.deepcopy(test)):
            print 'Solved'
        else:
            print 'Failed'
    print
    #for x in gen_all_tests():
    #    print x
