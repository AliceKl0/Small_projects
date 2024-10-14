def get_rows_by_number(table_load, start, stop, copy_table):
    if copy_table:
        new_table = table_load.copy()

        if stop is None:
            return new_table[start - 1]
        else:
            return new_table[start - 1: stop]
    else:
        if stop is None:
            return table_load[start - 1]
        else:
            return table_load[start - 1: stop]


def get_rows_by_index(table_load, copy_table, *args):
    key_list = list(table_load[0])

    if copy_table:
        if len(args) == 1:  # Получение одной строки по значению в первом столбце
            val = args[0]
            new_table = [row for row in table_load if row[key_list[0]] == val]
        else:  # Получение таблицы из строк со значениями в первом столбце
            new_table = [row for row in table_load if row[key_list[0]] in args]

        return new_table
    else:
        if len(args) == 1:  # Получение одной строки по значению в первом столбце
            val = args[0]
            table_load = [row for row in table_load if row[key_list[0]] == val]
        else:  # Получение таблицы из строк со значениями в первом столбце
            table_load = [row for row in table_load if row[key_list[0]] in args]

        return table_load


def get_column_types(table_load, by_number):
    first_row = table_load[0]
    column_types = {}
    index = 1

    for key, value in first_row.items():
        if by_number:
            column_types[index] = type(table_load[0][key])
            index += 1
        else:
            column_types[key] = type(table_load[0][key])

    return column_types


def set_column_types(table_load, types_dict, by_number):
    headers = list(table_load[0].keys())
    headers = {i + 1: headers[i] for i in range(len(headers))}

    if not by_number:
        for column, column_type in types_dict.items():
            if column_type in [int, float, str, bool]:
                for row in table_load:
                    try:
                        row[column] = column_type(row[column])
                    except:
                        continue
            else:
                print(f"Тип данных не распознан: {column_type}!")
    else:
        for column, column_type in types_dict.items():
            if column_type in [int, float, str, bool]:
                for row in table_load:
                    try:
                        row[headers[column]] = column_type(row[headers[column]])
                    except:
                        continue
            else:
                print(f"Тип данных не распознан: {column_type}!")

    column_types = get_column_types(table_load, by_number)

    return table_load, column_types

def get_values(table_load, column):
    headers = table_load[0].keys()

    if isinstance(column, int):
        column_types = get_column_types(table_load, True).get(column)
        column_name = list(headers)[column - 1]
    else:
        column_types = get_column_types(table_load, False).get(column)
        column_name = column

    column_values = []
    for row in table_load:
        value = row.get(column_name)

        try:
            column_values.append(column_types(value))
        except:
            column_values.append(value)

    return column_values


def get_value(table_load, column, row_number):
    column_values = get_values(table_load, column)
    row_value = column_values[row_number - 1]

    return row_value


def set_values(table_load, values, column):
    headers = table_load[0].keys()

    if isinstance(column, int):
        column_types = get_column_types(table_load, True).get(column)
        column_name = list(headers)[column - 1]
    else:
        column_types = get_column_types(table_load, False).get(column)
        column_name = column

    for index, row in enumerate(table_load):
        if index < len(values):
            value = values[index]

            try:
                value = column_types(value)
                row[column_name] = value

            except:
                row[column_name] = value
        else:
            break

    return table_load


def set_value(table_load, value, column, row_number):
    if isinstance(column, int):
        column_types = get_column_types(table_load, True).get(column)
    else:
        column_types = get_column_types(table_load, False).get(column)

    column_values = get_values(table_load, column)

    try:
        column_values[row_number - 1] = column_types(value)
    except:
        column_values[row_number - 1] = value

    return set_values(table_load, column_values, column)


def print_table(table_load):
    max_len = max(len(str(i)) for i in list(table_load[0]))

    for column in range(len(table_load[0])):
        column_values = get_values(table_load, column)
        max_len = max(max_len, max(len(str(i)) for i in column_values))

    space = max_len + 4
    list_row = list(table_load[0])
    list_row = [str(i) + ' ' * (space - len(i)) for i in list_row]
    row = '|'.join(list_row)

    print(row)
    print('-' * len(row))

    for i in table_load:
        list_row = [i.get(j) for j in i]
        list_row = [str(i) + ' ' * (space - len(i)) for i in list_row]

        print('|'.join(list_row))


def add(table_load, column, value, all=True, row_number=0):
    if isinstance(column, int):
        column_type = get_column_types(table_load, True).get(column)
    else:
        column_type = get_column_types(table_load, False).get(column)

    if column_type in [int, float, bool]:

        if not all: # Применяем к одному элементу
            column_value = get_value(table_load, column, row_number)

            try:
                column_value = column_type(column_value)
                column_value += column_type(value)
                set_value(table_load, column_value, column, row_number)
            except:
                column_value = column_value

        else: # Применяем ко всем, используем один и тот же параметр
            column_values = get_values(table_load, column)

            for index in range(len(column_values)):

                try:
                    column_values[index] = column_type(column_values[index])
                    column_values[index] += column_type(value)
                except:
                    column_values[index] = column_values[index]

            set_values(table_load, column_values, column)

        return table_load
    else:
        return "Недопустимый тип/формат данных для арифм. операций!"


