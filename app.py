from flask import Flask, redirect, url_for, render_template, request
import os
import requests
import json
app = Flask(__name__)

try:
    SERVICE_BASE_URL = os.environ['SERVICE_BASE_URL']
    USER_ID = os.environ['USER_ID']
except KeyError:
    SERVICE_BASE_URL = 'http://localhost:5000/'
    USER_ID = ''


@app.route("/")
def hello():
    return redirect(url_for('lists'))


@app.route('/lists', methods=['GET', 'POST'])
def lists():
    response = requests.get(SERVICE_BASE_URL + 'lists')
    result = json.loads(response.content)
    return render_template('lists.jinja', lists=result.items())


@app.route('/lists/new', methods=['GET', 'POST'])
def new_list():
    if request.method == 'POST':
        payload = {'name': request.form['name'], 'user_id': USER_ID}
        response = requests.post(SERVICE_BASE_URL + 'lists', payload)
        if response.status_code == 201:
            return redirect('lists')
    return render_template('new_list.jinja')


@app.route('/lists/<list_id>')
def delete_list(list_id):
    requests.delete(SERVICE_BASE_URL + 'lists/' + list_id)
    return redirect('lists')


@app.route('/lists/<list_id>/items')
def items(list_id):
    response = requests.get(SERVICE_BASE_URL + 'lists/' + list_id + '/items')
    result = json.loads(response.content)
    return render_template('items.jinja', items=result)


@app.route('/lists/<list_id>/items/new', methods=['GET', 'POST'])
def new_item(list_id):
    if request.method == 'POST':
        payload = {'name': request.form['name'], 'priority': request.form['priority']}
        response = requests.post(SERVICE_BASE_URL + 'lists/' + list_id + '/items', payload)
        if response.status_code == 201:
            return redirect('lists/{}/items'.format(list_id))
    return render_template('new_item.jinja')


@app.route('/lists/<list_id>/items/<name>')
def delete_item(list_id, name):
    requests.delete(SERVICE_BASE_URL + 'lists/' + list_id + '/items/' + name)
    return redirect('lists/{}/items'.format(list_id))


@app.route('/profile/<user_id>')
def profile(user_id):
    response = requests.get(SERVICE_BASE_URL + 'users/' + user_id)
    result = json.loads(response.content)
    return render_template('profile.jinja', profile=result)


@app.route('/login')
def login():
    return "Login"


@app.route('/logout')
def logout():
    return "None"


@app.route('/signup')
def signup():
    return "Signup"


if __name__ == "__main__":
    try:
        port = int(os.environ['PORT'])
    except KeyError:
        port = 5000

    app.debug = True
    app.run(host='0.0.0.0', port=port)
