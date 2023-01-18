class Car:
    def __init__(self,color,speed,distance=0): # параметры
        self.color = color # поле(атрибут)
        self.speed = speed
        self.distance = distance
     
    def drive(self):
        self.distance += 1

    def reset(self,result):
        self.distance = result

class Truck (Car):
    def __init__(self, color, speed, weith ,distance=0):
        super().__init__(color, speed, distance)
        self.weith = weith   
    def crash(self):
        print("Truck is crashed")
    def drive(self):
        self.distance += 5

c1=Car('red',100,50)
print(c1.distance)
c1.drive()
print(c1.distance)
t1=Truck('green',150,35000,1500)
print(t1.distance)
t1.drive()
print(t1.distance)