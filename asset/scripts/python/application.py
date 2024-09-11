import tkinter as tk
from tkinter import colorchooser
from tkinter import ttk, scrolledtext, messagebox, Menu, Toplevel
import tkinter.font as tkfont
from datetime import datetime
from personal_ai import PersonalAI
from PIL import Image, ImageTk
import cv2
import subprocess
import sys
import os
import threading
import queue
import webbrowser

#Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 

ai = PersonalAI()

#Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 

class AppSettings:
    def __init__(self):
        self.theme = "dark"
        self.accent_color = "#00ff00"  # matrix green
        self.privacy_mode = False

#Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 

app_settings = AppSettings()
root = None
privacy_button = None
username_label = None
profile_frame = None
change_user_button = None

#Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 

class ChatHistory:
    def __init__(self):
        self.conversations = []
        self.load_conversations()

    def load_conversations(self):
        self.conversations = ai.get_chat_history()

    def add_conversation(self, user_message, ai_response):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.conversations.insert(0, (timestamp, user_message, ai_response))

    def get_conversation(self, index):
        if index < len(self.conversations):
            timestamp, user_message, ai_response = self.conversations[index]
            return f"[{timestamp}]\nYou: {user_message}\nAI: {ai_response}"
        return ""

#Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 

chat_history = ChatHistory()

#Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 

def main():
    global root, privacy_button, video_player, menu_buttons, main_content_frame, canvas, output_text, camera_running, detection_running, frame_queue
    root = tk.Tk()
    root.title("DegeAI Assistant")
    root.geometry("1000x700")
    #Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 

    main_frame = tk.Frame(root, bg='#000000')
    main_frame.place(x=0, y=0, relwidth=1, relheight=1)

    style = ttk.Style()
    style.theme_use("clam")
    configure_styles()
    
    create_menu(main_frame)
    #Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 

    privacy_button = ttk.Button(main_frame, text="🔓", command=toggle_privacy, style="Outline.TButton", width=6)
    privacy_button.place(relx=1.0, y=10, anchor="ne", x=-10)

    video_player.update_frame()

    show_home(main_content_frame)

    root.mainloop()
    ai.close()  

#Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 

def show_home(frame):
    clear_frame(frame)
    video_player.lift()
    highlight_current_page("🏠")

#Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 

def highlight_current_page(title):
    for button in menu_buttons:
        if (title == "🏠" and button.cget("text") == "🏠") or button.cget("text") == title:
            button.configure(style="ActiveIcon.TButton")
        else:
            button.configure(style="Icon.TButton")

#Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 

def configure_styles():
    style = ttk.Style()
    

    modern_font = ("Schön", 11)
    large_font = ("Schön", 13)
    
    style.configure("TFrame", background="#000000")
    style.configure("TLabel", background="#000000", foreground="white", font=modern_font)
    style.configure("TButton", background="#149414", foreground="white", font=modern_font, padding=10)
    style.map("TButton", background=[("active", "#149414")])
    style.configure("Outline.TButton", background="#149414", foreground="black", borderwidth=2, font=modern_font)
    style.map("Outline.TButton", background=[("active", "#149414")])
    style.configure("TNotebook", background="#000000")
    style.configure("TNotebook.Tab", background="#149414", foreground="black", padding=[20, 10], font=modern_font)
    style.map("TNotebook.Tab", background=[("selected", "#149414")])
    #Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 


    style.configure("TEntry", font=modern_font, fieldbackground="black", foreground="white")
    style.configure("TCombobox", font=modern_font, fieldbackground="black", foreground="white")
    style.configure("TCheckbutton", font=modern_font, background="black", foreground="white")
    style.configure("Treeview", font=modern_font, background="black", foreground="white", fieldbackground="black")
    style.configure("Treeview.Heading", font=large_font, background="black", foreground="white")
    #Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 


    style.configure("Chat.TEntry", fieldbackground="black", foreground="white", insertcolor="white")
    style.configure("Chat.TButton", background="#149414", foreground="white")
    style.map("Chat.TButton", background=[("active", "#1abc1a")])
    style.configure("Icon.TButton", background="black", foreground="white", font=modern_font, padding=10)
    style.map("Icon.TButton", background=[("active", "#149414")])
    style.configure("ActiveIcon.TButton", background="white", foreground="black", font=modern_font, padding=10)
    style.configure("Title.TLabel", background="black", foreground="white", font=("Schön", 16, "bold"))
    style.configure("Home.TButton", background="#149414", foreground="white", font=("Schön", 14, "bold"), padding=5, width=3)
    style.map("Home.TButton", background=[("active", "#1abc1a")])
    #Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 


    style.configure("TMenu", background="black", foreground="white", activebackground="#149414", activeforeground="white")
    

    style.configure("Black.TLabel", background="black", foreground="white")
    style.configure("TEntry", fieldbackground="black", foreground="white")
    style.configure("TButton", background="#149414", foreground="white")

#Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 

class VideoPlayer(tk.Label):
    def __init__(self, parent, video_path, width, height):
        super().__init__(parent)
        self.video_path = video_path
        self.video = cv2.VideoCapture(self.video_path)
        self.width = width
        self.height = height
        self.update_frame()

    def update_frame(self):
        ret, frame = self.video.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (self.width, self.height))
            image = Image.fromarray(frame)
            photo = ImageTk.PhotoImage(image=image)
            self.config(image=photo)
            self.image = photo
        else:
            self.video.set(cv2.CAP_PROP_POS_FRAMES, 0)
        self.after(33, self.update_frame) 

#Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 

def create_menu(parent):
    global main_content_frame, video_player, menu_buttons
    
#Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 

    container_frame = ttk.Frame(parent, style="TFrame")
    container_frame.place(x=0, y=0, relwidth=1, relheight=1)

#Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 

    video_path = r"C:\Users\degeb\OneDrive\Masaüstü\AI PROJECT IMPORTANT\IMG\degeaiend.mp4"
    video_player = VideoPlayer(container_frame, video_path, 1390, 1060)
    video_player.place(relx=0, rely=0, relwidth=0.7, relheight=1)


    black_frame = ttk.Frame(container_frame, style="Black.TFrame")
    black_frame.place(relx=0.7, rely=0, relwidth=0.3, relheight=1)
#Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 


    home_button = ttk.Button(black_frame, text="🏠", command=lambda: show_home(main_content_frame), style="Home.TButton")
    home_button.place(relx=0.01, rely=0.01)
#Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 


    icon_frame = ttk.Frame(black_frame, style="Black.TFrame")
    icon_frame.place(relx=0.5, rely=0.5, anchor="center")

#Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 

    main_content_frame = ttk.Frame(container_frame, style="TFrame")
    main_content_frame.place(relx=0, rely=0, relwidth=0.7, relheight=1)


    menu_items = [
        ("art.png", "DEGEAI Visual Detection", lambda: open_interface(main_content_frame, create_coding_interface, "DEGEAI Visual Detection")),
        ("face.png", "DEGEAI Chat", lambda: open_interface(main_content_frame, create_chat_interface, "DEGEAI Chat")),
        ("settings.png", "Settings", lambda: open_interface(main_content_frame, create_settings, "Settings")),
        ("programmer.png", "Help/Dev", lambda: open_interface(main_content_frame, create_help_content, "Help/Dev")),
    ]
#Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 

    menu_buttons = []  
#Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 


    for icon_file, label_text, command in menu_items:
        icon_path = r"C:\Users\degeb\OneDrive\Masaüstü\AI PROJECT IMPORTANT\IMG\\" + icon_file
        try:
            icon_image = Image.open(icon_path)
            icon_image = icon_image.resize((40, 40))
            icon_photo = ImageTk.PhotoImage(icon_image)

            item_frame = ttk.Frame(icon_frame, style="Black.TFrame")
            item_frame.pack(pady=10, fill="x")

            icon_button = ttk.Button(item_frame, image=icon_photo, text=label_text, compound="left", command=command, style="Icon.TButton")
            icon_button.image = icon_photo
            icon_button.pack(side="left", padx=(0, 10), fill="x", expand=True)
            menu_buttons.append(icon_button)

        except FileNotFoundError:
            print(f"Warning: Icon file not found: {icon_path}")
            text_button = ttk.Button(icon_frame, text=label_text, command=command, style="Icon.TButton")
            text_button.pack(pady=10, fill="x", expand=True)
            menu_buttons.append(text_button)

    profile_frame = tk.Frame(black_frame, bg="#149414", cursor="hand2")
    profile_frame.place(relx=0.5, rely=0.95, anchor="s", relwidth=0.7)


    profile_icon_path = r"C:\Users\degeb\OneDrive\Masaüstü\AI PROJECT IMPORTANT\IMG\Degepp.jpg"
    try:
        profile_image = Image.open(profile_icon_path)
        profile_image = profile_image.resize((30, 30))
        profile_photo = ImageTk.PhotoImage(profile_image)
        profile_label = tk.Label(profile_frame, image=profile_photo, bg="#149414")
        profile_label.image = profile_photo
        profile_label.pack(side="left", padx=5, pady=5)
    except FileNotFoundError:
        print(f"Warning: Profile icon not found: {profile_icon_path}")


    username_label = tk.Label(profile_frame, text="Dege34", bg="#149414", fg="white", font=("Schön", 12))
    username_label.pack(side="left", padx=(0, 10), pady=5)

#Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

#Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 

def show_home(frame):
    clear_frame(frame)
    video_player.lift()
    highlight_current_page(None)

#Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 

def open_interface(frame, create_func, title):
    clear_frame(frame)
    create_func(frame)
    highlight_current_page(title)
    frame.lift()

#Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 

def highlight_current_page(title):
    for button in menu_buttons:
        if button.cget("text") == title:
            button.configure(style="ActiveIcon.TButton")
        else:
            button.configure(style="Icon.TButton")

#Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 

def create_coding_interface(parent):
    frame = ttk.Frame(parent)
    frame.pack(expand=True, fill="both", padx=20, pady=20)

    title = ttk.Label(frame, text="DEGEAI Visual Detection", style="Title.TLabel")
    title.pack(pady=(0, 10))


    button_container = ttk.Frame(frame)
    button_container.pack(expand=True, fill="both")

    button_container.columnconfigure(0, weight=1)
    button_container.rowconfigure(0, weight=1)

    detect_button = ttk.Button(button_container, text="Start Face Detection", command=start_face_detection)
    detect_button.grid(row=0, column=0)

    detect_button.configure(width=20)  

#Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 

def start_face_detection():
    file_path = r"C:\Users\degeb\OneDrive\Masaüstü\AI PROJECT IMPORTANT\degeface_tracking.py"
    try:
        threading.Thread(target=lambda: subprocess.run([sys.executable, file_path], check=True), daemon=True).start()
    except Exception as e:
        print(f"Error starting face detection: {str(e)}")

#Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 

def create_chat_interface(parent):

    parent.grid_columnconfigure(0, weight=1)
    parent.grid_rowconfigure(0, weight=3)
    parent.grid_rowconfigure(1, weight=1)
    parent.grid_rowconfigure(2, weight=0)

    chat_display = scrolledtext.ScrolledText(parent, wrap=tk.WORD, font=("Schön", 12))
    chat_display.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    chat_display.config(state=tk.DISABLED, bg="black", fg="white", insertbackground="white")


    chat_display.tag_configure("sender", foreground="#149414", font=("Schön", 14, "bold"))
    chat_display.tag_configure("message", foreground="white")
    chat_display.tag_configure("timestamp", foreground="#F98866")


    history_frame = ttk.Frame(parent)
    history_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
    history_frame.grid_columnconfigure(0, weight=1)
    history_frame.grid_rowconfigure(0, weight=1)

    history_listbox = tk.Listbox(history_frame, bg="black", fg="white", selectbackground="#149414", selectforeground="white")
    history_listbox.grid(row=0, column=0, sticky="nsew")
    history_listbox.bind('<<ListboxSelect>>', lambda e: show_selected_conversation(chat_display, history_listbox))

    input_frame = ttk.Frame(parent)
    input_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
    input_frame.grid_columnconfigure(0, weight=1)

    input_field = ttk.Entry(input_frame, style="Chat.TEntry")
    input_field.grid(row=0, column=0, padx=(0, 10), sticky="ew")

    send_button = ttk.Button(input_frame, text="Send", command=lambda: send_message(input_field, chat_display, history_listbox), style="Chat.TButton")
    send_button.grid(row=0, column=1)


    input_field.bind("<Return>", lambda event: send_message(input_field, chat_display, history_listbox))

    update_history_listbox(history_listbox)

def send_message(input_field, chat_display, history_listbox):
    message = input_field.get()
    if message:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        chat_display.config(state=tk.NORMAL)
        #Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 

   
        ai_response = ai.chat(message)
        
 
        chat_display.insert(tk.END, f"[{timestamp}] ", "timestamp")
        chat_display.insert(tk.END, "You: ", "sender")
        chat_display.insert(tk.END, f"{message}\n", "message")
        
        #Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 

        chat_display.insert(tk.END, f"\n[{timestamp}] ", "timestamp")
        chat_display.insert(tk.END, "AI: ", "sender")
        chat_display.insert(tk.END, f"{ai_response}\n\n", "message")

        chat_display.see(tk.END)
        chat_display.config(state=tk.DISABLED)
        input_field.delete(0, tk.END)

        chat_history.add_conversation(message, ai_response)
        update_history_listbox(history_listbox)
#Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 

