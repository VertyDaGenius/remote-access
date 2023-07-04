import socket
import tkinter as tk
import threading
import time

SERVER_IP = '127.0.0.1'
SERVER_PORT = 8081

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client_socket.connect((SERVER_IP, SERVER_PORT))
except ConnectionRefusedError:
    print("Error: Connection refused. Please check the server IP and port. Or make sure the server is also running the script..")
    time.sleep(3)
    exit()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))

window = tk.Tk()
window.title("SSH Client")

logs_label = tk.Label(window, text="Logs:")
logs_label.pack()

output_text = tk.Text(window, height=20, width=100)
output_text.pack()

command_entry = tk.Entry(window, width=50)

placeholder_text = "Enter a command to send to the server"
command_entry.insert(0, placeholder_text)


def on_entry_click(event):
    if command_entry.get() == placeholder_text:
        command_entry.delete(0, tk.END)


command_entry.bind("<Button-1>", on_entry_click)

command_entry.pack()


def send_command():
    command = command_entry.get()
    if command.lower() == 'exit':
        client_socket.send(command.encode())
        client_socket.close()
        window.destroy()
        return

    client_socket.send(command.encode())

    while True:
        output = client_socket.recv(4096).decode()

        output_text.insert(tk.END, output + '\n')
        window.update()

        if not output:
            break

    command_entry.delete(0, tk.END)
    command_entry.insert(0, placeholder_text)


def start_command():
    threading.Thread(target=send_command).start()


start_button = tk.Button(window, text="Start", command=start_command)
start_button.pack()

window.mainloop()
