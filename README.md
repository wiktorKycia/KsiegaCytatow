# Księga cytatów - Quotes book
Python Flask app, that is being created to save
some funny things that teachers often say

## Technical stuff and how it works

### Database
The app connects to MariaDB database in XAMPP

see more information about database [here](database_info/info.md)

### Features (future)
- searching the quotes
- liking quotes
- adding quotes
- adding authors (admin only)
- adding nicknames to authors
  - since one person can be called in a different ways
- api
  - for others that will create a better looking front-end app
  - to be able to create a discord bot, that will retrieve new quotes from discord

## How do I run this on my own computer?

### Installation

#### IDE
- For IDE I would recommend [PyCharm](https://www.jetbrains.com/pycharm/download/?section=windows) like I am using or alternatively [Visual Studio Code](https://code.visualstudio.com/download).
- You don't have to have the Professional version of PyCharm - the Community one will be enough.
- You can also use any other IDE, however they are not included in this tutorial.

#### Tools
- You will obviously need Python programming language ([version 3.12](https://www.python.org/downloads/))
- For database you will need the [XAMPP enviroment](https://www.apachefriends.org/pl/download.html)

### Setting up a project
* After you install the .zip file and unzip it on your computer, open the folder in an IDE
* open the terminal in your IDE (Ctrl+Shift+` in VSCode, Alt+F12 in PyCharm)
* if there is no venv (virtual enviroment) create it:
```bash
python -m venv venv
```
Run the command in the terminal
...


















