from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
import bcrypt

app = Flask(__name__)
app.secret_key = 'your-secret-key'  

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",  
        database="file_sharing"
    )

@app.route('/')
def home():
    username = request.args.get('username')  
    if not username:
        flash('Please log in first', 'error')
        return redirect(url_for('login'))
    return render_template('home.html', username=username)

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
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except mysql.connector.Error as e:
            return render_template('register.html', error=f"Error: {e}")
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
                return redirect(url_for('home', username=username))
            else:
                flash('Invalid username or password', 'error')
                return render_template('login.html')
        except mysql.connector.Error as e:
            flash(f"Error: {e}", 'error')
            return render_template('login.html')
    return render_template('login.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)