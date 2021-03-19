import tkinter as tk
import tkinter.ttk as ttk
from tkinter import simpledialog, messagebox

def messages_main_tx(tx): #important defination for apps
    from lib.mixlib import dprint
    dprint("Messages TX: "+str(tx))


def messages_main_gui(main_gui,column,row,path,import_arguments): #important defination for apps
    print("gui sending")


    main_gui.send_message_button = ttk.Button(main_gui.frame)
    main_gui.emails_65x50_png = tk.PhotoImage(file=path+"/emails_65x50.png")
    main_gui.send_message_button.configure(compound='top', image=main_gui.emails_65x50_png, text='Send Message')
    main_gui.send_message_button.grid(column=str(column), padx='25', pady='20', row=str(row), sticky='n')
    import_arguments = f"{import_arguments} send_message_gui"
    func_name = "send_message_gui"
    main_gui.send_message_button.configure(command= lambda: main_gui.apps_func(import_arguments,func_name))


    """
    if you want the add more buttons you will do this;
    
    row += 1
    if row == 6:
        column +=1
        row = 1

    and other button or another thinks with this row and column settings
    """



def send_message_gui(main_gui):
    received_adress = simpledialog.askstring("Input", "Please write receiver adress: ",
                            parent=main_gui.toplevel)
    if received_adress is not None:
        print("Receiver adress: ", received_adress)
    else:
        print("You don't write a receiver adress ?")
        
    message = simpledialog.askstring("Input", "Please write message: ",
                            parent=main_gui.toplevel)
    if message is not None:
        print("Message: ", message)
    else:
        print("You don't write a message ?")
        
    okey = messagebox.askokcancel("Okey",("Receiver adress: "+received_adress+"\n"+"Message: "+message))

    if okey:
        from func.send_message import send_message
        send_message(message,received_adress)


def messages_main_cli(): 
    print("cli sending")
    from lib.mixlib import menu_maker, menu_space

    print(
        menu_maker(menu_number="sm",menu_text="Send Message") + \
        menu_space())

def messages_main_cli_command(choices_input): 
    print("cli command")

    if choices_input == "sm":
        from func.send_message import send_message
        send_message(input("Message: "),input("Please write receiver adress: "))



class message:
    def __init__(self,room_signature,message_signature,message):
        self.room_signature = room_signature
        self.message_signature = message_signature
        self.message = message

class message_rooms:
    def __init__(self,signature,sender,recipients,users):
        self.signature = signature
        self.sender = sender
        self.recipients = recipients
        self.messages = []

class messages_main:
    def __init__(self):
        self.rooms = []
        self.title = "Messages"


    def save_message_rooms(self):
        from config import get_config
        import os
        old_cwd = os.getcwd()
        os.chdir(get_config().main_folder)
        with open('apps/Messages/messages.decentra_network', 'wb') as message_rooms_file:
            pickle.dump(self, message_rooms_file,protocol=2)
        os.chdir(old_cwd)


def get_message_rooms():
    from config import get_config
    import os
    old_cwd = os.getcwd()
    os.chdir(get_config().main_folder)
    try:
     with open('apps/Messages/messages.decentra_network', 'rb') as message_rooms_file:
        return pickle.load(message_rooms_file)
    except:
        message_rooms_class = messages_main()
        message_rooms_class.save_message_rooms()
        return message_rooms_class
    os.chdir(old_cwd)




    