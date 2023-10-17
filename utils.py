# Function to print the board.
# Takes the board positions list as a parameter.
from copy import deepcopy


def printBoard(board, mill_board_state):
    player = "W"
    AI = "B"
    empty = " "
    print(" " * 7, end="")
    print(*list(range(9)), sep=" " * 10)
    print("   ", end="")
    print("_" * 98)
    for col in range(9):
        print(str(col) + "  ", end="")
        for row in range(9):
            if mill_board_state[col * 9 + row * 1] == True:
                mill = "(M)"
            else:
                mill = "  "

            if board[col * 9 + row * 1] == "1":
                color = player
            elif board[col * 9 + row * 1] == "2":
                color = AI
            else:
                color = " "

            print(f"{color:^5}{mill:^5}|", end="")
        print("")
        print("   ", end="")
        print("_" * 98)


# Function to find adjacent locations for a given location.
# Returns a list of adjacent location


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


# Function to check if a player can make a mill in the next move.
# Return True if the player can create a mill
def checkNextMill(position, board, player, mill_board_state):
    # potential_mills: list of all possible mills in that "position"
    # potential_mills[index]: the three position of one possible mill.

    potential_mills = []
    row = position // 9
    col = position % 9

    if 0 < col < 8 and all(
        board[mill_p] == player and not mill_board_state[mill_p]
        for mill_p in [position, position - 1, position + 1]
    ):
        potential_mills.append([position, position - 1, position + 1])

    if 0 < row < 8 and all(
        board[mill_p] == player and not mill_board_state[mill_p]
        for mill_p in [position, position - 9, position + 9]
    ):
        potential_mills.append([position, position - 9, position + 9])

    if col > 1 and all(
        board[mill_p] == player and not mill_board_state[mill_p]
        for mill_p in [position, position - 2, position - 1]
    ):
        potential_mills.append([position, position - 2, position - 1])

    if col < 7 and all(
        board[mill_p] == player and not mill_board_state[mill_p]
        for mill_p in [position, position + 1, position + 2]
    ):
        potential_mills.append([position, position + 1, position + 2])

    if row > 1 and all(
        board[mill_p] == player and not mill_board_state[mill_p]
        for mill_p in [position, position - 2 * 9, position - 1 * 9]
    ):
        potential_mills.append([position, position - 2 * 9, position - 1 * 9])

    if row < 7 and all(
        board[mill_p] == player and not mill_board_state[mill_p]
        for mill_p in [position, position + 1 * 9, position + 2 * 9]
    ):
        potential_mills.append([position, position + 1 * 9, position + 2 * 9])

    selected_mill = None
    if len(potential_mills) > 1:
        # selected_mill = ui.get_mill_choice_input(potential_mills)
        selected_mill = potential_mills[0]
    elif len(potential_mills):
        selected_mill = potential_mills[0]
    if selected_mill:
        for piece in selected_mill:
            mill_board_state[piece] = True
        return True
    return False


# if player breaks a mill, in that "position", update the mill_board_state
def checkDeletetMill(position, board, player, mill_board_state):
    potential_mills = []
    row = position // 9
    col = position % 9

    if 0 < col < 8 and all(
        board[mill_p] == player and mill_board_state[mill_p]
        for mill_p in [position, position - 1, position + 1]
    ):
        potential_mills.append([position, position - 1, position + 1])

    if 0 < row < 8 and all(
        board[mill_p] == player and mill_board_state[mill_p]
        for mill_p in [position, position - 9, position + 9]
    ):
        potential_mills.append([position, position - 9, position + 9])

    if col > 1 and all(
        board[mill_p] == player and mill_board_state[mill_p]
        for mill_p in [position, position - 2, position - 1]
    ):
        potential_mills.append([position, position - 2, position - 1])

    if col < 7 and all(
        board[mill_p] == player and mill_board_state[mill_p]
        for mill_p in [position, position + 1, position + 2]
    ):
        potential_mills.append([position, position + 1, position + 2])

    if row > 1 and all(
        board[mill_p] == player and mill_board_state[mill_p]
        for mill_p in [position, position - 2 * 9, position - 1 * 9]
    ):
        potential_mills.append([position, position - 2 * 9, position - 1 * 9])

    if row < 7 and all(
        board[mill_p] == player and mill_board_state[mill_p]
        for mill_p in [position, position + 1 * 9, position + 2 * 9]
    ):
        potential_mills.append([position, position + 1 * 9, position + 2 * 9])

    selected_mill = None
    if len(potential_mills) > 1:
        # selected_mill = ui.get_mill_choice_input(potential_mills)
        selected_mill = potential_mills[0]
    elif len(potential_mills):
        selected_mill = potential_mills[0]
    if selected_mill:
        for piece in selected_mill:
            mill_board_state[piece] = False

    return mill_board_state


