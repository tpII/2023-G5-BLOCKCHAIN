from flask import Flask, render_template, request
from flask_ngrok import run_with_ngrok
import pickle

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))
run_with_ngrok(app)

@app.route("/") #decorador, modifica el comportamiento de una función o de una clase
def home():
    return render_template('index.html')

@app.route("/predecir", methods=['POST'])
def predecir():
    cuartos = int(request.form['cuartos'])
    distancia = int(request.form['distancia'])
    prediccion = model.predict([[cuartos, distancia]]) #Devuelve una lista
    output = round(prediccion[0], 2)

    return render_template('index.html', prediccion_texto=f'La casa con {cuartos} cuartos y localizado a {distancia} km tiene un valor de ${output}K')

if __name__ == "__main__": 
    app.run()