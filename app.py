from flask import Flask, render_template, request,jsonify

app = Flask(__name__)
data = ['','']
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pi', methods=['POST'])
def pi():
    pico_data = request.json
    print(f'Vaule on server {pico_data}') #--> Value on server {'temp': 100, 'temp_1': 150}
    #{'temp_2': 150, 'temp_1': 100}
    data[0] = pico_data['temp_1']
    data[1] = pico_data['temp_2']
    
    return 'done'

@app.route('/dashboard')
def dashboard():
    
    return render_template('dashboard.html')

    
#Get data
@app.get('/update')
def update():
    
    return jsonify(temp1=data[0],temp2=data[1])


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')