# Return True if a player can form a "new" mill on the given position
# Each position has an index
def isMill(position, board, mill_board_state):
    p = board[position]
    # The player on that position
    if p != "x":
        # If there is some player on that position
        return checkNextMill(position, board, p, mill_board_state)
    else:
        return False


# Function to return number of pieces owned by a player on the board.
# value is '1' or '2' (player number)
def numOfPieces(board, value):
    return board.count(value)


##if a player form a mill
# check whether there is a piece of opponent that doesn't form a mill which is possible to remove.
def check_No_Removable_Pieces(board, mill_board_state):
    all_opponent_pos = [i for i in range(len(board)) if board[i] == "2"]
    all_possible_remove_opponent_pos = [
        j for j in all_opponent_pos if mill_board_state[j] == False
    ]
    if len(all_possible_remove_opponent_pos) == 0:
        return True


# Function to remove a piece from the board.
# Takes a copy of the board, current positions,
# and player number as input.
# If the player is 1, then a piece of player 2 is removed, and vice versa
def removePiece(
    board_copy, board_list, player, mill_board_state_copy, mill_board_state_list, stage
):
    for i in range(len(board_copy)):
        if player == "1":
            opp = "2"
        else:
            opp = "1"

        if stage != 3 and board_copy[i] == opp:
            if not mill_board_state_copy[i] == True:
                new_board = deepcopy(
                    board_copy
                )  # boad_copy would not be affected when new_board changes
                new_board[i] = "x"
                # Making a new board and emptying the position where piece is removed
                board_list.append(new_board)
                mill_board_state_list.append(mill_board_state_copy)

        if stage == 3 and board_copy[i] == opp:
            new_board = deepcopy(
                board_copy
            )  # boad_copy would not be affected when new_board changes
            new_board[i] = "x"
            # Making a new board and emptying the position where piece is removed
            mill_board_state_copy = checkDeletetMill(
                i, board_copy, opp, mill_board_state_copy
            )
            board_list.append(new_board)
            mill_board_state_list.append(mill_board_state_copy)
    return board_list, mill_board_state_list


#####################################################################
### ALL FUNCTIONS NECESSARY FOR AI:


# Generating all possible moves for stage 1 of the game.
# That is, when the players are still placing their pieces.
def possibleMoves_stage1(board, mill_board_state):
    stage = 1
    board_list = []
    mill_board_state_list = []
    for i in range(len(board)):
        # Fill empty positions with player 1
        if board[i] == "x":
            # Creating a clone of the current board
            # and removing pieces if a Mill can be formed
            board_copy = deepcopy(board)
            board_copy[i] = "1"
            mill_board_state_copy = deepcopy(mill_board_state)

            if isMill(i, board_copy, mill_board_state_copy):
                # Remove a piece if a mill is formed on that position
                ## player 1 form a mill and remove a piece of player 2

                No_removable_pieces = check_No_Removable_Pieces(
                    board_copy, mill_board_state_copy
                )

                if No_removable_pieces:
                    board_list.append(board_copy)
                    mill_board_state_list.append(mill_board_state_copy)

                else:
                    board_list, mill_board_state_list = removePiece(
                        board_copy,
                        board_list,
                        "1",
                        mill_board_state_copy,
                        mill_board_state_list,
                        stage,
                    )
            else:
                # No mill, so just append the position
                board_list.append(board_copy)
                mill_board_state_list.append(mill_board_state_copy)

    return board_list, mill_board_state_list


# Generating all possible moves for stage 2 of the game
# That is, when both players have placed all their pieces
from copy import deepcopy


def possibleMoves_stage2(board, player, mill_board_state):
    stage = 2
    board_list = []
    mill_board_state_list = []
    for i in range(len(board)):
        if board[i] == player:
            adjacent_list = adjacentLocations(i)

            for pos in adjacent_list:
                if board[pos] == "x":
                    # If the location is empty, then the piece can move there
                    # Hence, generating all possible combinations
                    board_copy = deepcopy(board)
                    mill_board_state_copy = deepcopy(mill_board_state)
                    # check the mill condition before delete the piece in i position
                    mill_board_state_copy = checkDeletetMill(
                        i, board_copy, player, mill_board_state_copy
                    )

                    board_copy[i] = "x"
                    # Emptying the current location, moving the piece to new position
                    board_copy[pos] = player
                    # print("Move", i, "to", pos)

                    if isMill(pos, board_copy, mill_board_state_copy):
                        # in case of mill, remove Piece
                        No_removable_pieces = check_No_Removable_Pieces(
                            board_copy, mill_board_state_copy
                        )

                        if No_removable_pieces:
                            board_list.append(board_copy)
                            mill_board_state_list.append(mill_board_state_copy)

                        else:
                            board_list, mill_board_state_list = removePiece(
                                board_copy,
                                board_list,
                                player,
                                mill_board_state_copy,
                                mill_board_state_list,
                                stage,
                            )
                    else:
                        board_list.append(board_copy)
                        mill_board_state_list.append(mill_board_state_copy)
    return board_list, mill_board_state_list


