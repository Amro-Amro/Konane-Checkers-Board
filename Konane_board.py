#Name: Amro Abu-atieh

import random

print('Hello, welcome to the Konane Game, this is the Hawaiian version of Checkers.')


def generate_board(an_int):
    '''First this function will see if the input is empty and if it is it will output
    and empty set. Then it will take an argument an_int, and go through an iteration to
    make a list full of all the numbers that are needed. '''
    if an_int <= 0:
        return []

    board_size = []
    for row in range(an_int):
        row_list = []
        for col in range(an_int):
            if (row + col) % 2 == 0:
                row_list.append(1)
            else:
                row_list.append(2)
        board_size.append(row_list)
    return board_size

def generate_board_r(an_int_row, an_int_col):
    '''This is the same as the last function, but the difference is that it takes two arguments,
    and with those  two arguments its goes in two for loops to print out a board with the
    qualifications of the width and the length.'''
    if an_int_row <= 0 or an_int_col <= 0:
        return []

    board_size = []
    for row in range(an_int_row):
        row_list = []
        for col in range(an_int_col):
            if (row + col) % 2 == 0:
                row_list.append(1)
            else:
                row_list.append(2)
        board_size.append(row_list)
    return board_size


def get_board_as_string(board):
    '''This function will take the board that you put in it, and will first check
    if its empty then it will go through all the numbers 1, and 2 in this list and based
    on the numbers it will print either a black dot or a white dot, and if empty nothing.'''
    if not board:
        return ''

    board_str = ''
    num_columns = len(board[0])
    header = ' '

    for i in range(num_columns):
        header += f' {i % 10}'
    header += '\n'

    board_str += header

    for row_board in range(len(board)):
        board_str += ' ' + '+-' * len(board[0]) + '+\n'
        board_str += f'{row_board % 10}|'
        for cell in board[row_board]:
            if cell == 1:
                board_str += '○|'
            elif cell == 2:
                board_str += '●|'
            else:
                board_str += ' |'
        board_str += '\n'
    board_str += ' ' + '+-' * len(board[0]) + '+'
    return board_str


