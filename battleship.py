# -----------------------------------___Импорт___-----------------------------------------------------------------------
import random


# -----------------------------------___Игровое поле___-----------------------------------------------------------------
class Dot:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def __eq__(self, other):                            # Проверка на совпадение точек(Координат)
        return self.x == other.x and self.y == other.y

    def __repr__(self):                                 # Создание и вывод точки (Координаты)
        return f"({self.x}, {self.y})"                  # и проверка нахождения в списках


# -----------------------------------___Исключения___-------------------------------------------------------------------
class SeaBug(Bug):                                      # Общий класс исключений
    pass


class SeaOutBug(SeaBug):                                 #  Выстрел вне поля
    def __str__(self):
        return f"Там точно нет кораблей противника!\n Заряжай по новой."


class SeaUsedBug(SeaBug):                                 #  Выстрел в одну и туже точку
    def __str__(self):
        return f"Капитан снаряд не может попасть в одну и туже точку дважды.\n Заряжай по новой"


class SeaWrongShipBug(SeaBug):                             #  Проверка размещения кораблей
    pass


-----------------------------------___Корабли___------------------------------------------------------------------------

