import requests
import tkinter as tk
from tkinter import ttk

server_ip = '127.0.0.1'
server_port = 8080

username = 'admin'
password = '4dm1n5'

token = ''

def request_directory_tree(ip, port):
    global r
    try:
        url = f"http://{server_ip}:{server_port}/directory"
        r = requests.get(url, params={"token": token})
        r.raise_for_status()
        return dict(r.json()) + {"errors": f"{r.status_code}"}
    except:
        return {}

def authorize():    
    global token
    global r
    url = f"http://{server_ip}:{server_port}/authorize"
    r = requests.get(url, params={"username": username, "password": password})
    r.raise_for_status()
    token = r.json()["username"]

def logout():
    try:
        url = f"http://{server_ip}:{server_port}/logout"
        r = requests.delete(url, params={"token": token})
        r.raise_for_status()
    except:
        print("error occured")
        

def populate_tree(tree: ttk.Treeview, parent: str, data: dict):
    if len(data.items()) < 1:
        tree.insert(parent, "end", text="directory is empty")
        return

    for name, content in data.items():
        if isinstance(content, dict):
            node = tree.insert(parent, "end", text=name, open=False)
            populate_tree(tree, node, dict(content))
        else:
            tree.insert(parent, "end", text=name)

def build_gui(directory_tree):
    root = tk.Tk()
    root.title(username + ": server environment")

    def on_closing():
        logout()
        root.destroy()   

    root.protocol("WM_DELETE_WINDOW", on_closing)

    main = tk.PanedWindow(root, orient=tk.HORIZONTAL)
    main.pack(fill=tk.BOTH, expand=True)

    frame_left = tk.Frame(main)
    tree = ttk.Treeview(frame_left)
    tree.pack(fill=tk.BOTH, expand=True)
    main.add(frame_left, width=300)

    populate_tree(tree, "", directory_tree)

    frame_right = tk.Frame(main, bg="#CFCFCF")
    main.add(frame_right, width=300, height=600)

    root.mainloop()

def authorization_window():

    auth_window = tk.Tk()
    auth_window.title("Authorize")

    auth_main = tk.PanedWindow(auth_window, orient=tk.HORIZONTAL)
    auth_main.pack(fill=tk.ALL, expand=True)

def installation_window():
    install_window = tk.Tk()
    install_window.title("Install")

    install_main = tk.PanedWindow(install_window, orient=tk.HORIZONTAL)
    install_main.pack(fill=tk.ALL, expand=True)

if __name__ == '__main__':
    try:
        authorize()
        directory_tree = { username: request_directory_tree(server_ip, server_port) }
        build_gui(directory_tree) 
    except Exception as e:
        data = { "connection error": {f"{repr(e)}" : { f"{str(r.content)}": None }} }
        build_gui(data)