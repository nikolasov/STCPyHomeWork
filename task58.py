#todo: Создать абстрактный класс Transport (транспорт) содержащий:
# Поля:
# скорость;
# себестоимость перевозки груза;
# стоимость перевозки груза.
# В классе должны быть абстрактные методы:
# метод Cost (без параметров) – вычисление стоимости перевозки груза.
# Метод Info - информация (без параметров), который возвращает строку, содержащую информацию об объекте.
#
# На его основе реализовать дочерние классы:
# Marine - морской транспорт,
# Ground - наземный транспорт.

from abc import ABC, abstractmethod


class Transport(ABC):
    vel = 0
    self_transport_cost = 0
    transport_cost = 0

    @abstractmethod
    def Cost(self):
        pass

    @abstractmethod
    def Info(self):
        pass


class Marine(Transport):
    def __init__(self, _vel, _self_t_cost) -> None:
        super().__init__()
        self.vel = _vel
        self.self_transport_cost = _self_t_cost
        self.Cost()

    def Cost(self):
        #Условная формула рассчета общей стоимости перевозок в зависимости от себестоимости и скорости
        self.transport_cost = self.vel * self.self_transport_cost
    
    def Info(self):
        return str(f"Морские перевозки: v = {self.vel}, себестоимость = {self.self_transport_cost},  общая стоимость = {self.transport_cost}")


class Ground(Transport):
    def __init__(self,_vel,_self_t_cost) -> None:
        super().__init__()
        self.vel = _vel
        self.self_transport_cost = _self_t_cost
        self.Cost()
    
    def Cost(self):
        #Условная формула рассчета общей стоимости перевозок в зависимости от себестоимости и скорости
        self.transport_cost = self.vel * self.self_transport_cost - 150
    
    def Info(self): 
        return str(f"Наземные перевозки: v = {self.vel}, себестоимость = {self.self_transport_cost},  общая стоимость = {self.transport_cost}")


m = Marine(30, 100)
g = Ground(60, 300)

print(m.Info())
print(g.Info())