# Generating all possible moves for stage 3 of the game
# That is, when one player has only 3 pieces
def possibleMoves_stage3(board, player, mill_board_state):
    stage = 3
    board_list = []
    mill_board_state_list = []

    for i in range(len(board)):
        if board[i] == player:
            for j in range(len(board)):
                if board[j] == "x":
                    board_copy = deepcopy(board)
                    mill_board_state_copy = deepcopy(mill_board_state)
                    # check the mill condition before delete the piece in i position
                    mill_board_state_copy = checkDeletetMill(
                        i, board_copy, player, mill_board_state_copy
                    )
                    # The piece can fly to any empty position, not only adjacent ones
                    # So, generating all possible positions for the pieces
                    board_copy[i] = "x"
                    board_copy[j] = player

                    if isMill(j, board_copy, mill_board_state_copy):
                        # No_removable_pieces = check_No_Removable_Pieces(
                        #     board_copy, mill_board_state_copy
                        # )

                        # if No_removable_pieces:
                        #     board_list.append(board_copy)
                        #     mill_board_state_list.append(mill_board_state_copy)
                        # else:

                        # If a Mill is formed, remove piece
                        board_list, mill_board_state_list = removePiece(
                            board_copy,
                            board_list,
                            player,
                            mill_board_state_copy,
                            mill_board_state_list,
                            stage,
                        )
                    else:
                        board_list.append(board_copy)
                        mill_board_state_list.append(mill_board_state_copy)

    return board_list, mill_board_state_list


# Checks if game is in stage 2 or 3
# Returns possible moves accordingly
def possibleMoves_stage2or3(board, player, mill_board_state):
    if numOfPieces(board, "1") > 3 and numOfPieces(board, "2") > 3:
        return possibleMoves_stage2(board, player, mill_board_state)
    else:
        return possibleMoves_stage3(board, player, mill_board_state)


# Class to check if the game is completed, and who won
class evaluate:
    def __init__(self):
        self.evaluate = 0
        self.board = []
        self.mill_board_state = []


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


# Function to generate inverted board lists from a list of board_ state.
def generateInvertedBoardList(possible_configs_board, possible_configs_mill):
    result = []
    # i: a board_state
    for i in possible_configs_board:
        result.append(InvertedBoard(i))
    return result, possible_configs_mill


