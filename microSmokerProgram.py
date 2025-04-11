# Smoker air flow and temperature control with micro python
# Author: Joel Reyes   joel.reyeseng@gmail.com

'''
This program will not run without a raspberry pi pico microcontroller.
'''

import machine
from ssd1306 import SSD1306_I2C

try:
    import utime
except:
    import time as utime
    
'''
to do list:
- Get the wireless remote working

'''

# ADC to temperature dictionary
lookup_dict = {'34700': 150, '34800': 151, '34900': 152, '35000': 153, '35100': 154, '35200': 155, '35300': 156, '35400': 157,
               '35500': 158, '35600': 159, '35700': 160, '35800': 161, '35900': 162, '36000': 163, '36100': 164, '36200': 165,
               '36300': 166, '36400': 167, '36500': 168, '36600': 169, '36700': 170, '36800': 171, '36900': 172, '37000': 173,
               '37100': 174, '37200': 175, '37300': 176, '37400': 177, '37500': 178, '37600': 179, '37700': 180, '37800': 181,
               '37900': 182, '38000': 183, '38100': 184, '38200': 185, '38300': 186, '38400': 187, '38500': 188, '38600': 189,
               '38700': 190, '38800': 191, '38900': 192, '39000': 193, '39100': 194, '39200': 195, '39300': 196, '39400': 197,
               '39500': 198, '39600': 199, '39700': 200, '39800': 201, '39900': 202, '40000': 203, '40100': 204, '40200': 205,
               '40300': 206, '40400': 207, '40500': 208, '40600': 209, '40700': 210, '40815': 211, '40930': 212, '41045': 213,
               '41160': 214, '41275': 215, '41390': 216, '41505': 217, '41620': 218, '41735': 219, '41850': 220, '41965': 221,
               '42080': 222, '42195': 223, '42310': 224, '42425': 225, '42540': 226, '42655': 227, '42770': 228, '42885': 229,
               '43000': 230, '43030': 231, '43060': 232, '43090': 233, '43120': 234, '43150': 235, '43180': 236, '43210': 237,
               '43240': 238, '43270': 239, '43300': 240, '43330': 241, '43360': 242, '43390': 243, '43420': 244, '43450': 245,
               '43480': 246, '43510': 247, '43540': 248, '43570': 249, '43600': 250, '43706': 251, '43812': 252, '43918': 253,
               '44024': 254, '44130': 255, '44236': 256, '44342': 257, '44448': 258, '44554': 259, '44660': 260, '44766': 261,
               '44872': 262, '44978': 263, '45084': 264, '45190': 265, '45296': 266, '45402': 267, '45508': 268, '45614': 269,
               '45720': 270, '45826': 271, '45932': 272, '46038': 273, '46144': 274, '46250': 275, '46356': 276, '46462': 277,
               '46568': 278, '46674': 279, '46780': 280, '46886': 281, '46992': 282, '47098': 283, '47204': 284, '47310': 285,
               '47416': 286, '47522': 287, '47628': 288, '47734': 289, '47840': 290, '47946': 291, '48052': 292, '48158': 293,
               '48264': 294, '48370': 295, '48476': 296, '48582': 297, '48688': 298, '48794': 299, '48900': 300, '48956': 301,
               '49012': 302, '49068': 303, '49124': 304, '49180': 305, '49236': 306, '49292': 307, '49348': 308, '49404': 309,
               '49460': 310, '49516': 311, '49572': 312, '49628': 313, '49684': 314, '49740': 315, '49796': 316, '49852': 317,
               '49908': 318, '49964': 319, '50020': 320, '50076': 321, '50132': 322, '50188': 323, '50244': 324, '50300': 325,
               '50356': 326, '50412': 327, '50468': 328, '50524': 329, '50580': 330, '50636': 331, '50692': 332, '50748': 333,
               '50804': 334, '50860': 335, '50916': 336, '50972': 337, '51028': 338, '51084': 339, '51140': 340, '51196': 341,
               '51252': 342, '51308': 343, '51364': 344, '51420': 345, '51476': 346, '51532': 347, '51588': 348, '51644': 349,
               '51700': 350, '51774': 351, '51848': 352, '51922': 353, '51996': 354, '52070': 355, '52144': 356, '52218': 357,
               '52292': 358, '52366': 359, '52440': 360, '52514': 361, '52588': 362, '52662': 363, '52736': 364, '52810': 365,
               '52884': 366, '52958': 367, '53032': 368, '53106': 369, '53180': 370, '53254': 371, '53328': 372, '53402': 373,
               '53476': 374, '53550': 375, '53624': 376, '53698': 377, '53772': 378, '53846': 379, '53920': 380, '53994': 381,
               '54068': 382, '54142': 383, '54216': 384, '54290': 385, '54364': 386, '54438': 387, '54512': 388, '54586': 389,
               '54660': 390, '54734': 391, '54808': 392, '54882': 393, '54956': 394, '55030': 395, '55104': 396, '55178': 397,
               '55252': 398, '55326': 399, '55400': 400}

