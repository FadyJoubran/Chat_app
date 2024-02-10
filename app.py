from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Lputwwd2002-MySQL3",
    database="chat_db"
)

cursor = db.cursor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save', methods=['POST'])
def save():
    text = request.json['text']
    # Insert text into database
    sql = "INSERT INTO texts (text) VALUES (%s)"
    val = (text,)
    cursor.execute(sql, val)
    db.commit()
    return "Text saved successfully."

@app.route('/get_messages')
def get_messages():
    cursor.execute("SELECT text FROM texts")
    messages = cursor.fetchall()
    return jsonify(messages)

@app.route('/delete_all', methods=['POST'])
def delete_all():
    print("Request IP Address:", request.remote_addr)
    # Check if the request is coming from a trusted source
    if request.remote_addr == '127.0.0.1':
        # Delete all records from the texts table
        cursor.execute("DELETE FROM texts")
        db.commit()
        return "All records deleted successfully."
    else:
        return "Unauthorized", 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
