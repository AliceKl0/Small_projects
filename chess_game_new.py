import re

print("*" * 10, " Шахматы ", "*" * 10)
print("       Доступные команды:       \n1. < -вернуться на ход назад; \n2. reading -чтение нотации из файла; "
      "\n  1) - -ход назад; \n  2) + -ход вперёд \n3. recording -запись игры \n4. end -конец игры \n")

# Задаём игровое поле
board = [
    ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
    ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
]

history = []
history_record = []

# Выводим игровое поле
def print_board():
    print('  a b c d e f g h')
    for i in range(8):
        print(str(8 - i) + ' ' + ' '.join(board[i]))
    print('  a b c d e f g h')

# Корректна ли введённая позиция?
def is_valid_position(position):
    position = position.lower() # Позицию в нижний регистр
    return re.match('[a-h][1-8]', position) is not None


# Получаем координаты из позиции
def get_coordinates(position):
    column = ord(position[0]) - ord('a')
    row = 8 - int(position[1])
    return row, column

# Что за фигура?
def what_piece(coord, board):
    coord_row, coord_col = get_coordinates(coord)

    return board[coord_row][coord_col]

# Передвижение фигур
def move_piece(source, target):
    if not is_valid_position(source) or not is_valid_position(target):
        return False

    source_row, source_col = get_coordinates(source)
    target_row, target_col = get_coordinates(target)

    piece = board[source_row][source_col]

    # Проверяем, что между начальной и конечной позициями нет фигур
    if piece.lower() != 'n':
        if source_row == target_row:  # По горизонтали
            start_col, end_col = sorted([source_col, target_col])
            if any(board[source_row][col] != '.' for col in range(start_col + 1, end_col)):
                return False
        elif source_col == target_col:  # По вертикали
            start_row, end_row = sorted([source_row, target_row])
            if any(board[row][source_col] != '.' for row in range(start_row + 1, end_row)):
                return False
        elif abs(source_row - target_row) == abs(source_col - target_col):  # По диагонали
            start_row, end_row = sorted([source_row, target_row])
            start_col, end_col = sorted([source_col, target_col])

            for row in range(start_row + 1, end_row):
                for col in range(start_col + 1, end_col):
                    find_piece = board[row][col] != '.'

                    break

                if find_piece:
                    break
                    return False

    # Проверяем, корректен ли ход для выбранной фигуры
    if not is_valid_move(piece, source_row, source_col, target_row, target_col, board):
        return False

    # Проверяем, необходимость превращения пешки
    if piece.lower() == 'p' and target_row in [0, 7]:
        piece = ''  # Превращаем пешку в слона

    # Передвигаем фигуру
    board[source_row][source_col] = '.'
    board[target_row][target_col] = piece

    return True

# Корректен ли ход для выбранной фигуры?
def is_valid_move(piece, source_row, source_col, target_row, target_col, board):
    if board[source_row][source_col] != '.':
            if board[target_row][target_col] != '.':
                same_registr = not (board[source_row][source_col] + board[target_row][target_col]).islower()\
            and not (board[source_row][source_col] + board[target_row][target_col]).isupper()
            else:
                same_registr = True

            if same_registr:
                # Ладья
                if piece.lower() == 'r':
                    # Ход по вертикали/горизонтали?
                    if source_row == target_row or source_col == target_col:
                        return True
                    else:
                        return False

                # Конь
                elif piece.lower() == 'n':
                    # Ход буквой L?
                    if abs(target_row - source_row) == 2 and abs(target_col - source_col) == 1:
                        return True
                    elif abs(target_row - source_row) == 1 and abs(target_col - source_col) == 2:
                        return True
                    else:
                        return False

                # Слон
                elif piece.lower() == 'b':
                    # Ход по диагонали?
                    if abs(target_row - source_row) == abs(target_col - source_col):
                        return True
                    else:
                        return False

                # Королева
                elif piece.lower() == 'q':
                    # Вертикаль, горизонталь, диагональ?
                    if is_valid_move('r', source_row, source_col, target_row, target_col, board) or \
                            is_valid_move('b', source_row, source_col, target_row, target_col, board):
                        return True
                    else:
                        return False

                # Король
                elif piece.lower() == 'k':
                    # Ход на "единичку" ?
                    if abs(target_row - source_row) <= 1 and abs(target_col - source_col) <= 1:
                        return True
                    else:
                        return False

                # Пешка
                elif piece.lower() == 'p':
                    if source_row in [1, 6]:
                        if ((source_col == target_col and (
                                abs(target_row - source_row) == 1 or abs(target_row - source_row) == 2) and
                             board[target_row][target_col] == '.') or (
                                    abs(target_col - source_col) == 1 and abs(target_row - source_row) == 1 and
                                    board[target_row][target_col] != '.')) \
                                and (source_row - target_row > 0 if piece == 'P' else source_row - target_row < 0):
                            return True
                        else:
                            return False
                    else:
                        if ((source_col == target_col and abs(target_row - source_row) == 1 and board[target_row][
                            target_col].lower() == '.') or \
                            (abs(target_col - source_col) == 1 and abs(target_row - source_row) == 1 and
                             board[target_row][target_col] != '.')) \
                                and (source_row - target_row > 0 if piece == 'P' else source_row - target_row < 0):
                            return True
                        else:
                            return False
    else:
        print('В исходной клетке нет фигуры!')
        return False

