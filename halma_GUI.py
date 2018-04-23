from tkinter import *


class halma_GUI:
    alphabet =["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
    board_size = 8
    start_move = True
    halma_board = None
    app_GUI = None
    internal_board = None
    pawn_in_play = None
    player = 1
    player_label = None
    jump_list = None
    has_jumped = False
    old_move = None

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

        #self._set_up_title_lable()

    def _make_TK_GUI(self):
        return Tk()

    def _set_name_to_board(self):
        self.halma_board.title("Halma board")

    def _set_default_window_size(self):
        self.halma_board.geometry("1000x750")

    def _set_window_grid(self):
        for x in range(self.board_size + 4):
            Grid.columnconfigure(self.halma_board , x, weight=1)

        for y in range(self.board_size + 4):
            Grid.rowconfigure(self.halma_board , y, weight=1)

    def _place_buttons(self):
        for x in range(self.board_size):
            for y in range(self.board_size):
                button = Button(self.halma_board, command=lambda row = x, column = y:self.move(row,column))
                button.y_position = y
                button.x_position = x
                button.grid(column=(x + 2), row=(y + 2), sticky=N + S + E + W)
                button.configure(bg='white')

                self.internal_board[x][y] = button

    def _set_up_internal_board(self):
        self.internal_board = [[0 for x in range(self.board_size)] for y in range(self.board_size)]

    def _set_up_pawns(self):
        for row in range(3):
            for column in range(3):
                self.internal_board[row][column].configure(bg="green")
                self.internal_board[self.board_size - row - 1][self.board_size - column - 1].configure(bg="red")
        self._set_up_side_pawns()

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

    def _set_up_title_lable(self):

        size_mid_point = self.halma_board.grid_size()[0]

        label_location = size_mid_point//2 - 1

        label = Label(self.halma_board, text="Team Deep Indigo")
        label.config(font=("Courier", 44))
        label.grid(row = 0, column=label_location, columnspan = 2)

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

    def _set_up_player_label(self):
        label = Label(self.halma_board, text="Player's 1 turn")
        label.grid(row=0,column=0)
        label.configure(bg='white')
        self.player_label = label

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

    def _highlight_adjacent_squares(self, adjacent_squares):
        for square in adjacent_squares:
            test_color = self.internal_board[square[0]][square[1]].cget('bg')
            if test_color == 'white':
                self.internal_board[square[0]][square[1]].configure(bg='gray')

    def _clean_highlight(self):
        for row in range(self.board_size):
            for column in range(self.board_size):
                test_color = self.internal_board[row][column].cget('bg')
                if test_color == 'gray':
                    self.internal_board[row][column].configure(bg='white')

    def _get_jumping_squares(self, adjacent_squares):
        returning_list = []
        for square in adjacent_squares:
            temp_val = self._see_if_there_is_a_jumpable_spot(square, self.pawn_in_play)
            if temp_val != None:
                returning_list.append(temp_val)
        return returning_list

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

    def _clean_adjacent_squares(self, adjacent_squares):
        returning_list = []
        for squares in adjacent_squares:
            if self.internal_board[squares[0]][squares[1]].cget('bg') == 'white':
                returning_list.append(squares)
        return returning_list

    def run(self):
        self.halma_board.mainloop()

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

    def _start_move_sequence(self,row_position, column_position):
        if self.player == 1 and self.internal_board[row_position][column_position].cget('bg') == 'green':
            self._clean_highlight()
            self.pawn_in_play = (row_position, column_position)
            adjacent_squares = self._get_adjacent_squares(row_position, column_position)
            self.jump_list = self._get_jumping_squares(adjacent_squares)
            print(self.jump_list)
            self._highlight_adjacent_squares(adjacent_squares)
            self.start_move = False
        elif self.player == 2 and self.internal_board[row_position][column_position].cget('bg') == 'red':
            self._clean_highlight()
            self.pawn_in_play = (row_position, column_position)
            adjacent_squares = self._get_adjacent_squares(row_position, column_position)
            self.jump_list = self._get_jumping_squares(adjacent_squares)
            self._highlight_adjacent_squares(adjacent_squares)
            self.start_move = False

    def _unselect_pawn_from_play(self):
        self.start_move = True
        self._clean_highlight()
        self.pawn_in_play = None

    def _move_pawn(self, row_position, column_position):
        test_color = self.internal_board[row_position][column_position].cget('bg')
        if test_color == 'gray':
            if self.player == 1:
                self._players_move(row_position, column_position, 'green')

            elif self.player == 2:
                self._players_move(row_position, column_position, 'red')

    def _players_move(self, row_position, column_position, color):
        self.internal_board[row_position][column_position].configure(bg=color)
        self.internal_board[self.pawn_in_play[0]][self.pawn_in_play[1]].configure(bg='white')
        self._clean_highlight()
        if (row_position, column_position) in self.jump_list:
            self.jump_list.remove((row_position, column_position))
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

    #def _see_if_you_can_jump_again(self,row_position, column_position):




test = halma_GUI(8)
test.run()






#
# # make the board window.
# halma_board_window = Tk()
#
#
# # set some default values
#
# halma_board_window.title("Halma board")
# halma_board_window.geometry("1000x750")
#
# app = Frame(halma_board_window)
# app.grid()
# label = Label(app, text="tester")
#
# button1 = Button(app, text="This is a button")
# button1.grid()
#
# button2 = Button(app, text="This is a button2")
# button2.grid()
#
# button3 = Button(app)
# button3.grid()
# button3.configure(text ="hello")
#
# button4 = Button(app)
# button4.grid()
# button4["text"] = "yo yo yo yo yo"
#
#
# label.grid()
#
#
#
#
# # open the board
# halma_board_window.mainloop()
