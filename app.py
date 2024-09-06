from flask import Flask, render_template, request, flash, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def execute_query(query):
    db_path = 'sqlite-sakila.db'
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    connection.close()
    return rows, column_names

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form.get('query')
        
        if query:
            try:
                rows, columns = execute_query(query)
                return render_template('index.html', rows=rows, columns=columns, query=query)
            except sqlite3.Error as e:
                flash(f"An error occurred: {e}")
                return redirect(url_for('index'))
    
    return render_template('index.html', rows=None, columns=None, query=None)

if __name__ == '__main__':
    app.run(debug=True)
