# PayPerks E-Wallet Application

This is a simple sample digital transaction wallet with Remote MySQL database backend, featuring the basic applications of the e-wallet.

The key features of the project are:
    - User Sign-Up with password hashing
    - OTP Authentication system for new user registration(sends OTP via email)
    - User Sign-In with session handling
    - Transaction system between accounts
    - Reward Points currency convertible to the the regular currency.
    - Azure based remote MySQL database for storing user details, transaction history, login sessions, rewards.

Project Dependencies (Python Libraries):
    -Tkinter for GUI
    -PIL(pillow) for handling images
    -smtp for email service
    -mysql.connector for database connection
    -hashlib for password hashing
    -matplotlib for figures
    -uuid for session management

Requirements
  -Python3 (with standard library)
  ***use pip install for:***
  -Pillow
  -mysql-connector-python
  -matplotlib

Create a MySQL server and replace the connection parameters to connect the app with your own database.
