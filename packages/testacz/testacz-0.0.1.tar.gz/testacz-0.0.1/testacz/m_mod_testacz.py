# def name(firstname, lastname):
#     return f"{firstname.title()} {lastname.title()}"
import numpy

def get_numpy_arr(lst):
    """Returns list of array of numpy"""
    return numpy.array(lst)


a = [1, 2, 3, 4]
print(get_numpy_arr(a))




def name(firstname, lastname):
    full = "Witaj: " + firstname + " " + lastname
    full = full.lower().title()
    return "Witaj: " + full

