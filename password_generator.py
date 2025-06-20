import string
import argparse
import pyperclip
import random

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--length', type=int, default=10, help='Length of the password? (Default %(default)s)')
    parser.add_argument('-c', '--count', type=int, default=1, help='Number of passwords (Default %(default)s)')
    parser.add_argument('-u', '--upper', action='store_true', help='Upper case characters?')
    parser.add_argument('-n', '--number', action='store_true', help='Numbers?')
    parser.add_argument('-s', '--symbol', action='store_true', help='Symbols?')
    parser.add_argument('-y', '--copy', action="store_true", help="Copy to clipboard?")
    args = parser.parse_args()
    return args


def add_chars(usable_chars: str, addable_chars: str, password: str):
    usable_chars += addable_chars
    password += addable_chars[random.randrange(0, len(addable_chars))]
    return usable_chars, password

def shuffle_pass(password:str) -> str:
    orig_pass = list(password)
    random.shuffle(orig_pass)
    shuffled_pass = ''.join(orig_pass)
    return shuffled_pass

def generate_password(args) -> str:
    
    usable_chars = ''
    password = ''
    
    usable_chars, password = add_chars(usable_chars, string.ascii_lowercase, password)
    
    if args.upper:
        usable_chars, password = add_chars(usable_chars, string.ascii_uppercase, password)
        
    if args.number:
        usable_chars, password = add_chars(usable_chars, string.digits, password)
        
    if args.symbol:
        usable_chars, password = add_chars(usable_chars, string.punctuation, password)
        
    for i in range(args.length - len(password)):
        password += usable_chars[random.randrange(0, len(usable_chars))]
        
    shuffled_pass = shuffle_pass(password)
    
    return shuffled_pass

if __name__ == "__main__":
    
    args = get_args()
    passwords = []
    
    for i in range(args.count):
        password = generate_password(args)
        passwords.append(password)
    
    passwords = '\n'.join(passwords)
    print(f"{args.count} Password(s) Generated: \n{passwords}")
    
    if(args.copy):
        pyperclip.copy(passwords)
        print("\nCopied to Clipboard!")