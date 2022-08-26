from tkinter import *
import socket
import threading as td

BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202B"
TEXT_COLOR = "#EAECEE"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"
flag = True

def listen_to_server(client: socket.socket, txt: Text):
    global flag
    while (flag):
        data = (client.recv(1024)).decode()
        if data == 'bye' or data == 'BYE' or data == 'Bye':
            txt.insert(END, "\n\n" + "Connection closed!")
            client.close()
            flag = False
            exit(0)
        else:
            txt.insert(END, "\n\n" + f"{server_name} -> " + data)


def listen_to_client():
    txt.insert(END, "\n\n" + f"Me -> {data.get()}")
    if data.get() == 'bye' or data.get() == 'BYE' or data.get() == 'Bye':
        client_socket.send("bye".encode())
        client_socket.close()
        global flag
        flag = False
        exit(0)
    client_socket.send((data.get()).encode())
    e.delete(0, END)


if __name__ == '__main__':
    # Socket Part
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    PORT = 5500
    IP = '127.0.0.1'
    name = input("Enter name : ")
    client_socket.connect((IP, PORT))  # Connects to server
    client_socket.send(name.encode())
    server_name = (client_socket.recv(1024)).decode()
    root = Tk()
    root.title(name)

    txt = Text(root, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT, width=60)
    txt.grid(row=1, column=0, columnspan=2)

    scrollbar = Scrollbar(txt)
    scrollbar.place(relheight=1, relx=0.974)
    data = StringVar()
    e = Entry(root, bg="#2C3E50", fg=TEXT_COLOR,
              font=FONT, width=55, textvariable=data)
    e.grid(row=2, column=0)

    send = Button(root, text="Send", font=FONT_BOLD, bg=BG_GRAY,
                  command=listen_to_client)

    send.grid(row=2, column=1)
    from_server_td = td.Thread(
        target=listen_to_server, args=(client_socket, txt))
    from_server_td.start()
    root.mainloop()
    # Threads
