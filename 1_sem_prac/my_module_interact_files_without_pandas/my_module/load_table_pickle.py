from pickle import *


def l_t_pickle(*file_names):
    table_load = []
    columns = False

    for file_name in file_names:
        with open(file_name, 'rb') as pickle:
            table_1 = load(pickle)
            table = []

            if not isinstance(table_1, list):
                table.append(table_1)
            else:
                table = [i for i in table_1]

            if not columns:
                columns = list(table[0])
                table_load = [i for i in table]

            if list(table[0]) != columns:
                print('Ошибка в структуре таблиц!')
            else:
                for i in table:
                    table_load.append(i)
    return table_load


def s_t_pickle(file_name, table_load):
    with open(file_name, 'wb') as pickle:
        dump(table_load, pickle)