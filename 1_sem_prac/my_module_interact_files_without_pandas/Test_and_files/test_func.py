from pickle import * # создам пользовательский файл прям в этой программе
from my_module import load_table_csv
from my_module import load_table_pickle
from my_module import save_table_txt
from my_module import base_oper

# n = input("Введите путь исходного файла: ")
# n1 = input("Введите путь файла для записи: ")

'''
C:/Users/Alice Klimovich/PycharmProjects/pythonProject/my_module/CSV.file.csv
C:/Users/Alice Klimovich/PycharmProjects/pythonProject/my_module/pickle.txt
C:/Users/Alice Klimovich/PycharmProjects/pythonProject/my_module/txt.txt
'''


# csv
# table = load_table_csv.l_t_csv(n)

# print(table)

# load_table_csv.s_t_csv(n1, table)

# pickle
# table_1 = {'1': 'a', '2': 'b'}
# dump(table_1, open('pickle.txt', 'wb')) # создание исходного пользовательского файла
# table = load_table_pickle.l_t_pickle(n)
# print(table)

# save_table_pickle.s_t_pickle(n1, table)

# txt
# save_table_txt.s_table_txt(n1, table)

# save_table_txt.print_table(table)

test = load_table_csv.l_t_csv('C:/Users/Alice Klimovich/PycharmProjects/pythonProject/my_module/CSV.file.csv')

# print(base_oper.get_rows_by_number(test, 3, None, True))

# print(base_oper.get_rows_by_index(test, False, '6'))

# print(base_oper.get_column_types(test, False))

# types_dict = {'№пп': int, 'Фамилия': int}
# print(base_oper.set_column_types(test, types_dict, False)[0])
# print(base_oper.set_column_types(test, types_dict, False)[1])

# print(base_oper.get_values(test, 2))

# print(base_oper.get_value(test, 'Фамилия', 2))

# values = ['Т', 'Е', 'С', 'Т']
# print(base_oper.set_values(test, values, 2))

# value = 123
# print(base_oper.set_value(test, value, 'Фамилия', 2))

# base_oper.print_table(test)

# types_dict = {'№пп': int}
# test = base_oper.set_column_types(test, types_dict, False)[0]
# print(base_oper.mul(test, 1, 4, False, 1))

'''''''''
table = [
    {'Name': 25, 'Age': 25, 'Salary': 25},
    {'Name': 30, 'Age': 30, 'Salary': 60000},
    {'Name': 'Bob', 'Age': 35, 'Salary': 70000}
]

bool_list = base_oper.eq(table, 1, 2)

print(base_oper.filter_rows(table,bool_list))
'''''''''

'''''''''
table = [
    {'Name': 25, 'Age': 25},
    {'Name': 30, 'Age': 30},
    {'Name': 'Bob', 'Age': 35}
]

table1 = [
    {'Name': 25, 'Age': 25, 'Salary': 25},
    {'Name': 30, 'Age': 30, 'Salary': 60000},
    {'Name': 'Bob', 'Age': 35, 'Salary': 70000}
]

print(base_oper.concat(table, table1))
print(base_oper.split(table1, 2))
'''''''''


# print(load_table_csv.l_t_csv(n))
# print(len(load_table_csv.l_t_csv(n)))

# print(load_table_pickle.l_t_pickle(n, n1))
# print(len(load_table_pickle.l_t_pickle(n, n1)))