from flask import Flask, jsonify, render_template
import random

app = Flask(__name__)

blacklist = {
    "049 437 100 01",
    "049 437 100 02",
    # …
}

whitelist = [
    "158 311 360 07",
    "318 597 160 46",
    "018 787 253 40 01",
    # …
]

@app.route('/')
def index():
    # Отдаём HTML из templates/index.html
    return render_template('index.html')

@app.route('/api/draw')
def draw():
    # Мгновенный выбор «выигрышного» билета из white‑list
    ticket = random.choice(whitelist)
    return jsonify({ 'ticket': ticket })

if __name__ == '__main__':
    app.run(debug=True)
