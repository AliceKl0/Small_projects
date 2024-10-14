alph_chisla = {'ноль':0,'один':1, 'два':2, 'две':'2','три':3, 'четыре':4, 'пять':5, 'шесть':6, 'семь':7, 'восемь':8, 'девять':9, 'десять':10,
      'одиннадцать':11, 'двенадцать':12, 'тринадцать':13, 'четырнадцать':14, 'пятнадцать':15, 'шестнадцать':16, 'семнадцать':17, 'восемнадцать':18,
      'девятнадцать':19, 'двадцать':20, 'тридцать':30, 'сорок':40, 'пятьдесят':50, 'шестьдесят':60, 'семьдесят':70, 'восемьдесят':80, 'девяносто':90,
      'сто':100, 'двести':200, 'триста':300, 'четыреста':400, 'пятьсот':500,'шестьсот':600,'семьсот':700,'восемьсот':800,'девятьсот':900,'тысяча':1000,
      'тысяч(и)':'000','минус':'-','плюс':'+','умножитьна':'*', 'скобкаоткрывается':'(', 'скобказакрывается':')', 'плюсминус':'-', 'минусплюс':'-',
      'минусминус':'+'}
znack = ["плюс","минус","умножитьна", '+', '-', '*', 'плюсминус', 'минусплюс', 'минусминус']
scob = ['скобкаоткрывается', 'скобказакрывается', '(', ')']
zamen = ['скобка открывается', 'скобка закрывается', 'умножить на', 'плюс минус', 'минус плюс', 'минус минус']

chis = input("Введите выражение в буквенном виде: ")
for i in zamen:
      while i in chis:
            chis = chis.replace(i, ''.join(i.split()), 1)
chis = chis.split(" ")

ch = []
e = 0
p = False
for i in range (len(chis)):
      if chis[i] not in znack and chis[i] not in scob:
            e += alph_chisla[chis[i]]
            p = True
      else:
            if p:
                  ch.append(e)
                  e = 0
                  p = False
            ch.append(alph_chisla[chis[i]])
      if i == len(chis)-1 and ch[-1] in znack:
            ch.append(e)

kl_zn = ch.count('*') + ch.count('+') + ch.count('-')
if kl_zn >= len(ch) // 2 - ch.count(scob[2]) - ch.count(scob[3]):
      for i in range (len(ch)):
            if ch[i] == '-' and type(ch[i+1]) == int and (i == 0 or (type(ch[i-1]) != int and ch[i-1] != ')')):
                  ch[i+1] = -ch[i+1]
                  ch[i] = '#'
ch =  [i for i in ch if i != '#']

sc_start = []
for i in range(len(ch)):
      if ch[i] == '(':
            sc_start.append(i)
sc_start = sc_start[::-1]

def vch(expr):
      while '*' in expr:
            for ind in range(len(expr)):
                  if expr[ind] == '*':
                        expr[ind] = expr[ind - 1] * expr[ind + 1]
                        expr.pop(ind + 1)
                        expr.pop(ind - 1)
                        break
      while '+' in expr or '-' in expr:
            for ind in range(len(expr)):
                  if expr[ind] == '+':
                        expr[ind] = expr[ind - 1] + expr[ind + 1]
                        expr.pop(ind + 1)
                        expr.pop(ind - 1)
                        break
                  elif expr[ind] == '-':
                        expr[ind] = expr[ind - 1] - expr[ind + 1]
                        expr.pop(ind + 1)
                        expr.pop(ind - 1)
                        break
      return expr

for i in sc_start:
      for j in range (i+1, len(ch)):
            if ch[j] == ')':
                  expr = ch[i+1:j]
                  sc_end = j
                  break
      vch(expr)
      ch[i] = expr[0]
      for a in range(i + 1, sc_end + 1):
            ch[a] = '#'
      ch = [x for x in ch if x != '#']

s = vch(ch)[0]
b = False
sign = True if str(s)[0] == '-' else False
s = abs(s)
for i in alph_chisla:
      if s == alph_chisla[i]:
            b = True
            print ("Ответ:", i) if not sign else print ("Ответ:", 'минус ' + i)
            break
if not b:
      two_end = int(str(s)[-2:])
      d = False
      if two_end != 0:
          for y in alph_chisla:
              if two_end == alph_chisla[y]:
                  d = True
                  break
      s = list(str(s))
      otv = []
      if not d:
            for i in range(len(s)):
                  if s[i] != '0':
                        x = int(s[i]) * 10 ** len(s[i + 1:])
                        if x <= 1000:
                              otv.append(x)
                        elif 1000 < x < 10000:
                              otv.append(int(str(x)[0]) if int(str(x)[0]) != 2 else str(x)[0])
                              otv.append(str(x)[1:])
                        elif x == 10000:
                              otv.append(int(str(x)[:2]))
                              otv.append(str(x)[2:])
      else:
            for i in range(len(s)-2):
                  if s[i] != '0':
                        x = int(s[i]) * 10 ** len(s[i + 1:])
                        if x <= 1000:
                              otv.append(x)
                        elif 1000 < x < 10000:
                              otv.append(int(str(x)[0]) if int(str(x)[0]) != 2 else str(x)[0])
                              otv.append(str(x)[1:])
                        elif x == 10000:
                              otv.append(int(str(x)[:2]))
                              otv.append(str(x)[2:])
            otv.append(two_end)

      otv_str = '' if not sign else 'минус '
      for i in otv:
            for j in alph_chisla:
                  if i == alph_chisla[j]:
                        otv_str += j + ' '
                        break

      print("Ответ:", otv_str)