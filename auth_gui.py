import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from customtkinter import CTkImage
from itertools import cycle
import smtplib
from email.mime.text import MIMEText
import random
import threading
from db_queries import DatabaseManager
from dashboard_main import PayPerksDashboard

class PayPerksAuth:
    def __init__(self):
        threading.Thread(target=self.db_init,daemon=True).start()
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Window setup
        self.window = ctk.CTk(fg_color="white")
        self.window.title('PayPerks Auth')
        self.window.geometry('925x500')
        self.window.resizable(False, False)

        self.bg_index = [0]
        self.bg_images = ['img/bg.png', 'img/bg3.png','img/bg4.png']
        self.is_animating = [False]
        self.words = cycle([
            "Secure. Simple. Smart Wallet.",
            "Your money, your control.",
            "Fast, safe & easy transactions."
        ])

        self.current_user_email = None
        self.setup_ui()
        self.window.after(5000, self.swap_bg_and_animate)
    
    def run(self):
        self.window.mainloop()

    def db_init(self):
        self.db = DatabaseManager()

    def raise_frame(self, frame):
        frame.tkraise()

    def setup_ui(self):
        # Image and Label
        img = Image.open('img/PAYPERKS2.png').resize((200, 200))
        self.payperks_img = CTkImage(light_image=img, size=(200, 200))
        ctk.CTkLabel(self.window, image=self.payperks_img, text="", bg_color='white').place(x=500, y=-40)

        self.bg_label = ctk.CTkLabel(self.window, text="", bg_color='white')
        self.bg_label.place(x=20, y=50)
        self.load_bg(self.bg_index[0])

        self.typing_label = ctk.CTkLabel(self.window, text='', text_color='black', font=ctk.CTkFont("Segoe UI", 16, "bold"))
        self.typing_label.place(x=90, y=390)
        self.text_to_type = "Welcome to PayPerks!"
        self.type_text()

        # Sign Up and Sign In Frames
        self.signup_frame = ctk.CTkFrame(self.window, width=450, height=360, fg_color='white')
        self.signin_frame = ctk.CTkFrame(self.window, width=450, height=360, fg_color='white')
        for frame in (self.signup_frame, self.signin_frame):
            frame.place(x=400, y=110)

        self.build_signup_form()
        self.build_signin_form()
        self.raise_frame(self.signup_frame)

    def load_bg(self, index):
        bg_img = Image.open(self.bg_images[index]).resize((350, 350))
        ctk_img = CTkImage(light_image=bg_img, size=(350, 350))
        self.bg_label.configure(image=ctk_img)
        self.bg_label.image = ctk_img

    def type_text(self, index=0):
        if index < len(self.text_to_type):
            self.typing_label.configure(text=self.typing_label.cget("text") + self.text_to_type[index])
            self.window.after(100, self.type_text, index + 1)

    def erase_text(self):
        self.is_animating[0] = True
        current = self.typing_label.cget("text")
        if current:
            self.typing_label.configure(text=current[:-1])
            self.window.after(50, self.erase_text)
        else:
            self.show_next_word()

    def show_next_word(self):
        word = next(self.words)
        self.typing_label.configure(text="")
        self.type_word(word)

    def type_word(self, word, index=0):
        if index < len(word):
            self.typing_label.configure(text=self.typing_label.cget("text") + word[index])
            self.window.after(150, self.type_word, word, index + 1)
        else:
            self.window.after(1200, self.erase_text)

    def slide_bg_out(self, x=10):
        if x > -400:
            self.bg_label.place(x=x, y=50)
            self.window.after(5, self.slide_bg_out, x - 10)
        else:
            self.swap_bg_image()

    def slide_bg_in(self, x=-400):
        if x < 10:
            self.bg_label.place(x=x, y=50)
            self.window.after(5, self.slide_bg_in, x + 10)
        else:
            self.window.after(100, lambda: self.is_animating.__setitem__(0, False))

    def swap_bg_image(self):
        self.bg_index[0] = (self.bg_index[0] + 1) % len(self.bg_images)
        self.load_bg(self.bg_index[0])
        self.slide_bg_in()
        self.erase_text()

    def swap_bg_and_animate(self):
        if not self.is_animating[0]:
            self.slide_bg_out()
            self.is_animating[0] = True
        self.window.after(5000, self.swap_bg_and_animate)
        

    def build_signup_form(self):
        ctk.CTkLabel(self.signup_frame, text='Sign Up', text_color='#57a1f8', font=ctk.CTkFont(size=23, weight="bold")).place(x=25, y=10)

        self.name = ctk.CTkEntry(self.signup_frame, width=300, placeholder_text="Full Name")
        self.name.place(x=30, y=50)

        self.email = ctk.CTkEntry(self.signup_frame, width=300, placeholder_text="Email")
        self.email.place(x=30, y=100)

        self.code = ctk.CTkEntry(self.signup_frame, width=300, placeholder_text="Password", show="*")
        self.code.place(x=30, y=150)

        self.confirm_code = ctk.CTkEntry(self.signup_frame, width=300, placeholder_text="Confirm Password", show="*")
        self.confirm_code.place(x=30, y=200)

        signup_btn = ctk.CTkButton(self.signup_frame, text="Sign Up", width=300, fg_color="#57a1f8", hover_color="#0052cc", command=self.signup)
        signup_btn.place(x=30, y=250)

        ctk.CTkLabel(self.signup_frame, text="I have an account?", text_color="black", font=ctk.CTkFont(size=11)).place(x=30, y=280)
        ctk.CTkButton(self.signup_frame, width=50, text="Sign In", fg_color="transparent", text_color="#57a1f8", hover=False, command=lambda: self.raise_frame(self.signin_frame)).place(x=130, y=280)

    def build_signin_form(self):
        ctk.CTkLabel(self.signin_frame, text='Sign In', text_color='#57a1f8', font=ctk.CTkFont(size=23, weight="bold")).place(x=25, y=10)

        self.email_signin = ctk.CTkEntry(self.signin_frame, width=300, placeholder_text="Email")
        self.email_signin.place(x=30, y=60)

        self.code_signin = ctk.CTkEntry(self.signin_frame, width=300, placeholder_text="Password", show="*")
        self.code_signin.place(x=30, y=120)

        self.signin_btn = ctk.CTkButton(self.signin_frame, text="Sign In", width=300, fg_color="#57a1f8", hover_color="#0052cc", command=self.signin)
        self.signin_btn.place(x=30, y=180)

        ctk.CTkLabel(self.signin_frame, text="Don't have an account?", text_color="black", font=ctk.CTkFont(size=11)).place(x=30, y=230)
        ctk.CTkButton(self.signin_frame, width=50, text="Sign Up", fg_color="transparent", text_color="#57a1f8", hover=False, command=lambda: self.raise_frame(self.signup_frame)).place(x=148, y=230)

    def signup(self):
        full_name = self.name.get()
        email = self.email.get()
        password = self.code.get()
        confirm_password = self.confirm_code.get()
        
        # Clear fields
        self.name.delete(0,'end')
        self.email.delete(0,'end')
        self.code.delete(0,'end')
        self.confirm_code.delete(0,'end')

        if email == '' or password == '' or confirm_password == '':
            messagebox.showerror("Error", "All fields are required")
        elif password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match")
        else:
            threading.Thread(target=self.check_email_threaded, args=(email,), daemon=True).start()
            self.popup = ctk.CTkToplevel(self.window)
            self.popup.title("Email Verification")
            self.popup.geometry("400x300")
            self.popup.resizable(False, False)
            self.popup.lift()
            self.popup.focus_force()
            self.popup.grab_set()
            
            ctk.CTkLabel(self.popup, text="Enter Verification Code:", font=ctk.CTkFont(size=20,weight='bold'),text_color='#57a1f8').pack(pady=(30,20))
            ctk.CTkLabel(self.popup, text="A verification code has been sent to your email.", font=ctk.CTkFont(size=12)).pack(pady=0)
            self.verify_code_entry = ctk.CTkEntry(self.popup, width=200, placeholder_text="Enter Verification Code")
            self.verify_code_entry.pack(pady=(0,20))
            
            code = str(random.randint(100000, 999999))
            print(code)
            threading.Thread(target=lambda: self.send_email(email, code), daemon=True).start()
            ctk.CTkButton(self.popup, text="OK", command=lambda: self.verify_code(code,full_name,email,password)).pack(pady=10)

    def send_email(self, recipient, code):
        sender_email = "payperks@zohomail.com"
        password = "freefire00"
        msg = MIMEText("Your verification code is: " + str(code))
        msg['Subject'] = 'PayPerks Verification Code'
        msg['From'] = sender_email
        msg['To'] = recipient
        
        for attempt in range(2):
            try:
                server = smtplib.SMTP_SSL('smtp.zoho.com', 465)
                server.login(sender_email, password)
                server.send_message(msg)
                server.quit()
                break
            except Exception as e:
                print("Email send failed:", e)

    def verify_code(self, code, full_name, email, password):
        entered_code = self.verify_code_entry.get()
        if code == entered_code:
            messagebox.showinfo("Success", "Successfully Registered!")
            self.popup.destroy()
            db = DatabaseManager() 
            db.register_user(full_name, email, password)
            db.close()
        else:
            messagebox.showerror("Error", "Invalid verification code. Please try again.")
        self.popup.destroy()

    def check_email_threaded(self, email):
        db = DatabaseManager()
        if db.email_exists(email):
            self.window.after(0, lambda: (self.popup.destroy()))
            messagebox.showerror('Error', 'Email is already registered!')   

    def signin(self):
        email = self.email_signin.get()
        password = self.code_signin.get()

        if email == '' or password == '':
            messagebox.showerror("Error", "All fields are required")
            return
        self.current_user_email = email

        def handle_result():
          #  self.signin_btn.configure(state="normal")
            if self.db.authenticate_user(email,password):
                self.email_signin.delete(0,'end')
                self.code_signin.delete(0,'end')
                self.open_dashboard()
            else:
                messagebox.showerror("Error", "Invalid email or password")
            self.email_signin.delete(0, 'end')
            self.code_signin.delete(0, 'end')

        self.window.after(0, handle_result)

    def open_dashboard(self):
        """Open the dashboard and close the auth window"""
        self.window.destroy()
        dashboard = PayPerksDashboard(self.current_user_email,self.db)
        dashboard.run()
        