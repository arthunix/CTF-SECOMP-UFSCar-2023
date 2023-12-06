from flask import Flask, request, render_template
import sqlite3
import tempfile
from simple_sanitize import sanitize_input

app = Flask(__name__)

flag = open("flag").read().strip()


class TemporaryDB:
    def __init__(self):
        self.db_file = tempfile.NamedTemporaryFile("x", suffix=".db")

    def execute(self, sql, parameters=()):
        connection = sqlite3.connect(self.db_file.name)
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        result = cursor.execute(sql, parameters)
        connection.commit()
        return result


db = TemporaryDB()

@app.route('/', methods=['GET', 'POST'])
def index():
    
    db.execute(("CREATE TABLE IF NOT EXISTS keys AS "
                'SELECT ? as key'),
                (flag,))

    if request.method == 'POST':
        key = request.form.get('key')
        if sanitize_input(key):
            keys = db.execute(f'SELECT * FROM keys WHERE key = "{key}"').fetchall()
            if not keys:
                return('InvalidKeyError("Invalid key")', 401)
            return(f"Logged sucessfully, here's your flag: {flag}")
        return("Blocked!", 777)
    
    return render_template('auth.html')
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug = False) # take care of the debug option (this should not be on the final)
    