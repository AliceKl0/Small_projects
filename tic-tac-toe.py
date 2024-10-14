print ("Крестики-нолики")

play_field = list(range(1,10))

def draw_play_field (play_field):
    print (" " + "-" * 13)
    for i in range(3):
        print( " " + "|", play_field[0 + i * 3], "|", play_field[1 + i * 3], "|", play_field[2 + i * 3], "|")
        print(" " + "-" * 13)

def game (n_player):
    b = False
    while not b:
        move = input ("В какую клетку ставим " + n_player + "? ")
        try:
            move=int(move)
        except:
            print ("Вы должны ввести число от 1 до 9 включительно!")
            continue
        if 1<=move<=9:
            if str(play_field[move - 1]) not in 'OX':
                play_field[move - 1]=n_player
                b=True
            else:
                print ("Клетка занята!")
        else:
            print("Вы должны ввести число от 1 до 9 включительно!")

def win (play_field):
    win_pose = [[0,3,6],[1,4,7],[2,5,8],[0,1,2],[3,4,5],[6,7,8],[0,4,8],[2,4,6]]
    for i in win_pose:
        if play_field[i[0]]==play_field[i[1]]==play_field[i[2]]:
            return (play_field [i[0]])
    return False

def process (play_field):
    winn=False
    schetchik=0
    while not winn:
        draw_play_field(play_field)
        if schetchik%2==0:
            game("O")
        else:
            game("X")
        schetchik+=1
        if schetchik >= 5:
            pobedaTF=win(play_field)
            if pobedaTF:
                winn = True
                print ("Победил игрок", pobedaTF)
        if schetchik == 9:
            print ("Ничья")
            break
    draw_play_field (play_field)
process (play_field)