class Smoker():
    
    profiles = [['ribs',215,221,190],['brisket',223,229,203],
                ['boston',225,231,203],['loaf',250,257,155],
                ['bird',324,330,164],['warm',163,169,180]]
    
    def __init__(self,name,min_tp=215,max_tp=221):
        self.name = name
        self.min_tp = min_tp # Smoker minimum target temperature
        self.max_tp = max_tp # Smoker maximum target temperature
        self.hot_cycles = 0 # Record of concurrent hot cycles
        self.cold_cycles = 0 # Record of concurrent cold cycles
        self.profile_select = 0 # index number of current profile
        self.food_type = 'ribs' # string value from profile for the display
        self.offset = 0 # calibration offset to agree with a 3rd party thermometer
        self.cal_flag = False # Set to True after cal to prevent lid open sleep
        
    def range_up(self):
        '''
        shifts the target range up one degree when a button is pressed
        '''
        self.min_tp += 1
        self.max_tp += 1
        blink_LED(max_LED)
        
    def range_down(self):
        '''
        shifts the target range down one degree when a button is pressed
        '''
        self.min_tp -= 1
        self.max_tp -= 1
        blink_LED(min_LED)

def blink_LED(led):
    led.value(1)
    utime.sleep(.25)
    led.value(0)
    
def all_LED_off():
    led_cold.value(0)
    led_cool.value(0)
    led_perf.value(0)
    led_perf_cool.value(0)
    led_perf_warm.value(0)
    led_hot.value(0)
    led_warm.value(0)
    
def display_text(text1,text2,t1_xPos=2,t2_xPos=7,t3_xPos=2):
    '''
    displays 2 or 3 lines of text on a tiny screen
    '''
    oled.fill(0)
    oled.text(text1, t1_xPos, 2)
    oled.text(text2 + ' ' + 'os:' + str(my_smoker.offset), t2_xPos, 12)
    oled.text('range:' + str(my_smoker.min_tp) + ' - ' + 
              str(my_smoker.max_tp), t3_xPos, 22)
    oled.show()
    
def irq_hand_max(pin):
    '''
    Interupt handling for button that increases the smoker target range.
    '''
    max_adjust.irq(handler=None)
    my_smoker.range_up()
    display_text('t:' + str(smoker_temp),my_smoker.food_type)
    max_adjust.irq(handler=irq_hand_max)

def irq_hand_min(pin):
    '''
    Interupt handling for button that decreases the smoker target range.
    '''
    min_adjust.irq(handler=None)
    my_smoker.range_down()
    display_text('t:' + str(smoker_temp),my_smoker.food_type)
    min_adjust.irq(handler=irq_hand_min)
    
def irq_hand_prof(pin):
    '''
    Interupt handling for button that switches the smoker profile.
    '''
    mode_select.irq(handler=None)
    my_smoker.profile_select += 1
    # this section enables the mode select to loop throught the profiles
    top_range = len(my_smoker.profiles)
    if my_smoker.profile_select in range(0,top_range):
        new_profile = my_smoker.profiles[my_smoker.profile_select]
    else:
        my_smoker.profile_select -= top_range
        new_profile = my_smoker.profiles[my_smoker.profile_select]
    my_smoker.food_type = new_profile[0]        
    my_smoker.min_tp = new_profile[1]
    my_smoker.max_tp = new_profile[2]
    display_text('t:' + str(smoker_temp),my_smoker.food_type)
    utime.sleep(.30)
    mode_select.irq(handler=irq_hand_prof)
    
