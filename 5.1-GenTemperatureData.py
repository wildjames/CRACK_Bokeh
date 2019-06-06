import numpy as np
import time
import datetime
import os

temperature_file = open('data/TemperatureData.txt', 'a', os.O_NONBLOCK)

while True:
    t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    temp = 26. + (np.random.randn(1)[0] * 5.)
    print("At {}, the temperature is {}".format(t, temp))

    temperature_file.write("{}, {}\n".format(t, temp))
    temperature_file.flush()
    
    time.sleep(0.5)