import random
import string

def key_generator(length=5, upper=True, lower=False, digit=False):
    choices = ''
    if upper:
        choices += string.ascii_uppercase
    if lower:
        choices += string.ascii_lowercase
    if digit:
        choices += string.digits
    key = ''.join(random.SystemRandom().choice(choices) for _ in range(length))
    return key

for i in range(400):
    print(key_generator())