def irq_calibrate(pin):
    '''
    this function sets an offset value to agree with a
    user chosen input
    '''
    def choose_temp():
        '''
        Provides user input via a potentiometer
        '''
        analog_value = machine.ADC(26)  # physical pin 26, ADC 0
        temp_select = machine.Pin(27, machine.Pin.IN,
                                 machine.Pin.PULL_DOWN) # Physical pin 32
        jump_size = 65500 // len(pos_outcomes)
        choice_list = list(range(0,len(pos_outcomes)*jump_size,jump_size))
        counter = 0
        my_choice = 0
        prev_choice = 0
        while temp_select.value() == 0:
            # if pot val does not change, return false after about 10 secs
            if my_choice == prev_choice:
                counter += 1
                if counter > 100:
                    return False
            else:
                counter = 0
            prev_choice = my_choice
            read_pot = analog_value.read_u16()
            
            my_choice = min(choice_list, key=lambda x:abs(x-read_pot))
            j = choice_list.index(my_choice)
            k = pos_outcomes[j]
            l = lookup_dict[str(k)]
            display_text('T should be:',str(l))
            utime.sleep(.05)
        my_smoker.cal_flag = True
        return l
    
    calibrate.irq(handler=None)
    # Get a fresh ADC reading
    recent_adc_read = read_smoker()
    # Get the current temp
    round_adc_read = adc_round(recent_adc_read)
    current_temp = lookup_dict[str(round_adc_read)]
    # User provides a modified temperature
    new_val = choose_temp()
    if new_val == False:
        display_text('t:' + str(smoker_temp) + ' adc:' +
                     str(recent_adc_read),'exiting cal!')
        utime.sleep(.75)
        calibrate.irq(handler=irq_calibrate)
        return None
    
    my_smoker.offset = (current_temp - new_val)*-1
    display_text('t:' + str(current_temp + my_smoker.offset) + ' adc:'
                 +str(recent_adc_read),'cal complete!')
    utime.sleep(1)
    calibrate.irq(handler=irq_calibrate)
    
def adc_round(adc_read):
    '''
    rounds the ADC reading to the closest dictionary outcome
    '''
    if adc_read < pos_outcomes[0] -100:
        display_text('temp too low','out of scope')
        return pos_outcomes[0]
    elif adc_read > pos_outcomes[-1] +100:
        display_text('temp too high','out of scope')
        return pos_outcomes[-1]
    else:
        i = min(pos_outcomes, key=lambda x:abs(x-adc_read))
        return i

def read_smoker():
    '''
    reads smoker adc and returns value
    '''
    display_text('EVALUATING...','  ')
    counter = 0
    results = []
    while counter < 21:
        reading = analog_value.read_u16()
        results.append(reading)
        utime.sleep(.1)
        counter += 1
    results.sort()
   
    return results[10]
    
def fan_mode(mode_int):
    '''
    This function controls fan-on time depending on the incoming temperature
    '''
    fan_time = 2
    sleep_time = 10
    all_LED_off()
    
    # temp too high, no fan time
    if mode_int == 0:
        my_smoker.hot_cycles += 1
        my_smoker.cold_cycles = 0
        if my_smoker.hot_cycles > 10:
            fan.value(1)
            utime.sleep(fan_time*.5)
            fan.value(0)
            my_smoker.hot_cycles = 0
        elif my_smoker.profile_select == len(my_smoker.profiles)-1 and my_smoker.hot_cycles > 9:
            fan.value(1)
            utime.sleep(fan_time*.5)
            fan.value(0)
            my_smoker.hot_cycles = 0
        led_hot.value(1)
        led_warm.value(1)
        utime.sleep(sleep_time)
    
    # temp too high, no fan time
    elif mode_int == 1:
        my_smoker.hot_cycles += 1
        my_smoker.cold_cycles = 0
        if my_smoker.profile_select == len(my_smoker.profiles)-1 and (my_smoker.hot_cycles > 9):
            fan.value(1)
            utime.sleep(fan_time)
            fan.value(0)
            my_smoker.hot_cycles = 0
        led_warm.value(1)
        utime.sleep(sleep_time)
            
    # temp just right, maintain temp
    elif mode_int == 2:
        my_smoker.hot_cycles = 0
        my_smoker.cold_cycles = 0
        # temper is on the cool edge of optimal
        if smoker_temp < min_temper + 2:
            led_perf_cool.value(1)
            fan_time += 2
            sleep_time -= 5
        # temper is on the hot edge of optimal
        elif smoker_temp > max_temper - 3:
            led_perf_warm.value(1)
            fan_time -= .75
            sleep_time += 2
        led_perf.value(1)
        fan.value(1)
        utime.sleep(fan_time)
        fan.value(0)
        utime.sleep(sleep_time)
            
    # low temp, more fan time
    elif mode_int == 3:
        my_smoker.hot_cycles = 0
        my_smoker.cold_cycles += .5
        led_cool.value(1)
        fan.value(1)
        utime.sleep(fan_time*3)
        fan.value(0)
        utime.sleep(sleep_time/2)
        if my_smoker.cold_cycles > 1:
            fan.value(1)
            utime.sleep(fan_time + my_smoker.cold_cycles)
            fan.value(0)
            
    # very low temp, much more fan time
    elif mode_int == 4:
        my_smoker.hot_cycles = 0
        my_smoker.cold_cycles += .5
        led_cold.value(1)
        led_cool.value(1)
        fan.value(1)
        utime.sleep(fan_time*4)
        fan.value(0)
        utime.sleep(sleep_time/2)
        fan.value(1)
        utime.sleep(fan_time + my_smoker.cold_cycles)
        fan.value(0)