# change stage1 stage 2 in maximizer and minimizer
# Our main function to find solutions for the Game. Uses MiniMax algorithm.
def minimax(
    board, mill_board_state, depth, player1, alpha, beta, isStage1, heuristic, isStage3
):
    finalEvaluation = evaluate()
    if depth == 0:
        finalEvaluation.evaluate = heuristic(board, isStage1, mill_board_state)

    elif depth != 0:
        currentEvaluation = evaluate()

        if player1:
            if isStage1:
                possible_configs_board, possible_configs_mill = possibleMoves_stage1(
                    board, mill_board_state
                )

            else:
                possible_configs_board, possible_configs_mill = possibleMoves_stage2or3(
                    board, "1", mill_board_state
                )

        else:
            if isStage1:
                possible_configs_board, possible_configs_mill = possibleMoves_stage1(
                    InvertedBoard(board), mill_board_state
                )
                (
                    possible_configs_board,
                    possible_configs_mill,
                ) = generateInvertedBoardList(
                    possible_configs_board, possible_configs_mill
                )

            else:
                possible_configs_board, possible_configs_mill = possibleMoves_stage2or3(
                    InvertedBoard(board), "1", mill_board_state
                )
                (
                    possible_configs_board,
                    possible_configs_mill,
                ) = generateInvertedBoardList(
                    possible_configs_board, possible_configs_mill
                )

        movablePieces = len(possible_configs_board)
        ###
        if player1:  ## ismaximizing player
            if isStage1:
                maxEva = float("-inf")
                for move, new_mill_board_state in zip(
                    possible_configs_board, possible_configs_mill
                ):
                    currentEvaluation = minimax(
                        move,
                        new_mill_board_state,
                        depth - 1,
                        False,
                        alpha,
                        beta,
                        isStage1,
                        heuristic,
                        isStage3,
                    )

                    if currentEvaluation.evaluate > maxEva:
                        maxEva = currentEvaluation.evaluate
                        finalEvaluation.evaluate = currentEvaluation.evaluate
                        finalEvaluation.board = move
                        finalEvaluation.mill_board_state = new_mill_board_state

                    alpha = max(currentEvaluation.evaluate, alpha)

                    if beta <= alpha:
                        break
            else:
                if numOfPieces(board, "1") < 3 or movablePieces == 0:
                    finalEvaluation.evaluate = float("-inf")

                elif numOfPieces(board, "2") < 3:
                    finalEvaluation.evaluate = float("inf")

                else:
                    maxEva = float("-inf")
                    for move, new_mill_board_state in zip(
                        possible_configs_board, possible_configs_mill
                    ):
                        if isStage3:
                            currentEvaluation = minimax(
                                move,
                                new_mill_board_state,
                                0,
                                False,
                                alpha,
                                beta,
                                isStage1,
                                heuristic,
                                isStage3,
                            )
                        else:
                            currentEvaluation = minimax(
                                move,
                                new_mill_board_state,
                                depth - 1,
                                False,
                                alpha,
                                beta,
                                isStage1,
                                heuristic,
                                isStage3,
                            )

                        if currentEvaluation.evaluate > maxEva:
                            maxEva = currentEvaluation.evaluate
                            finalEvaluation.evaluate = currentEvaluation.evaluate
                            finalEvaluation.board = move
                            finalEvaluation.mill_board_state = new_mill_board_state

                        alpha = max(currentEvaluation.evaluate, alpha)

                        if beta <= alpha:
                            break

        else:
            if isStage1:
                minEva = float("inf")

                for move, new_mill_board_state in zip(
                    possible_configs_board, possible_configs_mill
                ):
                    currentEvaluation = minimax(
                        move,
                        new_mill_board_state,
                        depth - 1,
                        True,
                        alpha,
                        beta,
                        isStage1,
                        heuristic,
                        isStage3,
                    )

                    if currentEvaluation.evaluate < minEva:
                        minEva = currentEvaluation.evaluate
                        finalEvaluation.evaluate = currentEvaluation.evaluate
                        finalEvaluation.board = move
                        finalEvaluation.mill_board_state = new_mill_board_state

                    beta = min(currentEvaluation.evaluate, beta)
                    if beta <= alpha:
                        break
            else:
                if numOfPieces(board, "1") < 3 or movablePieces == 0:
                    finalEvaluation.evaluate = float("-inf")

                elif numOfPieces(board, "2") < 3:
                    finalEvaluation.evaluate = float("inf")

                else:
                    minEva = float("inf")

                    for move, new_mill_board_state in zip(
                        possible_configs_board, possible_configs_mill
                    ):
                        if isStage3:
                            currentEvaluation = minimax(
                                move,
                                new_mill_board_state,
                                0,
                                False,
                                alpha,
                                beta,
                                isStage1,
                                heuristic,
                                isStage3,
                            )
                        else:
                            currentEvaluation = minimax(
                                move,
                                new_mill_board_state,
                                depth - 1,
                                False,
                                alpha,
                                beta,
                                isStage1,
                                heuristic,
                                isStage3,
                            )

                        if currentEvaluation.evaluate < minEva:
                            minEva = currentEvaluation.evaluate
                            finalEvaluation.evaluate = currentEvaluation.evaluate
                            finalEvaluation.board = move
                            finalEvaluation.mill_board_state = new_mill_board_state

                        beta = min(currentEvaluation.evaluate, beta)
                        if beta <= alpha:
                            break

    return finalEvaluation


# HEURISTICS:

# Heuristic that finds number of pieces on the board.
# Lose if the player has less than  3 pieces.


def numPiecesHeuristic(board, isStage1, mill_board_state):
    if not isStage1:
        movablePieces = len(
            possibleMoves_stage2or3(board, "1", mill_board_state)
        )  # player 1 的possible_move
        if numOfPieces(board, "1") < 3 or movablePieces == 0:
            evaluation = float("-inf")
        elif numOfPieces(board, "2") < 3:
            evaluation = float("inf")
        else:
            evaluation = 2 * (numOfPieces(board, "1") - numOfPieces(board, "2"))
    else:
        evaluation = 1 * (numOfPieces(board, "1") - numOfPieces(board, "2"))

    return evaluation


