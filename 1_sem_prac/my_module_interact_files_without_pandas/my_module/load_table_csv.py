from csv import *


def l_t_csv(*file_names):
    table_load = []
    columns = False

    for file_name in file_names:
        with open(file_name, 'r', newline='') as csvfile:
            file = DictReader(csvfile, delimiter=';')
            table_1 = list(file)
            table = []

            if not isinstance(table_1, list):
                table.append(table_1)
            else:
                table = [i for i in table_1]

            if not columns:
                columns = list(table[0])

            if list(table[0]) != columns:
                print('Ошибка в структуре таблиц!')
            else:
                for i in table:
                    table_load.append(i)
            # s = list(map(list, zip(*list(file))))
            # table = {line[0]: line[1::] for line in s}
    return table_load


def s_t_csv(file_name, table_load):
    with open(file_name, 'w', newline='') as csvfile:
        file = writer(csvfile, delimiter=';')
        file.writerow(table_load[0])
        for i in table_load:
            file.writerow([i.get(j) for j in i])