def sub(table_load, column, value, all=True, row_number=0):
    if isinstance(column, int):
        column_type = get_column_types(table_load, True).get(column)
    else:
        column_type = get_column_types(table_load, False).get(column)

    if column_type in [int, float, bool]:

        if not all:  # Применяем к одному элементу
            column_value = get_value(table_load, column, row_number)

            try:
                column_value = column_type(column_value)
                column_value -= column_type(value)
                set_value(table_load, column_value, column, row_number)
            except:
                column_value = column_value

        else:  # Применяем ко всем, используем один и тот же параметр
            column_values = get_values(table_load, column)

            for index in range(len(column_values)):

                try:
                    column_values[index] = column_type(column_values[index])
                    column_values[index] -= column_type(value)
                except:
                    column_values[index] = column_values[index]

            set_values(table_load, column_values, column)

        return table_load
    else:
        return "Недопустимый тип/формат данных для арифм. операций!"


def mul(table_load, column, value, all=True, row_number=0):
    if isinstance(column, int):
        column_type = get_column_types(table_load, True).get(column)
    else:
        column_type = get_column_types(table_load, False).get(column)

    if column_type in [int, float, bool]:

        if not all:  # Применяем к одному элементу
            column_value = get_value(table_load, column, row_number)

            try:
                column_value = column_type(column_value)
                column_value *= column_type(value)
                set_value(table_load, column_value, column, row_number)
            except:
                column_value = column_value

        else:  # Применяем ко всем, используем один и тот же параметр
            column_values = get_values(table_load, column)

            for index in range(len(column_values)):

                try:
                    column_values[index] = column_type(column_values[index])
                    column_values[index] *= column_type(value)
                except:
                    column_values[index] = column_values[index]

            set_values(table_load, column_values, column)

        return table_load
    else:
        return "Недопустимый тип/формат данных для арифм. операций!"


def div(table_load, column, value, all=True, row_number=0):
    if value != 0:
        if isinstance(column, int):
            column_type = get_column_types(table_load, True).get(column)
        else:
            column_type = get_column_types(table_load, False).get(column)

        if column_type in [int, float, bool]:

            if not all:  # Применяем к одному элементу
                column_value = get_value(table_load, column, row_number)

                try:
                    column_value = column_type(column_value)
                    column_value /= column_type(value)
                    set_value(table_load, column_value, column, row_number)
                except:
                    column_value = column_value

            else:  # Применяем ко всем, используем один и тот же параметр
                column_values = get_values(table_load, column)

                for index in range(len(column_values)):

                    try:
                        column_values[index] = column_type(column_values[index])
                        column_values[index] += column_type(value)
                    except:
                        column_values[index] /= column_values[index]

                set_values(table_load, column_values, column)

            return table_load
        else:
            return "Недопустимый тип/формат данных для арифм. операций!"
    else:
        return "Деление на ноль невозможно!"


def eq(table_load, *columns):
    if not isinstance(columns[0], int):
        return [all(row[col] == row[columns[0]] for col in columns[1::]) for row in table_load]
    else:
        headers = list(table_load[0])
        headers = {i + 1: headers[i] for i in range(len(headers))}
        return [all(row[headers[col]] == row[headers[columns[0]]] for col in columns[1::]) for row in table_load]


def gr(table_load, *columns):
    if not isinstance(columns[0], int):
        return [all(row[col] > row[columns[0]] for col in columns[1::]) for row in table_load]
    else:
        headers = list(table_load[0])
        headers = {i + 1: headers[i] for i in range(len(headers))}
        return [all(row[headers[col]] > row[headers[columns[0]]] for col in columns[1::]) for row in table_load]


def ls(table_load, *columns):
    if not isinstance(columns[0], int):
        return [all(row[col] < row[columns[0]] for col in columns[1::]) for row in table_load]
    else:
        headers = list(table_load[0])
        headers = {i + 1: headers[i] for i in range(len(headers))}
        return [all(row[headers[col]] < row[headers[columns[0]]] for col in columns[1::]) for row in table_load]


def ge(table_load, *columns):
    if not isinstance(columns[0], int):
        return [all(row[col] >= row[columns[0]] for col in columns[1::]) for row in table_load]
    else:
        headers = list(table_load[0])
        headers = {i + 1: headers[i] for i in range(len(headers))}
        return [all(row[headers[col]] >= row[headers[columns[0]]] for col in columns[1::]) for row in table_load]


def le(table_load, *columns):
    if not isinstance(columns[0], int):
        return [all(row[col] <= row[columns[0]] for col in columns[1::]) for row in table_load]
    else:
        headers = list(table_load[0])
        headers = {i + 1: headers[i] for i in range(len(headers))}
        return [all(row[headers[col]] <= row[headers[columns[0]]] for col in columns[1::]) for row in table_load]


def ne(table_load, *columns):
    if not isinstance(columns[0], int):
        return [any(row[col] != row[columns[0]] for col in columns[1::]) for row in table_load]
    else:
        headers = list(table_load[0])
        headers = {i + 1: headers[i] for i in range(len(headers))}
        return [all(row[headers[col]] != row[headers[columns[0]]] for col in columns[1::]) for row in table_load]


def filter_rows(table_load, bool_list, copy_table=False):
    if not copy_table:
        return [row for row, boolean in zip(table_load, bool_list) if boolean]
    else:
        table_load = [row for row, boolean in zip(table_load, bool_list) if boolean]
        return table_load


def concat(table1, table2):
    # Проверяем совпадение количества столбцов в обеих таблицах
    if len(table1[0]) != len(table2[0]):
        return "Количество столбцов в таблицах не совпадает"
    else:
        result = [row for row in table1]
        result.extend(row for row in table2)
        return result


def split(table, row_number):
    # Проверяем, что номер строки находится в допустимом диапазоне
    if row_number < 0 or row_number >= len(table):
        return f"Недопустимый номер строки: {row_number}"

    else:
        table1 = table[:row_number]  # Строки до указанной строки (не включая её)
        table2 = table[row_number:]  # Строки от указанной строки включительно

        return table1, table2