def numMillandPiecesHeuristic(board, isStage1, mill_board_state):
    numMillsPlayer1 = Mill_count(board, "1", mill_board_state)
    numMillsPlayer2 = Mill_count(board, "2", mill_board_state)
    # numPossibleMillsPlayer1 = potentialMill_count(board, "1", mill_board_state)
    # numPossibleMillsPlayer2 = potentialMill_count(board, "2", mill_board_state)

    if not isStage1:
        movablePieces = len(possibleMoves_stage2or3(board, "1", mill_board_state))
        if numOfPieces(board, "1") < 3 or movablePieces == 0:
            evaluation = float("-inf")
        elif numOfPieces(board, "2") < 3:
            evaluation = float("inf")
        else:
            evaluation = (
                2 * (numOfPieces(board, "1") - numOfPieces(board, "2"))
                + numMillsPlayer1
                - numMillsPlayer2
                # + numPossibleMillsPlayer1
                # - numPossibleMillsPlayer2
            )
    else:
        evaluation = (
            1 * (numOfPieces(board, "1") - numOfPieces(board, "2"))
            + numMillsPlayer1
            - numMillsPlayer2
            # + numPossibleMillsPlayer1
            # - numPossibleMillsPlayer2
        )

    return evaluation


# not use
# Heuristic that calculates potential mills as the factor.
def potentialMillsHeuristic(board, isStage1, mill_board_state):
    evaluation = 0

    numPossibleMillsPlayer1 = potentialMill_count(board, "1", mill_board_state)
    numPossibleMillsPlayer2 = potentialMill_count(board, "2", mill_board_state)
    numMillsPlayer1 = Mill_count(board, "1", mill_board_state)
    numMillsPlayer2 = Mill_count(board, "2", mill_board_state)

    if not isStage1:
        movablePieces = len(possibleMoves_stage2or3(board, "1", mill_board_state))

    if not isStage1:
        if numOfPieces(board, "1") < 3 or movablePieces == 0:
            evaluation = float("-inf")
        elif numOfPieces(board, "2") < 3:
            evaluation = float("inf")
        else:
            if numOfPieces(board, "1") < 4:
                evaluation += 1 * numPossibleMillsPlayer1
                evaluation -= 2 * numPossibleMillsPlayer2
                evaluation += 2 * numMillsPlayer1
                evaluation -= 2 * numMillsPlayer2
            else:
                evaluation += 2 * numPossibleMillsPlayer1
                evaluation -= 1 * numPossibleMillsPlayer2
                evaluation += 2 * numMillsPlayer1
                evaluation -= 2 * numMillsPlayer2
    else:
        if numOfPieces(board, "1") < 4:
            evaluation += 1 * numPossibleMillsPlayer1
            evaluation += 2 * numPossibleMillsPlayer2
            evaluation += 2 * numMillsPlayer1
            evaluation -= 2 * numMillsPlayer2
        else:
            evaluation += 2 * numPossibleMillsPlayer1
            evaluation += 1 * numPossibleMillsPlayer2
            evaluation += 2 * numMillsPlayer1
            evaluation -= 2 * numMillsPlayer2

    return evaluation


# not use
def potentialMill_count(board, player, mill_board_state):
    count = 0
    for position in range(len(board)):
        if board[position] == "x":
            row = position // 9
            col = position % 9

            if 0 < col < 8 and all(
                board[mill_p] == player and mill_board_state[mill_p]
                for mill_p in [position - 1, position + 1]
            ):
                count += 1

            if 0 < row < 8 and all(
                board[mill_p] == player and mill_board_state[mill_p]
                for mill_p in [position - 9, position + 9]
            ):
                count += 1
            if col > 1 and all(
                board[mill_p] == player and mill_board_state[mill_p]
                for mill_p in [position - 2, position - 1]
            ):
                count += 1
            if col < 7 and all(
                board[mill_p] == player and mill_board_state[mill_p]
                for mill_p in [position + 1, position + 2]
            ):
                count += 1
            if row > 1 and all(
                board[mill_p] == player and mill_board_state[mill_p]
                for mill_p in [position - 2 * 9, position - 1 * 9]
            ):
                count += 1
            if row < 7 and all(
                board[mill_p] == player and mill_board_state[mill_p]
                for mill_p in [position + 1 * 9, position + 2 * 9]
            ):
                count += 1
    return count


def Mill_count(board, player, mill_board_state):
    count = 0
    for position in range(len(board)):
        if board[position] == player and mill_board_state[position] == True:
            count += 1
    return count
