from flask import Flask, render_template, request, redirect
from main import *

app = Flask(__name__)

@app.route('/')
def homePage(): 
    return render_template('home.html')

@app.route('/route_finder', methods = ['POST'])
def routeFinder():
    if request.method == 'POST': 
        startAddress = request.form['startAddress'] 
        endAddress = request.form['endAddress']
        displayAddress(startAddress, endAddress)            
        return render_template('display.html', start = startAddress, end = endAddress)

def displayAddress(start, end): 
    print(start)
    print(end)

if __name__ == '__main__':
    app.run(port = 5000, debug = True)