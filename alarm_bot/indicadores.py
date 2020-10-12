
def bollinger(df, mean, std):
    print(mean, std)
    #df['Open Time'] = pd.to_datetime(df['Open Time'], unit='ms')
    df['Mean'] = df['Close'].rolling(mean).mean()
    df['Upper'] = df['Close'].rolling(mean).mean() + std*(df['Close'].rolling(mean).std())
    df['Lower'] = df['Close'].rolling(mean).mean() - std*(df['Close'].rolling(mean).std())
    #df[['Close','Mean','Upper','Lower']].plot(figsize=(16,6))
    if df['Close'].iloc[-1] > df['Upper'].iloc[-1]:
        return ('BTC Cruce Bollinger banda superior, precio: $' + str(df['Close'].iloc[-1]))
    if df['Close'].iloc[-1] < df['Lower'].iloc[-1]:
        return ('BTC Cruce Bollinger banda inferior, precio: $' + str(df['Close'].iloc[-1]))
    return ''

def ma(df, mean, direction):  
    #df['Open Time'] = pd.to_datetime(df['Open Time'], unit='ms')
    df['Mean'] = df['Close'].rolling(mean).mean()
    #df[['Close','Mean']].plot(figsize=(16,6))
    if direction == 'up' and df['Close'].iloc[-1] > df['Mean'].iloc[-1]:
        return ('BTC Cruce MA hacia arriba, precio: $' + str(df['Close'].iloc[-1]))
    elif direction == 'down' and df['Close'].iloc[-1] < df['Mean'].iloc[-1]:
        return ('BTC Cruce MA hacia abajo, precio: $' + str(df['Close'].iloc[-1]))
    return ''