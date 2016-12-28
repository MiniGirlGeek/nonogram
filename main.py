from flask import Flask, request, render_template
import nonogram
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def hello_world():
	if request.method == 'POST':
		return nonogram.populate_grid(request)
		#draw.test()
		#draw.send_data(request)
	else:
		return render_template('index.html')
