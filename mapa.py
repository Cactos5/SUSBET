# mapa.py

from flask import Flask, render_template, jsonify, request
import requests

app = Flask(__name__)

# Rota principal que carrega o mapa
@app.route('/')
def index():
    return render_template('mapa.html')

# Função para buscar locais de saúde próximos
@app.route('/health-facilities', methods=['GET'])
def get_health_facilities():
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    
    # Definir a consulta Overpass API para encontrar hospitais e clínicas num raio de 20km
    overpass_query = f'''
    [out:json];
    (
      node["amenity"="hospital"](around:20000,{lat},{lng});
      node["amenity"="clinic"](around:20000,{lat},{lng});
      node["amenity"="doctors"](around:20000,{lat},{lng});
      node["amenity"="pharmacy"](around:20000,{lat},{lng});
    );
    out body;
    '''

    # URL da Overpass API
    overpass_url = "https://overpass-api.de/api/interpreter"

    try:
        # Fazer a requisição para a Overpass API
        response = requests.get(overpass_url, params={'data': overpass_query})
        response.raise_for_status()  # Verifica se houve erro na requisição
        data = response.json()

        # Retorna os dados de locais de saúde em formato JSON para o front-end
        return jsonify(data)

    except requests.exceptions.RequestException as e:
        # Em caso de erro, retornar uma mensagem de erro
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
