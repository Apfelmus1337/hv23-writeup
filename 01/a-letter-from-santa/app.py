from flask import Flask, render_template, request
import string

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        alphabet = {char: "" for char in string.ascii_lowercase}
        alphabet[request.form['alphabet_select']] = request.form['user_input']

        return render_template('santa.j2', **alphabet)
    else:
        return render_template('index.html', alphabet=string.ascii_lowercase)

if __name__ == '__main__':
    app.run(host="0.0.0.0")
