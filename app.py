from flask import Flask, render_template, request, redirect
from nav import generate_route

app = Flask(__name__)

@app.route('/')
def homePage(): 
    return render_template('home.html')

@app.route('/route_finder', methods = ['POST'])
def routeFinder():
    if request.method == 'POST': 
        startAddress = request.form['startAddress'] 
        endAddress = request.form['endAddress']
        generate_route(startAddress, endAddress)
        return render_template('route.html', start = startAddress, end = endAddress)

if __name__ == '__main__':
    app.run(port = 5000, debug = True)