# На ход назад
def rollback_move():
    if len(history) > 0:
        last_move = history.pop(-1)
        i_1, i_2, i_3, i_4 = last_move
        history_record.append([i_2, i_1, '#' + i_4, i_3])
        source_row, source_col = get_coordinates(last_move[0])
        target_row, target_col = get_coordinates(last_move[1])
        board[source_row][source_col] = last_move[2]
        board[target_row][target_col] = last_move[3]

        return board, history, history_record

    else:
        print("Нет возможности вернуться к предыдущему ходу!")

        return False

# Запись игры
def record_game(ind, record_start, history_record, game_on=True):
    with open('chess_game.txt', 'a+') as file:
        if len(history_record) >= 2 and record_start == False:
            for index in range(1, len(history_record), 2):

                file.write(str(ind) + '.' + ' ' + history_record[index - 1][2] + history_record[index - 1][0]
                           + ('-' if history_record[index - 1][3] == '.'
                              else 'x' + history_record[index - 1][3])
                           + history_record[index - 1][1]
                           + ' ' + history_record[index][2] + history_record[index][0]
                           + ('-' if history_record[index][3] == '.'
                              else 'x' + history_record[index][3])
                           + history_record[index][1] + '\n')

                ind += 1

        elif len(history_record) >= 2 and len(history_record) % 2 == 0 and record_start and game_on:
            file.write(str(ind) + '.' + ' ' + history_record[-2][2] + history_record[-2][0]
                       + ('-' if history_record[-2][3] == '.' else 'x' + history_record[-2][3])
                       + history_record[-2][1] + ' ' +
                       history_record[-1][2] + history_record[-1][0]
                       + ('-' if history_record[-1][3] == '.' else 'x' + history_record[-1][3])
                       + history_record[-1][1] + '\n')

            ind += 1

        elif not game_on and len(history_record) % 2 != 0 and record_start:
            file.write(str(ind) + '.' + ' ' + history_record[-1][2] + history_record[-1][0]
                       + ('-' if history_record[-1][3] == '.' else 'x' + history_record[-1][3])
                       + history_record[-1][1])

            ind += 1

    return ind

# Чтение игры
def read_game(filename):
    with open(filename, 'r') as file:
        history_read_ = ['-'.join(row.split()) for row in file]

    for row_i in range(len(history_read_)):
        while 'x' in history_read_[row_i]:
            history_read_[row_i] = history_read_[row_i].replace('x', '-', 1)

    history_read_ = [row.split('-')[1::] for row in history_read_]
    history_read_ = [[coord[0] + '+' + coord[1::] if len(coord) == 3 else coord if coord[0] != '#'
    else coord[:2:] + '+' + coord[2::] if len(coord) == 4 else coord for coord in row] for row in history_read_]

    history_read__ = []

    for row in history_read_:
        history_read__.append([row[0], row[1]])

        if len(row) == 4:
            history_read__.append([row[2], row[3]])

    for row in history_read__:
        if len(row[1]) == 2:
            row[1] = '.' + '+' + row[1]


    for row_i in range(len(history_read__)):
        history_read__[row_i] = '+'.join(history_read__[row_i]).split('+')

    history_read = []

    for row_i in range(len(history_read__)):
        i_1, i_2, i_3, i_4 = history_read__[row_i]
        history_read.append([i_2, i_4, i_1, i_3])

    return history_read

