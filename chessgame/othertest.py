import sqlite3
try:
    # for Python2
    from Tkinter import *
except ImportError:
    # for Python3
    from tkinter import *
import os
from main import chess_game as offline_chess
from servertest import chess_game as server_chess
from clienttest import chess_game as client_chess
from PIL import ImageTk, Image


connection = sqlite3.Connection('Users.db')
c = connection.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS Users(
    USERNAME text PRIMARY KEY,
    PASSWORD text,
    GAMESWON int,
    GAME_SET text)""")
# Designing window for registration


def register():
    global register_screen
    register_screen = Toplevel(main_screen)
    register_screen.title("Register")
    register_screen.geometry("300x250")

    global username
    global password
    global username_entry
    global password_entry
    username = StringVar()
    password = StringVar()

    Label(register_screen, text="Please enter details below", bg="blue").pack()
    Label(register_screen, text="").pack()
    username_lable = Label(register_screen, text="Username * ")
    username_lable.pack()
    username_entry = Entry(register_screen, textvariable=username)
    username_entry.pack()
    password_lable = Label(register_screen, text="Password * ")
    password_lable.pack()
    password_entry = Entry(register_screen, textvariable=password, show='*')
    password_entry.pack()
    Label(register_screen, text="").pack()
    Button(register_screen, text="Register", width=10, height=1, bg="blue", command=lambda:register_user(c, connection)).pack()


# Designing window for login

def login():
    global login_screen
    login_screen = Toplevel(main_screen)
    login_screen.title("Login")
    login_screen.geometry("300x250")
    Label(login_screen, text="Please enter details below to login").pack()
    Label(login_screen, text="").pack()

    global username_verify
    global password_verify

    username_verify = StringVar()
    password_verify = StringVar()

    global username_login_entry
    global password_login_entry

    Label(login_screen, text="Username * ").pack()
    username_login_entry = Entry(login_screen, textvariable=username_verify)
    username_login_entry.pack()
    Label(login_screen, text="").pack()
    Label(login_screen, text="Password * ").pack()
    password_login_entry = Entry(login_screen, textvariable=password_verify, show='*')
    password_login_entry.pack()
    Label(login_screen, text="").pack()
    Button(login_screen, text="Login", width=10, height=1, command=lambda: login_verify(c)).pack()


# Implementing event on register button

def register_user(c, conn):
    username_info = username.get()
    password_info = password.get()
    s = Label(register_screen, text="Registration Success", fg="green", font=("calibri", 11))
    c.execute("""SELECT * FROM Users WHERE USERNAME = ?""", (username_info,))
    InDB = c.fetchall()
    if len(InDB) == 1:
        user_exist()
    else:
        c.execute("""INSERT INTO Users VALUES(?,?,?,?)""", (username_info, password_info, 0, ""))
        conn.commit()

        s.pack()
    #file = open(username_info, "w")
    #file.write(username_info + "\n")
    #file.write(password_info)
    #file.close()

    username_entry.delete(0, END)
    password_entry.delete(0, END)



# Implementing event on login button

def login_verify(c):
    username1 = username_verify.get()
    password1 = password_verify.get()
    username_login_entry.delete(0, END)
    password_login_entry.delete(0, END)

    #list_of_files = os.listdir()
    #if username1 in list_of_files:
        #file1 = open(username1, "r")
        #verify = file1.read().splitlines()
        #if password1 in verify:
            #login_success()

        #else:
            #password_not_recognised()

    #else:
        #user_not_found()
    try:
        c.execute("""SELECT * FROM Users WHERE USERNAME = ?""", (username1,))
        global InDB
        InDB = c.fetchall()

        if len(InDB) == 1:
            if InDB[0][1] == password1:

                login_success()
            else:
                password_not_recognised()
        else:
            user_not_found()
        #need to find way to check the password too
        #for row in records:
            #if row[1] == password1:
                #login_success()
            #else:
                #password_not_recognised()

    except sqlite3.Error:
        user_not_found()

# Designing popup for login success
def start_game(set):
    game = offline_chess(set)
    game.main()

def start_server(set):
    global online_choice
    online_choice = Toplevel(login_success_screen)
    online_choice.geometry("450x300")
    online_choice.title("Online")
    Button(online_choice, text="Create room", command =online_room).pack()
    Button(online_choice, text="Join room", command=join_room).pack()

def online_room():
    global room
    room = Toplevel(online_choice)
    room.title("Choose Your Color")
    room.geometry("450x300")
    Button(room, text="Play black", command=lambda: create_room('black')).pack()
    Button(room, text="Play white", command=lambda:create_room('white')).pack()
    Button(room, text="Play random", command=lambda:create_room('random')).pack()
    #Button(room, text="Play", command= host_play).pack()

def create_room(color):
    global join
    join = Toplevel(online_choice)
    join.geometry("450x300")
    join.title("Create room")
    room_id = StringVar()
    Entry(join,textvariable=room_id , text="enter id").pack()
    kp = 0
    room =Button(join, text="create room", command= lambda: creategame(room_id.get(),kp,color))
    room.pack()
    Label(join, text="Put port number as password for room", font=("calibri", 11)).pack()

def join_room():
    global join
    join = Toplevel(online_choice)
    join.geometry("450x300")
    join.title('Join Room')
    Label(join,text = 'Put the port to connect').pack()
    room_id = StringVar()
    room_id.set(5000)
    Entry(join, textvariable=room_id, text="enter id").pack()
    kp = 0
    room = Button(join, text="join room", command=lambda: joingame(room_id.get(), kp))
    room.pack()
def joingame(room_id, kp):
    main_screen.destroy()
    kp += 1
    if kp < 2:
        print(int(room_id))
        client_chess(int(room_id), InDB[0][3]).mainclient()
def creategame(room_id, kp,color):
    main_screen.destroy()
    kp+=1
    if kp < 2:
        if len(room_id) == 0:
            room_id = 5000
        print(int(room_id))
        server_chess(int(room_id), InDB[0][3],color).mainserver()
def login_success():
    global login_success_screen
    login_success_screen = Toplevel(login_screen)
    login_success_screen.title("Mainpage")
    login_success_screen.geometry("250x150")
    Label(login_success_screen, text="Main Screen", bg="green", width="250", height="2", font=("Calibri", 13)).pack()
    Label(text="").pack()
    Button(login_success_screen, text="User settings", command=user_settings).pack()
    Button(login_success_screen, text="play online", command = lambda: start_server(get_set())).pack()
    Button(login_success_screen, text="play offline", command= lambda: start_game(get_set())).pack()
    Button(login_success_screen, text="Exit game", command=delete_login_success).pack()

def get_set():
    return InDB[0][3]

def update_indb(new):
    global InDB
    InDB = new

def user_settings():
    user_page = Toplevel(login_success_screen)
    user_page.title("Set Settings")
    user_chess_set = Entry()
    set_name = "" + InDB[0][3] + ""
    text = StringVar()
    text.set(set_name)
    match_name = Entry(user_page, textvariable=text, text="Change your set")
    match_name.pack()
    t = Label(user_page, text="Put the set name that you want to use", font=("calibri", 11))
    t.pack()
    t1 = Label(user_page, text="download the images to the images folder", font=("calibri", 11))
    t2 = Label(user_page, text="name them: first the set, then the color of the piece (b - black, w - white)", font=("calibri", 11))
    t3 = Label(user_page, text="and then the initial of the piece name", font=("calibri", 11))
    t4 = Label(user_page, text="p - pawn, B- bishop, N - knight, K- king, Q - queen, R - rook ", font=("calibri", 11))
    t1.pack()
    t2.pack()
    t3.pack()
    t4.pack()
    global Vame_label
    Vame_label = Label(user_page, text=set_name)
    print(set_name)
    change_name_button =Button(user_page, text="change set", command= lambda: change_set(match_name.get()))

    change_name_button.pack()
    Vame_label.pack()

#def Change_name_label():
    #Vame_label.config(text="" +)
def fetch_new(username):
    c.execute("""SELECT * FROM Users WHERE USERNAME = ?""", (username,))
    NewInDB = c.fetchall()
    return NewInDB
def change_set(set):
    c.execute(''' UPDATE USERS
                  SET GAME_SET = ?
                  WHERE USERNAME = ?''', (set, InDB[0][0]))
    connection.commit()
    name = InDB[0][0]
    new =fetch_new(name)
    print(new[0][3])
    update_indb(new)
    print(InDB[0][3])
# Designing popup for login invalid password


def password_not_recognised():
    global password_not_recog_screen
    password_not_recog_screen = Toplevel(login_screen)
    password_not_recog_screen.title("Success")
    password_not_recog_screen.geometry("150x100")
    Label(password_not_recog_screen, text="Invalid Password ").pack()
    Button(password_not_recog_screen, text="OK", command=delete_password_not_recognised).pack()


def user_exist():
    global user_exist_screen
    user_exist_screen = Toplevel(register_screen)
    user_exist_screen.title("Failure")
    user_exist_screen.geometry("150x100")
    Label(user_exist_screen, text="Username already exists").pack()
    Button(user_exist_screen, text="OK", command=delete_user_exist_screen).pack()
# Designing popup for user not found

def user_not_found():
    global user_not_found_screen
    user_not_found_screen = Toplevel(login_screen)
    user_not_found_screen.title("Success")
    user_not_found_screen.geometry("150x100")
    Label(user_not_found_screen, text="User Not Found").pack()
    Button(user_not_found_screen, text="OK", command=delete_user_not_found_screen).pack()


# Deleting popups

def delete_login_success():
    login_success_screen.destroy()
def delete_user_exist_screen():
    user_exist_screen.destroy()

def delete_password_not_recognised():
    password_not_recog_screen.destroy()


def delete_user_not_found_screen():
    user_not_found_screen.destroy()


# Designing Main(first) window

def main_account_screen():
    global main_screen
    global logged_in
    logged_in = False
    main_screen = Tk()
    main_screen.geometry("280x220")
    t = Label(main_screen, text="Simple Chess - Asaf Elran Lichtenstein", bg = 'blue')
    t.pack()
    bg = ImageTk.PhotoImage(Image.open("images/chesspicture.png"))
    canvas1 = Canvas(width=400, height=400)
    canvas1.pack(fill="both", expand=True)
    canvas1.create_image(0, 0, image=bg, anchor="nw")
    canvas1.create_text(150, 210, text="Welcome")
    Start_button = Button(text="Press to start", command=lambda: Login_registerscreen(canvas1,t ))
    button1_canvas = canvas1.create_window(100, 10, anchor="nw", window=Start_button)
    main_screen.mainloop()


def Login_registerscreen(canvas1, t):
    t.destroy()
    canvas1.destroy()
    main_screen.title("Account Login")
    Label(text="Select Your Choice", bg="blue", width="300", height="2", font=("Calibri", 13)).pack()
    Label(text="").pack()
    Button(text="Login", height="2", width="30", command=login).pack()
    Label(text="").pack()
    Button(text="Register", height="2", width="30", command=register).pack()

def main():
    main_account_screen()

if __name__ == '__main__':
    main()