def prep_board_human(board):
    '''This function first prints the board. This will then check if the input
    is valid. I purposely did value error, just in case someone puts letters into the
    program. I originally put first_removed equal to false, which allows for the code to interpert
    what to do, and what not to do. Then the program goes to the second input, and if it's in the
    board then it rteuns true. This will later be used to get valid inputs in general. '''
    print(get_board_as_string(board))

    first_removed = False
    while not first_removed:
        try:
            row1, col1 = map(int, input("Enter the first row and column to remove Ex) 1, 2): ").split(', '))
            if 0 < row1 < len(board) - 1 and 0 < col1 < len(board[0]) - 1 and board[row1][col1] != 0:
                board[row1][col1] = 0
                first_removed = True
            else:
                print("Invalid location. Try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    second_removed = False
    while not second_removed:
        try:
            row2, col2 = map(int,
                             input("Enter the second row and column to remove (must be a different color): ").split(', '))
            if (0 < row2 < len(board) - 1 and 0 < col2 < len(board[0]) - 1 and board[row2][col2] != 0
                    and (row1, col1) != (row2, col2) and board[row2][col2] != board[row1][col1]):
                board[row2][col2] = 0
                second_removed = True
            else:
                print("Invalid location or color. Try again.")
        except ValueError:
            print("Invalid input. Try again.")


def is_valid_move(board, move):
    '''This function will check if the move is valid, by taking the argument, and
    returning either true or false. I defined end, start and moves first, then checked if the
    move is in the new parameters I set. I then chekced the end and the middle, returning false
    if it's not on the board, or not a valid move to do.
    '''
    start, end, direction = move
    start_row, start_col = start
    end_row, end_col = end

    if not (0 <= start_row < len(board) and 0 <= start_col < len(board[0])):
        return False
    if not (0 <= end_row < len(board) and 0 <= end_col < len(board[0])):
        return False

    middle_row = (start_row + end_row) // 2
    middle_col = (start_col + end_col) // 2

    if board[end_row][end_col] != 0:
        return False
    if board[middle_row][middle_col] == 0 or board[middle_row][middle_col] == board[start_row][start_col]:
        return False

    return True

def get_valid_moves_for_stone(board, stone):
    '''This function will check for valid moves for the stones. If there are no
    stones then an empty list will be returned. For the term direction I made it 2 and
     not 1, because I wanted to allow for double jumps.'''
    valid_row, valid_col = stone
    player = board[valid_row][valid_col]
    directions = [(-2, 0), (2, 0), (0, -2), (0, 2)]
    valid_moves = []

    for d in directions:
        new_row = valid_row + d[0]
        new_col = valid_col + d[1]
        move = ((valid_row, valid_col), (new_row, new_col), d)
        if is_valid_move(board, move):
            valid_moves.append(move)
    return valid_moves


def get_valid_moves(board, player):
    '''This function will accept a board and an integer representing a "Black" or "White" player.
    The function will return a list of the valid moves for that player given the current
    board state.'''
    valid_moves = []
    for row in range(len(board)):
        for col in range(len(board[0])):
            if board[row][col] == player:
                stone_moves = get_valid_moves_for_stone(board, (row, col))
                valid_moves.extend(stone_moves)
    return valid_moves


def human_player(board, player):
    '''This function first prints the board as a string, then checks for valid moves with the
    get_valid_moves function. If it's not valid it executes an empty tuple. Next it goes into a while loop
    that executes until the game is finished. This while loop checks if the moves are valid, and
    makes sure the game runs smoothly'''
    print(get_board_as_string(board))
    valid_moves = get_valid_moves(board, player)
    possible_move = True

    if not valid_moves:
        return ()

    while True:
        try:
            start_row, start_col = map(int,
                                       input(f"Player {player}, choose the piece that you want to (row, column): ").split(', '))
            possible_moves = [move for move in valid_moves if move[0] == (start_row, start_col)]
            if possible_moves:
                possible_move = False
            else:
                print("Invalid selection. Please choose a piece with valid moves.")
        except ValueError:
            print("Invalid input. Please enter two integers separated by commas.")

    while True:
        try:
            end_row, end_col = map(int, input(f"Player {player}, choose where to jump to (row, column): ").split(', '))
            move = next(
                ((start, end, direction) for (start, end, direction) in possible_moves if end == (end_row, end_col)),
                None)
            if move:
                return move
            else:
                print("Invalid move. Choose a valid jump.")
        except ValueError:
            print("Invalid input. Please enter two integers separated by commas.")

def random_player(board, player):
    '''This function picks a random valid move, until there's no more moves..'''
    valid_moves = get_valid_moves(board, player)
    if valid_moves:
        return random.choice(valid_moves)
    return ()

def ai_player(board, player):
    '''This Ai,  is not the smartest, it just picks the first valid move for the
    given player.'''
    valid_moves = get_valid_moves(board, player)
    if valid_moves:
        return valid_moves[0]
    return ()

def first_move(board, player):
    '''First this function prints the board as a string. This function then asks for the first
    move from the player. This allows the game to flow easier. If the move is valid then the peice is
    removed otherwise the loop will continue, and the message will print out'''
    print(get_board_as_string(board))
    while True:
        try:
            row, col = map(int,
                           input(f"Player {player}, choose your first piece to remove (row, column): ").split(', '))
        except ValueError:
            print("Invalid input. Please enter two integers separated by a comma.")
            continue

        if (0 <= row < len(board) and 0 <= col < len(board[0])):
            if board[row][col] == player:
                board[row][col] = 0
                return
            else:
                print("Choose your piece, not the opponents piece.")
        else:
            print("Invalid location. Try again.")


def check_for_double_jump(board, player, move, direction):
    '''This function was added to make the double jump logic. Checks if a double jump is possible
     by first accesing the second element of the move tuple. Then the code checks of there is a valid
     second jump based on the position and the first move. '''
    new_row = move[1][0]
    new_col = move[1][1]

    possible_moves = get_valid_moves_for_stone(board, (new_row, new_col))
    for next_move in possible_moves:
        if next_move[2] == direction:
            return next_move
    return None


def play_game(ai_black, ai_white, board=None):
    '''This function will play a game with either human, random player or Ai. The function uses the arguments
    ai_black and ai_white to make sure the game runs smoothly no matter the piece you put. It first randomly picks
    between 1 and 2 When there are no more valid moves, the next player is the winner. The coe first checks for the first
    move then it goes into a while loop to allow the gam eto play on until there are no valid moves. Once
    in the while loop the function checks if a double jump is also possible. Then it finally checks for anymore
    moves and executes the winner.'''
    if board is None:
        board = generate_board(8)

    print(get_board_as_string(board))

    first_player = random.choice([1, 2])
    second_player = 3 - first_player  # The other player

    print(f"Player {first_player} goes first.")
    first_move(board, first_player)
    print(f"It's player {second_player}'s turn to remove a piece.")
    first_move(board, second_player)

    current_player = first_player

    while True:
        print(f"It's player {current_player}'s turn.")
        if current_player == 1:
            move = ai_black(board, current_player)
        else:
            move = ai_white(board, current_player)

        if not move:
            print(f"Player {3 - current_player} wins!")
            return 3 - current_player

        start, end, direction = move
        board[end[0]][end[1]] = board[start[0]][start[1]]
        board[start[0]][start[1]] = 0

        middle_row = (start[0] + end[0]) // 2
        middle_col = (start[1] + end[1]) // 2
        board[middle_row][middle_col] = 0

        print(get_board_as_string(board))

        next_move = check_for_double_jump(board, current_player, move, direction)
        if next_move:
            print(f"Player {current_player}, double jumped.")
            start, end, direction = next_move
            board[end[0]][end[1]] = board[start[0]][start[1]]
            board[start[0]][start[1]] = 0
            middle_row = (start[0] + end[0]) // 2
            middle_col = (start[1] + end[1]) // 2
            board[middle_row][middle_col] = 0
            print(get_board_as_string(board))

        if not get_valid_moves(board, 1) and not get_valid_moves(board, 2):
            print("There are no available moves for both players. Game over!")
            return

        current_player = 3 - current_player
