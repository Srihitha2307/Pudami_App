import serial

def get_reading():
    try:
        # Change 'COM3' to your USB port
        ser = serial.Serial('COM3', 9600, timeout=1) 
        line = ser.readline().decode('utf-8').strip()
        items = dict(item.split(":") for item in line.split(","))
        return {k: float(v) for k, v in items.items()}
    except:
        # Failsafe simulation data
        return {"vol": 48.0, "ph": 6.5, "n": 25.0, "sun": 820.0}
