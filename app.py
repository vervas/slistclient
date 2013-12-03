from flask import Flask, redirect, url_for, render_template
import requests, json
app = Flask(__name__)


SERVICE_BASE_URL = 'http://snf-24511.vm.okeanos.grnet.gr:5000/'

@app.route("/")
def hello():
    return redirect(url_for('login'))


@app.route('/lists')
def lists():
    response = requests.get(SERVICE_BASE_URL + 'lists')
    result = json.loads(response.content)
    return render_template('lists.jinja', lists=result.items())


@app.route('/lists/<list_id>/items')
def items(list_id):
    response = requests.get(SERVICE_BASE_URL + 'lists/' + list_id + '/items')
    result = json.loads(response.content)
    return render_template('items.jinja', items=result)


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
    app.run(debug=True)
