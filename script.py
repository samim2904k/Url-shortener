from flask import Flask,render_template,jsonify,request,redirect
import pymysql
import string
import random

app=Flask(__name__)

db_config = {
    'host':'localhost',
    'user':'root',
    'password': '',
    'database': 'url_shortener'
}

time_stamp = ""

def get_db_conn():
    conn=pymysql.connect(**db_config)
    return conn

def generate_code():
    available_characters = string.ascii_letters + string.digits
    code = ''.join(random.choice(available_characters) for _ in range(6))
    return code

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit" , methods=["POST","GET"])
def shorten():
    conn=get_db_conn()
    cursor=conn.cursor()

    long_url = request.form.get("long_url")
    code = generate_code()
    print(long_url)
    print(time_stamp)
    print(code)

    short_url = request.url_root + code
    print(short_url)

    print(f"select short_code from url_info;")
    cursor.execute(f"select short_code from url_info;")
    unavailable_code = cursor.fetchall()
    
    while True:
        if code in unavailable_code:
            print("This code is unavailable")
            code=generate_code()
            short_url = request.url_root + code
            print(short_url)
        else:
            print("This code is available")
            break
    
    print(f"insert into url_info(long_url,short_code) values ('{long_url}','{code}');")
    cursor.execute(f"insert into url_info(long_url,short_code) values ('{long_url}','{code}');")
    conn.commit()

    return render_template("index.html",shorten_link=short_url)

@app.route("/time_update",methods=["POST","GET"])
def time_updation():
    global time_stamp
    json_data = request.get_json()
    time_stamp = json_data.get("time_stamp")
    print(time_stamp)
    return jsonify(success=True)

@app.route('/<code>')
def original_url(code):
    conn=get_db_conn()
    cursor=conn.cursor()

    print(f"select * from url_info where short_code = '{code}';")
    cursor.execute(f"select * from url_info where short_code = '{code}';")
    data=cursor.fetchone()

    if data:
        print(data[1])
        return redirect(data[1])
    else:
        return "Short Url not Found.", 404

if __name__=="__main__":
    app.run(debug=True)