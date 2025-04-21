from flask import Flask, render_template, request, redirect
import mysql.connector
import bcrypt

app = Flask(__name__)

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="file_sharing"
    )

@app.route('/')
def home():
    return 'Hello, this is my file sharing app!'

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')
        password_hash = bcrypt.hashpw(password, bcrypt.gensalt())
        try:
            db = connect_db()
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
                (username, password_hash)
            )
            db.commit()
            cursor.close()
            db.close()
            return redirect('/')
        except mysql.connector.Error as e:
            return f"Error: {e}"
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')
        try:
            db = connect_db()
            cursor = db.cursor()
            cursor.execute("SELECT password_hash FROM users WHERE username = %s", (username,))
            result = cursor.fetchone()
            cursor.close()
            db.close()
            if result and bcrypt.checkpw(password, result[0]):
                return 'Login successful!' 
            else:
                return render_template('login.html', error='Invalid username or password')
        except mysql.connector.Error as e:
            return f"Error: {e}"
    return render_template('login.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)