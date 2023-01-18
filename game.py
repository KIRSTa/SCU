from mobs import Mob_carry,Mob_Tank

#два игрока ходят по очереди (player1,player2)
#вопрос, за кого вы хотите играть (танк/убийца)
#while true (0-tank,1-killer)
#создание двух объектов (mobs - tank/killer)
#пропуск хода или атака 
#если пропуск хода, то прибавляем 10 hp, а если атака, то -hp у противника (method - damage (20))
#либо вывод hp, либо смерть; выход из игры Break
last_played = 1

choise_player_1= input("Выберите либо Танка (0), либо Кери (1): ")
if choise_player_1 == '0':
    player1=Mob_Tank()
else:
    player1=Mob_carry()

choise_player_2= input("Выберите либо Танка (0), либо Кери (1): ")
if choise_player_2 == '0':
    player2=Mob_Tank()
else:
    player2=Mob_carry()

while True:
    choise_player= input("Что вы хотите сделать (0)-пропуск хода, (1)-атака: ")
    if choise_player == '0':
        if last_played == 1:
            player1.hill() # дописать метод в класс mob
        else:
            player2.hill()



    if last_played == 1:
        last_played == 2
    else:
        last_played == 1

