from flask import Flask, render_template, request, redirect, session, flash
import mysql.connector

# For Database
DB_HOST = "localhost"
DB_USER = "root"
DB_PASS = ""
DB_NAME = "flower_shop"

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Add a secret key for sessions

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
        try:
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
            flash("Flower created successfully!", "success")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            flash("Error saving flower data. Please try again.", "danger")
        finally:
            my_cursor.close()
            my_db.close()

        return redirect("/create")
    else:
        return "<h1>No Way!</h1>"

if __name__ == "__main__":
    app.run(debug=True)
