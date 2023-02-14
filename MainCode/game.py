from tkinter import *
from customtkinter import *
from PIL import Image 
from tkinter import messagebox
import random
import main
import sqlite3 
with sqlite3.connect("Registration_Table.db") as conn  :
    c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, email TEXT NOT NULL, password TEXT NOT NULL)""")

with sqlite3.connect("All_Question_Database.db") as db:
    q = db.cursor()

q.execute("""Create table if not exists AllQuestionData( id INTEGER PRIMARY KEY AUTOINCREMENT, question TEXT NOT NULL, ans1 TEXT NOT NULL, ans2 TEXT NOT NULL, ans3 TEXT NOT NULL, ans4 TEXT NOT NULL, correct_ans TEXT NOT NULL)""")

current_question = 0
sum = 0

def newGameScreen() :  
    playerWindow = CTk()
    playerWindow.title("QUIZ GAME")
    playerWindow.iconbitmap("E:\\1.Main_Quiz\\Image Folder\\logo.ico")
    height = 600
    width = 700
    y = (playerWindow.winfo_screenheight()//2) - (width // 3)
    x = (playerWindow.winfo_screenwidth()//2) - (height // 2)
    playerWindow.geometry('{}x{}+{}+{}'.format(width,height,x,y))
    playerWindow.resizable(False,False)
    
    tabview = CTkTabview(playerWindow, width = width, height = height)
    tabview.pack(fill= BOTH, pady = 10 , padx = 10)
    
    # different tabs for user
    tab_1 = tabview.add("GAME")
    tab_2 = tabview.add("ACCOUNT")
    tabview.set("GAME")
    
    # game window
    # gameFrame 
    gameFrame = CTkFrame( master = tab_1, fg_color = "black", height = 450 , width = width,)
    gameFrame.pack()
    gameFrame.propagate(False)
    
    try :
        # fetching all correct answer
        q.execute("select correct_ans from AllQuestionData")
        correctAnswer = q.fetchall()
        
        # Fetching all questions from database
        q.execute("Select * from AllQuestionData")
        Qall = q.fetchall()
    
    except Exception as e :
        print("Error while fetching data frim database: " + str(e))
    
    # SHUFFLING all questions AND MAKING THEM IN ORDER
    random.shuffle(Qall)
    question_10 = random.sample(Qall,10)
    
    #answer list
    answerlist = [ question_10[current_question][2], question_10[current_question][3],
                  question_10[current_question][4], question_10[current_question][5]]
 
    #gamelabel
    gameQuestionlabel = CTkLabel(master = gameFrame, text = question_10[current_question][1],
                                 width= 100, height= 50, font=("Bodoni MT", 15))
    gameQuestionlabel.place(x = 20, y = 50)
    
    radio_var = StringVar()  # Getting the radio variable value
    
    def newquestion() :
        global current_question
        global sum
        global answerlist

        answerlist = [ question_10[current_question][2], question_10[current_question][3],
                      question_10[current_question][4], question_10[current_question][5]]
        ans1Radiobtn.configure(text = answerlist[0])
        ans2Radiobtn.configure(text = answerlist[1])
        ans3Radiobtn.configure(text = answerlist[2])
        ans4Radiobtn.configure(text = answerlist[3])    

        # if current_question == 9 :
        #     messagebox.showinfo("SCORE",f"Congratulation for completing, \n your score is {sum} !!.\n CLick ok for further information to new game.")
        #     playerWindow.destroy()
        #     playerWindow.withdraw()
        #     new_game = messagebox.askyesno("New Game", "Do you want to play new game ?")
            
        #     if new_game :
        #         current_question = 0
        #         sum = 0
        #         playerWindow.destroy()
        #         playerscreen()
        #     else :
        #         playerWindow.deiconify()
        #         return
        
        if current_question == 9:
            new_game = messagebox.askyesno("SCORE", f"Congratulation for completing, \n your score is {sum} !!.\n Click on yes to play new game.")
            # playerWindow.withdraw()
            submitBtn.configure(text = "New Game")
            
            if new_game:
                current_question = 0
                sum = 0
                playerWindow.destroy()
                playerscreen()
                
            else:
                playerWindow.deiconify()
                return 
            
        value = radio_var.get()
        if value == "":
            messagebox.showinfo("INVALID", "Please select a answer")
            return False

        if value ==  "1":
            submitBtn.configure(state=NORMAL)
            if (answerlist[0],) in correctAnswer:
                sum = sum + 10
            else:
                sum = sum + 0
                
        elif value == "2":
            if (answerlist[1],) in correctAnswer:
                sum = sum + 10
            else:
                sum = sum + 0
                
        elif value == "3":
            if (answerlist[2],) in correctAnswer:
                sum = sum + 10
            else:
                sum = sum + 0
                
        else:
            if (answerlist[3],) in correctAnswer:
                sum = sum + 10
            else:
                sum = sum + 0

        current_question = current_question + 1
        gameQuestionlabel.configure(text=question_10[current_question][1])
        answerlist = [question_10[current_question][2], question_10[current_question][3], 
                    question_10[current_question][4], question_10[current_question][5]]

        ans1Radiobtn.configure(text=answerlist[0])
        ans2Radiobtn.configure(text=answerlist[1])
        ans3Radiobtn.configure(text=answerlist[2])
        ans4Radiobtn.configure(text=answerlist[3])
        
    
    ans1Radiobtn = CTkRadioButton(master = gameFrame, text = answerlist[0], font=("Bodoni MT", 16), value = 1, variable = radio_var)
    ans1Radiobtn.place( x =  40, y = 150)

    ans2Radiobtn = CTkRadioButton(master = gameFrame, text = answerlist[1], font=("Bodoni MT", 16), value = 2, variable = radio_var)
    ans2Radiobtn.place( x = 40, y = 200)

    ans3Radiobtn = CTkRadioButton(master = gameFrame, text = answerlist[2], font=("Bodoni MT", 16), value = 3, variable = radio_var)
    ans3Radiobtn.place(x = 40, y = 250)

    ans4Radiobtn = CTkRadioButton(master = gameFrame, text = answerlist[3], font=("Bodoni MT", 16), value = 4 , variable = radio_var)
    ans4Radiobtn.place(x = 40, y = 300)

    submitBtn = CTkButton(master = tab_1, text = "SUBMIT", 
                          command= newquestion,
                          ) 
    submitBtn.place( x = 250 , y = 475)
    
    def useraccount() :
        # Title
        account_title = CTkLabel(master = tab_2, text = "PROFILE", font = ("Bodoni MT", 28, "bold"))
        account_title.place( x = 60 , y = 10 )
        
        Updateaccount_title = CTkLabel(master = tab_2, text = "UPDATE YOUR ACCOUNT DETAILS", font = ("Bodoni MT", 28, "bold"))
        Updateaccount_title.place( x = 60 , y = 230 )
        
        #image
        ProfileImage = CTkImage(  dark_image=Image.open("E:\\1.Main_Quiz\\Image Folder\\profile.png"),
                                size=(280, 200))
        accountimagelabel = CTkLabel(master = tab_2, image= ProfileImage, text = "" )
        accountimagelabel.place(x= 400, y = 10)
        
        # details info 
        info1 = CTkLabel(master = tab_2, text = "Username :", fg_color= "transparent")
        info1.place(x = 30 , y = 70)
        
        info1 = CTkLabel(master = tab_2, text = "Password :", fg_color= "transparent")
        info1.place(x = 30 , y = 150)
        
        usernameLabel0= CTkLabel(master = tab_2, width= 200, height = 30,font=("Bodoni Mt",17), fg_color= "transparent", text_color= "black", text="")
        usernameLabel0.place(x = 35, y = 100)
        usernameLabel0.configure(text = main.loginusername)
        
        passwordLabel0 = CTkLabel(master = tab_2, width= 200, height = 30,font=("Bodoni Mt",17), fg_color= "transparent", text_color= "black", text="")
        passwordLabel0.place(x = 35, y = 180)
        passwordLabel0.configure(text = main.loginpassword)
        
        # Entry Boxs
        
        Entrybox1 = CTkEntry(master = tab_2, width = 200, height = 30, font=("Bodoni MT",14), text_color= "lightgrey",placeholder_text= " Username")
        Entrybox1.place(x = 250, y = 280)
        
        Entrybox2 = CTkEntry(master = tab_2, width = 200, height = 30, font=("Bodoni MT",14), text_color= "lightgrey",placeholder_text= " Email")
        Entrybox2.place(x = 250, y = 330)
        
        Entrybox3 = CTkEntry(master = tab_2, width = 200, height = 30, font=("Bodoni MT",14), text_color= "lightgrey",placeholder_text= " Password")
        Entrybox3.place(x = 250, y = 380)
        
        
        # Selecting new data
        def selectData():
            global username, password
            try:
                username = main.loginusername
                password = main.loginpassword
                
            except AttributeError as e:
                messagebox.showerror("ERROR", "Username or password is missing")
                return

            try:
                c.execute("SELECT * FROM users WHERE username=? and password=?", (username, password))
                records = c.fetchone()
                if records is None:
                    messagebox.showerror("ERROR", "No user found with the given credentials")
                    return
                
            except Exception as e:
                messagebox.showerror("ERROR", "An error occurred while fetching data")
                return

            Entrybox1.delete(0, END)
            Entrybox2.delete(0, END)
            Entrybox3.delete(0, END)
            
            Entrybox1.insert(0, records[1])
            Entrybox2.insert(0, records[2])
            Entrybox3.insert(0, records[3])

        
        # updating the data 
        def updateData():
            newUsername = Entrybox1.get()
            newEmail = Entrybox2.get()
            newPassword = Entrybox3.get()
            
            try:
                c.execute("SELECT * FROM users where username='"+username+"' and password='"+password+"'")
                records = c.fetchone()
                if records is None:
                    raise Exception("No record found with given username and password")
                new_id = records[0]
                
            except:
                messagebox.showerror("Error", "Failed to fetch user data.")
                return
            
            if not all([newUsername, newEmail, newPassword]):
                messagebox.showwarning("Invalid", "All fields are required.")
                
            elif newUsername == newEmail or newUsername == newPassword:
                messagebox.showerror("ERROR", "Username cannot be similar to email or password.")
                
            elif newEmail == newPassword:
                messagebox.showerror("ERROR", "Email cannot be similar to password.")
                
            elif "@" not in newEmail or ".com" not in newEmail:
                messagebox.showerror("ERROR", "Invalid email format.")
                
            elif len(newPassword) <= 7:
                messagebox.showerror("ERROR", "Password is too short.")
                
            else:
                try:
                    c.execute("update users set username=:usernameData,email=:emailData, password=:passwordData WHERE oid=:id",
                            {
                                "id": new_id,
                                "usernameData": newUsername,
                                "emailData": newEmail,
                                "passwordData": newPassword,
                            })
                    messagebox.showinfo("Success", "User updated successfully.")
                    conn.commit()

                    Entrybox1.delete(0,END)
                    Entrybox2.delete(0,END)
                    Entrybox3.delete(0,END)
                    
                except:
                    messagebox.showerror("Error", "Failed to update user data.")
                
        
        # To destroy the window
        def destroyGame ():
            playerWindow.destroy()
            
            
        SelectingDataButton = CTkButton(master = tab_2 , text = "Select Your Data", fg_color = "transparent", font =  ("Bodoni MT",14) , corner_radius= 8, command = selectData)
        SelectingDataButton.place ( x = 40 , y = 300)
        
        updatingDataButton = CTkButton(master = tab_2 , text = "Update Data", fg_color = "transparent", font =  ("Bodoni MT",14) , corner_radius= 8, command = updateData)
        updatingDataButton.place ( x = 40 , y = 360)
        
        ExistButton = CTkButton(master = tab_2, text= "Exist", font = ("Bodoni MT", 13, "bold"), width= 125, height = 30, corner_radius = 10, state ="normal", command= destroyGame, fg_color= "transparent")
        ExistButton.place( x = 40 , y = 500)
    
    useraccount()
    playerWindow.mainloop()
# newGameScreen()


# First Screen Setup
def playerscreen() :  
    playerWindow = CTk()
    playerWindow.title("QUIZ GAME")
    playerWindow.iconbitmap("E:\\1.Main_Quiz\\Image Folder\\logo.ico")
    height = 600
    width = 700
    y = (playerWindow.winfo_screenheight()//2) - (width // 3)
    x = (playerWindow.winfo_screenwidth()//2) - (height // 2)
    playerWindow.geometry('{}x{}+{}+{}'.format(width,height,x,y))
    playerWindow.resizable(False,False)
    
    tabview = CTkTabview(playerWindow, width = width, height = height)
    tabview.pack(fill= BOTH, pady = 10 , padx = 10)
    
    # different tabs for user
    tab_1 = tabview.add("GAME")
    tab_2 = tabview.add("ACCOUNT")
    tabview.set("GAME")
    
    # game window
    # gameFrame 
    gameFrame = CTkFrame( master = tab_1, fg_color = "black", height = 450 , width = width,)
    gameFrame.pack()
    gameFrame.propagate(False)
    
    q.execute("select correct_ans from AllQuestionData")
    correctAnswer = q.fetchall()
    
    # Fetching all questions from database
    q.execute("Select * from AllQuestionData")
    Qall = q.fetchall()
    
    # SHUFFLING all questions AND MAKING THEM IN ORDER
    random.shuffle(Qall)
    question_10 = random.sample(Qall,10)
    
    #answer list
    answerlist = [ question_10[current_question][2], question_10[current_question][3], question_10[current_question][4], question_10[current_question][5]]
 
    #gamelabel
    gameQuestionlabel = CTkLabel(master = gameFrame, text = question_10[current_question][1], width= 100, height= 50, font=("Bodoni MT", 15))
    gameQuestionlabel.place(x = 20, y = 50)
    
    radio_var = StringVar()  # Getting the radio variable
    
    def submit_answer():
        global current_question
        global sum
        global answerlist

        try:
            answerlist = [question_10[current_question][2], question_10[current_question][3], 
                        question_10[current_question][4], question_10[current_question][5]]
            
        except IndexError as e:
            messagebox.showerror("ERROR", f"An error occurred: {str(e)}")
            return

        ans1Radiobtn.configure(text=answerlist[0])
        ans2Radiobtn.configure(text=answerlist[1])
        ans3Radiobtn.configure(text=answerlist[2])
        ans4Radiobtn.configure(text=answerlist[3])    
        
        
        if current_question == 9:
            new_game = messagebox.askyesno("SCORE", f"Congratulation for completing, \n your score is {sum} !!.\n Click on yes to play new game.")
            # playerWindow.withdraw()
            submitBtn.configure(text = "New Game")
            
            if new_game:
                current_question = 0
                sum = 0
                playerWindow.destroy()
                newGameScreen()
                
            else:
                playerWindow.deiconify()
                return     


        value = radio_var.get()
        if value == "":
            messagebox.showinfo("INVALID", "Please select a answer")
            return False

        if value ==  "1":
            submitBtn.configure(state=NORMAL)
            if (answerlist[0],) in correctAnswer:
                sum = sum + 10
            else:
                sum = sum + 0
                
        elif value == "2":
            if (answerlist[1],) in correctAnswer:
                sum = sum + 10
            else:
                sum = sum + 0
                
        elif value == "3":
            if (answerlist[2],) in correctAnswer:
                sum = sum + 10
            else:
                sum = sum + 0
                
        else:
            if (answerlist[3],) in correctAnswer:
                sum = sum + 10
            else:
                sum = sum + 0

        current_question = current_question + 1
        gameQuestionlabel.configure(text=question_10[current_question][1])
        answerlist = [question_10[current_question][2], question_10[current_question][3], 
                    question_10[current_question][4], question_10[current_question][5]]

        ans1Radiobtn.configure(text=answerlist[0])
        ans2Radiobtn.configure(text=answerlist[1])
        ans3Radiobtn.configure(text=answerlist[2])
        ans4Radiobtn.configure(text=answerlist[3])
       
    
    ans1Radiobtn = CTkRadioButton(master = gameFrame, text = answerlist[0], font=("Bodoni MT", 16), value = 1, variable = radio_var)
    ans1Radiobtn.place( x =  40, y = 150)

    ans2Radiobtn = CTkRadioButton(master = gameFrame, text = answerlist[1], font=("Bodoni MT", 16), value = 2, variable = radio_var)
    ans2Radiobtn.place( x = 40, y = 200)

    ans3Radiobtn = CTkRadioButton(master = gameFrame, text = answerlist[2], font=("Bodoni MT", 16), value = 3, variable = radio_var)
    ans3Radiobtn.place(x = 40, y = 250)

    ans4Radiobtn = CTkRadioButton(master = gameFrame, text = answerlist[3], font=("Bodoni MT", 16), value = 4 , variable = radio_var)
    ans4Radiobtn.place(x = 40, y = 300)

    submitBtn = CTkButton(master = tab_1, text = "SUBMIT", 
                          command= submit_answer,
                          ) 
    submitBtn.place( x = 250 , y = 475)
    
    
    def useraccount() :
        account_title = CTkLabel(master = tab_2, text = "PROFILE", font = ("Bodoni MT", 28, "bold"))
        account_title.place( x = 60 , y = 10 )
        
        Updateaccount_title = CTkLabel(master = tab_2, text = "UPDATE YOUR ACCOUNT DETAILS", font = ("Bodoni MT", 28, "bold"))
        Updateaccount_title.place( x = 60 , y = 230 )
        
        #image
        ProfileImage = CTkImage(  dark_image=Image.open("E:\\1.Main_Quiz\\Image Folder\\profile.png"),
                                size=(280, 200))
        accountimagelabel = CTkLabel(master = tab_2, image= ProfileImage, text = "" )
        accountimagelabel.place(x= 400, y = 10)
        
        # details info 
        info1 = CTkLabel(master = tab_2, text = "Username :", fg_color= "transparent", font = ("Bodoni MT",15,"bold"))
        info1.place(x = 30 , y = 70)
        
        info1 = CTkLabel(master = tab_2, text = "Password :", fg_color= "transparent", font = ("Bodoni MT",15,"bold"))
        info1.place(x = 30 , y = 150)
        
        usernameLabel= CTkLabel(master = tab_2, width= 200, height = 30,font=("Bodoni Mt",17), fg_color= "transparent", text_color= "black", text="")
        usernameLabel.place(x = 35, y = 100)
        usernameLabel.configure(text = main.loginusername)
        
        passwordLabel= CTkLabel(master = tab_2, width= 200, height = 30,font=("Bodoni Mt",17), fg_color= "transparent", text_color= "black", text="")
        passwordLabel.place(x = 35, y = 180)
        passwordLabel.configure(text = main.loginpassword)
        
        # Entry Boxs
        
        Entrybox1 = CTkEntry(master = tab_2, width = 200, height = 30, font=("Bodoni MT",14), text_color= "lightgrey",placeholder_text= " Username")
        Entrybox1.place(x = 250, y = 280)
        
        Entrybox2 = CTkEntry(master = tab_2, width = 200, height = 30, font=("Bodoni MT",14), text_color= "lightgrey",placeholder_text= " Email")
        Entrybox2.place(x = 250, y = 330)
        
        Entrybox3 = CTkEntry(master = tab_2, width = 200, height = 30, font=("Bodoni MT",14), text_color= "lightgrey",placeholder_text= " Password")
        Entrybox3.place(x = 250, y = 380)
        
        
        # selecting userdata from main window
        def selectData():
            global username1, password1
            username1 = main.loginusername
            password1 = main.loginpassword

            try:
                c.execute("SELECT * FROM users WHERE username=? AND password=?", (username1, password1))
                record = c.fetchone()
                
            except Exception as e:
                print(f"An error occurred while fetching data: {e}")
                return

            if record is None:
                print("No record found for the given username and password.")
                return
                
            Entrybox1.delete(0, END)
            Entrybox2.delete(0, END)
            Entrybox3.delete(0, END)

            Entrybox1.insert(0, record[1])
            Entrybox2.insert(0, record[2])
            Entrybox3.insert(0, record[3])


        # updating the data 
        def updateData():
            newUsername = Entrybox1.get()
            newEmail = Entrybox2.get()
            newPassword = Entrybox3.get()
            
            try:
                c.execute("SELECT * FROM users where username='"+username+"' and password='"+password+"'")
                records = c.fetchone()
                if records is None:
                    raise Exception("No record found with given username and password")
                new_id = records[0]
                
            except:
                messagebox.showerror("Error", "Failed to fetch user data.")
                return
            
            if not all([newUsername, newEmail, newPassword]):
                messagebox.showwarning("Invalid", "All fields are required.")
                
            elif newUsername == newEmail or newUsername == newPassword:
                messagebox.showerror("ERROR", "Username cannot be similar to email or password.")
                
            elif newEmail == newPassword:
                messagebox.showerror("ERROR", "Email cannot be similar to password.")
                
            elif "@" not in newEmail or ".com" not in newEmail:
                messagebox.showerror("ERROR", "Invalid email format.")
                
            elif len(newPassword) <= 7:
                messagebox.showerror("ERROR", "Password is too short.")
                
            else:
                try:
                    c.execute("update users set username=:usernameData,email=:emailData, password=:passwordData WHERE oid=:id",
                            {
                                "id": new_id,
                                "usernameData": newUsername,
                                "emailData": newEmail,
                                "passwordData": newPassword,
                            })
                    messagebox.showinfo("Success", "User updated successfully.")
                    conn.commit()

                    Entrybox1.delete(0,END)
                    Entrybox2.delete(0,END)
                    Entrybox3.delete(0,END)
                    
                except:
                    messagebox.showerror("Error", "Failed to update user data.")

                
        # TO destroy the game
        def destroyGame ():
            playerWindow.destroy()
  
        SelectingDataButton = CTkButton(master = tab_2 , text = "Select Your Data", fg_color = "transparent", font =  ("Bodoni MT",14) , corner_radius= 8, command = selectData)
        SelectingDataButton.place ( x = 40 , y = 300)
        
        updatingDataButton = CTkButton(master = tab_2 , text = "Update Data", fg_color = "transparent", font =  ("Bodoni MT",14) , corner_radius= 8, command = updateData)
        updatingDataButton.place ( x = 40 , y = 360)
        
        ExistButton = CTkButton(master = tab_2, text= "Exist", font = ("Bodoni MT", 13, "bold"), width= 125, height = 30, corner_radius = 10, state ="normal", command= destroyGame, fg_color= "transparent")
        ExistButton.place( x = 40 , y = 500)
    
    useraccount()
    playerWindow.mainloop()
# playerscreen()



# ADMIN PART
def adminmain() :
    admin_screen = CTk()
    admin_screen.title("QUIZ GAME")
    admin_screen.iconbitmap("E:\\1.Main_Quiz\Image Folder\\logo.ico")
    height = 500
    width = 700
    y = (admin_screen.winfo_screenheight()//2) - (width // 4)
    x = (admin_screen.winfo_screenwidth()//2) - (height // 2)
    admin_screen.geometry('{}x{}+{}+{}'.format(width,height,x,y))
    admin_screen.resizable(False,False)
    
    tabview = CTkTabview(admin_screen, width = width, height = height, corner_radius= 10, border_color = "black", border_width = 2)
    tabview.pack(fill= BOTH, pady = 10 , padx = 10)
    
    #CREATING TABS
    tab_1 = tabview.add("HOME")
    tab_2 = tabview.add("MY-ACCOUNT")
    tab_3 = tabview.add("GAME SETTINGS")
    tabview.set("HOME")
    
    
    def killgame0():
        admin_screen.destroy()
    
    
    ExistButton  = CTkButton(master = tab_1, text= "Exist", font = ("Bodoni MT", 13, "bold"), width= 125, height = 30, corner_radius = 10, state ="normal", command= killgame0, fg_color= "transparent")
    ExistButton.place( x = 35 , y = 380)
    
    
    def adminAccountWin() :
        accounttitlelabel = CTkLabel(master = tab_2, text = "Account Details", font =("Bodoni MT", 28, "bold"))
        accounttitlelabel.place( x = 50 , y = 10)
        
        usertitlelabel = CTkLabel(master = tab_2, text = "User Account Details", font =("Bodoni MT", 28, "bold"))
        usertitlelabel.place( x = 90 , y = 205)
        
        accountimage = CTkImage(  dark_image=Image.open("E:\\1.Main_Quiz\\Image Folder\\chainsaw.gif"),
                                size=(280, 200))
        accountimagelabel = CTkLabel(master = tab_2, image= accountimage, text = "" )
        accountimagelabel.place(x= 350, y = 10)
        
        #DETAILS of Administrator
        info1 = CTkLabel(master = tab_2, text = "Admin Username :", fg_color= "transparent")
        info1.place(x = 30 , y = 70)

        info1 = CTkLabel(master = tab_2, text = ": Rohan", fg_color= "transparent")
        info1.place(x = 30 , y = 100)
        
        info1 = CTkLabel(master = tab_2, text = "Admin password :", fg_color= "transparent")
        info1.place(x = 30 , y = 130)
        
        info1 = CTkLabel(master = tab_2, text = ": Universe.369", fg_color= "transparent")
        info1.place(x = 30 , y = 160)
        
        userAccountsLabel= CTkLabel(master = tab_2, width= 350, height = 100,font=("Bodoni Mt",14), corner_radius= 8, fg_color= "lightgrey", text_color= "black", text="")
        userAccountsLabel.place(x = 35, y = 255)
        
        valueEntry = CTkEntry(master = tab_2, width = 150 , height = 30, placeholder_text= "Data ID" )
        valueEntry.place( x = 450, y = 250)
        
        
        # for reading the user account data
        def readdata1():
            
            try:
                newValue1 = valueEntry.get()
                c.execute("SELECT * FROM users WHERE oid=?", (newValue1,))
                allUsers = c.fetchall()

                if not allUsers:
                    raise Exception("No such record found for the given OID")

                userdata1 = allUsers[0]
                userCredentials = f"{userdata1[1]}\n{userdata1[2]}\n{userdata1[3]}"
                userAccountsLabel.configure(text=userCredentials)
                valueEntry.delete(0, END)
                
            except Exception as e:
                print(f"Error: {e}")
                userAccountsLabel.configure(text="")
                valueEntry.delete(0, END)

        
        # Deleteing the user from admin panel
        def deletedata():
            
            try:
                newValue2 = valueEntry.get()
                c.execute("delete from users where oid=?", (newValue2,))
                conn.commit()
                
            except Exception as e:
                messagebox.showerror("ERROR", "AN ERROR OCCURRED: {}".format(e))
                
            finally:
                userAccountsLabel.configure(text="")
                valueEntry.delete(0, END)
        
        
        # deleting the game data
        def killgame () :
            admin_screen.destroy()
            
            
        # buttons
        dataShowButton0 = CTkButton(master = tab_2, text = "Show data", font=("Bodoni MT", 14, "bold"), width = 150 , height = 30, corner_radius= 8, state = "normal", 
                                   command = readdata1,
                                   )
        dataShowButton0.place( x = 450, y = 300)
        
        dataDeleteButton0 = CTkButton(master = tab_2, text = "Delete data", font=("Bodoni MT", 14, "bold"), width = 150 , height = 30, corner_radius= 8, state = "normal",
                                     command = deletedata,
                                     )
        dataDeleteButton0.place( x = 450, y = 350)
        
        ExistButton2  = CTkButton(master = tab_2, text= "Exist", font = ("Bodoni MT", 13, "bold"), width= 125, height = 30, corner_radius = 10, state ="normal", command= killgame, fg_color= "transparent")
        ExistButton2.place( x = 35 , y = 380)
        
    adminAccountWin()
    
  
    
    # GAME-SETTING WINDOW
    def adminSettingWin() :
        # Title
        settingTitle = CTkLabel(master = tab_3, text = "Welcome to the Game Settings", font=("Bodoni MT", 30, "bold"))
        settingTitle.place( x = 150 , y = 5)
        
        # label to display
        displayLabel = CTkLabel(master = tab_3,width = 450, height = 80, corner_radius= 8, text= "", fg_color = ("white"), text_color ="black")
        displayLabel.place( x = 30 , y = 100)
        
        # Entry Boxes
        
        readEntry = CTkEntry(master = tab_3, width = 100 , height = 30, placeholder_text= "Data ID" )
        readEntry.place( x = 60, y = 60)
        
        questionEntryBox = CTkEntry(master = tab_3,width = 350 , height = 20, font = ("Bodoni MT", 12, "bold"),placeholder_text= "Enter a Question", corner_radius= 8)
        questionEntryBox.place( x = 300, y = 200)
        
        firstAnswerBox = CTkEntry(master = tab_3,width =200 , height = 20 , font = ("Bodoni MT", 12, "bold"),placeholder_text= "Enter the first answer", corner_radius=8)
        firstAnswerBox.place(x = 300 , y = 235)
        
        secondAnswerBox = CTkEntry(master = tab_3,width = 200, height = 20 , font = ("Bodoni MT",12, "bold"), placeholder_text= "Enter the second answer", corner_radius=8)
        secondAnswerBox.place(x = 300 , y = 270)
        
        thirdAnswerBox = CTkEntry(master = tab_3,width = 200, height =20, font = ("Bodoni MT",12, "bold"), placeholder_text = "Enter the third answer", corner_radius=8)
        thirdAnswerBox.place(x = 300 , y = 305)
        
        fourthAnswerBox = CTkEntry(master = tab_3,width =200, height= 20, font = ("Bodoni MT",12, "bold"), placeholder_text = "Enter the fourth answer", corner_radius=8)
        fourthAnswerBox.place(x = 300 , y = 340)
        
        correctAnswerBox = CTkEntry(master = tab_3,width =200 , height = 20 , font = ("Bodoni MT", 12, "bold"),placeholder_text= "Enter the correct answer", corner_radius=8)
        correctAnswerBox.place(x = 300 , y = 375)
                        
                               
        # Adding new Question
        def addingquestion():
            question0 = questionEntryBox.get()
            firstanswer0 = firstAnswerBox.get()
            secondanswer0 = secondAnswerBox.get()
            thirdanswer0 = thirdAnswerBox.get()
            fourthanswer0 = fourthAnswerBox.get()
            correctanswer0 = correctAnswerBox.get()

            try:
                q.execute("SELECT COUNT(*) FROM AllQuestionData WHERE question = '" + question0 + "' ")
                question_records = q.fetchone()[0]

                questiondata0 = [
                    question0,
                    firstanswer0,
                    secondanswer0,
                    thirdanswer0,
                    fourthanswer0,
                    correctanswer0,
                ]
                
                # Return is important and mandatory after every statement
                if question_records > 0:
                    messagebox.showerror("INVALID", "ERROR: QUESTION ALREADY EXISTS")
                    return

                elif not all(questiondata0):
                    messagebox.showerror("INVALID UPDATE", "ERROR: ALL FIELDS ARE REQUIRED")
                    return

                elif question0 in questiondata0[1:]:
                    messagebox.showwarning("WARNING", "QUESTION AND ANSWER CANNOT BE SIMILAR")
                    return

                elif len(set(questiondata0[1:4])) != len(questiondata0[1:4]):
                    messagebox.showwarning("WARNING", "ALL ANSWERS MUST BE DIFFERENT")
                    return

                elif correctanswer0 not in [firstanswer0, secondanswer0, thirdanswer0, fourthanswer0]:
                    messagebox.showwarning("WARNING", "Correct answer must be equal to one of the answer choices.")
                    return

                else:
                    messagebox.showinfo("SUCCESS", "SUCCESSFULLY ADDED QUESTION")
                    q.execute("INSERT INTO AllQuestionData (question, ans1, ans2, ans3, ans4, correct_ans) "
                            "VALUES (?,?,?,?,?,?)", questiondata0)
                    db.commit()
                    questionEntryBox.delete(0, END)
                    firstAnswerBox.delete(0, END)
                    secondAnswerBox.delete(0, END)
                    thirdAnswerBox.delete(0, END)
                    fourthAnswerBox.delete(0, END)
                    correctAnswerBox.delete(0, END)

            except Exception as e:
                messagebox.showerror("ERROR", "AN ERROR OCCURRED: {}".format(e))

        
        # For Reading and displaying the answer and question in the label box
        def readdata2():
            
            try:
                newValue3 = readEntry.get()
                q.execute("SELECT * FROM AllQuestionData WHERE oid='" + newValue3 + "'")
                questionShown = q.fetchall()

                if not questionShown:
                    raise ValueError("No record found for the given ID")

                questiondata = questionShown[0]
                displayedQuestion = questiondata[1] + "\n" + questiondata[2] + "\n" + questiondata[3] + "\n" + questiondata[4] + "\n" + questiondata[5]
                displayLabel.configure(text=displayedQuestion)
                readEntry.delete(0, END)

            except ValueError as e:
                messagebox.showerror("ERROR", str(e))

            except Exception as e:
                messagebox.showerror("ERROR", "An error occurred: {}".format(e))
        
        
        # For deleting the Data
        def deletedata2():
            
            try:
                newValue4 = readEntry.get()
                q.execute("DELETE FROM AllQuestionData WHERE oid = '" + newValue4 + "'")
                db.commit()
                displayLabel.configure(text="")
                readEntry.delete(0, END)

            except Exception as e:
                messagebox.showerror("ERROR", "AN ERROR OCCURRED: {}".format(e))
                
        
        # For selecting Data to update
        def selectquestion():
            try:
                new_value = int(readEntry.get())
                
            except ValueError:
                messagebox.showerror("INVALID INPUT", "ERROR: Please enter a valid integer value")
                return
            
            try:
                q.execute("select * from AllQuestionData where oid=?", (new_value,))
                data = q.fetchall()
                
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"An error occured while fetching data: {e}")
                return
            
            if not data:
                messagebox.showerror("NO DATA FOUND", "ERROR: No data found for the given ID")
                return
            
            # Delete previous question and answer data
            questionEntryBox.delete(0, END)
            firstAnswerBox.delete(0, END)
            secondAnswerBox.delete(0, END)
            thirdAnswerBox.delete(0, END)
            fourthAnswerBox.delete(0, END)
            correctAnswerBox.delete(0, END)
            
            # Insert question and answer data
            questionEntryBox.insert(0, data[0][1])
            firstAnswerBox.insert(0, data[0][2])
            secondAnswerBox.insert(0, data[0][3])
            thirdAnswerBox.insert(0, data[0][4])
            fourthAnswerBox.insert(0, data[0][5])
            correctAnswerBox.insert(0, data[0][6])
            
            readEntry.delete(0, END)

        
        # Updating the question and answer.
        def updateData():
            
            try:
                question0 = questionEntryBox.get()
                firstanswer0 = firstAnswerBox.get()
                secondanswer0 = secondAnswerBox.get()
                thirdanswer0 = thirdAnswerBox.get()
                fourthanswer0 = fourthAnswerBox.get()
                correctanswer0 = correctAnswerBox.get()
                newValue6 = readEntry.get()
                
                if question0 == "" or correctanswer0 == "" or firstanswer0 == "" or secondanswer0 == "" or thirdanswer0 == "" or fourthanswer0 == "":
                    raise ValueError("All fields are required !!")
                
                if question0 in [correctanswer0, firstanswer0, secondanswer0, thirdanswer0, fourthanswer0]:
                    raise ValueError("Question and answer cannot be similar")
                
                if firstanswer0 in [secondanswer0, thirdanswer0, fourthanswer0]:
                    raise ValueError("Answer repetition detected, all answers must be different")
                
                if secondanswer0 in [thirdanswer0, fourthanswer0] or thirdanswer0 == fourthanswer0:
                    raise ValueError("Some answers are still found similar")

                q.execute("UPDATE AllQuestionData SET question=:question9, ans1=:firstans9, ans2=:secondans9, ans3=:thirdans9, ans4=:fourthans9, correct_ans=:correctans9 WHERE id=:id",
                        {"id": newValue6, 
                        "question9": question0, 
                        "fisrtans9": firstanswer0,
                        "secondans9": secondanswer0, 
                        "thirdans9": thirdanswer0, 
                        "fourthans9": fourthanswer0,
                        "correctans9": correctanswer0,
                        })
                db.commit()
                
            except Exception as e:
                messagebox.showerror("INVALID UPDATE", f"ERROR: {str(e)}")
                
            else:
                questionEntryBox.delete(0, END)
                firstAnswerBox.delete(0, END)
                secondAnswerBox.delete(0, END)
                thirdAnswerBox.delete(0, END)
                fourthAnswerBox.delete(0, END)
                correctAnswerBox.delete(0, END)

        
        # Showing all data
        def alldata() :
            qustwin= CTkToplevel()
            qustwin.title("QUIZ GAME")
            qustwin.iconbitmap("E:\\1.Main_Quiz\\Image Folder\\logo.ico")
            height = 500
            width = 600
            y = (qustwin.winfo_screenheight()//2) - (width // 4)
            x = (qustwin.winfo_screenwidth()//2) - (height // 4)
            qustwin.geometry('{}x{}+{}+{}'.format(width,height,x,y))
            qustwin.resizable(False,False)
            
            alldatatextbox = CTkTextbox(master = qustwin, font=("Bodoni MT", 15), corner_radius= 8, width = 580, height = 430, activate_scrollbars = True, text_color="white")
            alldatatextbox.place( x = 10, y = 50)
            
            # Fetching all Questions:
            def showallquestion():
                try:
                    q.execute("SELECT * FROM AllQuestionData")
                    questionShown = q.fetchall()
                    
                    alldatatextbox.insert("0.0", questionShown)
                    alldatatextbox.configure(state="disabled")
                except Exception as e:
                    messagebox.showerror("Error", "An error occurred while fetching the question data: {}".format(e))
                
            allDataButton = CTkButton(master = qustwin , text = "SHOW ALL QUESTIONS", font=("Bodoni MT", 16), corner_radius= 8, 
                                      command = showallquestion)
            allDataButton.place( x = 200, y = 10)
                        
        
        # Destroy game
        def decimategame () :
            admin_screen.destroy()
            
        
        # Buttons for game settings
        dataShowButton = CTkButton(master = tab_3, text = "SHOW DATA",width=100, font=("Bodoni MT", 14, "bold"), corner_radius= 8, 
                                   state = "normal", 
                                   command = readdata2,
                                   )
        dataShowButton.place( x = 180, y = 60)
        
        dataDeleteButton = CTkButton(master = tab_3, text = "DELETE DATA",width=100, font=("Bodoni MT", 14, "bold"), corner_radius= 8, 
                                     state = "normal",
                                     command = deletedata2,
                                     )
        
        dataDeleteButton.place( x = 310, y = 60)
        
        addquestionsButton = CTkButton(master = tab_3, text= "ADD NEW QUESTIONS", corner_radius = 8, font=("Bodoni MT",14, "bold"),state = "normal", width = 200,
                                       command = addingquestion,
                                       )
        addquestionsButton.place(x = 30 , y = 200)

        selectupdateQuestionsButton = CTkButton(master = tab_3, text= "SELECT DATA TO EDIT", corner_radius = 8, font=("Bodoni MT",14, "bold"),state = "normal",width = 200,
                                                command = selectquestion,
                                                )
        selectupdateQuestionsButton.place(x = 30 , y = 250)
        
        confirmUpdateQuestionsButton = CTkButton(master = tab_3, text= "UPDATE DATA", corner_radius = 8, font=("Bodoni MT",14, "bold"),
                                                state = "normal", 
                                                width = 200,
                                                command = updateData,
                                                )
        confirmUpdateQuestionsButton.place(x = 30 , y = 300)
        
        showAllQuestionsButton = CTkButton(master = tab_3, text= "SHOW ALL DATA", corner_radius = 8, font=("Bodoni MT",14, "bold"),
                                        state = "normal",
                                        command = alldata,
                                       )
        showAllQuestionsButton.place(x = 455 , y = 60)
        
        ExistButton3  = CTkButton(master = tab_3, text= "Exist", font = ("Bodoni MT", 13, "bold"), width= 125, height = 30, corner_radius = 10,
                                  state ="normal", command= decimategame, fg_color = "transparent")
        ExistButton3.place( x = 35 , y = 380)

    
    adminSettingWin()


    admin_screen.mainloop()
# adminmain()

 