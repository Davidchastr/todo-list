from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

todos = []

@app.route('/')
def index():
    return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def add_todo():
    task = request.form.get('task')
    category = request.form.get('category', 'Без категории')
    priority = request.form.get('priority', 'Низкий')
    if task:
        todos.append({'task': task, 'category': category, 'priority': priority, 'completed': False})
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete_todo(task_id):
    todos.pop(task_id)  # Оставляем баг для тестирования
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>')
def complete_todo(task_id):
    if 0 <= task_id < len(todos):
        todos[task_id]['completed'] = not todos[task_id]['completed']
    return redirect(url_for('index'))

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_todo(task_id):
    if 0 <= task_id < len(todos):
        if request.method == 'POST':
            task = request.form.get('task')
            category = request.form.get('category')
            priority = todos[task_id]['priority']  # Оставляем баг
            todos[task_id] = {'task': task, 'category': category, 'priority': priority, 'completed': todos[task_id]['completed']}
            return redirect(url_for('index'))
        return render_template('edit.html', todo=todos[task_id], task_id=task_id)
    return redirect(url_for('index'))