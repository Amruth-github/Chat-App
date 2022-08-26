import socket
from tkinter import *
import threading as td

BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202B"
TEXT_COLOR = "#EAECEE"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"
flag = True
def listen_to_client(client: socket.socket, txt: Text, name: str):
    global flag
    while (flag):
        data = (client.recv(1024)).decode()
        if data == 'bye' or data == 'BYE' or data == 'Bye':
            txt.insert(END, "\n\n" + "Connection closed!")
            client.close()
            flag = False
            exit(0)
        else:
            txt.insert(END, "\n\n" + f"{name} -> {data}")


def send_msg(client: socket.socket, data: StringVar, txt: Text, e: Entry):
    txt.insert(END, "\n\n" + "Me -> " + data.get())
    client.send((data.get()).encode())
    e.delete(0, END)


def start_conv(client: socket.socket, name: str, my_name: str):
    root = Tk()
    root.title(my_name)
    data = StringVar()
    txt = Text(root, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, width=60)
    txt.grid(row=1, column=0, columnspan=2)
    scrollbar = Scrollbar(txt)
    scrollbar.place(relheight=1, relx=0.974)

    e = Entry(root, bg="#2C3E50", fg=TEXT_COLOR,
              font=FONT, width=55, textvariable=data)
    e.grid(row=2, column=0)

    Button(root, text="Send", font=FONT_BOLD, bg=BG_GRAY,
           command=lambda: send_msg(client, data, txt, e)).grid(row=2, column=1)

    from_client_t = td.Thread(target=listen_to_client,
                              args=(client, txt, name))

    from_client_t.start()
    root.mainloop()
    from_client_t.join()



def listen_to_req():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    IP = '127.0.0.1'
    PORT = 5500
    s.bind((IP, PORT))
    s.listen()
    while (flag):
        client_socket, client_addr = s.accept()
        my_name = "Server"
        name = (client_socket.recv(1024)).decode()
        client_socket.send(my_name.encode())
        session_t = td.Thread(target=start_conv, args=(
            client_socket, name, my_name))

        session_t.start()


root: Tk

if __name__ == '__main__':
    listen_t = td.Thread(target=listen_to_req, args=())
    listen_t.start()
    listen_t.join()
