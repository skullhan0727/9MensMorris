from utils import *


def AI_vs_human(heuristic):
    board = []
    ##改
    for i in range(81):
        board.append("x")

    evaluation = evaluate()

    print("STAGE 1")

    for i in range(9):
        printBoard(board)
        finished = False

        # TAKING USER INPUT FOR STAGE 1
        while not finished:
            try:
                # pos = int(input("\nPlace a piece: "))
                print("\nPlace a piece: ")
                pos_x = int(input("x-coordinate (0-9): "))
                pos_y = int(input("y-coordinate (0-9): "))
                pos = pos_x + pos_y * 9

                if board[pos] == "x":
                    board[pos] = "1"

                    if isMill(pos, board):
                        itemPlaced = False
                        while not itemPlaced:
                            try:
                                print("Mill formed. Remove a '2' piece:")
                                pos_x = int(input("x-coordinate (0-9): "))
                                pos_y = int(input("y-coordinate (0-9): "))
                                pos = pos_x + pos_y * 9
                                if (
                                    board[pos] == "2"
                                    and not isMill(pos, board)
                                    or (
                                        isMill(pos, board)
                                        and numOfPieces(board, "1") == 3
                                    )
                                ):
                                    board[pos] = "x"
                                    itemPlaced = True
                                else:
                                    print("Invalid position. Try again.")

                            except Exception as e:
                                print(str(e))
                                print("Invalid input, Try again.")
                    finished = True
                else:
                    print("There is a piece there already. Try again.")
            except Exception as e:
                print(str(e))
                print("Try again. Invalid input.")

        printBoard(board)
        evalBoard = minimax(board, depth, False, alpha, beta, True, heuristic)

        if evalBoard.evaluate == float("inf"):
            print("YOU LOST!")
            exit()
        else:
            board = evalBoard.board

    print("STAGE 2")
    while True:
        printBoard(board)
        # TAKING USER INPUT FOR STAGE 2

        print("Player start====================")
        userMoved = False
        while not userMoved:
            try:
                # pos = int(input("\nMove a '1' piece: "))
                print("\nMove a '1' piece: ")
                pos_x = int(input("x-coordinate (0-9): "))
                pos_y = int(input("y-coordinate (0-9): "))
                pos = pos_x + pos_y * 9

                while board[pos] != "1":
                    print("Invalid. Try again.")
                    print("\nMove a '1' piece: ")
                    pos_x = int(input("x-coordinate (0-9): "))
                    pos_y = int(input("y-coordinate (0-9): "))
                    pos = pos_x + pos_y * 9

                userPlaced = False

                while not userPlaced:
                    # newpos = int(input("'1' New Location: "))

                    print("'1' New Location: ")
                    newpos_x = int(input("x-coordinate (0-9): "))
                    newpos_y = int(input("y-coordinate (0-9): "))
                    newpos = newpos_x + newpos_y * 9

                    if board[newpos] == "x":
                        board[pos] = "x"
                        board[newpos] = "1"

                        if isMill(newpos, board):
                            userRemoved = False
                            while not userRemoved:
                                try:
                                    # pos = int(input("\nMill formed. Remove a '2' piece: "))
                                    print("Mill formed. Remove a '2' piece:")
                                    pos_x = int(input("x-coordinate (0-9): "))
                                    pos_y = int(input("y-coordinate (0-9): "))
                                    pos = pos_x + pos_y * 9

                                    if (
                                        board[pos] == "2"
                                        and not isMill(pos, board)
                                        or (
                                            isMill(pos, board)
                                            and numOfPieces(board, "1") == 3
                                        )
                                    ):
                                        board[pos] = "x"
                                        userRemoved = True
                                    else:
                                        print("Invalid position")
                                except Exception:
                                    print("Error while accepting input")
                        userPlaced = True
                        userMoved = True
                    else:
                        print("Invalid Position. Try Again.")

            except Exception as e:
                print(str(e))
                print("Invalid entry. Try Again please.")

        if evaluation.evaluate == float("inf"):
            print("YOU WIN!!")
            exit(0)

        printBoard(board)
        print("Computer Start---------------------------")
        evaluation = minimax(board, depth, False, alpha, beta, False, heuristic)

        if evaluation.evaluate == float("-inf"):
            print("YOU LOST!")
            exit(0)
        else:
            board = evaluation.board

        if evaluation.evaluate == float("inf"):
            print("You WIN!")
            exit(0)


if __name__ == "__main__":
    print("WELCOME TO AI VS HUMAN 9 MENS MORRIS")
    print()
    # AI_vs_human(potentialMillsHeuristic)
    AI_vs_human(numPiecesHeuristic)

    # You can also use the number of pieces heuristic (worse results)
    # AI_vs_human(numPiecesHeuristic)
