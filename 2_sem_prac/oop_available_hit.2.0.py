import re

print("*" * 10, " Шахматы ", "*" * 10)
print("\nend -конец игры\nback_x -откат хода, x ∈ N\n")
print("*" * 31 + '\n')


class ChessBoard:
    def __init__(self):
        self.board = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]

    def print_board(self):
        print('  a b c d e f g h')
        for i in range(8):
            print(str(8 - i) + ' ' + ' '.join(self.board[i]))
        print('  a b c d e f g h')

        return ' '

    def move_piece(self, start_pos, end_pos, start_figure=False, end_figure=False):
        start_row, start_col = start_pos
        end_row, end_col = end_pos
        piece = self.board[start_row][start_col] if not end_figure else end_figure
        self.board[start_row][start_col] = '.' if not start_figure else start_figure
        self.board[end_row][end_col] = piece


class Figures:
    def __init__(self, piece__):
        self.color = piece__.islower()
        self.piece = piece__

    def move(self, start_pos, end_pos, board):
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        if self.register(end_row, end_col, board):
            # Есть ли фигуры на пути?
            if start_row == end_row:  # По горизонтали
                step = 1 if end_col > start_col else -1
                for col in range(start_col + step, end_col, step):
                    if board[start_row][col] != '.':
                        return False
            elif start_col == end_col:  # По вертикали
                step = 1 if end_row > start_row else -1
                for row in range(start_row + step, end_row, step):
                    if board[row][start_col] != '.':
                        return False
            else:  # По диагонали
                row_step = 1 if end_row > start_row else -1
                col_step = 1 if end_col > start_col else -1
                row, col = start_row + row_step, start_col + col_step
                while row != end_row and col != end_col:
                    if board[row][col] != '.':
                        return False
                    row += row_step
                    col += col_step

            return True

        return False

    def register(self, end_row, end_col, board):
        if board[end_row][end_col] != '.':
            reg = self.piece.islower() != board[end_row][end_col].islower()

            if not reg:
                print("Вы не можете атаковать собственную фигуру!")
                return False

            return True

        return True


class Pawn(Figures):
    def __init__(self, piece__):
        super().__init__(piece__)

    def move(self, start_pos, end_pos, board):
        super().move(start_pos, end_pos, board)

        start_row, start_col = start_pos
        end_row, end_col = end_pos
        target_piece = Figures(board[end_row][end_col])

        if start_row in [1, 6]:
            if ((start_col == end_col and (
                    abs(end_row - start_row) == 1 or abs(end_row - start_row) == 2) and
                 target_piece.piece == '.') or (
                        abs(end_col - start_col) == 1 and abs(end_row - start_row) == 1 and
                        target_piece.piece != '.')) \
                    and (start_row - end_row > 0 if not self.color else start_row - end_row < 0):
                return True and super().move(start_pos, end_pos, board)
            else:
                return False
        else:
            if ((start_col == end_col and abs(end_row - start_row) == 1 and target_piece.piece == '.') or
                (abs(end_col - start_col) == 1 and abs(end_row - start_row) == 1 and
                 target_piece.piece != '.')) \
                    and (start_row - end_row > 0 if not self.color else start_row - end_row < 0):
                return True and super().move(start_pos, end_pos, board)
            else:
                return False


class Rook(Figures):
    def __init__(self, piece__):
        super().__init__(piece__)

    def move(self, start_pos, end_pos, board):
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        # Ход по вертикали/горизонтали?
        if start_row == end_row or start_col == end_col:
            return True and super().move(start_pos, end_pos, board)
        else:
            return False


class Knight(Figures):
    def __init__(self, piece__):
        super().__init__(piece__)

    def move(self, start_pos, end_pos, board):
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        # Ход буквой L?
        if abs(end_row - start_row) == 2 and abs(end_col - start_col) == 1:
            return True and self.register(end_row, end_col, board)
        elif abs(end_row - start_row) == 1 and abs(end_col - start_col) == 2:
            return True and self.register(end_row, end_col, board)
        else:
            return False


class Bishop(Figures):
    def __init__(self, piece__):
        super().__init__(piece__)

    def move(self, start_pos, end_pos, board):
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        # Ход по диагонали?
        if abs(end_row - start_row) == abs(end_col - start_col):
            return True and super().move(start_pos, end_pos, board)
        else:
            return False


class Queen(Figures):
    def __init__(self, piece__):
        super().__init__(piece__)

    def move(self, start_pos, end_pos, board):

        # Вертикаль, горизонталь, диагональ?
        return (Bishop(self.piece).move(start_pos, end_pos, board)
                or Rook(self.piece).move(start_pos, end_pos, board)) and super().move(start_pos, end_pos, board)


class King(Figures):
    def __init__(self, piece__):
        super().__init__(piece__)

    def move(self, start_pos, end_pos, board):
        start_row, start_col = start_pos
        end_row, end_col = end_pos

        # Ход на "единичку" ?
        if abs(start_row - end_row) <= 1 and abs(end_col - start_col) <= 1:
            return True and super().move(start_pos, end_pos, board)
        else:
            return False


