from flask import Flask, render_template,request
from updateHTML import chamb_csv

#Use Flask to generate web server 
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/jtag')
def jtag():
    return render_template('JTAG.html')

@app.route('/chamber')
def chamber():
    return render_template('chamber.html')

@app.route('/chamber/process',methods = ['POST'])
def process():
    #Get chamber number from JavaScript
    data = request.get_json()
    run_num = data['run_numb']
    chamber_ = data['chamber']
    #Create FSM table for chamber page based on specific chamber
    chamb_csv(run_num,chamber_)
    return chamber_


@app.route('/hv_ml1')
def hv_ml1():
    return render_template('HV_ML1.html')

@app.route('/hv_ml2')
def hv_ml2():
    return render_template('HV_ML2.html')

@app.route('/lv')
def lv():
    return render_template('LV.html')

@app.route('/stats')
def statistics():
    return render_template('statistics.html')

if __name__ == "__main__":
    #Run server 
    app.run(debug=True)#,host = '0.0.0.0')
