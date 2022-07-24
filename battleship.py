from random import randint

# -----------------------------------___Переменные___-------------------------------------------------------------------
# a = 0 #
b = '~' * 30  #
c = ' Приветствуем вас '   #
d = ' Капитан! '           #
e = 'Готовы к сражению?!'  #
# x = 0  # Вертикаль
# y = 0  # Горизонталь
greetings = f"""{b:^30}\n{c:~^30}\n{d:~^30}\n{b}"""


# -----------------------------------___Внутренняя логика___------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# -----------------------------------___Исключения___-------------------------------------------------------------------
class BoardOutException(Exception):
    """Исключение выстрелить в клетку за пределами поля"""

    def __str__(self):
        return "Капитан, корабли не ходят по суше.\n Заряжай по новой.\n"


class BoardUsedException(Exception):
    """Повторный выстрел в одну и туже координату"""

    def __str__(self):
        return "Капитан снаряд не может попасть в одну и туже точку дважды.\n Заряжай по новой.\n"


class BoardWrongShipException(Exception):
    """Проверка размещения кораблей """
    pass


# -----------------------------------___Точки на поле___----------------------------------------------------------------
class Dot:
    """Класс точек"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):                                                # Проверка на совпадение точек(Координат)
        return self.x == other.x and self.y == other.y


# -----------------------------------___Корабли___----------------------------------------------------------------------
class Ship:
    """Корабли ship : начальная координата, length : Длинна, orient : Ориентация, lives : жизнь корабля"""
    def __init__(self,  ship, length, orient):
        self.ship = ship
        self.length = length
        self.orient = orient
        self.lives = length

    @property
    def dots(self):                                                         # Метод возвращает список всех точек корабля
        ship_dots = []
        for i in range(self.length):                                        # Корабль(длина)
            cur_x = self.ship.x
            cur_y = self.ship.y

            if self.orient == 0:                                            # Вертикальный
                cur_x += i

            elif self.orient == 1:                                          # Горизонтальный
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))                             # Добавление точки в список после выстрела
        return ship_dots

    def shooting(self, shot):                                                # Проверка попадания по кораблю
        return shot in self.dots


# -----------------------------------___Игровая доска___----------------------------------------------------------------
class Board:
    """Игровое поле (доска)"""
    def __init__(self, hid=False, size=6):                                     # Поле
        self.size = size
        self.hid = hid

        self.count = 0                                                          # Кол-во поражённых кораблей

        self.field = [["~"] * size for _ in range(size)]                        # Сетка

        self.busy = []                                                          # Занятые координаты
        self.ships = []                                                         # Список кораблей на доске

    def add_ship(self, ship):                                                   # Размещение корабля на поле

        for a in ship.dots:                                                     # Проверка на границы поля и занятость
            if self.out(a) or a in self.busy:                                   # Если ставить не получается
                raise BoardWrongShipException()                                 # Выбрасываем исключения
        for a in ship.dots:
            self.field[a.x][a.y] = "■"
            self.busy.append(a)

        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, verb=False):                                        # Положение корабля с соседними полями
        adjacent = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for a in ship.dots:
            for ax, ay in adjacent:
                cont = Dot(a.x + ax, a.y + ay)
                if not (self.out(cont)) and cont not in self.busy:
                    if verb:
                        self.field[cont.x][cont.y] = "."
                    self.busy.append(cont)

    def __str__(self):                                                            # выводит доску в консоль
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.hid:                                                               # Скрытие кораблей доски
            res = res.replace("■", "~")
        return res

    def out(self, a):                                                   # Проверка на нахождении координаты в поле доски
        return not ((0 <= a.x < self.size) and (0 <= a.y < self.size))

    def shot(self, a):                                                              # Стрельба
        if self.out(a):                                                             # Проверка на границы поля
            raise BoardOutException()

        if a in self.busy:                                                          # Проверка на повторный выстрел
            raise BoardUsedException()

        self.busy.append(a)                                                         # Отмечаем точку выстрела

        for ship in self.ships:                                                     # Проверка на наличие корабля
            if a in ship.dots:                                                      # Попадание по кораблю
                ship.lives -= 1
                self.field[a.x][a.y] = "X"                                          # Отмечаем попадание по кораблю
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, verb=True)                                 # Обводим контур уничтоженного корабля
                    print("Корабль уничтожен!")
                    return False
                else:
                    print("Корабль повреждён!")
                    return True

        self.field[a.x][a.y] = "T"                                                # Промах отмечаем на доске
        print("Не попал!")
        return False

    def begin(self):                                                              # Список выстрелов №№№№№№№
        self.busy = []


# -----------------------------------___Внешняя логика___---------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# -----------------------------------___Игроки___------------------------------------------------------------------------
class Player:
    """Класс родитель для классов с AI и с пользователем board : доска, ai_board : доска соперника"""
    def __init__(self, board, ai_board):
        self.board = board
        self.ai_board = ai_board

    def ask(self):                                                              # В какую клетку делается выстрел
        raise NotImplementedError()

    def move(self):                                                             # делаем ход в игре
        while True:
            try:
                question = self.ask()
                decision = self.ai_board.shot(question)
                return decision
            except BoardUsedException as bag:                                   # Обработка ошибки повторного выстрела
                print(bag)                                                      # по координатам
            except BoardOutException as bag:                                    # Обработка ошибки выстрела за пределы
                print(bag)                                                      # доски


class AI(Player):
    """Класс Компьютер игрок """
    def ask(self):
        a = Dot(randint(0, 5), randint(0, 5))
        print(f"Ход компьютера: {a.x + 1} {a.y + 1}")
        return a


class User(Player):
    """Класс Человек игрок """
    def ask(self):
        while True:
            coordinates = input("Залп по координатам: ").split()

            if len(coordinates) != 2:                                           # Проверка на ввод двух чисел
                print(" Введите два числа через пробел!\n")
                continue

            x, y = coordinates

            if not (x.isdigit()) or not (y.isdigit()):                        # Проверка на ввод чисел, а не др символов
                print(" Введите числа!\n")
                continue

            x, y = int(x), int(y)

            return Dot(x - 1, y - 1)


# -----------------------------------___Игровой процесс___--------------------------------------------------------------
class Game:
    """Игровой процесс"""
    def __init__(self, size=6):
        self.size = size
        player = self.random_board()
        computer = self.random_board()
        computer.hid = True

        self.ai = AI(computer, player)
        self.us = User(player, computer)

    def random_board(self):                                                          # Генератор случайных досок
        board = None
        while board is None:
            board = self.random_place()
        return board

    def random_place(self):                                                          # Генератор расстановки кораблей
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempt = 0
        for length in lens:
            while True:
                attempt += 1
                if attempt > 1000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), length, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board

    def greet(self):                                                                # Приветствие пользователя
        print(greetings)
        print(f"""{ 'формат ввода: x y ':^30}\n{' x - номер строки  ':^30}\n{' y - номер столбца ':^30}""")

    def loop(self):                                                             # Игровой цикл
        num = 0
        while True:                                                             # интерфейс
            print(f"""{b[:-3]}\n{' Доска пользователя: ':^30}\n{self.us.board}""")
            print(f"""{b[:-3]}\n{' Доска компьютера: ':^30}\n{self.ai.board}""")
            if num % 2 == 0:
                print(b[:-3])
                print("Ходит пользователь!")
                repeat = self.us.move()
            else:
                print(b[:-3])
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.count == 7:
                print(f"""{b[:-3]}\n{' Доска компьютера: ':^30}\n{self.ai.board}""")
                print(b[:-3])
                print("Пользователь выиграл!")
                break

            if self.us.board.count == 7:
                print(f"""{b[:-3]}\n{' Доска пользователя: ':^30}\n{self.us.board}""")
                print(b[:-3])
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):                                                             # Запуск игры
        self.greet()
        self.loop()


g = Game()
g.start()
