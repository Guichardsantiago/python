import schedule
import time
import telegram_bot
import indicadores
import binance_api
import iol_api
from datetime import datetime, timedelta

msg_id = ''
api_key = ''
event = 0
def setear_parametros(params, chat_id):
    global event
    length = len(params)
    btc = 'BTCUSDT'
    if length > 4 and params[0] == 'Alarm':
        if params[1] == btc:
            if params[2] == 'ma':
                #alarm BTCUSDT ma 20 up
                telegram_bot.enviar_mensaje('Se seteo alarma para ' + params[1] + ' trigger: ' + params[2], chat_id)
                def fnma():
                    df = binance_api.precio_btc(params[1], '1m', '50')
                    rta = indicadores.ma(df, int(params[3]), params[4])
                    telegram_bot.enviar_mensaje(rta, chat_id)
                if event != 0:
                    schedule.cancel(event)
                event = schedule.every(10).seconds.do(fnma)
                while True:
                   schedule.run_pending()
                   time.sleep(1)
            elif params[2] == 'bollinger':
                #alarm BTCUSDT bollinger 20 3
                telegram_bot.enviar_mensaje('Se seteo alarma para ' + params[1] + ' trigger: ' + params[2], chat_id)
                def fnbol():
                    df = binance_api.precio_btc(params[1], '1m', '50')
                    print(params[3]), int(params[4])
                    rta = indicadores.bollinger(df, int(params[3]), int(params[4]))
                    telegram_bot.enviar_mensaje(rta, chat_id)                              
                if event != 0:
                    schedule.cancel_job(event)
                event = schedule.every(10).seconds.do(fnbol)
        elif ':' in params[1]:
            mkt_ticket = str.split(params[1],':')
            market = mkt_ticket[0]
            ticket = mkt_ticket[1]
            global api_key
            api_key = iol_api.get_token()
            def get_api_key():
                global api_key
                api_key = iol_api.get_token()
            schedule.every(14).minutes.do(get_api_key)
            if params[2] == 'ma':
                #alarm nyse:ggal ma 20 up
                telegram_bot.enviar_mensaje('Se seteo alarma para ' + params[1] + ' trigger: ' + params[2], chat_id)                    
                def fnma():
                    global api_key
                    start_date = datetime.strftime(datetime.now(), '%Y-%m-%d')
                    end_date = datetime.strftime(datetime.now() + timedelta(1), '%Y-%m-%d')
                    df = iol_api.get_historico(ticket, market, start_date, end_date, '1T', api_key)
                    rta = indicadores.ma(df, int(params[3]), params[4])
                    if rta != '':
                        telegram_bot.enviar_mensaje(rta, chat_id)
                if event != 0:
                    schedule.cancel_job(event)
                event = schedule.every(10).seconds.do(fnma)
            elif params[2] == 'bollinger':
                #alarm BTCUSDT bollinger 20 3
                def fnbol():
                    global api_key
                    start_date = datetime.strftime(datetime.now(), '%Y-%m-%d')
                    end_date = datetime.strftime(datetime.now() + timedelta(1), '%Y-%m-%d')
                    df = iol_api.get_historico(ticket, market, start_date, end_date, '1T', api_key)
                    rta = indicadores.bollinger(df, int(params[3]), int(params[4]))
                    if rta != '':   
                        telegram_bot.enviar_mensaje(rta, chat_id)                            
                #if event != 0:
                #    schedule.cancel_job(event)
                event = schedule.every(10).seconds.do(fnbol)
                telegram_bot.enviar_mensaje(str(event) + ' Se seteo alarma para ' + params[1] + ' trigger: ' + params[2], chat_id)

    elif params[0] == 'Stop' :
        if event != 0:
            schedule.cancel_job(event)
            telegram_bot.enviar_mensaje('alarma cancelada', chat_id)                              

    elif params[0] == 'Jobs':
            telegram_bot.enviar_mensaje(str(schedule.jobs), chat_id)                              
    else:
        telegram_bot.enviar_mensaje('mensaje invalido', chat_id)                              

            
def ejecutar_ciclo():
    global msg_id
    msg = telegram_bot.leer_mensaje(msg_id)
    if msg['chat_id'] == 993892776:
        msg_id = msg['msg_id']
        if msg['texto'] != None:
            setear_parametros(str.split(msg['texto']), msg['chat_id'])

#telegram_bot.leer_mensaje('')
schedule.every(10).seconds.do(ejecutar_ciclo)
while True:
   schedule.run_pending()
   time.sleep(1)