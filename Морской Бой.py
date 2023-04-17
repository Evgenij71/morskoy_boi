from random import randint

class BoardException(Exception):
    pass

class BoardOutException(BoardException):
    def __str__(self):
        return "нельзя стрелять за доску"

class BoardUsedException(BoardException):
    def __str__(self):
        return "в клетку уже стреляли"

class BoardWrongShipException(BoardException):
    pass


class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Dot({self.x}, {self.y})"




class Ship:
    def __init__(self, b, l, o):
        self.b = b
        self.l = l
        self.o = o
        self.live = l

    @property
    def points(self):
        ship_points = []
        for i in range(self.l):
            c_x = self.b.x
            c_y = self.b.y

            if self.o == 0:
                c_x += i

            elif self.o == 1:
                c_y += i

            ship_points.append(point(c_x, c_y))

        return ship_points

    def shooting(self, fire):
        return fire in self.points


class Board:
    def __init__(self, hid=False, size=6):
        self.size = size
        self.hid = hid

        self.k = 0

        self.f = [["O"] * size for _ in range(size)]

        self.b = []
        self.ships = []

    def __str__(self):
        r = ""
        r += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.f):
            r += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.hid:
            r = r.replace("■", "O")
        return r

    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def K(self, ship, verb=False):
        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.points:
            for dx, dy in near:
                cur = point(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.b:
                    if verb:
                        self.f[cur.x][cur.y] = "."
                    self.b.append(cur)

    def a_ship(self, ship):
        for d in ship.points:
            if self.out(d) or d in self.b:
                raise BoardWrongShipException()
        for d in ship.points:
            self.f[d.x][d.y] = "■"
            self.b.append(d)

        self.ships.append(ship)
        self.K(ship)

    def fire(self, d):
        if self.out(d):
            raise BoardOutException()

        if d in self.b:
            raise BoardUsedException()

        self.b.append(d)

        for ship in self.ships:
            if d in ship.points:
                ship.live -= 1
                self.f[d.x][d.y] = "X"
                if ship.live == 0:
                    self.k += 1
                    self.K(ship, verb=True)
                    print("корабль подбит")
                    return False
                else:
                    print("попал!")
                    return True

        self.f[d.x][d.y] = "x"
        print("мимо")
        return False

    def xx(self):
        self.b = []


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.fire(target)
                return repeat
            except BoardException as e:
                print(e)


class AI(Player):
    def ask(self):
        d = point(randint(0, 5), randint(0, 5))
        print(f"Ход компьютера: {d.x + 1} {d.y + 1}")
        return d


class User(Player):
    def ask(self):
        while True:
            cords = input("Ваш ход: ").split()

            if len(cords) != 2:
                print(" Введите 2 координаты! ")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()):
                print(" Введите числа! ")
                continue

            x, y = int(x), int(y)

            return point(x - 1, y - 1)


class Game:
    def try_board(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(point(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.a_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.xx()
        return board

    def random_board(self):
        board = None
        while board is None:
            board = self.try_board()
        return board

    def __init__(self, size=6):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = True

        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def greet(self):
        print("-------------------")
        print("  Приветсвуем вас  ")
        print("      в игре       ")
        print("    морской бой    ")
        print("-------------------")
        print(" формат ввода: x y ")
        print(" x - номер строки  ")
        print(" y - номер столбца ")

    def loop(self):
        num = 0
        while True:
            print("-" * 20)
            print("Доска пользователя:")
            print(self.us.board)
            print("-" * 20)
            print("Доска компьютера:")
            print(self.ai.board)
            print("-" * 20)
            if num % 2 == 0:
                print("Ходит пользователь!")
                repeat = self.us.move()
            else:
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.k == 7:
                print("-" * 20)
                print("Пользователь выиграл!")
                break

            if self.us.board.k == 7:
                print("-" * 20)
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):
                self.greet()
                self.loop()

g = Game()
g.start()