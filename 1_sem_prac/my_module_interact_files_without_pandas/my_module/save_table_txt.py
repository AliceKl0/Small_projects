def s_table_txt(file_name, table_load, space):
    with open(file_name, 'w') as txtfile:
        list_row = list(table_load[0])
        list_row = [str(i) + ' ' * (space - len(i)) for i in list_row]
        row = '|'.join(list_row)

        txtfile.write(row)
        txtfile.write('-' * len(row))

        for i in table_load:
            list_row = [i.get(j) for j in i]
            list_row = [str(i) + ' ' * (space - len(i)) for i in list_row]

            txtfile.write('|'.join(list_row))


def print_table_txt(table_load, space):
    list_row = list(table_load[0])
    list_row = [str(i) + ' ' * (space - len(i)) for i in list_row]
    row = '|'.join(list_row)

    print(row)
    print('-' * len(row))

    for i in table_load:
        list_row = [i.get(j) for j in i]
        list_row = [str(i) + ' ' * (space - len(i)) for i in list_row]

        print('|'.join(list_row))