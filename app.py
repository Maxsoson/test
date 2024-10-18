import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def write_user(username, password):
    users = read_users()
    # Додаємо користувача до словника
    users[username] = {
        "name": username,
        "password": password
    }
    # Записуємо в JSON файл
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=4)  # Додаємо параметр indent для кращого форматування

def read_users():
    try:
        with open('users.json', 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):  # Обробка обох помилок
        return {}  # Повертаємо порожній словник

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        write_user(username, password)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = read_users()
        # Перевіряємо, чи користувач існує і чи правильний пароль
        if username in users and users[username]["password"] == password:
            return "Login Successful"
        return "Invalid credentials"
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)