from flask import Flask, request, render_template
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello_world():
	if request.method == 'POST':
		return 'orange'
	else:
		return render_template('index.html')