from flask import Flask, render_template, request, redirect, url_for, session, flash
import json

app = Flask(__name__,template_folder='frontend')
app.secret_key = 'supersecretkey'

# Sample users database
with open('users.json') as f:
    users = json.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    role = request.form['role']

    # Check credentials
    if email in users and users[email]['password'] == password and users[email]['role'] == role:
        session['user'] = email
        session['role'] = role
        if role == 'student':
            return redirect(url_for('student_dashboard'))
        elif role == 'faculty':
            return redirect(url_for('faculty_dashboard'))
        elif role == 'director':
            return redirect(url_for('director_dashboard'))
    else:
        flash('Invalid credentials')
        return redirect(url_for('index'))

@app.route('/student')
def student_dashboard():
    if 'role' in session and session['role'] == 'student':
        return render_template('student.html')
    return redirect(url_for('index'))

@app.route('/faculty')
def faculty_dashboard():
    if 'role' in session and session['role'] == 'faculty':
        return render_template('faculty.html')
    return redirect(url_for('index'))

@app.route('/director')
def director_dashboard():
    if 'role' in session and session['role'] == 'director':
        return render_template('director.html')
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
