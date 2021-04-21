import tkinter as t
import random as v

start_window = t.Tk()
start_window.geometry("800x640")
login = False


def callmainwindow():
    main_window = t.Toplevel(start_window)
    main_window.geometry("800x640")
    a = v.randrange(1, 999)
    username = "guest" + str(a) + ""
    if login == True:
        user = t.Button(main_window, text=username, command=lambda: userinfopage(main_window)).place(x=400, y=0)
    if login == False:
        t.Button(main_window, text="log in or sign up", command=callloginpage).place(x=400, y=0)


def userinfopage(main_window):
    userinfo = t.Toplevel(main_window)
    userinfo.geometry("800x640")


def callloginpage():
    global login_page
    login_page = t.Toplevel(start_window)
    login_page.geometry("300x250")
    login_page.title("Account Login")
    t.Label(login_page, text="Select Your Choice", bg="blue", width="300", height="2", font=("Calibri", 13))
    t.Label(login_page, text="").pack()
    tologin = t.Button(login_page, text="Login", height="2", width="30", command= logininterface).place(x=70, y=100)
    t.Label(login_page, text="").pack()
    toregister = t.Button(login_page, text="Register", height="2", width="30", command= registerinterface).place(x=70, y=200)


def registerinterface():
    registerscreen = t.Toplevel(login_page)
    usernameentry = t.Entry(registerscreen)
    usernameentry.pack()
    passwordentry = t.Entry(registerscreen)
    passwordentry.pack()


def logininterface():
    loginscreen = t.Toplevel(login_page)
    usernameentry = t.Entry(loginscreen)
    usernameentry.pack()
    passwordentry = t.Entry(loginscreen)
    passwordentry.pack()


titlemessage = t.Label(start_window, text="simplechess")
titlemessage.place(x=395, y=50)
guest_login = t.Button(start_window, text="login as guest", command=callmainwindow)
guest_login.place(x=300, y=200)
user_login = t.Button(start_window, text="register or log in", command=callloginpage)
user_login.place(x=150, y=200 )
start_window.mainloop()
