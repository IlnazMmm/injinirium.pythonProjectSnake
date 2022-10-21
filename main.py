from game_objects import *
import sqlite3
import sys

class Game:

    def __init__(self):

        pg.init()
        self.WINDOW_SIZE = 1000
        self.TILE_SIZE = 50
        self.screen = pg.display.set_mode([self.WINDOW_SIZE] * 2)
        self.clock = pg.time.Clock()
        self.text = ''
        self.new_game()
        with sqlite3.connect("database.db") as db:
            cursor = db.cursor()

            cursor.execute("""CREATE TABLE IF NOT EXISTS players(
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    name VARCHAR(10),
                                    score INTEGER
                    )""")

    def draw_grid(self):
        [pg.draw.line(self.screen, [50] * 3, (x, 0), (x, self.WINDOW_SIZE))
                                             for x in range(0, self.WINDOW_SIZE, self.TILE_SIZE)]
        [pg.draw.line(self.screen, [50] * 3, (0, y), (self.WINDOW_SIZE, y))
                                             for y in range(0, self.WINDOW_SIZE, self.TILE_SIZE)]

    def new_game(self):
        self.snake = Snake(self)
        self.food = Food(self)

    def update(self):
        self.snake.update()
        pg.display.flip()
        self.clock.tick(60)

    def draw(self):
        self.screen.fill('black')
        self.draw_grid()
        self.food.draw()
        self.snake.draw()

    def check_event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            self.snake.control(event)

    def run(self):
        while True:
            self.check_event()
            self.update()
            self.draw()

    def input_score(self, score):
        try:
            db = sqlite3.connect("database.db")
            cursor = db.cursor()

            sqlite_select_query = "SELECT score FROM players WHERE name = ?"
            cursor.execute(sqlite_select_query, (self.text,))
            record = cursor.fetchone()

            if (int(record[0])<score):
                cursor.execute("UPDATE players SET score = ? WHERE name = ?", (score, self.text))
            db.commit()
        except sqlite3.Error as e:
            print("Error", e)
        finally:
            cursor.close()
            db.close()

    def input_name(self):

        try:
            db = sqlite3.connect("database.db")
            cursor = db.cursor()
            cursor.execute("SELECT name FROM players WHERE name = ?", (self.text))
            record = cursor.fetchone()
            if record == self.text:
                cursor.execute("INSERT INTO players(name, score) VALUES(?, ?)", (self.text, 0))
            db.commit()
        except sqlite3.Error as e:
            print("Error", e)
        finally:
            cursor.close()
            db.close()

    def show_results(self):
        font = pg.font.Font(None, 32)
        x = 0
        y = 250
        color_inactive = pg.Color('lightskyblue3')
        color = color_inactive

        db = sqlite3.connect("database.db")
        cursor = db.cursor()

        sqlite_select_query = "SELECT * FROM players ORDER by score DESC LIMIT 5"

        txt_name = font.render("Имя", True, color)
        txt_score = font.render("Очки", True, color)
        self.screen.blit(txt_name, (x + 420, y))
        self.screen.blit(txt_score, (x + 560, y))

        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()

        flag = True
        while 1:
            for g in pg.event.get():
                if g.type == pg.QUIT:
                    sys.exit()
            if flag:
                for i in records:
                    y+=50
                    name = font.render(i[1], True, color)
                    score = font.render(str(i[2]), True, color)
                    self.screen.blit(name, (x + 420, y))
                    self.screen.blit(score, (x + 560, y))
                    pg.display.update()
                flag = False
        pygame.quit()
        db.commit()
        cursor.close()
        db.close()

    def write_name(self):
        font = pg.font.Font(None, 32)
        clock = pg.time.Clock()
        input_box = pg.Rect(450, 450, 140, 32)
        color_inactive = pg.Color('lightskyblue3')
        color_active = pg.Color('dodgerblue2')
        color = color_inactive
        active = False
        done = False

        while not done:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True
                if event.type == pg.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        active = not active
                    else:
                        active = False
                    color = color_active if active else color_inactive
                if event.type == pg.KEYDOWN:
                    if active:
                        if event.key == pg.K_RETURN:
                            self.run()
                        elif event.key == pg.K_BACKSPACE:
                            self.text = self.text[:-1]
                        else:
                            self.text += event.unicode

            self.screen.fill((30, 30, 30))

            txt_surface = font.render(self.text, True, color)
            txt = font.render("Напишите свое имя", True, color)

            width = max(200, txt_surface.get_width() + 10)
            input_box.w = width

            self.screen.blit(txt, (input_box.x - 5, input_box.y - 30))
            self.screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))

            pg.draw.rect(self.screen, color, input_box, 2)

            pg.display.flip()
            clock.tick(30)

if __name__ == '__main__':
    game = Game()
    game.write_name()