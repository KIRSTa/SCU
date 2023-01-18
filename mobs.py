import random 

class Token:
    def __init__(self,price,name,chain,cap): # параметры
        self.price = price # поле(атрибут)
        self.name = name
        self.chain = chain
        self.cap = cap
    def volume(self,rise):
        self.price+=rise
    def decrease(self):
        self.price/=2

def versus(token1:Token,token2:Token):
    if token1.cap > token2.cap:
        print(f"Buy {token1.name}")
    elif token1.cap < token2.cap:
        print(f"Sell {token2.name}")
    else:
        print("Hold")


class Mob:
    def __init__(self,hp,attack,speed):
        self.hp = hp
        self.attack = attack
        self.speed = speed
    def death(self):
        print("Mob is dead")
    def damage(self,power):
        self.hp -= power
        if self.hp < 0:
            self.death()
    
class Mob_mag(Mob):
    def __init__(self, hp, attack, speed,magic_power):
        super().__init__(hp, attack, speed)
        self.magic_power = magic_power

class Mob_carry(Mob):
    def __init__(self, hp, attack, speed,miss_change):
        super().__init__(hp, attack, speed)
        self.miss_change = miss_change
    def damage(self, power):
        if random.randint(0,101) > self.miss_change:
            self.hp -= power 
            if self.hp < 0:
                self.death()
        else:
            print("Miss")
        
class Mob_Tank(Mob):
    def __init__(self, hp, attack, speed,damage_ignore):
        super().__init__(hp, attack, speed)
        self.damage_ignore = damage_ignore
    def damage(self,power):
        self.hp -= power - self.damage_ignore
        if self.hp < 0:
            self.death()

mag1=Mob_mag(100,50,30,70)
mag1.damage(60)
mag1.damage(60)
tank1=Mob_Tank(100,50,30,20)
tank1.damage(60)
tank1.damage(60)
carry1=Mob_carry(100,50,30,50)
carry1.damage(60)
carry1.damage(60)

