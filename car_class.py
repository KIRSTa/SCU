class Car:
    def __init__(self,color,speed,distance=0): # параметры
        self.color=color # поле(атрибут)
        self.speed=speed
        self.distance=distance
    
    def drive(self):
        self.distance += 1

    def reset(self,result):
        self.distance = result

c1=Car(color="Green",speed=100)
c2=Car("Yellow",150)
print(f"Цвет: {c1.color} , Дистанция: {c1.distance}")
for i in range(10000):
    c1.drive()
print(f"Цвет: {c1.color} , Дистанция: {c1.distance}")
c1.reset(50)
print(f"Цвет: {c1.color} , Дистанция: {c1.distance}")

#создать класс токена
#дать поля(атрибуты): цена, название, сеть
#метод увеличения стоимости токена на введённое значение(параметр)
#метод, который уменьшает цену вполовину
#метод вывода инфы (show info)

class Token:
    def __init__(self,price,name,chain): # параметры
        self.price=price # поле(атрибут)
        self.name=name
        self.chain=chain
    def volume(self,rise):
        self.price+=rise
    def decrease(self):
        self.price/=2
t1=Token(245,"BNB","BSC")
print(f"Токен: {t1.name} , Цена: {t1.price} , Сеть: {t1.chain}")
t1.volume(55)
print(f"Токен: {t1.name} , Цена: {t1.price} , Сеть: {t1.chain}")
t1.decrease()
print(f"Токен: {t1.name} , Цена: {t1.price} , Сеть: {t1.chain}")
