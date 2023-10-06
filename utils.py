# Function to print the board.
# Takes the board positions list as a parameter.
from copy import deepcopy


def printBoard(board):
    # player = "\U0001F535"
    # AI = "\u26AA"
    player = "W"
    AI = "B"
    empty = " "
    print("    ", end="")
    print(*list(range(9)), sep="     ")
    print("   ", end="")
    print("_" * 54)
    for col in range(9):
        print(str(col) + "  ", end="")
        for row in range(9):
            if board[col * 9 + row * 1] == "1":
                color = player
            elif board[col * 9 + row * 1] == "2":
                color = AI
            else:
                color = " "

            print(f"{color:^5}|", end="")
        print("")
        print("   ", end="")
        print("_" * 54)


# Function to find adjacent locations for a given location.
# Returns a list of adjacent location


##改
def adjacentLocations(position):
    adjacent = [[] for _ in range(81)]
    for i in range(81):
        row = i // 9
        col = i % 9
        if col != 0:
            adjacent[i].append(i - 1)

        if col != 8:
            adjacent[i].append(i + 1)
        if row != 0:
            adjacent[i].append(i - 9)
        if row != 8:
            adjacent[i].append(i + 9)
    return adjacent[position]


# Function to check if 2 positions have the player on them
# Takes player symbol as input (1 or 2)
# Board list as input
# p1 and p2, the two positions
# Returns boolean values
def isPlayer(player, board, p1, p2):
    if board[p1] == player and board[p2] == player:
        return True
    else:
        return False


##改 for loop
# Function to check if a player can make a mill in the next move.
# Return True if the player can create a mill
def checkNextMill(position, board, player):
    mills_possible = [[] for _ in range(81)]
    for i in range(81):
        row = i // 9
        col = i % 9
        if col > 0 and col < 8:
            mills_possible[i].append([i - 1, i + 1])
        if row > 0 and row < 8:
            mills_possible[i].append([i - 9, i + 9])
        if col > 1:
            mills_possible[i].append([i - 2, i - 1])
        if col < 7:
            mills_possible[i].append([i + 1, i + 2])
        if row > 1:
            mills_possible[i].append([i - 2 * 9, i - 1 * 9])
        if row < 7:
            mills_possible[i].append([i + 1 * 9, i + 2 * 9])

    mill = [False for _ in range(81)]
    for i in range(81):
        for mill_possible in mills_possible[i]:
            if isPlayer(player, board, mill_possible[0], mill_possible[1]):
                mill[i] = True

    return mill[position]


# Return True if a player has a mill on the given position
# Each position has an index
def isMill(position, board):
    p = board[position]
    # The player on that position
    if p != "x":
        # If there is some player on that position
        return checkNextMill(position, board, p)
    else:
        return False


# Function to return number of pieces owned by a player on the board.
# value is '1' or '2' (player number)
def numOfPieces(board, value):
    return board.count(value)


## board list: possible remove
# Function to remove a piece from the board.
# Takes a copy of the board, current positions,
# and player number as input.
# If the player is 1, then a piece of player 2 is removed, and vice versa
def removePiece(board_copy, board_list, player):
    for i in range(len(board_copy)):
        if player == "1":
            opp = "2"
        else:
            opp = "1"
        if board_copy[i] == opp:
            if not isMill(i, board_copy):
                new_board = deepcopy(board_copy)
                new_board[i] = "x"
                # Making a new board and emptying the position where piece is removed
                board_list.append(new_board)
    return board_list


# Generating all possible moves for stage 1 of the game.
# That is, when the players are still placing their pieces.
def possibleMoves_stage1(board):
    board_list = []
    for i in range(len(board)):
        # Fill empty positions with player 1
        if board[i] == "x":
            # Creating a clone of the current board
            # and removing pieces if a Mill can be formed
            board_copy = deepcopy(board)
            board_copy[i] = "1"

            if isMill(i, board_copy):
                # Remove a piece if a mill is formed on that position
                board_list = removePiece(board_copy, board_list, "1")
            else:
                # No mill, so just append the position
                board_list.append(board_copy)

    return board_list


