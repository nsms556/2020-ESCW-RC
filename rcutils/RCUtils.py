def waveTimeToDis(time) :
    return time / 58.0

def steerValueToSig(value) :
    if value >= 117 and value <= 123 :
        signal = 7.7
    else :
        signal = round((float(200 - value) / 10), 1)
        if signal <= 5 :
            signal = 5
        elif signal >= 10.5 :
            signal = 10.5

    return signal

class QuitException(Exception) :
    pass

class ModeException(Exception) :
    pass