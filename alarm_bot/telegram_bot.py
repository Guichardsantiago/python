import requests
import json

bot_token = '*'
telegram_url = 'https://api.telegram.org/bot'

def update():
    URL = telegram_url + bot_token + '/'
    #Llamar al metodo getUpdates del bot haciendo una peticion HTTPS (se obtiene una respuesta codificada)
    respuesta = requests.get(URL + "getUpdates")
 
    #Decodificar la respuesta recibida a formato UTF8 (se obtiene un string JSON)
    mensajes_js = respuesta.content.decode("utf8")
 
    #Convertir el string de JSON a un diccionario de Python
    mensajes_diccionario = json.loads(mensajes_js)
    #Devolver este diccionario
    return mensajes_diccionario
 
def leer_mensaje(msg_id):
    #Llamar update() y guardar el diccionario con los mensajes recientes
    mensajes = update()
    #Calcular el indice del ultimo mensaje recibido
    fmensajes = list(filter(lambda msg: msg['message']['chat']['id']==993892776,mensajes['result']))
    print (fmensajes)
    indice = len(fmensajes)-1
    if fmensajes[indice]['message']['message_id'] == msg_id:
        return {'msg_id': msg_id, 'chat_id': 0}
    else:
        msg_id = fmensajes[indice]['message']['message_id']
        #Extraer el texto, nombre de la persona e id del último mensaje recibido
        texto = fmensajes[indice]['message']['text']
        persona = fmensajes[indice]['message']['from']['first_name']
        id_chat = fmensajes[indice]['message']['chat']['id']
 
        #Mostrar esta informacion por pantalla
        print(persona + " (id: " + str(id_chat) + ") ha escrito: " + texto)
        return { 'texto': texto, 'chat_id': id_chat, 'msg_id': msg_id}
    
def enviar_mensaje(msg, chat_id):
    send_text = telegram_url + bot_token + '/sendMessage?chat_id=' + str(chat_id) + '&parse_mode=Markdown&text=' + msg
    response = requests.get(send_text)
    return response.json()