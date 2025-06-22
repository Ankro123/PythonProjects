from threading import Thread
from argparse import ArgumentParser
import msvcrt
import time

def get_args():
    parser = ArgumentParser()
    parser.add_mutually_exclusive_group()
    parser.add_argument('--mode', choices=['timer', 'stopwatch'], required=True, help="Choose between Timer and Stopwatch")
    parser.add_argument('-m', '--minutes', type=int, default=0, help="(if Timer) Minutes (Default:%(default)s)")
    parser.add_argument('-s', '--seconds', type=int, default=0, help="(if Timer) Seconds (Default:%(default)s)")
    args = parser.parse_args()
    return args

class timer(Thread):
    def __init__(self, minutes:int, seconds:int):
        super().__init__()
        self.minutes = minutes
        self.seconds = seconds
        self.stop_thread = False    
        
    def stop(self):
        self.stop_thread = True
    
    def run(self):
        min = self.minutes
        sec = self.seconds
        for min in range(min, -1, -1):
            for sec in range(sec, -1, -1):
                if(self.stop_thread == True):
                    break
                print(f'\r{min:02d}:{sec:02d}', end='')
                time.sleep(0.4)
            if(self.stop_thread == True):
                break
            sec = 59

class stopwtach(Thread):
    def __init__(self):
        self.stop_time = False
        super().__init__()
    
    def stop(self):
        self.stop_time = True
    
    def run(self):
        min = 0
        sec = 0
        while True:
            for sec in range(60):
                if(self.stop_time == True):
                    break
                print(f'\r{min:02d}:{sec:02d}', end='')
                time.sleep(0.4)
            if(self.stop_time == True):
                break
            min += 1

if __name__ == "__main__":
    args = get_args()
    t1:Thread
    if(args.mode == 'timer'):
        minutes = args.minutes
        seconds = args.seconds
        t1 = timer(minutes, seconds)
        
    elif(args.mode == 'stopwatch'):
        t1 = stopwtach()
        
    print("Press 'x' to stop")
    t1.start()
    
    while(True):
        if msvcrt.kbhit():
            key = msvcrt.getch()
            if key == b'x':
                t1.stop()
                break