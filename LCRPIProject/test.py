from hx711 import HX711
import time

hx = HX711(29, 31)

hx.set_reading_format("MSB", "MSB")

hx.set_reference_unit(92)

hx.reset()

hx.tare()
while True:
    try:
        val = max(0, int(hx.get_weight(5)))
        print((val/1000)*9.807)
        hx.power_down()
        hx.power_up()
        time.sleep(1)
    except:
            print("error")
