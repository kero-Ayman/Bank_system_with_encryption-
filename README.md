Simple Bank CLI – JSON Storage + SHA-256 Passwords

A simple command-line banking system built in Python.
Users can log in, view balances, and grant or revoke permission for other users to view their balance.
The system uses JSON for data storage and SHA-256 hashing for secure password handling.
Features
     
  🔒 Secure Passwords
      Passwords are stored using SHA-256 hashing
      
  👑 Admin Account
      The admin (default: kerolos) can:
      Add new users
      View any user's balance
      Grant or revoke permissions

  🧑‍💻 User Actions
      Regular users can:
      View their own balance
      View another user’s balance only if they were granted permission
      Grant or revoke permission for others
