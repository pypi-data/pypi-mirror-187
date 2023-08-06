import numpy


def name(first, last):
    """Returns full date of parameters"""
    full = first + " " + last
    full = full.lower().title().strip()
    return "Witaj: " + full


def get_numpy_arr(lst):
    """Returns array of numpy package"""
    return numpy.array(lst)


a = [1, 2, 3, 4]
print(get_numpy_arr(a))