def back_forward_read(move, cur_ind, history_read, k):
    if move == '-' and cur_ind - 1 >= -1:
        source_row, source_col = get_coordinates(history_read[cur_ind][0])
        target_row, target_col = get_coordinates(history_read[cur_ind][1])
        board[source_row][source_col] = board[target_row][target_col]

        if history_read[cur_ind][3] == '.':
            board[target_row][target_col] = '.'
        else:
            board[target_row][target_col] = history_read[cur_ind][3]

        i_1, i_2, i_3, i_4 = history.pop(-1)
        history_record.append([i_2, i_1, '#' + i_4, i_3])

        return board, history, history_record, cur_ind - 1, k - 1

    elif move == '+' and cur_ind + 1 <= len(history_read) - 1:
        source_row, source_col = get_coordinates(history_read[cur_ind + 1][0])
        target_row, target_col = get_coordinates(history_read[cur_ind + 1][1])
        board[target_row][target_col] = board[source_row][source_col]
        board[source_row][source_col] = '.'

        history.append(history_read[cur_ind + 1])
        history_record.append(history_read[cur_ind + 1])

        return board, history, history_record, cur_ind + 1, k + 1

    else:
        print("Команда невозможна!")

# Основной цикл игры
def play_chess():
    print_board()

    record_start = False
    k = 0
    game_on = True

    while game_on:
        if k % 2 == 0:
            player = 'Белые'
        else:
            player = 'Чёрные'

        source = input('\n' + f'{player} делают ход. Выберите текущую позицию фигуры: ')

        if source == 'reading':
            filename = input("Введите имя файла: ")

            history_reading = read_game(filename)
            history_read = []

            for row in history_reading:
                history_record.append(row)
                history_read.append(row) if row[2][0] != '#' else history_read.pop(-1)

            current_index = len(history_read) - 1

            for row in history_read:
                k += 1
                source = row[0]
                target = row[1]

                history.append(row)

                move_piece(source, target)

                print('\n')
                print_board()
                print(f'Количество сделанных ходов: {k}')

        else:
            if source == 'recording' and record_start == False:
                i = 1

                ind = record_game(i, record_start, history_record)

                record_start = True

            elif source == 'recording' and record_start == True:
                print("Запись партии уже идёт!")

            elif source == '<':
                if len(rollback_move()) > 1:
                    print_board()

                    k -= 1

                    print(f'Количество сделанных ходов: {k}')

                    if record_start == True:
                        i = ind
                        ind = record_game(i, record_start, history_record)

            elif source == '-' or source == '+':

                try:
                    current_index_new = current_index
                    current_index, k = back_forward_read(source, current_index_new, history_read, k)[3::]

                    print_board()

                    print(f'Количество сделанных ходов: {k}')

                    if record_start == True:
                        i = ind
                        ind = record_game(i, record_start, history_record)

                except:
                    continue

            elif source == 'end':
                game_on = False

                if record_start:
                    record_game(ind, record_start, history_record, game_on)
                print("Игра окончена!")

            else:
                target = input(f'{player} делают ход. Выберите будущую позицию фигуры: ')

                try:
                    piece_source = what_piece(source, board)
                    piece_target = what_piece(target, board)

                except:
                    continue

                if move_piece(source, target):
                    history.append([source, target, piece_source, piece_target])
                    history_record.append([source, target, piece_source, piece_target])
                    k += 1

                    print_board()
                    print(f'Количество сделанных ходов: {k}')

                    if record_start == True:
                        i = ind
                        ind = record_game(i, record_start, history_record)

                else:
                    print('Ход невозможен. Попробуйте снова.')

# Запуск игры
play_chess()