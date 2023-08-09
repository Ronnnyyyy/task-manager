from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="task_management"
)

cursor = db.cursor()

@app.route('/')
def index():
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    return render_template('index.html', tasks=tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    title = request.form['title']
    description = request.form['description']
   
    insert_query = "INSERT INTO tasks (title, description) VALUES (%s, %s)"
    task_data = (title, description)
    cursor.execute(insert_query, task_data)
    db.commit()
    return redirect(url_for('index'))

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    if request.method == 'POST':
        new_title = request.form['new_title']
        new_description = request.form['new_description']
        
        update_query = "UPDATE tasks SET title = %s, description = %s WHERE id = %s"
        update_data = (new_title, new_description, task_id)
        cursor.execute(update_query, update_data)
        db.commit()

        return redirect(url_for('index'))
    else:
        cursor.execute("SELECT * FROM tasks WHERE id = %s", (task_id,))
        task = cursor.fetchone()
        return render_template('edit.html', task=task)

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    try:
        delete_query = "DELETE FROM tasks WHERE id = %s"
        cursor.execute(delete_query, (task_id,))
        db.commit()
    except Exception as e:
        print("Error:", e)
        db.rollback()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()