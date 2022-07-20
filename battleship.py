# -----------------------------------___Импорт___-----------------------------------------------------------------------
# import random
from random import randint
# -----------------------------------___Внутренняя логика___------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# -----------------------------------___Точки на поле___----------------------------------------------------------------


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # self.color = color

    def __eq__(self, other):                                            # Проверка на совпадение точек(Координат)
        return self.x == other.x and self.y == other.y

    def __repr__(self):                                                 # Создание и вывод точки (Координаты)
        return f"({self.x}, {self.y})"                                  # и проверка нахождения в списках


# -----------------------------------___Исключения___-------------------------------------------------------------------
class SeaBug(Exception):  # Общий класс исключений
    pass


class SeaOutBug(SeaBug):                                                # Выстрел вне поля
    def __str__(self):
        return "Вы пытаетесь выстрелить за доску!"


class SeaUsedBug(SeaBug):                                           # Выстрел в одну и туже точку
    def __str__(self):
        return f"Капитан снаряд не может попасть в одну и туже точку дважды.\n Заряжай по новой"


class SeaWrongShipBug(SeaBug):                                      # Проверка размещения кораблей
    pass


# -----------------------------------___Корабли___----------------------------------------------------------------------
class Ship:
    def __init__(self, bow, length, direct):
        self.bow = bow
        self.length = length
        self.direct = direct
        self.lives = length

    # self.color = color

    @property
    def dots(self):                                                 # Построение (положение) корабля
        ship_dots = []
        for i in range(self.length):                                # Корабль(положение)
            cur_x = self.bow.x
            cur_y = self.bow.y

            if self.direct == 0:                                         # Вертикальный
                cur_x += i

            elif self.direct == 1:                                       # Горизонтальный
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots

    def shooten(self, shot):                                        # Проверка попадания по кораблю
        return shot in self.dots


# -----------------------------------___Игровое поле___-----------------------------------------------------------------
class Sea:
    def __init__(self, mist=False, size=6):                           # Поле
        self.size = size
        self.mist = mist

        self.count = 0                                                  # Кол-во поражённых кораблей

        self.field = [["~"] * size for _ in range(size)]  # Сетка

        self.busy = []                                              # Занятые координаты
        self.ships = []                                             # Список кораблей доски

    def add_ship(self, ship):                                       # Размещение корабля на поле

        for d in ship.dots:                                         # Проверка на границы поля и занятость
            if self.out(d) or d in self.busy:
                raise SeaWrongShipBug()
            self.field[d.x][d.y] = "■"
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, verb=False):                            # Положение корабля с соседними полями
        near = [  # Сдвиги
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    def __str__(self):                                                  # Создание доски
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.mist:                                                    # Скрытие кораблей доски
            res = res.replace("■", "~")
        return res

    def out(self, d):                                                   # Проверка на нахождении координаты в поле доски
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def shot(self, d):                                                  # Стрельба
        if self.out(d):                                                 # Проверка на границы поля
            raise SeaOutBug()

        if d in self.busy:                                             # Проверка на повторный выстрел
            raise SeaUsedBug()

        self.busy.append(d)                                            # Занимаем точку

        for ship in self.ships:                                        # Проверка на наличие корабля
            if d in ship.dots:                                         # Попадание по кораблю
                ship.lives -= 1
                self.field[d.x][d.y] = "X"                             # Отмечаем попадание по кораблю
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)                      # Обводим контур уничтоженного корабля
                    print("Корабль уничтожен!")
                    return False
                else:
                    print("Корабль повреждён!")
                    return True

        self.field[d.x][d.y] = "0"                                     # Промах отмечаем на доске
        print("Не попал!")
        return False

    def begin(self):
        self.busy = []

# -----------------------------------___Внешняя логика___---------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# -----------------------------------___Игроки___------------------------------------------------------------------------


class Player:
    def __init__(self, sea, enemy):
        self.sea = sea                                          # Игровое поле игрока
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def side(self):                                                 # Выстрел
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except SeaUsedBug as e:
                print(e)


class AI(Player):                                                   # Компьютер
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f"Ход компьютера: {d.x + 1} {d.y + 1}")
        return d


class User(Player):                                                   # Игрок
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()

            if len(cords) != 2:                                     # Проверка на ввод двух чисел
                print(" Введите два числа через пробел! ")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):              # Проверка на числа
                print(" Введите числа! ")
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)                             # Возврат координаты

# -----------------------------------___Игровой процесс___--------------------------------------------------------------


class Game:
    def __init__(self, size=6):
        self.size = size
        player = self.random_sea()
        computer = self.random_sea()
        computer.mist = True

        self.ai = AI(computer, player)
        self.us = User(player, computer)

    def random_sea(self):
        sea = None
        while sea is None:
            sea = self.random_place()
        return sea

    def random_place(self):
        lens = [3, 2, 2, 1, 1, 1, 1]                         # Длины кораблей
        sea = Sea(size=self.size)
        attempts = 0
        for length in lens:                                 # Расстановка кораблей
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), length, randint(0, 1))
                try:
                    sea.add_ship(ship)
                    break
                except SeaWrongShipBug:
                    pass
        sea.begin()
        return sea

    def greet(self):
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("     Приветствуем вас     ")
        print("         Капитан          ")
        print("    Готовы к сражению     ")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("    формат ввода: x y     ")
        print("    x - номер строки      ")
        print("    y - номер столбца     ")

    def loop(self):
        num = 0
        while True:
            print("-" * 27)
            print("Доска пользователя:")
            print(self.us.sea)
            print("-" * 27)
            print("Доска компьютера:")
            print(self.ai.sea)
            if num % 2 == 0:                            # Ход игрока
                print("-" * 27)
                print("Ходит пользователь!")
                repeat = self.us.side()
            else:                                      # Ход компьютера
                print("-" * 27)
                print("Ходит компьютер!")
                repeat = self.ai.side()
            if repeat:
                num -= 1

            if self.ai.sea.count == 7:
                print("-" * 27)
                print("Пользователь выиграл!")
                break

            if self.us.sea.count == 7:
                print("-" * 27)
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):
        self.greet()
        self.loop()

# -----------------------------------___Запуск___-----------------------------------------------------------------------


g = Game()
g.start()
