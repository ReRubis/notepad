import random
import string


def get_random_string():
    the_random_string = ''
    length_of_string = random.randrange(5, 15)
    for i in range(1, length_of_string):
        number_or_letter = random.choice([1, 2])
        if number_or_letter == 1:
            the_random_string += (random.choice(string.ascii_letters))
        else:
            the_random_string += (random.choice(string.digits))
    return the_random_string


print(get_random_string())
