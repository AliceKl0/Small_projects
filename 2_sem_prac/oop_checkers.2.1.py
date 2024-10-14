import re

print("*" * 40, " Шашки ", "*" * 40)
print("\nend -конец игры")
print("\nПеред вами английская версия шашек. Правила:"
      "\n-чёрные ходят первыми"
      "\n-шашки ходят на одну клетку вперёд по диагонали"
      "\n-одна шашка бьёт все возможные фигуры соперника за свой ход"
      "\n-дойдя до края поля шашка превращается в дамку"
      "\n-правила обычных шашек сохраняются для дамки + возможен ход назад (диагональ, 1-на клетка)"
      "\n-если возможно взять шашку соперника, то необходимо это сделать\n")
print("*" * 91 + '\n')


class ChessBoard:
    def __init__(self):
        self.board = [
            ['.', 'b', '.', 'b', '.', 'b', '.', 'b'],
            ['b', '.', 'b', '.', 'b', '.', 'b', '.'],
            ['.', 'b', '.', 'b', '.', 'b', '.', 'b'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['w', '.', 'w', '.', 'w', '.', 'w', '.'],
            ['.', 'w', '.', 'w', '.', 'w', '.', 'w'],
            ['w', '.', 'w', '.', 'w', '.', 'w', '.']
        ]

    def print_board(self):
        print('  a b c d e f g h')
        for i in range(8):
            print(str(8 - i) + ' ' + ' '.join(self.board[i]))
        print('  a b c d e f g h')

        return ' '

    def move_piece(self, start_pos, end_pos):
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        piece = self.board[start_row][start_col]
        self.board[start_row][start_col] = '.'
        self.board[end_row][end_col] = piece.upper() if end_row in [0, 7] else piece

        if abs(start_row - end_row) == 2:
            self.board[(start_row + end_row) // 2][(start_col + end_col) // 2] = '.'


class Checkers:
    def __init__(self, piece_):
        self.piece = piece_

    def move(self, start_pos, end_pos, board):
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        target_piece = Checkers(board[end_row][end_col])

        if ((abs(end_col - start_col) == abs(end_row - start_row) == 1
             and ((start_row - end_row > 0 if self.piece.lower() == 'w' else start_row - end_row < 0)
                  or self.piece.isupper()))
            or abs(end_col - start_col) == abs(end_row - start_row) == 2) and target_piece.piece == '.':

            inter_figure = board[(start_row + end_row) // 2][(start_col + end_col) // 2] \
                if abs(end_row - start_row) == 2 else None

            if inter_figure != self.piece.lower() and inter_figure != '.' and abs(end_row - start_row) == 2 or \
                    inter_figure is None:
                return True

        return False


class ChessGame:
    def __init__(self):
        self.board = ChessBoard()
        self.current_turn = 'чёрные'
        self.is_game_over = False
        self.count = 0
        self.position = [f"{x}{y}" for y in range(1, 9) for x in 'abcdefgh']
        self.available_start_pos = []
        self.available_end_pos = []

    def switch_turn(self):
        self.current_turn = 'чёрные' if self.current_turn == 'белые' else 'белые'

    def make_move(self, start_pos, end_pos, piece_):
        # Тот ли игрок выполняет ход?
        if piece_.piece.lower() == 'w' and self.current_turn == 'белые':
            print("\nХод белых.")
        elif piece_.piece.lower() == 'b' and self.current_turn == 'чёрные':
            print("\nХод чёрных.")
        else:
            print("\nОшибка. Сейчас не ваш ход.")
            return

        figure = self.what_is(piece_)

        if figure.move(start_pos, end_pos, self.board.board):
            # Ход возможен, ошибок нет? Выполняем!
            self.board.move_piece(start_pos, end_pos)

            return True
        else:
            print(f"\nДля {piece_.piece} ход невозможен.")

            return False

    def print_board(self):
        self.board.print_board()

    def play(self):
        while not self.is_game_over:
            self.print_board()
            available_hit_l = self.available_hit()

            if available_hit_l is not False:
                start_input = input(f"\n{self.current_turn} делают ход. Стартовая позиция (из списка выше!!!): ")

                if start_input not in self.available_start_pos:
                    self.available_hit(False)
                    print("Выберите позицию из списка выше!")

                    continue
            else:
                start_input = input(f"\n{self.current_turn} делают ход. Стартовая позиция: ")

            if start_input.lower() == 'end':
                print("\nИгра окончена.")
                self.is_game_over = True
                break

            if self.is_valid_position(start_input):
                start_row, start_col = self.get_coords(start_input)
            else:
                print(f"\nТакого поля нет!")
                continue

            figure_ = self.what_is(Checkers(self.board.board[start_row][start_col]))

            if available_hit_l is not False:
                end_input = input(f"{self.current_turn} делают ход. Конечная позиция (из списка выше!!!): ")

                if end_input not in self.available_end_pos:
                    self.available_hit(False)
                    print("Выберите позицию из списка выше!")

                    continue
            else:
                end_input = input(f"{self.current_turn} делают ход. Конечная позиция: ")

            if end_input.lower() == 'end':
                print("\nИгра окончена.")
                self.is_game_over = True
                break

            if self.is_valid_position(end_input):
                end_row, end_col = self.get_coords(end_input)
            else:
                print(f"\nТакого поля нет!")
                continue

            is_end_input = True
            is_move = self.make_move((start_row, start_col), (end_row, end_col), figure_)

            self.available_start_pos = []
            self.available_end_pos = []

            if available_hit_l is not False:
                available_choice_l = self.available_choice((end_row, end_col), figure_)
                is_end_input = True
                end_input_copy = end_input
                self.available_start_pos = end_input_copy

                while available_choice_l is not False:
                    self.print_board()

                    if is_end_input:
                        end_input_copy = end_input

                    print(f"\n{self.current_turn} делают ход. Стартовая позиция (из списка выше!!!): {end_input_copy}")

                    start_row, start_col = self.get_coords(end_input_copy)
                    figure_ = self.what_is(Checkers(self.board.board[start_row][start_col]))
                    end_input = input(f"{self.current_turn} делают ход. Конечная позиция (из списка выше!!!): ")

                    if end_input not in self.available_end_pos:
                        self.available_choice((end_row, end_col), figure_, False)
                        print("Выберите позицию из списка выше!")
                        is_end_input = False

                        continue

                    if end_input.lower() == 'end':
                        print("\nИгра окончена.")
                        self.is_game_over = True
                        break

                    if self.is_valid_position(end_input):
                        end_row, end_col = self.get_coords(end_input)
                        is_end_input = True
                    else:
                        print(f"\nТакого поля нет!")
                        continue

                    self.make_move((start_row, start_col), (end_row, end_col), figure_)
                    self.available_start_pos = []
                    self.available_end_pos = end_input
                    available_choice_l = self.available_choice((end_row, end_col), figure_)

            if is_move and is_end_input:
                self.switch_turn()
                self.count += 1
                self.available_start_pos = []
                self.available_end_pos = []

            print(f"Количество сделанных ходов: {self.count}")

    def get_coords(self, position):
        column = ord(position[0]) - ord('a')
        row = 8 - int(position[1])
        return row, column

    def is_valid_position(self, position):
        position = position.lower()  # Позицию в нижний регистр
        return re.match('[a-h][1-8]', position) is not None

    def available_choice(self, start_pos, figure, is_move_=True):
        available_choice_ = []

        for end_input_ in self.position:
            end_pos = self.get_coords(end_input_)

            if figure.move(start_pos, end_pos, self.board.board) and abs(start_pos[0] - end_pos[0]) == 2:
                available_choice_.append([end_input_, self.board.board[(start_pos[0] + end_pos[0]) // 2]
                                                                      [(start_pos[1] + end_pos[1]) // 2]])

                if is_move_:
                    self.available_end_pos.append(end_input_)

        if len(available_choice_) > 0:
            print(f"Возможности взять очередную фигуру соперника:")

            for row in available_choice_:
                print(f"{row[1]}, ход на {row[0]}")

            return True

        return False

    def available_hit(self, is_move_=True):
        available_hit_ = []

        for start_input_ in self.position:
            available_hit_for_figure = []

            for end_input_ in self.position:

                if start_input_ != end_input_:
                    start_pos = self.get_coords(start_input_)
                    end_pos = self.get_coords(end_input_)
                    start_figure_ = self.board.board[start_pos[0]][start_pos[1]]

                    if start_figure_ != '.':
                        start_figure_ = self.what_is(Checkers(start_figure_))

                        if self.current_turn == 'белые' and start_figure_.piece.lower() == 'w' or \
                                self.current_turn == 'чёрные' and start_figure_.piece.lower() == 'b':

                            if start_figure_.move(start_pos, end_pos, self.board.board) and \
                                    abs(start_pos[0] - end_pos[0]) == 2:
                                available_hit_for_figure.append([self.board.board[(start_pos[0] + end_pos[0]) // 2]
                                                                 [(start_pos[1] + end_pos[1]) // 2], end_input_])

                                if is_move_:
                                    self.available_end_pos.append(end_input_)

            if len(available_hit_for_figure) > 0:
                available_hit_.append([[start_figure_.piece, start_input_], available_hit_for_figure])

                if is_move_:
                    self.available_start_pos.append(start_input_)

        if len(available_hit_) > 0:
            print(f"\nВы можете взять следующие фигуры соперника:")

            for row in available_hit_:
                row_print = f"С {row[0][0]} на {row[0][1]}: "

                for row_figure in row[1]:
                    row_print += f"взять {row_figure[0]}, ход на {row_figure[1]}; "

                print(row_print)

            return True

        return False

    def what_is(self, piece_):
        if piece_.piece.lower() == 'b' or 'w':
            return Checkers(piece_.piece)
        else:
            print("\nФигура не определена!")
            return


# Запуск
game = ChessGame()
game.play()