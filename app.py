import requests
import tkinter as tk
from tkinter import ttk

server_ip = '127.0.0.1'
server_port = 5000

username = 'guest'

def request_directory_tree(ip, port):
    url = f"http://{server_ip}:{server_port}/directory"
    r = requests.get(url, params={"username": username})
    r.raise_for_status()
    return r.json()

def populate_tree(tree, parent, data):
    for name, content in data.items():
        if isinstance(content, dict):
            node = tree.insert(parent, "end", text=name, open=False)
            populate_tree(tree, node, content)
        else:
            tree.insert(parent, "end", text=name)

def build_gui(directory_tree):
    root = tk.Tk()
    root.title(username + ": server environment")

    main = tk.PanedWindow(root, orient=tk.HORIZONTAL)
    main.pack(fill=tk.BOTH, expand=True)

    frame_left = tk.Frame(main)
    tree = ttk.Treeview(frame_left)
    tree.pack(fill=tk.BOTH, expand=True)
    main.add(frame_left, width=300)

    populate_tree(tree, username, directory_tree)

    frame_right = tk.Frame(main, bg="#CFCFCF")
    main.add(frame_right)

    root.mainloop()

def authorize():
    username = 'guest'

if __name__ == '__main__':
    try:
        directory_tree = request_directory_tree(server_ip, server_port)
        build_gui(directory_tree) 
    except Exception:
        data = { "connection error": None }
        populate_tree(directory_tree, username, data)
        build_gui(directory_tree)
     