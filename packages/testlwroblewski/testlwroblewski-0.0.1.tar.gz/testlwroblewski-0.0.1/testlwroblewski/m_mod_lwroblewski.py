import numpy

def name(first, last):
    """Returns full data of parameters"""
    full = first + " " + last
    full = full.lower().title().strip()
    return "Witaj: " + full

def get_numpy_arr(lst):
    """Returns array of numpy package"""
    return numpy.array(lst)

