import numpy


def introduce(name, surname):
    """Return full data of parameters"""

    full = name + " " + surname
    full =full.lower().title().strip()
    return f"Witaj {full}"


def get_numpy_arr(first):
    return numpy.arry(first)



print(introduce("jakub", "jasinski"))
print(introduce("JAkub", "jasiNski "))
print(introduce("    jakub", "jasinski "))