my_smoker = Smoker('my_smoker')

string_list = list(lookup_dict.keys())
pos_outcomes = [int(x) for x in string_list]
pos_outcomes.sort()

# define the gpio for the fan, LEDs, mode, etc.
fan = machine.Pin(11, machine.Pin.OUT)  # Physical pin 15
analog_value = machine.ADC(28)  # physical pin 34, ADC 2
led_hot = machine.Pin(22, machine.Pin.OUT)  # Physical pin 29
led_warm = machine.Pin(21, machine.Pin.OUT)  # Physical pin 27
led_perf_warm = machine.Pin(20, machine.Pin.OUT)  # Physical pin 26
led_perf = machine.Pin(19, machine.Pin.OUT)  # Physical pin 25
led_perf_cool = machine.Pin(18, machine.Pin.OUT)  # Physical pin 24
led_cool = machine.Pin(17, machine.Pin.OUT)  # Physical pin 22
led_cold = machine.Pin(16, machine.Pin.OUT)  # Physical pin 21
max_adjust = machine.Pin(12, machine.Pin.IN, machine.Pin.PULL_DOWN) # Physical pin 16
max_adjust.irq(trigger=machine.Pin.IRQ_RISING, handler=irq_hand_max)
min_adjust = machine.Pin(13, machine.Pin.IN, machine.Pin.PULL_DOWN) # Physical pin 17
min_adjust.irq(trigger=machine.Pin.IRQ_RISING, handler=irq_hand_min)
max_LED = machine.Pin(14, machine.Pin.OUT)  # Physical pin 19
min_LED = machine.Pin(15, machine.Pin.OUT)  # Physical pin 20
mode_select = machine.Pin(8, machine.Pin.IN, machine.Pin.PULL_DOWN) # Physical pin 11
mode_select.irq(trigger=machine.Pin.IRQ_RISING, handler=irq_hand_prof)
calibrate = machine.Pin(27, machine.Pin.IN, machine.Pin.PULL_DOWN) # Physical pin 32
calibrate.irq(trigger=machine.Pin.IRQ_RISING, handler=irq_calibrate)
# Set up the LCD screen:
w = 128
h = 32
i2c = machine.I2C(0, scl=machine.Pin(5), sda=machine.Pin(4), freq=200000)
addr = i2c.scan()[0]
oled = SSD1306_I2C(w, h, i2c, addr)

prev_temp = 0
smoker_temp = 0
fan.value(0)

while True:
    # ADC reading gets rounded, converted to a temp
    prev_temp = smoker_temp
    recent_adc_read = read_smoker()
    round_adc_read = adc_round(recent_adc_read)
    smoker_temp = lookup_dict[str(round_adc_read)]
    smoker_temp += my_smoker.offset
    display_text('t:' + str(smoker_temp) + ' adc:' +
                 str(recent_adc_read),my_smoker.food_type)

    # was the lid opened? If so, sleep x minutes
    if (smoker_temp < prev_temp -20) and my_smoker.cal_flag == False:
        all_LED_off()
        my_smoker.cal_flag = True # prevents x2 sleeping cycles
        if my_smoker.food_type == 'ribs':
            display_text('Lid was Open!','2 min pause...')
            utime.sleep(50)
            display_text('resuming soon...',my_smoker.food_type)
            utime.sleep(10)
            display_text('Lid was Open!','1 min pause...')
            utime.sleep(50)
            display_text('resuming soon...',my_smoker.food_type)
            utime.sleep(10)
            continue
        else:
            display_text('Lid was Open!','30sec pause...')
            utime.sleep(20)
            display_text('resuming soon...',my_smoker.food_type)
            utime.sleep(10)
            continue

    my_smoker.cal_flag = False

    min_temper = my_smoker.min_tp
    max_temper = my_smoker.max_tp
    
    # Temp is just right workflow
    if smoker_temp in range(min_temper,max_temper+1):
        fan_mode(2)
    # Temp is too high workflow
    elif smoker_temp > max_temper:
        if smoker_temp <= max_temper + 5:
            # make this a mini temper down
            fan_mode(1)
        else:
            # make this a larger temper down
            fan_mode(0)
    # Temp is too low workflow
    else:
        if smoker_temp >= min_temper -2:
            # make this a mini temper up
            fan_mode(3)
        else:
            # make this a larger temper up
            fan_mode(4)
