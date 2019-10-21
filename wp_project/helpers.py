import random
import string


def get_random_string(n=15):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=n))
