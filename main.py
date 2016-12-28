from flask import Flask, request, render_template
import nonogram
app = Flask(__name__)

@app.route('/')
def index():
		return render_template('index.html')

@app.route('/create', methods=['GET', 'POST'])
def create():
	if request.method == 'POST':
		return nonogram.populate_grid(request)
	else:
		return render_template('create.html')