# Generating all possible moves for stage 2 of the game
# That is, when both players have placed all their pieces
def possibleMoves_stage2(board, player):
    board_list = []
    for i in range(len(board)):
        if board[i] == player:
            adjacent_list = adjacentLocations(i)

            for pos in adjacent_list:
                if board[pos] == "x":
                    # If the location is empty, then the piece can move there
                    # Hence, generating all possible combinations
                    board_copy = deepcopy(board)
                    board_copy[i] = "x"
                    # Emptying the current location, moving the piece to new position
                    board_copy[pos] = player

                    if isMill(pos, board_copy):
                        # in case of mill, remove Piece
                        board_list = removePiece(board_copy, board_list, player)
                    else:
                        board_list.append(board_copy)
    return board_list


# Generating all possible moves for stage 3 of the game
# That is, when one player has only 3 pieces
def possibleMoves_stage3(board, player):
    board_list = []

    for i in range(len(board)):
        if board[i] == player:
            for j in range(len(board)):
                if board[j] == "x":
                    board_copy = deepcopy(board)
                    # The piece can fly to any empty position, not only adjacent ones
                    # So, generating all possible positions for the pieces
                    board_copy[i] = "x"
                    board_copy[j] = player

                    if isMill(j, board_copy):
                        # If a Mill is formed, remove piece
                        board_list = removePiece(board_copy, board_list, player)
                    else:
                        board_list.append(board_copy)
    return board_list


# Checks if game is in stage 2 or 3
# Returns possible moves accordingly
def possibleMoves_stage2or3(board, player="1"):
    if numOfPieces(board, player) == 3:
        return possibleMoves_stage3(board, player)
    else:
        return possibleMoves_stage2(board, player)


# ALL FUNCTIONS NECESSARY FOR AI:


# Class to check if the game is completed, and who won
class evaluate:
    def __init__(self):
        self.evaluate = 0
        self.board = []


pruned = 0
states_reached = 0
alpha = float("-inf")
beta = float("inf")
depth = 2
ai_depth = 3


# Function to invert the board, to train the artificial intelligence
def InvertedBoard(board):
    invertedboard = []
    for i in board:
        if i == "1":
            invertedboard.append("2")
        elif i == "2":
            invertedboard.append("1")
        else:
            invertedboard.append("x")
    return invertedboard


# Function to generate inverted board lists from a list of positions.
def generateInvertedBoardList(pos_list):
    result = []
    for i in pos_list:
        result.append(InvertedBoard(i))
    return result


# Function to find possible mill counts for a certain player.
def getPossibleMillCount(board, player):
    count = 0

    for i in range(len(board)):
        if board[i] == "x":
            if checkNextMill(i, board, player):
                count += 1
    return count


# Function to find if a potential mill is in correct formation
# Return boolean values
def potentialMillInFormation(position, board, player):
    adjacent_list = adjacentLocations(position)

    for i in adjacent_list:
        if (board[i] == player) and (not checkNextMill(position, board, player)):
            return True
    return False


# Function to get how many pieces can potentially form a mill
def getPiecesInPotentialMillFormation(board, player):
    count = 0

    for i in range(len(board)):
        if board[i] == player:
            adjacent_list = adjacentLocations(i)
            for pos in adjacent_list:
                if player == "1":
                    if board[pos] == "2":
                        board[i] = "2"
                        if isMill(i, board):
                            count += 1
                        board[i] = player
                else:
                    if board[pos] == "1" and potentialMillInFormation(pos, board, "1"):
                        count += 1
    return count


