import requests
import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import time

load_dotenv()
CODIGO_BITRIX = os.getenv('CODIGO_BITRIX')

app = Flask(__name__)

def extrair_numero(string):
    start_index = string.index("_") + 1
    numero = string[start_index:]
    return numero

# ROTA PARA TRANSFERENCIA DE BATE-PAPO NA BITRIX BATENDO COM RESPONSAVEL INDO PRA FILA
@app.route('/change-the-chat-channel/', methods=['POST'])
def change_the_chat_channel():
    CONTACT_ID = request.args.get('CONTACT_ID')
    QUEUE_ID = request.args.get('QUEUE_ID')

    if not CONTACT_ID or not QUEUE_ID:
        return jsonify({'error': 'CONTACT_ID and QUEUE_ID must be provided in the URL parameters'}), 400

    base_url = f'https://marketingsolucoes.bitrix24.com.br/rest/35002/{CODIGO_BITRIX}'
    url = f'{base_url}/imopenlines.crm.chat.getLastId?CRM.ENTITY_TYPE=CONTACT&CRM_ENTITY={CONTACT_ID}'
    
    response = requests.post(url)
    time.sleep(2)
    
    if response.status_code == 200:
        datajson = response.json()
        id_chat = datajson['result']
        
        url2 = f'{base_url}/imopenlines.operator.transfer?CHAT_ID={id_chat}&QUEUE_ID={QUEUE_ID}'
        response2 = requests.post(url2)
        
        if response2.status_code == 200:
            return "New responsible approved"
        else:
            return f"No responsible approved: {response2.text}" 
    else:
        return f"Failed to get chat ID: {response.text}"

# NOVA ROTA PARA TRANSFERENCIA DE BATE-PAPO COM RESPONSÁVEL
@app.route('/change-the-chat-responsible/', methods=['POST'])
def change_the_chat_responsability():
    CONTACT_ID = request.args.get('CONTACT_ID')
    TRANSFER_ID = request.args.get('TRANSFER_ID')

    if not CONTACT_ID or not TRANSFER_ID:
        return jsonify({'error': 'CONTACT_ID and TRANSFER_ID must be provided in the URL parameters'}), 400

    TRANSFER_ID = extrair_numero(TRANSFER_ID)

    base_url = f'https://marketingsolucoes.bitrix24.com.br/rest/35002/{CODIGO_BITRIX}'
    url = f'{base_url}/imopenlines.crm.chat.getLastId?CRM.ENTITY_TYPE=CONTACT&CRM_ENTITY={CONTACT_ID}'
    
    response = requests.post(url)
    time.sleep(2)
    
    if response.status_code == 200:
        datajson = response.json()
        id_chat = datajson['result']
        
        url2 = f'{base_url}/imopenlines.operator.transfer?CHAT_ID={id_chat}&TRANSFER_ID={TRANSFER_ID}'
        response2 = requests.post(url2)
        
        if response2.status_code == 200:
            return "New responsible approved"
        else:
            return f"No responsible approved: {response2.text}" 
    else:
        return f"Failed to get chat ID: {response.text}"

@app.route('/')
def index():
    return "Hello, this is the application!"

if __name__ == '__main__':
    app.run(port=8008, host='0.0.0.0')
