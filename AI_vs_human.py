from utils import *
from boardstate import BoardState
import sys


def AI_vs_human(heuristic, depth):
    boardstate = BoardState()
    board = boardstate.board
    # mill state of every position of board
    mill_board_state = boardstate.mill_board_state

    # the number of pieces of player and AI
    reserved_numOfPieces_player = 9
    reserved_numOfPieces_AI = 9

    evaluation = evaluate()

    # Stage 1 :place a piece
    round = 1
    for i in range(5):
        print("===Your Turn====")
        print("Round:", round)
        print("STAGE 1")
        print("*** Number of Player's Pieces:")
        print(
            "on the board:",
            numOfPieces(board, "1"),
            "reserve:",
            reserved_numOfPieces_player,
        )
        print()
        print("*** Number of AI's Pieces:")
        print(
            "on the board:",
            numOfPieces(board, "2"),
            "reserve:",
            reserved_numOfPieces_AI,
        )
        print()
        printBoard(board, mill_board_state)
        finished = False

        # TAKING USER INPUT FOR STAGE 1
        while not finished:
            try:
                print("\nPlace a piece: ")
                pos_x = int(input("x-coordinate (0-8): "))
                pos_y = int(input("y-coordinate (0-8): "))
                pos = pos_x + pos_y * 9

                if not (9 > pos_x >= 0 and 9 > pos_y >= 0):
                    print("Invalid position. Try again.")

                elif board[pos] == "x":
                    board[pos] = "1"
                    reserved_numOfPieces_player -= 1

                    # isMill function will update mill_board_state
                    if isMill(pos, board, mill_board_state):
                        itemPlaced = False
                        while not itemPlaced:
                            try:
                                print("Mill formed. Remove a '2' piece:")
                                No_removable_pieces = check_No_Removable_Pieces(
                                    board, mill_board_state
                                )

                                if No_removable_pieces:
                                    print(
                                        "****No removable pieces available on the board!***"
                                    )
                                    break

                                pos_x = int(input("x-coordinate (0-8): "))
                                pos_y = int(input("y-coordinate (0-8): "))
                                pos = pos_x + pos_y * 9

                                if not (9 > pos_x >= 0 and 9 > pos_y >= 0):
                                    print("Invalid position. Try again.")

                                elif board[pos] == "2":
                                    if mill_board_state[pos] == True:
                                        print(
                                            "The opponent formed a mill in this position!"
                                        )
                                    else:
                                        board[pos] = "x"
                                        itemPlaced = True

                                else:
                                    print("Invalid position. Try again.")

                            except Exception as e:
                                print(str(e))
                                print("Invalid input, Try again.")
                    finished = True

                    round += 1
                else:
                    print("There is a piece there already. Try again.")
            except Exception as e:
                print(str(e))
                print("Try again. Invalid input.")

        print("===AI Turn====")
        print("Round:", round)
        print("STAGE 1")

        print("*** Number of Player's Pieces:")
        print(
            "on the board:",
            numOfPieces(board, "1"),
            "reserve:",
            reserved_numOfPieces_player,
        )
        print()
        print("*** Number of AI's Pieces:")
        print(
            "on the board:",
            numOfPieces(board, "2"),
            "reserve:",
            reserved_numOfPieces_AI,
        )
        print()
        printBoard(board, mill_board_state)
        reserved_numOfPieces_AI -= 1

        alpha = float("-inf")
        beta = float("inf")
        evalBoard = minimax(
            board,
            mill_board_state,
            depth,
            False,
            alpha,
            beta,
            True,
            heuristic,
            False,
        )

        if evalBoard.evaluate == float("-inf"):
            print("AI turn stage1: YOU LOST!")
            print("Below is the final board state.")
            printBoard(evalBoard.board, evalBoard.mill_board_state)
            exit()
        else:
            # if the game doesn't end.Update the board and mill_board_state after the action of AI
            board = evalBoard.board
            mill_board_state = evalBoard.mill_board_state

    # Stage 2&3 :move a piece
    while round <= 300:
        print("===Your Turn====")
        print("Round:", round)

        if numOfPieces(board, "1") > 3 and numOfPieces(board, "2") > 3:
            stage = 2
            print("STAGE 2")
        else:
            stage = 3
            print("STAGE 3")

        print("*** Number of Player's Pieces:")
        print(
            "on the board:",
            numOfPieces(board, "1"),
            "reserve:",
            reserved_numOfPieces_player,
        )
        print()
        print("*** Number of AI's Pieces:")
        print(
            "on the board:",
            numOfPieces(board, "2"),
            "reserve:",
            reserved_numOfPieces_AI,
        )
        print()
        printBoard(board, mill_board_state)

        # TAKING USER INPUT FOR STAGE 2&3
        userMoved = False
        while not userMoved:
            try:
                print("\nMove a '1' piece: ")
                pos_x = int(input("x-coordinate (0-8): "))
                pos_y = int(input("y-coordinate (0-8): "))
                pos = pos_x + pos_y * 9

                no_empty_adjacent_pos = [
                    i for i in adjacentLocations(pos) if board[i] == "x"
                ]

                if not (9 > pos_x >= 0 and 9 > pos_y >= 0):
                    print("Invalid. Try again.")

                elif stage == 2 and len(no_empty_adjacent_pos) == 0:
                    print(
                        "This position doesn't have empty adjacent position. Try again."
                    )
                    continue

                else:
                    while board[pos] != "1":
                        print("Invalid. Try again.")
                        print("\nMove a '1' piece: ")
                        pos_x = int(input("x-coordinate (0-8): "))
                        pos_y = int(input("y-coordinate (0-8): "))
                        pos = pos_x + pos_y * 9

                        if not (9 > pos_x >= 0 and 9 > pos_y >= 0):
                            print("Invalid. Try again.")

                userPlaced = False

                while not userPlaced:
                    print("'1' New Location: ")
                    newpos_x = int(input("x-coordinate (0-8): "))
                    newpos_y = int(input("y-coordinate (0-8): "))
                    newpos = newpos_x + newpos_y * 9

                    if not (9 > newpos_x >= 0 and 9 > newpos_y >= 0):
                        print("Invalid position")

                    ##when stage is 2, check the new position that user want to move is adjacent
                    elif stage == 2 and newpos not in adjacentLocations(pos):
                        print("Not a adjacent Location")

                    elif board[newpos] == "x":
                        # checkDeletet function would lupdate mill_board_state if the user break the mill
                        mill_board_state = checkDeletetMill(
                            pos, board, "1", mill_board_state
                        )
                        board[pos] = "x"

                        board[newpos] = "1"
                        # isMill function will update mill_board_state
                        if isMill(newpos, board, mill_board_state):
                            userRemoved = False
                            while not userRemoved:
                                try:
                                    print("Mill formed. Remove a '2' piece:")

                                    if stage == 2:
                                        No_removable_pieces = check_No_Removable_Pieces(
                                            board, mill_board_state
                                        )

                                        if No_removable_pieces:
                                            print(
                                                "****No removable pieces available on the board!***"
                                            )
                                            break

                                    pos_x = int(input("x-coordinate (0-8): "))
                                    pos_y = int(input("y-coordinate (0-8): "))
                                    pos = pos_x + pos_y * 9
                                    if not (9 > pos_x >= 0 and 9 > pos_y >= 0):
                                        print("Invalid position")

                                    elif board[pos] == "2":
                                        if stage == 2:
                                            if mill_board_state[pos] == True:
                                                print(
                                                    "The opponent formed a mill in this position!"
                                                )
                                            else:
                                                mill_board_state = checkDeletetMill(
                                                    pos, board, "2", mill_board_state
                                                )
                                                board[pos] = "x"
                                                userRemoved = True

                                        if stage == 3:
                                            mill_board_state = checkDeletetMill(
                                                pos, board, "2", mill_board_state
                                            )
                                            board[pos] = "x"
                                            userRemoved = True

                                    else:
                                        print("Invalid position")
                                except Exception:
                                    print("Error while accepting input")
                        userPlaced = True
                        userMoved = True
                        round += 1

                    else:
                        print("Invalid Position. Try Again.")

            except Exception as e:
                print(str(e))
                print("Invalid entry. Try Again please.")

        if numOfPieces(board, "2") < 3:
            print("Your turn stage2&3: YOU WIN!!")
            print("Below is the final board state.")
            printBoard(board, mill_board_state)
            exit(0)

        print("===AI Turn====")
        print("Round:", round)
        if numOfPieces(board, "1") > 3 and numOfPieces(board, "2") > 3:
            stage = 2
            print("STAGE 2")
        else:
            stage = 3
            print("STAGE 3")

        print("*** Number of Player's Pieces:")
        print(
            "on the board:",
            numOfPieces(board, "1"),
            "reserve:",
            reserved_numOfPieces_player,
        )
        print()
        print("*** Number of AI's Pieces:")
        print(
            "on the board:",
            numOfPieces(board, "2"),
            "reserve:",
            reserved_numOfPieces_AI,
        )
        print()
        printBoard(board, mill_board_state)

        isStage3 = True if stage == 3 else False

        evaluation = minimax(
            board,
            mill_board_state,
            depth,
            False,
            alpha,
            beta,
            False,
            heuristic,
            isStage3,
        )

        if evaluation.evaluate == float("-inf"):
            print("AI turn stage 2&3: YOU LOST!")
            print("Below is the final board state.")
            printBoard(evaluation.board, evaluation.mill_board_state)
            exit(0)
        else:
            # if the game doesn't end.Update the board and mill_board_state after the action of AI
            board = evaluation.board
            mill_board_state = evaluation.mill_board_state

        if evaluation.evaluate == float("inf"):
            print("AI turn stage2&3: You WIN!")
            print("Below is the final board state.")
            printBoard(evaluation.board, evaluation.mill_board_state)
            exit(0)


if __name__ == "__main__":
    print("WELCOME TO AI VS HUMAN 9 MENS MORRIS")
    print()

    difficulty = ""

    # Ask the user for the game difficulty until the user enters 'quit' and the correct format of difficulty.
    while difficulty != "quit":
        difficulty = input(
            "Please choose difficulty( “1. easy, 2. medium 3. difficult”), or enter 'quit': "
        )
        if difficulty == "1":
            print("easy")
            AI_vs_human(numPiecesHeuristic, 1)

        elif difficulty == "2":
            print("medium")
            AI_vs_human(numPiecesHeuristic, 2)
            break
        elif difficulty == "3":
            print("difficult")
            AI_vs_human(numMillandPiecesHeuristic, 2)
            break
        else:
            print("error! Try again!")
# need check
# AI_vs_human(numMillandPiecesHeuristic, 1)
# AI_vs_human(numPiecesHeuristic, 1)
# AI_vs_human(numPiecesHeuristic, 2)
# check
# 3
# AI_vs_human(numMillandPiecesHeuristic, 2)
