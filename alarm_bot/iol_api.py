import requests
import pandas as pd
#import indicadores
#from datetime import datetime
    
def get_token():
# API Parameters
        URL = 'https://api.invertironline.com/token'
        Host = 'api.invertironline.com'
        ContentType = 'application/x-www-form-urlencoded'
        granttype = 'password'

        data = {
            'Host': Host,
            'username': '*',
            'password': '*',
            'grant_type': granttype
        }
        
        headers = {'Content-Type': ContentType}
        
        r = requests.post(url=URL, data=data, headers=headers)
        
        data = r.json()
        
        if 'error' in data.keys():
            print('Error found: ' + data['error'])
        else:
            return data['access_token']
        
def get_historico(ticket, market, start_date, end_date, time_frame, api_key):
    URL = 'https://api.invertironline.com/api/v2/'+market+'/Titulos/'+ticket+'/Cotizacion/seriehistorica/'+start_date+'/'+end_date+'/sinAjustar?api_key='+api_key
    headers = {'Authorization': 'Bearer ' + api_key}
 
    r = requests.get(url=URL, headers=headers)
    #nparray = np.array(r.json())
    #cols = nparray[0].keys()
    #print(nparray)
    df =  pd.DataFrame.from_records(r.json())
    df.rename(columns={'ultimoPrecio': 'Close'}, inplace=True)
    df["DATE"] = pd.to_datetime(df["fechaHora"])
    df.set_index("DATE", inplace=True)
    df1 = df.resample(time_frame).mean().ffill().loc[(start_date + ' 09:30:00'):(start_date + ' 17:00:00')]
    df2 = df.resample(time_frame).mean().ffill().loc[(end_date + ' 09:30:00'):(end_date + ' 17:00:00')]
    result = pd.concat([df1, df2])
    return result
 
def get_merval(api_key):
    URL = 'https://api.invertironline.com/api/v2/Cotizaciones/Acciones/Merval/argentina?panelCotizacion.instrumento=acciones&panelCotizacion.panel=merval&panelCotizacion.pais=argentina&api_key='+api_key
    headers = {'Authorization': 'Bearer ' + api_key}

    r = requests.get(url=URL, headers=headers)
    #print(r.json())
    #nparray = np.array(r.json())
    #cols = nparray[0].keys()
    #print(nparray)
    df =  pd.DataFrame.from_records(r.json()['titulos'])
    return df

df = get_merval(get_token())
df
#df = get_historico('YPFD', get_token())
#print(df)
#indicadores.bollinger(df, 20, 3)
#print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"))