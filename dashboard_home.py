import customtkinter as ctk
try:
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("Matplotlib not available. Chart will show placeholder.")
from PIL import Image
import random

class DashboardHome:
    def __init__(self, parent_window, user_email,user_data,db):
        self.parent_window = parent_window
        self.user_email = user_email
        self.user_data = user_data
        self.db = db

    def load_user_data(self):
        """Load user data from database"""
        self.user_data = self.db.get_user_by_email(self.user_email)

    def refresh_data(self):
        """Refresh user data and update UI"""
        self.load_user_data()
        if hasattr(self, 'dashboard_frame'):
            self.update_dashboard_values()

    def create_dashboard_frame(self):
        """Create and return the dashboard frame"""
        self.dashboard_frame = ctk.CTkFrame(self.parent_window, fg_color='white', width=725, height=500)
        
        # Welcome label
        welcome_text = f"Welcome! {self.user_data[0] if self.user_data else 'User'}"
        self.welcome_label = ctk.CTkLabel(
            self.dashboard_frame, 
            text=welcome_text, 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.welcome_label.place(x=80, y=65)
        
        # User Icon
        user_img = ['img/user_icon/user1.png', 'img/user_icon/user2.png', 
                   'img/user_icon/user3.png', 'img/user_icon/user4.png', 'img/user_icon/user5.png']
        random_user_img = random.choice(user_img)
        user_icon = ctk.CTkImage(light_image=Image.open(random_user_img), size=(50, 50))
        user_icon_label = ctk.CTkLabel(self.dashboard_frame, image=user_icon, text="")
        user_icon_label.place(x=20, y=50)
        
        # PayPerks Logo
        logo_img = ctk.CTkImage(light_image=Image.open('img/PAYPERKS2.png'), size=(250, 250))
        logo_label = ctk.CTkLabel(self.dashboard_frame, image=logo_img, text="")
        logo_label.place(x=400, y=-50)

        self.create_info_cards()
        self.create_activity_chart()
        
        return self.dashboard_frame

    def create_info_cards(self):
        """Create balance, income, expense, and reward cards"""
        # Balance Card
        balance_card = ctk.CTkFrame(
            self.dashboard_frame, width=300, height=80, fg_color='white', 
            border_color='#e0e1e2', border_width=2, corner_radius=10
        )
        balance_card.place(x=360, y=150)
        
        ctk.CTkLabel(
            balance_card, text="Available Balance", font=ctk.CTkFont(size=15, weight="bold"), 
            text_color='#1375d0', bg_color='transparent'
        ).place(x=20, y=5)
        
        balance_amount = f"${self.user_data[1]:.2f}" if self.user_data else "$0.00"
        self.balance_label = ctk.CTkLabel(
            balance_card, text=balance_amount, font=ctk.CTkFont(size=28, weight="bold"), 
            text_color='#222', bg_color='transparent'
        )
        self.balance_label.place(x=20, y=30)

        # Income Card
        income_card = ctk.CTkFrame(
            self.dashboard_frame, width=300, height=80, fg_color='white', 
            border_color='#e0e1e2', border_width=2, corner_radius=10
        )
        income_card.place(x=360, y=250)
        
        ctk.CTkLabel(
            income_card, text="Credit", font=ctk.CTkFont(size=15, weight="bold"), 
            text_color='#1375d0', bg_color='transparent'
        ).place(x=20, y=5)
        
        income_amount = f"${self.user_data[3]:.2f}" if self.user_data else "$0.00"
        self.income_label = ctk.CTkLabel(
            income_card, text=income_amount, font=ctk.CTkFont(size=28, weight="bold"), 
            text_color='#222', bg_color='transparent'
        )
        self.income_label.place(x=20, y=30)

        # Expense Card
        expense_card = ctk.CTkFrame(
            self.dashboard_frame, width=300, height=80, fg_color='white', 
            border_color='#e0e1e2', border_width=2, corner_radius=10
        )
        expense_card.place(x=360, y=350)
        
        ctk.CTkLabel(
            expense_card, text="Debit", font=ctk.CTkFont(size=15, weight="bold"), 
            text_color='#1375d0', bg_color='transparent'
        ).place(x=20, y=5)
        
        expense_amount = f"${self.user_data[4]:.2f}" if self.user_data else "$0.00"
        self.expense_label = ctk.CTkLabel(
            expense_card, text=expense_amount, font=ctk.CTkFont(size=28, weight="bold"), 
            text_color='#222', bg_color='transparent'
        )
        self.expense_label.place(x=20, y=30)

        # Reward Card
        reward_card = ctk.CTkFrame(
            self.dashboard_frame, width=300, height=80, fg_color='white', 
            border_color='#e0e1e2', border_width=2, corner_radius=10
        )
        reward_card.place(x=20, y=150)
        
        ctk.CTkLabel(
            reward_card, text="Reward Points", font=ctk.CTkFont(size=15, weight="bold"), 
            text_color='#1375d0', bg_color='transparent'
        ).place(x=20, y=5)
        
        reward_points = str(self.user_data[2]) if self.user_data else "0"
        self.reward_label = ctk.CTkLabel(
            reward_card, text=reward_points, font=ctk.CTkFont(size=28, weight="bold"), 
            text_color='#222', bg_color='transparent'
        )
        self.reward_label.place(x=20, y=30)

    def create_activity_chart(self):
        recent_activity_card = ctk.CTkFrame(
            self.dashboard_frame, width=300, height=220, fg_color='white', 
            border_color='#e0e1e2', border_width=2, corner_radius=10
        )
        recent_activity_card.place(x=20, y=250)
    
        recent_activity_label = ctk.CTkLabel(
            recent_activity_card, text="Recent Activity", 
            font=ctk.CTkFont(size=15, weight="bold"), 
            text_color='#1375d0', bg_color='transparent'
        )
        recent_activity_label.place(x=20, y=5)
        chart_data = self.db.get_transaction_chart_data(self.user_data[5],self.user_data[1])
        if MATPLOTLIB_AVAILABLE:
            try:
                if chart_data and len(chart_data) > 1:
                    x_values = list(range(1, len(chart_data) + 1))
                else:
                    x_values = [1, 2, 3, 4, 5]
                    chart_data = [0] * 5  # fallback data
            
                # Create matplotlib chart
                fig = Figure(figsize=(3.6, 2.3), dpi=100)
                ax = fig.add_subplot(111)
                ax.plot(x_values, chart_data, marker='o', color="#4899f0")
            
                ax.set_xlabel('Transaction', fontsize=8)
                ax.set_ylabel('Amount ($)', fontsize=8)
                ax.tick_params(axis='both', labelsize=8)
                fig.tight_layout(pad=1)

                canvas = FigureCanvasTkAgg(fig, master=recent_activity_card)
                canvas.draw()
                canvas.get_tk_widget().place(x=10, y=35)
            except Exception as e:
                print(f"Error creating chart: {e}")


    def update_dashboard_values(self):
        """Update dashboard values after data refresh"""
        if self.user_data:
            welcome_text = f"Welcome! {self.user_data[0]}"
            self.welcome_label.configure(text=welcome_text)
            
            self.balance_label.configure(text=f"${self.user_data[1]:.2f}")
            self.income_label.configure(text=f"${self.user_data[3]:.2f}")
            self.expense_label.configure(text=f"${self.user_data[4]:.2f}")
            self.reward_label.configure(text=str(self.user_data[2]))
