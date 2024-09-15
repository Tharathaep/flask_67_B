from flask import Flask, render_template, request, redirect, session, flash
import mysql.connector


app = Flask(__name__)

# For Database
DB_HOST = "localhost"
DB_USER = "root"
DB_PASS = ""
DB_NAME = "flower_shop"

app.config['SECRET_KEY'] = "adsasddsdsa1d654as1dsa3daadawwa"

@app.route("/home")
def home():
    # return "<h1>Hello World</h1>"
    name = "anya"
    age = 8
    my_dict = {"name": "Yor", "age": 26}
    return render_template("home.html", name=name, age=age, my_dict=my_dict)

@app.route("/create", methods=["GET"])
def create():
    return render_template("create.html")

@app.route("/store", methods=["POST"])
def store():
    if request.method == "POST":
        flower_name = request.form['flower_name']
        lat_num = request.form['lat_num']
        long_num = request.form['long_num']
        place = request.form['place']
        detail = request.form['detail']
        print("input:", flower_name, lat_num, long_num, place, detail)

        # Connect to Database
        my_db = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            db=DB_NAME
            )
        my_cursor = my_db.cursor(dictionary=True)

            # Insert data into database
        sql = "INSERT INTO flower (flower_name, lat_num, long_num, place, detail) VALUES (%s, %s, %s, %s, %s)"
        val = (flower_name, lat_num, long_num, place, detail)
        my_cursor.execute(sql, val)
        my_db.commit()
            
        session['alert_status'] = "success"
        session['alert_message'] = "Already Created!"
        return redirect("/")

        
    else:
        session['alert_status'] = "fail"
        session['alert_message'] = "Something went wrong!"
        return redirect("/")
    
@app.route("/")
def index ():
    # Connect to Database
            my_db = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASS,
                db=DB_NAME
            )
            my_cursor = my_db.cursor(dictionary=True)
            sql = "SELECT * FROM flower"
            my_cursor.execute(sql)
            results = my_cursor.fetchall()
            
            if "alert_status" in session and "alert_message" in session:
                alert_message = {
                    'status': session['alert_status'],
                    'message': session['alert_message'],
                }
                del session ['alert_status']
                del session ['alert_message']
            else:
                alert_message = {
                    'status': None,
                    'message': None,
                }

            return render_template("index.html", results = results , alert_message = alert_message)
        
@app.route("/edit/<id>", methods = ['GET'])
def edit (id):
    # Connect to Database
            my_db = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASS,
                db=DB_NAME
            )
            my_cursor = my_db.cursor(dictionary=True)
            sql = "SELECT * FROM flower WHERE id =" + id
            my_cursor.execute(sql)
            results = my_cursor.fetchall()
            
            return render_template("edit.html" , results = results)
        
@app.route("/update/<id>", methods = ["POST"])
def update(id):
    if request.method == "POST":
        flower_name = request.form['flower_name']
        lat_num = request.form['lat_num']
        long_num = request.form['long_num']
        place = request.form['place']
        detail = request.form['detail']
        print("input:", flower_name, lat_num, long_num, place, detail)

        # Connect to Database
        my_db = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            db=DB_NAME
            )
        my_cursor = my_db.cursor(dictionary=True)

            # Insert data into database
        sql = """
            UPDATE flower
            SET flower_name = %s,
                lat_num = %s,
                long_num = %s,
                place = %s,
                detail = %s
                WHERE id = %s
        """
        val = (flower_name, lat_num, long_num, place, detail, id)
        my_cursor.execute(sql, val)
        my_db.commit()
            
        session['alert_status'] = "success"
        session['alert_message'] = "Already Updated!"
        return redirect("/")
    else:
        session['alert_status'] = "fail"
        session['alert_message'] = "Something went wrong!"
        return redirect("/")
    
        
@app.route("/delete/<id>", methods=["GET"])
def delete(id):
    # Connect to Database
            my_db = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASS,
                db=DB_NAME
            )
            my_cursor = my_db.cursor(dictionary=True)
            sql = "DELETE FROM flower WHERE id =" + id
            my_cursor.execute(sql)
            my_db.commit()
            
            session['alert_status'] = "success"
            session['alert_message'] = "Already Deleted!"
            return redirect("/")
        
        
if __name__ == "__main__":
    app.run(debug=True)
