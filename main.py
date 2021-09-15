
import functools
import sys
import threading



sys.setrecursionlimit(300000)

def set_bit(value, bit):
    return value | (1 << bit)


def clear_bit(value, bit):
    return value & ~(1 << bit)


# 000000000
# 000000001

# 000000001

winnerMasks = [0b111000000, 0b000111000, 0b000000111, 0b100100100, 0b010010010, 0b001001001, 0b100010001, 0b001010100]


def get_bit(value, bit):
    mask = 0b000000001

    mask = mask << bit

    return mask & value


def printBoard(board1, board2):
    f0, f1, f2, f3, f4, f5, f6, f7, f8 = "0" * 9

    if get_bit(board1, 0):
        f0 = "1"
    elif get_bit(board2, 0):
        f0 = "2"

    if get_bit(board1, 1):
        f1 = "1"
    elif get_bit(board2, 1):
        f1 = "2"

    if get_bit(board1, 2):
        f2 = "1"
    elif get_bit(board2, 2):
        f2 = "2"

    if get_bit(board1, 3):
        f3 = "1"
    elif get_bit(board2, 3):
        f3 = "2"

    if get_bit(board1, 4):
        f4 = "1"
    elif get_bit(board2, 4):
        f4 = "2"

    if get_bit(board1, 5):
        f5 = "1"
    elif get_bit(board2, 5):
        f5 = "2"

    if get_bit(board1, 6):
        f6 = "1"
    elif get_bit(board2, 6):
        f6 = "2"

    if get_bit(board1, 7):
        f7 = "1"
    elif get_bit(board2, 7):
        f7 = "2"

    if get_bit(board1, 8):
        f8 = "1"
    elif get_bit(board2, 8):
        f8 = "2"

    print(f8, f7, f6)
    print(f5, f4, f3)
    print(f2, f1, f0)


def check_for_win(board):
    for mask in winnerMasks:
        if mask & board == mask:
            return True

    return False


def check_for_draw(b1, b2):
    return (b1 | b2) == 0b111111111


def generate_children(board):
    for i in range(9):
        if not get_bit(board, i):
            yield i


def best_move(board1, board2, depth):
    if check_for_win(board1):
        return 12 - depth

    if check_for_win(board2):
        return -12 + depth

    if check_for_draw(board1, board2):
        return 0

    if depth == 9:
        print(str(board1) + "  " + str(board2) + "Depth Done")
        return 0

    bestScore = -100
    for child in generate_children(board1 | board2):
        childBoard = set_bit(board1, child)
        score = worst_move(childBoard, board2, depth + 1)
        bestScore = max(bestScore, score)
    return bestScore




def worst_move(board1, board2, depth):
    if check_for_win(board1):
        return 12 - depth

    if check_for_win(board2):
        return -12 + depth

    if check_for_draw(board1, board2):
        return 0

    if depth == 9:
        print("Depth Done")
        return 0

    worstScore = 100
    for child in generate_children(board1 | board2):
        childBoard = set_bit(board2, child)
        score = best_move(board1, childBoard, depth + 1)
        worstScore = min(worstScore, score)
    return worstScore


def get_next_move(b1, b2):


    bestScore = -100
    bestAction = None
    for child in generate_children(b1 | b2):
        childBoard = set_bit(b1, child)
        score = worst_move(childBoard, b2, 1)
        print("\n" + str(child) + ": " + str(score))
        if score > bestScore:
            bestScore = score
            bestAction = child

    result = set_bit(b1, bestAction)
    return result






gameRunning = True

player1board = 0b000000000
player2board = 0b000000000

# TODO: This is the tictactoe field
#           f8 f7 f6
#           f5 f4 f3
#           f2 f1 f0


printBoard(player1board, player2board)


def playerTurn():
    global player2board
    x = input("Enter a position (1 - 9; 1 is the top left corner)\n> ")
    boolean1 = False
    for child in generate_children(player2board | player1board):
        if str(9 - int(x)) == str(child):
            boolean1 = True

    if(boolean1):

        player2board = set_bit(player2board, 9 - int(x))
        printBoard(player1board, player2board)
        if not check_game_over():
            aiTurn()

    else:
        print("Invalid turn!")
        playerTurn()


def aiTurn(firstTurn=False):
    print("NickNackNoe is thinking...")
    global player1board
    boardBefore = player1board
    if not firstTurn:
        player1board = get_next_move(player1board, player2board)
        print("NicNacNoe made a move!")
        printBoard(player1board, player2board)
    else:
        player1board = set_bit(player1board, 4)
        print("NicNacNoe made a move!")
        printBoard(player1board, player2board)

    if not check_game_over():
        playerTurn()


def check_game_over():
    if check_for_win(player1board):
        print("NicNacNoe beat you this time.")
        gameRunning = False
        return True

    if check_for_win(player2board):
        print("You win! (Cheater!)")
        gameRunning = False
        return True

    if check_for_draw(player1board, player2board):
        print("Tie!")
        gameRunning = False
        return True

    return False



input1 = input("Who should start? (N = NicNacNoeAI, everything else = you)\n> ")
if input1 == "N" or input1 == "n":
    aiTurn(True)
else:
    playerTurn()

