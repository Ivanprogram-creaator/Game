import random
import tkinter


def prepare_and_start():
    global player, exit, fires, enemies, player_pos
    obj_pos = []
    canvas.delete("all")
    player_pos = (random.randint(0, N_X - 1) * step,
                  random.randint(0, N_Y - 1) * step)
    obj_pos.append(player_pos)
    canvas.pack()
    player = canvas.create_image(player_pos, image=player_pic, anchor='nw')
    exit_pos = (random.randint(0, N_X - 1) * step,
                random.randint(0, N_Y - 1) * step)
    while exit_pos in obj_pos:
        exit_pos = (random.randint(0, N_X - 1) * step,
                    random.randint(0, N_Y - 1) * step)
    exit = canvas.create_image(exit_pos, image=exit_pic, anchor='nw')
    N_FIRES = 6  # Число клеток, заполненных огнем
    fires = []
    for i in range(N_FIRES):
        fire_pos = (random.randint(0, N_X - 1) * step,
                    random.randint(0, N_Y - 1) * step)
        while fire_pos in obj_pos:
            fire_pos = (random.randint(0, N_X - 1) * step,
                        random.randint(0, N_Y - 1) * step)
        fire = canvas.create_image(fire_pos, image=fire_pic, anchor='nw')
        fires.append(fire)
    N_ENEMIES = 5  # Число врагов
    enemies = []
    for i in range(N_ENEMIES):
        enemy_pos = (random.randint(0, N_X - 1) * step,
                     random.randint(0, N_Y - 1) * step)
        while enemy_pos in obj_pos:
            enemy_pos = (random.randint(0, N_X - 1) * step,
                         random.randint(0, N_Y - 1) * step)
        enemy = canvas.create_image(enemy_pos, image=enemy_pic,
                                    anchor='nw')
        enemies.append(enemy)
    label.config(text="Найди выход!")
    master.bind("<KeyPress>", key_pressed)


def random_move(enemy):
    ret = [0, 0]
    s = [canvas.coords(player)[0] - canvas.coords(enemy)[0],
         canvas.coords(player)[1] - canvas.coords(enemy)[1]]
    if s[0] < 0:
        ret[0] = canvas.coords(enemy)[0] - step
    elif s[0] > 0:
        ret[0] = canvas.coords(enemy)[0] + step
    if s[1] < 0:
        ret[1] = canvas.coords(enemy)[1] - step
    elif s[1] > 0:
        ret[1] = canvas.coords(enemy)[1] + step
    print(ret)
    return ret


def move_wrap(obj, move):
    if move[0] < 0:
        canvas.coords(obj, (step * N_X - step, move[1]))
    elif move[0] > step * N_X - step:
        canvas.coords(obj, (0, move[1]))
    elif canvas.coords(obj)[1] < 0:
        canvas.coords(obj, (move[0], step * N_Y - step))
    elif canvas.coords(obj)[1] > step * N_Y - step:
        canvas.coords(obj, (move[0], 0))


def do_nothing(x):
    pass


def check_move():
    if canvas.coords(player) == canvas.coords(exit):
        label.config(text="Победа!")
        master.bind("<KeyPress>", do_nothing)
    for f in fires:
        if canvas.coords(player) == canvas.coords(f):
            label.config(text="Ты проиграл!")
            master.bind("<KeyPress>", do_nothing)
    for e in enemies:
        if canvas.coords(player) == canvas.coords(e):
            label.config(text="Ты проиграл!")
            master.bind("<KeyPress>", do_nothing)


def key_pressed(event):
    if event.keysym == 'space':
        canvas.coords(player, (
            player_pos[0], player_pos[1]))
    if event.keysym == 'Up':
        canvas.move(player, 0, -step)
    elif event.keysym == 'Down':
        canvas.move(player, 0, step)
    elif event.keysym == 'Left':
        canvas.move(player, -step, 0)
    elif event.keysym == 'Right':
        canvas.move(player, step, 0)
    for enemy in enemies:
        direction = random_move(
            enemy)  # вызвать функцию перемещения у "врага"
        canvas.coords(enemy, direction[0], direction[1])
        move_wrap(enemy,
                  canvas.coords(enemy))  # произвести  перемещение
    move_wrap(player, canvas.coords(player))
    check_move()


step = 60  # Размер клетки
N_X = 10
N_Y = 10  # Размер сетки
master = tkinter.Tk()
player_pic = tkinter.PhotoImage(file="images/player.png")
exit_pic = tkinter.PhotoImage(file="images/exit.png")
fire_pic = tkinter.PhotoImage(file="images/fire.png")
enemy_pic = tkinter.PhotoImage(file="images/enemy.png")
label = tkinter.Label(master, text="Найди выход")

canvas = tkinter.Canvas(master, bg='cyan',
                        height=N_X * step, width=N_Y * step)
canvas.pack()
restart = tkinter.Button(master, text="Начать заново",
                         command=prepare_and_start)

prepare_and_start()
restart.pack()
label.pack()
master.mainloop()