# Our main function to find solutions for the Game. Uses MiniMax algorithm.
def minimax(board, depth, player1, alpha, beta, isStage1, heuristic):
    finalEvaluation = evaluate()

    global states_reached
    states_reached += 1

    if depth != 0:
        currentEvaluation = evaluate()

        if player1:
            if isStage1:
                possible_configs = possibleMoves_stage1(board)
                # print("p1:T, stage1:",possible_configs)
            else:
                possible_configs = possibleMoves_stage2or3(board)
                # print("p1:T, stage2/3:",possible_configs)

        else:
            if isStage1:
                possible_configs = generateInvertedBoardList(
                    possibleMoves_stage1(InvertedBoard(board))
                )
                # print("p1:F, stage1:",possible_configs)

            else:
                possible_configs = generateInvertedBoardList(
                    possibleMoves_stage2or3(InvertedBoard(board))
                )
                # print("p1:F, stage2/3:",possible_configs)

        for move in possible_configs:
            if player1:  ## ismaximizing player
                currentEvaluation = minimax(
                    move, depth - 1, False, alpha, beta, isStage1, heuristic
                )

                if currentEvaluation.evaluate > alpha:
                    alpha = currentEvaluation.evaluate
                    finalEvaluation.board = move
            else:
                currentEvaluation = minimax(
                    move, depth - 1, True, alpha, beta, isStage1, heuristic
                )

                if currentEvaluation.evaluate < beta:
                    beta = currentEvaluation.evaluate
                    finalEvaluation.board = move

        if player1:
            finalEvaluation.evaluate = alpha
        else:
            finalEvaluation.evaluate = beta

    else:
        if player1:
            finalEvaluation.evaluate = heuristic(board, isStage1)
        else:
            # finalEvaluation.evaluate = heuristic(
            #   InvertedBoard(board), isStage1)
            finalEvaluation.evaluate = heuristic(board, isStage1)

    return finalEvaluation


# HEURISTICS:

# Heuristic that finds number of pieces on the board.
# Lose if less than 3 pieces


def numPiecesHeuristic(board, isStage1):
    if not isStage1:
        movablePieces = len(possibleMoves_stage2or3(board))  # player 1 的possible_move
        if numOfPieces(board, "1") < 3 or movablePieces == 0:
            evaluation = float("-inf")  ## change inf to -inf
            # print("#p1<=3 or m==0","eva:",evaluation,"p1: ",numOfPieces(board, '1'),"p2: ",numOfPieces(board, '2'))
        elif numOfPieces(board, "2") < 3:
            evaluation = float("inf")  ##change -inf to inf
            # print("#p2<=3","eva:",evaluation,"p1: ",numOfPieces(board, '1'),"p2: ",numOfPieces(board, '2'))
        else:
            evaluation = 2 * (numOfPieces(board, "1") - numOfPieces(board, "2"))
            # print("#stage 2","eva:",evaluation,"p1: ",numOfPieces(board, '1'),"p2: ",numOfPieces(board, '2'))
    else:
        evaluation = 1 * (numOfPieces(board, "1") - numOfPieces(board, "2"))
        # print("#stage 1","eva:",evaluation,"p1: ",numOfPieces(board, '1'),"p2: ",numOfPieces(board, '2'))

    return evaluation


# Heuristic that calculates potential mills as the factor.
def potentialMillsHeuristic(board, isStage1):
    evaluation = 0

    numPossibleMillsPlayer1 = getPossibleMillCount(board, "1")

    if not isStage1:
        movablePieces = len(possibleMoves_stage2or3(board))

    potentialMillsPlayer2 = getPiecesInPotentialMillFormation(board, "2")

    if not isStage1:
        if numOfPieces(board, "2") <= 2 or movablePieces == 0:
            evaluation = float("inf")
            # print("#p2<=2 or m==0","p1: ",numOfPieces(board, '1'),"p2: ",numOfPieces(board, '2'))
        elif numOfPieces(board, "1") <= 2:
            evaluation = float("-inf")
            # print("#p1<=2","p1: ",numOfPieces(board, '1'),"p2: ",numOfPieces(board, '2'))
        else:
            if numOfPieces(board, "1") < 4:
                evaluation += 1 * numPossibleMillsPlayer1
                evaluation += 2 * potentialMillsPlayer2
            else:
                evaluation += 2 * numPossibleMillsPlayer1
                evaluation += 1 * potentialMillsPlayer2
    else:
        if numOfPieces(board, "1") < 4:
            evaluation += 1 * numPossibleMillsPlayer1
            evaluation += 2 * potentialMillsPlayer2
        else:
            evaluation += 2 * numPossibleMillsPlayer1
            evaluation += 1 * potentialMillsPlayer2
    # print(evaluation)
    return evaluation
