import tkinter
import random


def move_wrap(obj, move):
    canvas.move(obj, move[0], move[1])
    if canvas.coords(obj)[1] >= N_Y * step:
        x = canvas.coords(obj)[0]
        canvas.coords(obj, x,  0)
    elif canvas.coords(obj)[1] < 0:
        x = canvas.coords(obj)[0]
        canvas.coords(obj, x,  N_Y * step - step)
    elif canvas.coords(obj)[0] < 0:
        y = canvas.coords(obj)[1]
        canvas.coords(obj, N_X * step - step, y)
    elif canvas.coords(obj)[0] >= N_X * step:
        y = canvas.coords(obj)[1]
        canvas.coords(obj, 0, y)
 # Здесь нужно сделать так, чтобы ушедший
 # "за экран" игрок выходил с другой стороны
def to_player(c):
    p = canvas.coords(player)

    x = step
    if c[0] > p[0]:
        if c[0] - p[0] <= N_X * step - c[0] + p[0]:
            x = -step
    elif p[0] > c[0]:
        if N_X * step - p[0] + c[0] < p[0] - c[0]:
            x = -step
    else:
        x = 0

    y = step
    if c[1] > p[1]:
        if c[1] - p[1] <= N_Y * step - c[1] + p[1]:
            y = -step
    elif p[1] > c[1]:
        if N_Y * step - p[1] + c[1] < p[1] - c[1]:
            y = -step
    else:
        y = 0

    if x != 0 and y != 0:
        if random.randint(0, 1):
            x = 0
        else:
            y = 0

    return x, y


def prepare_and_start():
    global player, exit, fires, enemies, water
    canvas.delete("all")
    player_pos = (random.randint(0, N_X - 1) * step,
    random.randint(0, N_Y - 1) * step)
    player = canvas.create_image(
        (player_pos[0], player_pos[1]), image=player_pic,
        anchor='nw')
    exit_pos = (random.randint(0, N_X - 1) * step,
    random.randint(0, N_Y - 1) * step)

    exit = canvas.create_image(
        (exit_pos[0], exit_pos[1]), image=exit_pic,
        anchor='nw')
    N_FIRES = 7  # Число клеток, заполненных огнем
    fires = []
    for i in range(N_FIRES):
        fire_pos = (random.randint(0, N_X - 1) * step,
        random.randint(0, N_Y - 1) * step)
        fire = canvas.create_image(
            (fire_pos[0], fire_pos[1]), image=fire_pic,
            anchor='nw')
        fires.append(fire)
    N_ENEMIES = 4  # Число врагов
    enemies = []
    for i in range(N_ENEMIES):
        enemy_pos = (random.randint(0, N_X - 1) * step,
                     random.randint(0, N_Y - 1) * step)
        enemy = canvas.create_image(enemy_pos, image=enemy_pic, anchor='nw')
        enemies.append((enemy, random.choice([always_right, random_move, to_player])))
    label.config(text="Найди выход!")
    master.bind("<KeyPress>", key_pressed)
    water_pos = (random.randint(0, N_X - 1) * step,
                 random.randint(0, N_Y - 1) * step)
    water = canvas.create_image(
        (water_pos[0], water_pos[1]), image=water_pic,
        anchor='nw')

def always_right(c):
    return (step, 0)
#def always_left():
#return(-step, 0)
#def always_down():
#return (0, -step)
#def always_up():
# return (0, step)


def random_move(c):
    return random.choice([(step, 0), (-step, 0), (0, step), (0, -step)])


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
        if canvas.coords(player) == canvas.coords(e[0]):
            label.config(text="Ты проиграл!")
            master.bind("<KeyPress>", do_nothing)
    if canvas.coords(player) == canvas.coords(water):
        label.config(text="Holy Delete")
        for fire in fires:
            canvas.delete(fire)


def key_pressed(event):
    if event.keysym == 'Up':
        move_wrap(player, (0, -step))
    if event.keysym == 'Down':
        move_wrap(player, (0, step))
    elif event.keysym == 'Left':
        move_wrap(player, (-step, 0))
    elif event.keysym == 'Right':
        move_wrap(player, (step, 0))
    check_move()
    for enemy in enemies:
        direction = enemy[1](canvas.coords(enemy[0]))  # вызвать функцию перемещения у "врага"
        move_wrap(enemy[0], direction)  # произвести перемещение
 # Здесь нужно дописать то, что нужно,
 # чтобы все остальные клавиши работали
    check_move()


step = 50  # Размер клетки
N_X = 30
N_Y = 17  # Размер сетки
master = tkinter.Tk()
label = tkinter.Label(master, text="Найди выход")
label.pack()
canvas = tkinter.Canvas(master, bg='#FFFDD0',
 height=N_Y * step, width=N_X * step)
canvas.pack()
restart = tkinter.Button(master, text="Начать заново",
 command=prepare_and_start)
player_pic = tkinter.PhotoImage(file="jesus1.png")
exit_pic = tkinter.PhotoImage(file="krest.png")
fire_pic = tkinter.PhotoImage(file="iuda.png")
enemy_pic = tkinter.PhotoImage(file="legion (1).png")
water_pic = tkinter.PhotoImage(file="HolyWater.png")
restart.pack()
prepare_and_start()
master.mainloop()


