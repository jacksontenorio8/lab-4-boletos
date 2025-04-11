from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
import re

class Config:
    MONGO_URI = "mongodb://localhost:27017/boletos_db" # Replace with your MongoDB connection URI

class Boleto:
    def __init__(self, codigo_barras, valor, data_vencimento, pagador=None, beneficiario=None):
        self.codigo_barras = codigo_barras
        self.valor = valor
        self.data_vencimento = data_vencimento
        self.pagador = pagador
        self.beneficiario = beneficiario
        self.data_geracao = datetime.now()
        self.status = "pendente" # Default status

    def to_dict(self):
        return {
            "codigo_barras": self.codigo_barras,
            "valor": self.valor,
            "data_vencimento": self.data_vencimento,
            "pagador": self.pagador,
            "beneficiario": self.beneficiario,
            "data_geracao": self.data_geracao,
            "status": self.status
        }

    @staticmethod
    def gerar(valor, data_vencimento, pagador=None, beneficiario=None):
        # Implement a more robust barcode generation logic here based on bank rules
        # This is a simplified example
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        codigo_barras = f"{timestamp}{int(valor*100):010d}" # Simple concatenation
        return Boleto(codigo_barras, valor, data_vencimento, pagador, beneficiario)

    @staticmethod
    def validar_codigo_barras(codigo):
        # Basic validation: check length and if it's numeric
        return bool(re.match(r'^[0-9]+$', codigo)) and len(codigo) >= 20 # Adjust length as needed

class UI:
    @staticmethod
    def validar_boleto_data(data):
        if not all(key in data for key in ('valor', 'data_vencimento')):
            return False, "Campos 'valor' e 'data_vencimento' são obrigatórios."
        try:
            float(data['valor'])
            datetime.strptime(data['data_vencimento'], '%Y-%m-%d') # Expecting YYYY-MM-DD format
        except ValueError:
            return False, "Formato de 'valor' inválido ou formato de 'data_vencimento' incorreto (YYYY-MM-DD)."
        return True, None

class Storage:
    def __init__(self, mongo_uri):
        self.client = MongoClient(mongo_uri)
        self.db = self.client.get_database()
        self.boletos = self.db.boletos

    def salvar(self, boleto):
        boleto_data = boleto.to_dict()
        result = self.boletos.insert_one(boleto_data)
        return result.inserted_id

    def atualizar_status(self, codigo_barras, novo_status):
        result = self.boletos.update_one({"codigo_barras": codigo_barras}, {"$set": {"status": novo_status}})
        return result.modified_count > 0

    def buscar(self, codigo_barras):
        return self.boletos.find_one({"codigo_barras": codigo_barras})

app = Flask(__name__)
app.config.from_object(Config)
storage = Storage(app.config['MONGO_URI'])

@app.route('/gerar', methods=['POST'])
def gerar_boleto_endpoint():
    data = request.get_json()
    valid, message = UI.validar_boleto_data(data)
    if not valid:
        return jsonify({"erro": message}), 400

    boleto = Boleto.gerar(
        valor=data['valor'],
        data_vencimento=data['data_vencimento'],
        pagador=data.get('pagador'),
        beneficiario=data.get('beneficiario')
    )
    boleto_id = storage.salvar(boleto)
    return jsonify({"id": str(boleto_id), "codigo_barras": boleto.codigo_barras}), 201

@app.route('/validar', methods=['POST'])
def validar_boleto_endpoint():
    data = request.get_json()
    if not data or 'codigo' not in data:
        return jsonify({"erro": "Campo 'codigo' ausente no JSON."}), 400

    codigo = data['codigo']
    if not Boleto.validar_codigo_barras(codigo):
        return jsonify({"valido": False, "mensagem": "Código de barras inválido."}), 400

    boleto_existente = storage.buscar(codigo)
    if boleto_existente:
        return jsonify({"valido": True, "boleto": {
            "codigo_barras": boleto_existente['codigo_barras'],
            "valor": boleto_existente['valor'],
            "data_vencimento": boleto_existente['data_vencimento'],
            "status": boleto_existente['status']
        }}), 200
    else:
        return jsonify({"valido": False, "mensagem": "Boleto não encontrado."}), 404

if __name__ == '__main__':
    app.run(debug=True)