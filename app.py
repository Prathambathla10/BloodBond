from flask import Flask,render_template,redirect, request,url_for,send_file
import mysql.connector

app=Flask(__name__)


def get_mysql_connection():
    return mysql.connector.connect(
        host='localhost',
        user='prathambathla',
        password='0101',
        database='blood'
    )


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/register')
def signup():
    return render_template('register.html')


@app.route("/register",methods=["POST","GET"])
def signup1():
    
    
    full_name= request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    age = request.form['age']
    college = request.form['college']
    group = request.form['group']
    dob = request.form['dob']
    address = request.form['address']
    password = request.form['password']

    connection = get_mysql_connection()
    cursor = connection.cursor()

    # Check if the username is already taken
    cursor.execute('SELECT * FROM users WHERE phone = %s', (phone,))
    existing_user = cursor.fetchone()

    if existing_user:
        # Phone already exists, handle accordingly (e.g., display an error message)
        return "Phone number already exists. Please choose a different phone number."

    # If the username is unique, insert the new user into the database
    cursor.execute('INSERT INTO users (full_name,email,phone,age,college,blood_group,dob,address,password) VALUES (%s, %s,%s, %s,%s, %s,%s, %s,%s)', (full_name,email,phone,age,college,group,dob,address,password))
    connection.commit()

    cursor.close()
    connection.close()

    # Successful signup, you can redirect to a login page or another page
    return render_template("successfull")


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST','GET'])
def login1():

    phone = request.form['phone']
    password = request.form['password']

    connection = get_mysql_connection()
    cursor = connection.cursor(dictionary=True)
    
    
    cursor.execute('SELECT * FROM users WHERE phone = %s AND password = %s', (phone, password))
    user = cursor.fetchone()


    cursor.close()
    connection.close()


    if user:
        # Successful login, you can redirect to a dashboard or another page

        return send_file("static/cons.jpg", mimetype='image/jpg')
        
    else:
        # Invalid credentials, redirect back to the login page
        return "phone or password is incorrect"
    
@app.route("/find-blood")
def findblood():
    return render_template("findblood.html")

@app.route("/aboutus")
def aboutus():
    return send_file("static/cons.jpg", mimetype='image/jpg')

@app.route('/events')
def events():
    return send_file("static/cons.jpg", mimetype='image/jpg')

app.run(debug=False,host='0.0.0.0')
