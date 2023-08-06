import numpy


def name(first, last):
    full = first + " " + last
    full = full.lower().title().strip()
    """najpierw robię lower ,a później dodaje tittle - aby pierwsze litery były duze w pierwszych wyrazach, 
    stripe usuwa białe znaki na początku oraz na końcu"""
    return "Witaj: " + full


def get_numpy_arr(lst):
    """Returns array of numpy package"""

    return numpy.array(lst)

a = [1, 2, 3, 4]
print(get_numpy_arr(a))

print(name("Kamila", "czajKOWska"))
print(name("kamila", "CzAjKOWska"))
print(name("      Kamila", "CzajKOWska   "))

