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

# These sets of function are used to setup the GUI.
# What I mean by setup or set_up is create all of the base widgets needed to make the GUI.

    # this function makes the main GUI object, this is saved as self.halma_board
    def _make_TK_GUI(self):
        return Tk()

    # this function will give the GUI a title.  you can see it in the upper left corner of the GUI
    def _set_name_to_board(self):
        self.halma_board.title("Halma board")

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
    # red is player 2
    # green is player 1
    # gray is a valid move.
    def _set_up_internal_board(self):
        self.internal_board = [[0 for x in range(self.board_size)] for y in range(self.board_size)]

    # this gose and colors in where the pawns should be.
    def _set_up_pawns(self):
        for row in range(3):
            for column in range(3):
                self.internal_board[row][column].configure(bg="green")
                self.internal_board[self.board_size - row - 1][self.board_size - column - 1].configure(bg="red")
        self._set_up_side_pawns()

    # I did not know how to make a clean for loop to place all of the pawns, so this gets the rest of them.
    def _set_up_side_pawns(self):
        self.internal_board[0][3].configure(bg="green")
        self.internal_board[1][3].configure(bg="green")
        self.internal_board[3][0].configure(bg="green")
        self.internal_board[3][1].configure(bg="green")

        self.internal_board[self.board_size - 1][self.board_size - 4].configure(bg="red")
        self.internal_board[self.board_size - 2][self.board_size - 4].configure(bg="red")
        self.internal_board[self.board_size - 4][self.board_size - 1].configure(bg="red")
        self.internal_board[self.board_size - 4][self.board_size - 2].configure(bg="red")


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
        label = Label(self.halma_board, text="Player's 1 turn")
        label.grid(row=0,column=0)
        label.configure(bg='white')
        self.player_label = label

    # this setups a timer so we can see the clock run down.
    def _set_up_timer(self):
        label = Label(self.halma_board, text="Timer: 120 seconds remaining")
        label.grid(row=1,column=0)
        label.configure(bg='white')
        self.timer_Label = label

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


        if look_here_y + temp_y >= 0 and look_here_x + temp_x >= 0 and look_here_y + temp_y != self.board_size and \
                                look_here_x + temp_x != self.board_size:
            if self.internal_board[look_here_x][look_here_y].cget('bg') == 'green' or \
               self.internal_board[look_here_x][look_here_y].cget('bg') == 'red':

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
            self.pawn_in_play = None
            self.player = 3 - self.player
            self.start_move = True
            string = "Player's " + str(self.player) +" turn"
            self.player_label.configure(text=string)
            self.has_jumped = False
            self._clean_highlight()
        else:
            self._move_pawn(row_position, column_position)

    # this function does the logic for the start of someones turn.
    #   if it is player X then
    #       clean the board of gray squares
    #       save the pawn in play,  the pawn the player selected.
    #       get the adjacent squares to that pawn.
    #       get the jump moves for that pawn
    #       color in the adjacent squares to gray
    #       start move = false, or over

    def _start_move_sequence(self,row_position, column_position):
        if self.player == 1 and self.internal_board[row_position][column_position].cget('bg') == 'green':
            self._clean_highlight()
            self.pawn_in_play = (row_position, column_position)
            adjacent_squares = self._get_adjacent_squares(row_position, column_position)
            self.jump_list = self._get_jumping_squares(adjacent_squares)
            self._highlight_adjacent_squares(adjacent_squares)
            self.start_move = False
        elif self.player == 2 and self.internal_board[row_position][column_position].cget('bg') == 'red':
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
                self._players_move(row_position, column_position, 'green')

            elif self.player == 2:
                self._players_move(row_position, column_position, 'red')

    # this is a helper method for _move_pawn.
    # this will color in spot the player selected.
    # set its old spot white.
    # clean the highlighted spotes.
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
                self.start_move = True
                string = "Player's " + str(self.player) + " turn"
                self._clean_highlight()
                self.player_label.configure(text=string)
                self.has_jumped = False
                self.timer_Label.configure(text="Timer: 120 seconds remaining")
            else:
                self.start_move = True
                self.has_jumped = True
                self.internal_board[self.old_move[0]][self.old_move[1]].configure(bg='white')
        else:
            self.pawn_in_play = None
            self.player = 3 - self.player
            self.start_move = True
            string = "Player's " + str(self.player) +" turn"
            self.player_label.configure(text=string)
            self.has_jumped = False
            self.timer_Label.configure(text="Timer: 120 seconds remaining")





''' unit tests '''
test = halma_GUI(8)
test.run()