import numpy

def name(first, last):
    full = first.capitalize().strip() + " " + last.capitalize().strip()
    return "Hello " + full

def get_numpy_arr(lst):
    """Returns array of numpy package"""
    return numpy.array(lst)

