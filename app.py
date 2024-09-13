# IMPORTING LIBRARIES AND MODULES FROM PYTHON
from flask import Flask, render_template, request,jsonify, redirect, url_for
import bcrypt
from mysql.connector import Error

#  IMPORTING FUNCTIONS FROM OTHER FILES
from connection import connection

# CREATING AN INSTANCE OF FLASK
app = Flask(__name__)

# Preparing my first function of pushing data from form to backend database of aiven
@app.route("/")
def landing_page():
    return render_template("index.html")

# SHOWING THE PLANS PAGE
@app.route("/plans")
def plans():
  return render_template("plans.html")

# Rendering the form page and taking the submissions and storing them into the table
@app.route("/forms", methods = ["POST","GET"])
def form_render():
  if(request.method == "GET"):
    return render_template("forms.html")
  elif(request.method=="POST"):
    name = request.form['name']
    email = request.form['email']
    mobile = request.form['mobile']
    dob = request.form['dob']
    height = request.form['height']
    weight = request.form['weight']
    address = request.form['address']
    plan = request.form['plan']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    disease = request.form['disease']
    trainer = request.form['trainer']

    try:
      conn = connection()
      cursor = conn.cursor()

      #Creating Table users if it don't exist
      cursor.execute("""CREATE TABLE IF NOT EXISTS person (
    user_id INT AUTO_INCREMENT,        -- Auto-incrementing unique ID for each person
    name VARCHAR(100) NOT NULL,           -- Compulsory Name
    email VARCHAR(100) UNIQUE,            -- Unique Email
    mobile VARCHAR(14) NOT NULL,   -- Compulsory Mobile Number (Assuming 15-digit max for international format)
    dob DATE NOT NULL,          -- Compulsory Date of Birth
    height DECIMAL(5,2),                  -- Height in cm (can handle up to 999.99 cm)
    weight DECIMAL(5,2),                  -- Weight in kg (can handle up to 999.99 kg)
    address TEXT NOT NULL,                -- Compulsory Address
    plan ENUM('Monthly', 'Quarterly', 'Yearly') NOT NULL, -- Plan (Dropdown options)
    password VARCHAR(255) NOT NULL,       -- Compulsory Password
    confirm_password VARCHAR(255) NOT NULL, -- Compulsory Confirm Password
    disease VARCHAR(255) DEFAULT 'NA', -- Any chronic disease (NA if not)
    trainer varchar(32) NOT NULL, -- Trainer's Name
    join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Automatic current join date
    PRIMARY KEY (user_id)               -- Setting user_id as primary key
    FOREIGN KEY (user_id) REFERENCES person(person_id)
    ON UPDATE CASCADE
);
""")
      
      #CREATING QUERY FOR INSERTION
      query_insert = 'INSERT INTO person(name,email,mobile,dob,height,weight,address,plan,password,confirm_password,disease,trainer) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
      cursor.execute(query_insert,(name,email,mobile,dob,height,weight,address,plan,password,confirm_password,disease,trainer))
      conn.commit()
      cursor.close()
      conn.close()
      print('One insert query has been successfully executed')
      return jsonify({'message': 'Data inserted successfully!'})
    
    except Error as e:
      return jsonify({'error': str(e)})
    
    
# SIGNUP FOR USERS/TRAINERS AND STORING DATA IN USERS TABLE IN THE DATABASE
@app.route("/signup", methods = ["POST","GET"])
def signup():
  if(request.method=="GET"):
    return render_template("signup.html")
  elif(request.method == "POST"):
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    hash_password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
    hash_pass_str = hash_password.decode('utf-8')
    role = request.form['role']

    try:
      conn = connection()
      cursor = conn.cursor()

      cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
        user_id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) NOT NULL,
        email VARCHAR(100) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        role varchar(15) NOT NULL DEFAULT 'user',
        created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
      )
      query_insert = 'INSERT INTO users(username, email, password, role) VALUES (%s,%s,%s,%s);'
      cursor.execute(query_insert,(username,email,hash_pass_str,role))
      conn.commit()
      cursor.close()
      conn.close()
      print('One insert query has been successfully executed')
      return jsonify({'message': 'Data inserted successfully!'})
    
    except Error as e:
      return jsonify({'error': str(e)})


# LOGIN FOR USERS/TRAINERS/ADMIN AND VERIFYING DATA FROM THE DATA IN DATABASE
@app.route("/login", methods = ["POST","GET"])
def login():
  if (request.method== "GET"):
    return render_template("login.html")
  
  elif(request.method == "POST"):
    email = request.form['email']
    password = request.form['password']
    role = request.form['role']

    conn = connection()
    cursor = conn.cursor()

    query = 'SELECT email, password, role FROM users WHERE email = %s AND role = %s '
    cursor.execute(query,(email,role))
    login_data = cursor.fetchone()
    if login_data:
      password_get= login_data[1]
      pass_final = password_get.encode('utf-8')
      if(bcrypt.checkpw(password.encode('utf-8'),pass_final)):
        return (f"HO gya login {email}")
      else:
        return(f'Incorrect password for {email}')
    else:
      return ("NO USER FOUND!!!")
    





if __name__ == "__main__":
  app.run(debug=True , port=8000)