class ChessGame:
    def __init__(self):
        self.board = ChessBoard()
        self.current_turn = 'белые'
        self.is_game_over = False
        self.count = 0
        self.history = []
        self.position = [f"{x}{y}" for y in range(1, 9) for x in 'abcdefgh']

    def switch_turn(self):
        self.current_turn = 'чёрные' if self.current_turn == 'белые' else 'белые'

    def make_move(self, start_pos, end_pos, piece_):
        # Тот ли игрок выполняет ход?
        if piece_.color and self.current_turn == 'белые':
            print("\nХод белых.")
        elif not piece_.color and self.current_turn == 'чёрные':
            print("\nХод чёрных.")
        else:
            print("\nОшибка. Сейчас не ваш ход.")
            return

        figure = self.what_is(piece_)

        if figure.move(start_pos, end_pos, self.board.board):
            # Ход возможен, ошибок нет? Выполняем!
            self.history.append([[start_pos, piece_.piece], [end_pos, self.board.board[end_pos[0]][end_pos[1]]]])
            self.board.move_piece(start_pos, end_pos)
            self.switch_turn()
            self.count += 1

        else:
            print(f"\nДля {piece_.piece} ход невозможен.")

    def print_board(self):
        self.board.print_board()

    def play(self):
        while not self.is_game_over:
            self.print_board()
            self.available_hit()

            start_input = input(f"\n{self.current_turn} делают ход. Стартовая позиция: ")

            if start_input.lower() == 'end':
                print("\nИгра окончена.")
                self.is_game_over = True
                break

            elif 'back_' in start_input:
                try:
                    count_back = abs(int(start_input.lower().split('_')[1]))
                    self.rollback_move(count_back)
                except:
                    print("\nx ∈ N!")
            else:
                if self.is_valid_position(start_input):
                    start_row, start_col = self.get_coords(start_input)
                else:
                    print(f"\nТакого поля нет!")
                    continue

                self.available_choice((start_row, start_col),
                                     self.what_is(Figures(self.board.board[start_row][start_col])))

                end_input = input(f"{self.current_turn} делают ход. Конечная позиция: ")

                if end_input.lower() == 'end':
                    print("\nИгра окончена.")
                    self.is_game_over = True
                    break
                elif 'back_' in end_input:
                    try:
                        count_back = abs(int(end_input.lower().split('_')[1]))
                        self.rollback_move(count_back)
                    except:
                        print("\nx ∈ N!")
                else:
                    if self.is_valid_position(end_input):
                        end_row, end_col = self.get_coords(end_input)
                    else:
                        print(f"\nТакого поля нет!")
                        continue

                    self.make_move((start_row, start_col), (end_row, end_col),
                                   Figures(self.board.board[start_row][start_col]))

                    print(f"Количество сделанных ходов: {self.count}")

    def get_coords(self, position):
        column = ord(position[0]) - ord('a')
        row = 8 - int(position[1])
        return row, column

    def is_valid_position(self, position):
        position = position.lower()  # Позицию в нижний регистр
        return re.match('[a-h][1-8]', position) is not None

    def rollback_move(self, count_back):
        if len(self.history) >= count_back:
            len_True = len(self.history) == count_back

            for _ in range(count_back):
                last_move = self.history.pop(-1)
                self.board.move_piece(last_move[0][0], last_move[1][0], last_move[0][1], last_move[1][1])
                self.current_turn = 'чёрные' if self.current_turn == 'белые' else 'белые'
                self.count -= 1

            if not len_True:
                print("\nХод белых.") if self.current_turn == 'чёрные' else print("\nХод чёрных.")
                print(f"Количество сделанных ходов: {self.count}")
            else:
                print('\n')

            return True

        else:
            print(f"\nНевозможно вернуться назад на {count_back}!")

            return False

    def available_choice(self, start_pos, figure):
        available_choice_ = []

        for end_input_ in self.position:
            end_pos = self.get_coords(end_input_)
            end_figure = self.board.board[end_pos[0]][end_pos[1]]

            if end_figure.islower() != figure.color or end_figure == '.':
                if figure.move(start_pos, end_pos, self.board.board):
                    available_choice_.append(end_input_)

        if len(available_choice_) > 0:
            print(f"Возможные ходы: {'; '.join(available_choice_)}")

        return

    def available_hit(self):
        available_hit_ = []

        for end_input_ in self.position:
            available_hit_for_figure = []

            for start_input_ in self.position:

                if start_input_ != end_input_:
                    start_pos = self.get_coords(start_input_)
                    end_pos = self.get_coords(end_input_)
                    start_figure_ = self.board.board[start_pos[0]][start_pos[1]]

                    if start_figure_ != '.':
                        start_figure_ = self.what_is(Figures(start_figure_))

                        if self.current_turn == 'белые' and not start_figure_.color or \
                                self.current_turn == 'чёрные' and start_figure_.color:
                            end_figure_ = self.board.board[end_pos[0]][end_pos[1]]

                            if end_figure_.islower() != start_figure_.color and end_figure_ != '.':
                                if start_figure_.move(start_pos, end_pos, self.board.board):
                                    available_hit_for_figure.append([start_figure_.piece, start_input_])

            if len(available_hit_for_figure) > 0:
                available_hit_.append([[end_figure_, end_input_], available_hit_for_figure])

        if len(available_hit_) > 0:
            print(f"\nОсторожно, ваши фигуры под ударом:")

            for row in available_hit_:
                row_print = f"{row[0][0]} на {row[0][1]}: "

                for row_figure in row[1]:
                    row_print += f"{row_figure[0]} на {row_figure[1]}; "

                print(row_print)

        return

    def what_is(self, piece_):
        if piece_.piece.lower() == 'p':
            return Pawn(piece_.piece)
        elif piece_.piece.lower() == 'r':
            return Rook(piece_.piece)
        elif piece_.piece.lower() == 'b':
            return Bishop(piece_.piece)
        elif piece_.piece.lower() == 'n':
            return Knight(piece_.piece)
        elif piece_.piece.lower() == 'q':
            return Queen(piece_.piece)
        elif piece_.piece.lower() == 'k':
            return King(piece_.piece)
        else:
            print("\nФигура не определена!")
            return


# Запуск
game = ChessGame()
game.play()