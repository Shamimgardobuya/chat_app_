from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
import customtkinter as ctk


import base64 # Needed to encode the signature for sending
import port

import threading
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
from user import User
import re
import customtkinter as ctk
import json
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
from user import User
import re
import customtkinter as ctk
import json
import tkinter as tk
import new_client
import queue
import time
BUFSIZ = 1024
address = {}
class PortWindow:
    def __init__(self, root, queue):
        self.root = root
        self.address = address
        self.root.title("Enter Server credentials")
        self.root.geometry("700x550")
        self.qu = queue
        tk.Label(root, text="Enter host :").pack(pady=10)
        self.host_entry = tk.Entry(root)
        self.host_entry.pack()
        
        tk.Label(root, text="Enter port :").pack(pady=10)
        self.port_entry = tk.Entry(root)
        self.port_entry.pack()

        tk.Button(root, text="Submit", command=self.submit).pack(pady=10)

    def submit(self):
        host = self.host_entry.get().strip()
        port = self.port_entry.get().strip()
        if host:
            address["HOST"] = host
            address["PORT"] = port
            self.address = address
            print("add", address)
            # self.root.destroy()
                                
            ADDR = ( address["HOST"], int(address["PORT"]))
                                    
            client_socket = socket(AF_INET, SOCK_STREAM)

            client_socket.connect(ADDR)
            # ChatRoomApp(client_socket, self.qu)
            def start_chatroom():
                print("heree")
                chat_ui = ChatRoomApp(client_socket, self.qu)
                chat_ui.mainloop()
            print("<<<<<<<<<<<<<<<")
            self.root.after(100, start_chatroom)
            # self.root.destroy()
                
            # Thread(target=chatt.receive, args=(self.qu,), daemon=True).start()
            
    
            # task_queue.put(Thread(target=chatt.receive, daemon=True).start())
            # receive_thread = Thread(target=chatt.receive, daemon=True)
            # # # self.q.get()
            # # receive_thread.daemon = True
    
            
ctk.set_appearance_mode("System")  
ctk.set_default_color_theme("blue")  

class ChatRoomApp(ctk.CTk):
    def __init__(self, client_socket, que):
        super().__init__()
        print("reached chat room cass")
        self.title("Chat Room")
        self.geometry("700x500")
        self.client_socket = client_socket
        self.q = que
        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=150)
        self.sidebar.pack(side="left", fill="y", padx=10, pady=10)
        
        ctk.CTkLabel(self.sidebar, text="Contacts", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=10)
        self.contact_list = ctk.CTkTextbox(self.sidebar, width=120, height=300)
        self.contact_list.pack(pady=5)
        

                

        # Main chat area
        self.chat_frame = ctk.CTkFrame(self)
        self.chat_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.chat_display = ctk.CTkTextbox(self.chat_frame, wrap="word", state="disabled", height=300)
        self.chat_display.pack(fill="both", expand=True, pady=(0, 10))

        # Entry area
        self.entry_frame = ctk.CTkFrame(self.chat_frame)
        self.entry_frame.pack(fill="x")

        self.message_entry = ctk.CTkEntry(self.entry_frame, placeholder_text="Type your message...")
        self.message_entry.pack(side="left", fill="x", expand=True, padx=(0, 10), pady=5)
        self.message_entry.bind("<Return>", self.send)

        self.send_button = ctk.CTkButton(self.entry_frame, text="Send", command=self.send)
        self.send_button.pack(side="right", pady=5)
        
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    
        self.after(100, self.start_receiving)
    
        
    def on_closing(self):
        print("Closing chat room...")
        self.destroy()

    def send(self, event=None):
        message = self.message_entry.get().strip()
        # print("messageee", message)
        if message:
            self.chat_display.configure(state="normal")
            self.chat_display.insert("end", f"{message}\n")
            self.chat_display.yview("end")
            self.chat_display.configure(state="disabled")
            self.client_socket.send(bytes(message, "utf8"))
            if message == "{quit}":
                self.client_socket.close()
            list_names = message.split(":")
            self.contact_list.insert("end", f"{list_names[0]}\n")
            self.contact_list.configure(state="disabled")
            self.message_entry.delete(0, "end")
            
    def start_receiving(self):
        receiver_thread = Thread(target=self.receive,args=(self.q,), daemon=True)
        receiver_thread.start()

      
    def updateUi(self,msg):
        print("UI update running on:", threading.current_thread().name)

        if msg == "{quit}":
            self.client_socket.close()
            self.on_closing()
            return

        if self.chat_display.winfo_exists():
            self.chat_display.configure(state="normal")
            self.chat_display.insert("end", msg + "\n")
            self.chat_display.yview("end")
            self.chat_display.configure(state="disabled")

        if self.message_entry.winfo_exists():
            self.message_entry.delete(0, "end")
            
                    
    def receive(self, queue):
        while True:
            
            try:
                
                if queue.empty() :
                    
                    msg = self.client_socket.recv(BUFSIZ).decode("utf-8")
                    
                    queue.put(msg)
                    time.sleep(1)
                msg_q = queue.get()
                print("message from socket", msg_q)
                self.after(0, lambda: self.updateUi(msg_q))

                # self.updateUi(msg_q)
            
                
            except OSError :
                break

if __name__ == "__main__" :
        

    root = tkinter.Tk()
    task_queue = queue.Queue()

    PortWindow(root, task_queue)


    root.mainloop()


    


        




