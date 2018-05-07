# author James Todd
# created 4-21-18
# thing to possibly implement:
# 1. a time to be passed in to the object so that is it not just 2m it is what ever we want.
# 2. an argument to pass in saying player 1 is a human and player 2 is an AI
#                               or player 1 is an AI and player 2 is a human
#                               or player 1 is an AI and player 2 is an AI
# 3. a stop button
# 4. a pause button
from tkinter import *
import math

class halma_GUI:
    alphabet =["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    internal_board = None
    pawn_in_play = None
    player_label = None
    halma_board = None
    has_jumped = False
    timer_Label = None
    start_move = True
    jump_list = None
    old_move = None
    app_GUI = None
    board_size = 8
    player = 1
    status_label = None
    red_goal = None
    green_goal = None

    def __init__(self, board_size):
        if board_size >= 8:
            self.board_size = board_size
        self.halma_board = self._make_TK_GUI()
        self._set_name_to_board()
        self._set_default_window_size()
        self._set_window_grid()
        self.app_GUI = Frame(self.halma_board)
        self._set_up_internal_board()
        self._place_buttons()
        self._set_up_pawns()
        self.halma_board.configure(bg="white")
        self._set_up_number_and_letters_icons()
        self._set_up_player_label()
        self._set_up_timer()
        self._set_up_start_button()
        self._set_up_status()
        self.green_goal = (self.board_size-1,self.board_size-1)
        self.red_goal = (0,0)

# These sets of function are used to setup the GUI.
# What I mean by setup or setup is create all of the base widgets needed to make the GUI.

    # this function makes the main GUI object, this is saved as self.halma_board
    def _make_TK_GUI(self):
        return Tk()

    # this function will give the GUI a title.  you can see it in the upper left corner of the GUI
    def _set_name_to_board(self):
        self.halma_board.title("Halma")

    # this function sets the default pixels size of the board
    def _set_default_window_size(self):
        self.halma_board.geometry("1000x750")

    # this function will set up the grid where all of the widgets will be placed in.
    # if the size of the board we want to make is an 8x8, then we will get a 12x12 grid.
    # this is because I have a 2 block buffer all around the NxN board
    # N being the number we pass in when creating the object.
    # I did this so we can put things around the game board easily.
    def _set_window_grid(self):
        for x in range(self.board_size + 4):
            Grid.columnconfigure(self.halma_board , x, weight=1)

        for y in range(self.board_size + 4):
            Grid.rowconfigure(self.halma_board , y, weight=1)

    # this method places all of the game 'buttons' or playable space.
    def _place_buttons(self):
        for x in range(self.board_size):
            for y in range(self.board_size):
                button = Button(self.halma_board, command=lambda row = x, column = y:self.move(row,column))
                button.y_position = y
                button.x_position = x
                button.grid(column=(x + 2), row=(y + 2), sticky=N + S + E + W)
                button.configure(bg='white')

                self.internal_board[x][y] = button

    # this is just an internal board of the game buttons.
    # this is so we can look at the button and see what color it is.
    # white is a open space.
    # red is player 1
    # green is player 2
    # gray is a valid move.
    def _set_up_internal_board(self):
        self.internal_board = [[0 for x in range(self.board_size)] for y in range(self.board_size)]

    # this gose and colors in where the pawns should be.
    def _set_up_pawns(self):
        for row in range(3):
            for column in range(3):
                self.internal_board[row][column].configure(bg="red")
                self.internal_board[self.board_size - row - 1][self.board_size - column - 1].configure(bg="green")
        self._set_up_side_pawns()

    # I did not know how to make a clean for loop to place all of the pawns, so this gets the rest of them.
    def _set_up_side_pawns(self):
        self.internal_board[0][3].configure(bg="red")
        self.internal_board[1][3].configure(bg="red")
        self.internal_board[3][0].configure(bg="red")
        self.internal_board[3][1].configure(bg="red")

        self.internal_board[self.board_size - 1][self.board_size - 4].configure(bg="green")
        self.internal_board[self.board_size - 2][self.board_size - 4].configure(bg="green")
        self.internal_board[self.board_size - 4][self.board_size - 1].configure(bg="green")
        self.internal_board[self.board_size - 4][self.board_size - 2].configure(bg="green")


        #image = PhotoImage(file="blank.gif").subsample(2,2)
        #button = self.internal_board[row][column]
        #button.config(image=image, compound=CENTER)
        #button.image = image
        #self.internal_board[0][0] = button

    # this will place the numbers and the Letter around the board.
    def _set_up_number_and_letters_icons(self):
        size_mid_point = self.halma_board.grid_size()[0]
        for row in range(self.board_size):
            label = Label(self.halma_board, text=str(row + 1))
            label.configure(bg="white")
            label.grid(row=(row+2), column=1)

        for column in range(self.board_size):
            label = Label(self.halma_board, text=str(self.alphabet[column]))
            label.configure(bg="white")
            label.grid(row=1, column=(column+2))

    # this setup the player label in the top left so we can see whos turn it is. also it is saved as self.player_label
    def _set_up_player_label(self):
        label = Label(self.halma_board, text="Player 1's (red) turn")
        label.grid(row=0,column=0)
        label.configure(bg='white')
        self.player_label = label

    # this sets up a timer so we can see the clock run down.
    def _set_up_timer(self):
        label = Label(self.halma_board, text="Timer: 180 seconds remaining")
        label.grid(row=1,column=0)
        label.configure(bg='white')
        self.timer_Label = label

    def _set_up_status(self):
        label = Label(self.halma_board, text="Game Ready")
        label.grid(row=3,column=0)
        label.configure(bg='white')
        self.status_label = label

    # this is a recursive function the gets played in the background. the main GUI object handles it.
    # all it does is count down the timer.
    def _update_clock(self):
        label_text = self.timer_Label.cget("text")
        label_text = label_text.split(' ')
        time = int(label_text[1])
        string ="Timer: " + str(time - 1) + " seconds remaining"
        self.timer_Label.configure(text=string)
        self.halma_board.after(1000, self._update_clock)

    # this function will place the start button in the upper left.
    # all this start button does is starts the timer.
    def _set_up_start_button(self):
        button = Button(self.halma_board, text="Start", command=self._start_game)
        button.configure(bg="white")
        button.grid(row=2,column=0)

    # function call for the start button. which starts the timer.
    def _start_game(self):
        self.halma_board.after(1000,self._update_clock())
        string = "Game Started"
        self.status_label.configure(text=string)

    # red wins when all of its pieces are in the bottom right corner
    # loops through top left 4x4 square ignoring non-goal zones,
    # checks that each one is colored red
    # if both loops terminate without the method returning,
    # red is in a win state
    def _check_red_wins(self):
        for i in range(0,3):
            for j in range(0,3):
                if (i + j) == 5 or (i + j) == 6:
                    # skip
                    print("")
                elif self.internal_board[self.board_size - (1 + i)][self.board_size - (1+ j)].cget('bg') != 'red':
                    return False
        string = "Player 1 (red) wins."
        self.status_label.configure(text=string)
        print("Red wins")
        return True

    # green wins when all of its pieces are in the top left corner
    # loops through top left 4x4 square ignoring non-goal zones,
    # checks that each one is colored green
    # if both loops terminate without the method returning,
    # green is in a win state
    def _check_green_wins(self):
        for i in range(0,3):
            for j in range(0,3):
                if (i + j) == 5 or (i + j) == 6:
                    # skip
                    print("")
                elif self.internal_board[i][j].cget('bg') != 'green':
                    return False
        string = "Player 2 (green) wins."
        self.status_label.configure(text=string)
        print("Green wins")
        return True

    # gets all the peg locations of a certain color, foundation for AI movement
    # returns a list of all locations where pegs exists for this player
    def _get_all_peg_positions(self, player, row_position, column_position, peg_locations):
        if column_position <= len(self.internal_board[0]) - 1 and row_position <= len(self.internal_board) - 1:
            if self.internal_board[row_position][column_position].cget('bg') == player:
                peg_locations.append([row_position, column_position])
            if column_position == len(self.internal_board[0]) - 1:
                return self._get_all_peg_positions(player, row_position + 1, 0, peg_locations)
            else:
                return self._get_all_peg_positions(player, row_position, column_position + 1, peg_locations)
        else:
            return peg_locations

    # gets all the pegs adjacent squares for the current player
    # returns in the format ==> [[[0,0], (1, 0), (0, 1), (1, 1)]] where [0, 0] is the checked peg, and the others are adjacent to it
    def _get_all_peg_adjacency(self, all_moves, all_adjacencies):
        if len(all_moves) == 0:
            return all_adjacencies
        all_adjacencies.append([all_moves[0], self._get_adjacent_squares(all_moves[0][0], all_moves[0][1])])
        del all_moves[0]
        return self._get_all_peg_adjacency(all_moves, all_adjacencies)

    # calculates simple straight line distance from a peg to the other corner of the board
    def _distance_to_goal(self, curr_location, goal_location):
        distance_to_goal = 0
        distance_to_goal = math.sqrt(((curr_location[1] - goal_location[1]) ** 2) + ((curr_location[0] - goal_location[0]) ** 2)) # calc. straight line distance
        return distance_to_goal

    # we are at the end of the board setup. the functions below are used for move logic.

    # this function given an index for the row and column position
    # will return a list of adjacent squares to those index.
    # EX if i pass in 0,0 then i will get back something like this: [(1,0),(1,1),(0,1)]
    def _get_adjacent_squares(self,row_position, column_position):
        returning_list = []
        if row_position + 1 != self.board_size:
            returning_list.append((row_position + 1, column_position))

        if row_position - 1 >= 0:
            returning_list.append((row_position - 1, column_position))

        if column_position + 1 != self.board_size:
            returning_list.append((row_position, column_position + 1))

        if column_position - 1 >= 0:
            returning_list.append((row_position, column_position - 1))

        if column_position + 1 != self.board_size and row_position + 1 != self.board_size:
            returning_list.append((row_position + 1, column_position + 1))

        if column_position + 1 != self.board_size and row_position - 1 >= 0:
            returning_list.append((row_position - 1, column_position + 1))

        if column_position - 1 >= 0 and row_position + 1 != self.board_size:
            returning_list.append((row_position + 1, column_position - 1))

        if column_position - 1 >= 0 and row_position - 1  >= 0:
            returning_list.append((row_position - 1, column_position - 1))
        return returning_list

    # this will go and change all of the valid playable spaces to gray.
    # so if I am green and I want to move my pawn at 0,0 it will color [(1,0),(1,1),(0,1)] if that are open.
    def _highlight_adjacent_squares(self, adjacent_squares):
        for square in adjacent_squares:
            test_color = self.internal_board[square[0]][square[1]].cget('bg')
            if test_color == 'white':
                self.internal_board[square[0]][square[1]].configure(bg='gray')

    # this will change all of the gray buttons back to white buttons
    def _clean_highlight(self):
        for row in range(self.board_size):
            for column in range(self.board_size):
                test_color = self.internal_board[row][column].cget('bg')
                if test_color == 'gray':
                    self.internal_board[row][column].configure(bg='white')

    # so what this does is looks within the adjacent_squares list and looks to see if there are valid jumping spots.
    # if so make them gray!
    def _get_jumping_squares(self, adjacent_squares):
        returning_list = []
        for square in adjacent_squares:
            temp_val = self._see_if_there_is_a_jumpable_spot(square, self.pawn_in_play)
            if temp_val != None:
                returning_list.append(temp_val)
        return returning_list

    # this is a helper method to the method above
    def _see_if_there_is_a_jumpable_spot(self, square, square_in_question):
        temp_x = (square[0] - square_in_question[0])
        temp_y = (square[1] - square_in_question[1])
        look_here_x = temp_x + square_in_question[0]
        look_here_y = temp_y + square_in_question[1]
        if look_here_y + temp_y >= 0 and look_here_x + temp_x >= 0 and look_here_y + temp_y < self.board_size and \
                                look_here_x + temp_x < self.board_size:
            if self.internal_board[look_here_x][look_here_y].cget('bg') == 'red' or \
               self.internal_board[look_here_x][look_here_y].cget('bg') == 'green':

                if self.internal_board[look_here_x + temp_x][look_here_y + temp_y].cget('bg') == 'white':
                    self.internal_board[look_here_x + temp_x][look_here_y + temp_y].configure(bg='gray')
                    return look_here_x + temp_x, look_here_y + temp_y

    # this will change all of the adjcent squares back to white
    def _clean_adjacent_squares(self, adjacent_squares):
        returning_list = []
        for squares in adjacent_squares:
            if self.internal_board[squares[0]][squares[1]].cget('bg') == 'white':
                returning_list.append(squares)
        return returning_list

    # this function will 'turn on the gui'. if you make the object it does it no good if you don't tell it to run.
    def run(self):
        self.halma_board.mainloop()

    # this function handles moving.
    #  so:
    #       if the last move was not a jump move
    #           if this is a players starting move
    #               highlight the adjacent squares to the pawn they want to move, if possible
    #           elif look to see if this player picked that same pawn
    #               then unselect that one and act as if the player has not made a move.
    #           else the player wants to move is pawn to a gray spot.
    #       elif the player did a jump move and can jump again but they don't want too.
    #           this is because they re-picked the active pawn to end their turn.
    #           When turn ends, check if either side is a victor
    #       else the player want to jump again.
    def move(self, row_position, column_position):

        if not self.has_jumped:
            if self.start_move:
                self._start_move_sequence(row_position, column_position)
            elif row_position == self.pawn_in_play[0] and column_position == self.pawn_in_play[1]:
                self._unselect_pawn_from_play()
            else:
                self._move_pawn(row_position, column_position)
        elif self.has_jumped and (row_position, column_position) == self.pawn_in_play:
            self._clean_highlight()
            self.pawn_in_play = None
            self.player = 3 - self.player
            self.start_move = True
            if self.player == 1:
                color = "red"
            else:
                color = "green"
            self.start_move = True
            string = "Player " + str(self.player) + "'s (" + color + ") turn"
            self.player_label.configure(text=string)
            self.has_jumped = False
            #self._clean_highlight()
            #self._check_red_wins()
            self._check_green_wins()
        else:
            self._move_pawn(row_position, column_position)
        self._test_print_internal_board()

    # this function does the logic for the start of someones turn.
    #   if it is player X then
    #       clean the board of gray squares
    #       save the pawn in play,  the pawn the player selected.
    #       get the adjacent squares to that pawn.
    #       get the jump moves for that pawn
    #       color in the adjacent squares to gray
    #       start move = false, or over

    def _start_move_sequence(self,row_position, column_position):
        self._clean_highlight()
        # for testing here, we will change where this stuff is called
        if self.player == 1:
            player_color = 'red'
        else:
            player_color = 'green'
        all_pegs = self._get_all_peg_positions(player_color, 0, 0, [])
        all_adj = self._get_all_peg_adjacency(all_pegs, [])

        if player_color == 'red':
            dist = self._distance_to_goal([row_position, column_position], [0, 0])
        else:
            dist = self._distance_to_goal([row_position, column_position], [len(self.internal_board) - 1, len(self.internal_board[0]) - 1])


        if self.player == 1 and self.internal_board[row_position][column_position].cget('bg') == 'red':
            self._clean_highlight()
            self.pawn_in_play = (row_position, column_position)
            adjacent_squares = self._get_adjacent_squares(row_position, column_position)
            self.jump_list = self._get_jumping_squares(adjacent_squares)
            self._highlight_adjacent_squares(adjacent_squares)
            self.start_move = False
        elif self.player == 2 and self.internal_board[row_position][column_position].cget('bg') == 'green':
            self._clean_highlight()
            self.pawn_in_play = (row_position, column_position)
            adjacent_squares = self._get_adjacent_squares(row_position, column_position)
            self.jump_list = self._get_jumping_squares(adjacent_squares)
            self._highlight_adjacent_squares(adjacent_squares)
            self.start_move = False

    # this function is for if you want to pick a diffrent pawn than from the one you already pick.
    # i will un-color the adjacent squares and set the start turn back to true.
    def _unselect_pawn_from_play(self):
        self.start_move = True
        self._clean_highlight()
        self.pawn_in_play = None

    # this will move a pawn a player has selected to a spot a player has selected, aka a gray spot.
    def _move_pawn(self, row_position, column_position):
        test_color = self.internal_board[row_position][column_position].cget('bg')
        if test_color == 'gray':
            if self.player == 1:
                self._players_move(row_position, column_position, 'red')

            elif self.player == 2:
                self._players_move(row_position, column_position, 'green')

    # this is a helper method for _move_pawn.
    # this will color in spot the player selected.
    # set its old spot white.
    # clean the highlighted spots.
    # and then looks to see if the move the player did was a jump move.
    # if so:
    #   set the old move to the pawn in play, this was the old spot you moved from.
    #   set the pawn in play to the new spot.
    #   get the adjacent squares to the new spot.
    #   get the new jump list
    #   remove the old move from the new jump list.
    #   look to see if the jump list is empty
    #       if so then there are no more moves for this player end their turn
    #           set the pawn in play to nothing
    #           change the player to player 2
    #           make sure the starting move variable is set to true
    #           clean off the gray squares.
    #           make the has jump variable false
    #           reset the time.
    #       else if the list is not empty
    #           set start move to true
    #           set has jump to true
    # else the play did not jump and it is the end of their turn.
    #   set the pawn in play to nothing
    #   change the player to player 2
    #   make sure the starting move variable is set to true
    #   clean off the gray squares.
    #   make the has jump variable false
    #   reset the time.

    def _players_move(self, row_position, column_position, color):
        self.internal_board[row_position][column_position].configure(bg=color)
        # TODO update this part of the method to color the moved pawn and previous space each time
        self.internal_board[self.pawn_in_play[0]][self.pawn_in_play[1]].configure(bg='white')
        self._clean_highlight()
        if (row_position, column_position) in self.jump_list:
            self.old_move = self.pawn_in_play
            self.pawn_in_play = (row_position, column_position)
            adjacent_squares = self._get_adjacent_squares(row_position, column_position)
            self.jump_list = self._get_jumping_squares(adjacent_squares)
            self.jump_list.remove(self.old_move)
            if len(self.jump_list) == 0:
                self.pawn_in_play = None
                self.player = 3 - self.player
                if self.player == 1:
                    color = "red"
                else:
                    color = "green"
                self.start_move = True
                string = "Player " + str(self.player) + "'s (" + color + ") turn"
                self._clean_highlight()
                self._check_red_wins()
                self._check_green_wins()
                self.player_label.configure(text=string)
                self.has_jumped = False
                self.timer_Label.configure(text="Timer: 180 seconds remaining")
            else:
                self.start_move = True
                self.has_jumped = True
                self.internal_board[self.old_move[0]][self.old_move[1]].configure(bg='white')
        else:
            self.pawn_in_play = None
            self.player = 3 - self.player
            self.start_move = True
            if self.player == 1:
                color = "red"
            else:
                color = "green"
            string = "Player " + str(self.player) + "'s (" + color + ") turn"
            self._check_red_wins()
            self._check_green_wins()
            self.player_label.configure(text=string)
            self.has_jumped = False
            self.timer_Label.configure(text="Timer: 180 seconds remaining")


    def _test_print_internal_board(self):
        print("==============================================")
        print("==============================================")
        current_board = self.internal_board
        self._test_print_moves_list(self._make_internal_move_list_for('red', current_board))
        print("==============================================")
        self._test_print_moves_list(self._flatten_move_list(self._make_internal_move_list_for('red', current_board)))
        print("==============================================")

        print("==============================================")
        print("==============================================")
        #self._test_print_moves_list(self._make_internal_move_list_for('green'))
        print("==============================================")
        print("==============================================")
        for column in range(self.board_size):
            print("| ", end="")
            for row in range(self.board_size):

                pawn = self.internal_board[row][column].cget('bg')
                if pawn == 'gray':
                    print("w", " | ", end="")
                else:
                    print(pawn[0], " | ", end="")
            print()

    def _test_print_moves_list(self, moves_list):
        for move in moves_list:
            print(move)

    def _make_internal_move_list_for(self, color, board):
        returning_full_move_list = []

        for column in range(self.board_size):

            for row in range(self.board_size):
                pawn = board[row][column].cget('bg')
                if pawn == color:
                    adjacent_squares = self._get_adjacent_squares(row, column)
                    temp_list = []
                    if color is 'red':

                        this_pawn = (row, column, self._distance_to_goal((row, column), self.red_goal))
                        temp_list = self._get_possible_jump_list((row, column), adjacent_squares, board)
                        temp_list = self._write_values_to_jumping_moves(temp_list, color)
                    else:
                        this_pawn = (row, column, self._distance_to_goal((row, column), self.green_goal))
                        temp_list = self._get_possible_jump_list((row, column), adjacent_squares, board)
                        temp_list = self._write_values_to_jumping_moves(temp_list, color)
                    if temp_list is not None:
                        returning_full_move_list.append([this_pawn] + temp_list +self._get_valid_moves_from_adjacent_squares(adjacent_squares, color, board))
                    else:
                        returning_full_move_list.append([this_pawn] + self._get_valid_moves_from_adjacent_squares(adjacent_squares, color, board))
        return returning_full_move_list


    def _get_valid_moves_from_adjacent_squares(self, adjacent_squares, color, board):
        returning_move_list = []
        for move in adjacent_squares:
            test_color = board[move[0]][move[1]].cget('bg')
            if test_color == 'white' or test_color == 'gray':
                if color is 'red':

                    returning_move_list.append((move[0], move[1], self._distance_to_goal(move, self.red_goal)))

                else:
                    returning_move_list.append((move[0], move[1], self._distance_to_goal(move, self.green_goal)))
        return returning_move_list

    def _get_possible_jump_list(self, move, adjacent_squares, board):
        returning_jump_list = []
        temp_list = self._get_jumping_moves(adjacent_squares, move, board)
        temp_sub_list = []
        for move_in_temp_list in temp_list:

            sub_move_adjacent_squares = self._look_to_see_if_double_jump(move_in_temp_list, move, temp_list, board)
            temp_sub_list = temp_sub_list + [[temp_list[0]] + sub_move_adjacent_squares]

        if [] in temp_sub_list:
            temp_sub_list = temp_sub_list.remove([])

        if temp_sub_list != [] and temp_sub_list != None:
            returning_jump_list = returning_jump_list + temp_sub_list


        return returning_jump_list

    def _look_to_see_if_double_jump(self, move, old_move, old_moves, board):

        temp_val = self._get_jumping_moves(self._get_adjacent_squares(move[0],move[1]),move, board, old_move)
        if temp_val is not None and temp_val != []:
            if old_moves is not []:
                for known_move in old_moves:
                    if known_move in temp_val:
                        temp_val.remove(known_move)

            temp_list = temp_val
            old_moves = old_moves + temp_list
            if temp_val == []:
                return []
            else:
                return temp_list + self._look_to_see_if_double_jump(temp_val[0], move, old_moves, board)
        else:
            return []

    def _get_jumping_moves(self, adjacent_squares, from_this_pawn, board, remove_this_jump = None):
        returning_list = []
        for square in adjacent_squares:
            temp_val = self._see_if_there_is_a_jumpable_move(square, from_this_pawn, board)
            if temp_val != None:
                if remove_this_jump != temp_val:
                    returning_list.append(temp_val)
        return returning_list

    def _see_if_there_is_a_jumpable_move(self, square, square_in_question, board):
        temp_x = (square[0] - square_in_question[0])
        temp_y = (square[1] - square_in_question[1])
        look_here_x = temp_x + square_in_question[0]
        look_here_y = temp_y + square_in_question[1]
        if look_here_y + temp_y >= 0 and look_here_x + temp_x >= 0 and look_here_y + temp_y < self.board_size and \
                                look_here_x + temp_x < self.board_size:
            if board[look_here_x][look_here_y].cget('bg') == 'red' or \
                            board[look_here_x][look_here_y].cget('bg') == 'green':

                if board[look_here_x + temp_x][look_here_y + temp_y].cget('bg') == 'gray' or \
                   board[look_here_x + temp_x][look_here_y + temp_y].cget('bg') == 'white':
                    return look_here_x + temp_x, look_here_y + temp_y

    def _write_values_to_jumping_moves(self, jumping_moves_lists, color):
        if jumping_moves_lists == []:
            return []
        returning_list = []
        for move_list in jumping_moves_lists:
            inner_temp_list = []
            for move in move_list:
                if color == 'red':
                    inner_temp_list.append((move[0],move[1], self._distance_to_goal(move, self.red_goal)))
                else:
                    inner_temp_list.append((move[0], move[1], self._distance_to_goal(move, self.green_goal)))
            returning_list.append(inner_temp_list)

        return returning_list

    # this function takes in a list of moves generated by _make_internal_move_list_for
    # and flattens it into a list of 5 part tuples of the form:
    # (start_x, start_y, end_x, end_y, h)
    # where h = h(end) - h(start) or: the difference in value between positions of the move
    def _flatten_move_list(self, moves):
        flat_move_list = []
        for move_set in moves:
            # first move is always the pawn's starting position, get starting x and y
            move_base_start_x = move_set[0][0]
            move_base_start_y = move_set[0][1]
            # get the heuristic value for current position
            heuristic_diff = move_set[0][2]
            # end positions are all moves after the first
            end_positions = move_set[1:]
            for end_position in end_positions:
                # check if the end_position is a jump set
                if isinstance(end_position, list):
                    # end_position is a jump set, loop through jump_set
                    jump_set = end_position
                    for jump in jump_set:
                        # compute final heuristic for each jump in jump set
                        end_x = jump[0]
                        end_y = jump[1]
                        final_heuristic = jump[2] - heuristic_diff
                        flat_move = (move_base_start_x, move_base_start_y, end_x, end_y, final_heuristic)
                        # add the jump move to the flat_move_list
                        flat_move_list.append(flat_move)
                else:
                    # end position is a normal move, compute final heuristic
                    end_x = end_position[0]
                    end_y = end_position[1]
                    final_heuristic = end_position[2] - heuristic_diff
                    flat_move = (move_base_start_x, move_base_start_y, end_x, end_y, final_heuristic)
                    flat_move_list.append(flat_move)
        return flat_move_list

    # function gets the max valued move from a flat move list
    # returns a 5 part tuple of the form:
    # (start_x, start_y, end_x, end_y, h)
    # with greatest h among all moves examined
    def _get_max_move(self, moves):
        best_move = None
        best_value = -9999
        for move in moves:
            # check if the move is better than the current best
            if move[4] > best_value:
                # update the best move
                best_value = move[4]
                best_move = move
        print("Move chosen: " + best_move)
        return best_move

    def _minimax(self, pruning):
        # TODO pruning
        # get a flat move list for current board
        red_moves = self._make_internal_move_list_for('red', self.internal_board)
        print("")
