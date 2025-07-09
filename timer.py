import time
from argparse import ArgumentParser

def get_args():
    parser = ArgumentParser()
    parser.add_argument('-m', '--minutes', type=int, default=0, help="Minutes (Default:%(default)s)")
    parser.add_argument('-s', '--seconds', type=int, default=0, help="Seconds (Default:%(default)s)")
    args = parser.parse_args()
    return args



if __name__ == "__main__":
    args = get_args()
    minutes = args.minutes
    seconds = args.seconds

    for min in range(minutes, -1, -1):
        for sec in range(seconds, -1, -1):
            print(f'\r{min:02d}:{sec:02d}', end='')
            time.sleep(0.4)
        seconds = 59