def show_selected_conversation(chat_display, history_listbox):
    selection = history_listbox.curselection()
    if selection:
        index = selection[0]
        chat_display.config(state=tk.NORMAL)
        chat_display.delete("1.0", tk.END)
        #Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 

        timestamp, user_message, ai_response = chat_history.conversations[index]

        chat_display.insert(tk.END, f"[{timestamp}] ", "timestamp")
        chat_display.insert(tk.END, "You: ", "sender")
        chat_display.insert(tk.END, f"{user_message}\n", "message")
        #Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 

        chat_display.insert(tk.END, f"[{timestamp}] ", "timestamp")
        chat_display.insert(tk.END, "AI: ", "sender")
        chat_display.insert(tk.END, f"{ai_response}\n\n", "message")
        #Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 

        chat_display.config(state=tk.DISABLED)
        chat_display.see(tk.END)

def update_history_listbox(history_listbox):
    history_listbox.delete(0, tk.END)
    for conversation in chat_history.conversations:
        history_listbox.insert(tk.END, conversation[0])
#Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 

def create_settings(parent):
    #Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 
    parent.grid_columnconfigure(1, weight=1)
    #Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 
    ttk.Label(parent, text="Theme:").grid(row=0, column=0, sticky="w", pady=10, padx=10)#Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 
    theme_var = tk.StringVar(value=app_settings.theme)#Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 
    theme_combo = ttk.Combobox(parent, textvariable=theme_var, values=["light", "dark"], state="readonly")
    theme_combo.grid(row=0, column=1, sticky="ew", pady=10, padx=10)
    theme_combo.bind("<<ComboboxSelected>>", lambda e: update_theme(theme_var.get()))

    ttk.Label(parent, text="Accent Color:").grid(row=1, column=0, sticky="w", pady=10, padx=10)
    color_button = ttk.Button(parent, text="Choose Color", command=choose_accent_color, style="Outline.TButton")
    color_button.grid(row=1, column=1, sticky="ew", pady=10, padx=10)

    privacy_var = tk.BooleanVar(value=app_settings.privacy_mode)
    privacy_check = ttk.Checkbutton(parent, text="Privacy Mode", variable=privacy_var, command=toggle_privacy)
    privacy_check.grid(row=2, column=0, columnspan=2, sticky="w", pady=10, padx=10)
#Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 

def update_theme(theme):
    app_settings.theme = theme
    print(f"Theme changed to: {theme}")
#Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 

def choose_accent_color():
    color = colorchooser.askcolor(title="Choose Accent Color")[1]
    if color:
        app_settings.accent_color = color

        print(f"Accent color changed to: {color}")
#Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 

def toggle_privacy():
    app_settings.privacy_mode = not app_settings.privacy_mode
    privacy_button.configure(text="🔒" if app_settings.privacy_mode else "🔓")
    # Implement additional privacy mode logic here
    print(f"Privacy mode: {'On' if app_settings.privacy_mode else 'Off'}")
#Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 

def create_help_content(parent):
    help_text = """
    DegeAI Assistant

    Version: 1.0

    Developer: Dogan Ege BULTE

    Contact with Developer:
     
                            -> www.thedege.com

                            -> dege.bulte@studenti.polito.it

                            -> www.github.com/Dege34

                            -> www.linkedin.com/in/degebulte

                            
    License:

    This software is released under the MIT License.

    Copyright (c) 2024 Dogan Ege BULTE

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"),
    to deal in the Software without restriction, including without limitation 
    the rights to use, copy, modify, merge, publish, distribute, sublicense,
    and/or sell copies of the Software, and to permit persons to whom the Software 
    is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in 
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN 
    THE SOFTWARE.
    """

    help_display = scrolledtext.ScrolledText(parent, wrap=tk.WORD, font=("Schön", 11))
    help_display.pack(expand=True, fill="both", padx=10, pady=10)
    help_display.insert(tk.END, help_text)
    help_display.config(state=tk.DISABLED, bg="black", fg="white")

    links = [
        ("www.thedege.com", "https://www.thedege.com"),
        ("dege.bulte@studenti.polito.it", "mailto:dege.bulte@studenti.polito.it"),
        ("www.github.com/Dege34", "https://www.github.com/Dege34"),
        ("www.linkedin.com/in/degebulte", "https://www.linkedin.com/in/degebulte")
    ]

    for text, url in links:
        start = help_display.search(text, "1.0", tk.END)
        if start:
            end = f"{start}+{len(text)}c"
            help_display.tag_add(f"link_{url}", start, end)
            help_display.tag_config(f"link_{url}", foreground="red", underline=True)
            help_display.tag_bind(f"link_{url}", "<Button-1>", lambda e, url=url: webbrowser.open(url))
            help_display.tag_bind(f"link_{url}", "<Enter>", lambda e: e.widget.config(cursor="hand2"))
            help_display.tag_bind(f"link_{url}", "<Leave>", lambda e: e.widget.config(cursor=""))
            
#Coded and Designed by Dege, Copyright (c) 2024 Dogan Ege BULTE 

if __name__ == "__main__":
    main()