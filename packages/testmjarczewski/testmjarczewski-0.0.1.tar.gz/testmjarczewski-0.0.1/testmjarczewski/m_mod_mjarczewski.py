import numpy

def name(first, last):
    '''Returns full data of parameters'''
    full = first + ' ' + last
    full = full.lower().title().strip()
    return 'Witaj: ' + full

# print(name('marek', 'jarczewski'))
# print(name('mAREk', 'JarczewsKI'))
# print(name('   mAREk', 'JarczewsKI    '))

def get_numpy_arr(lst):
    '''Returns array of numpy package'''

    return numpy.array(lst)


# a = [1, 2, 3, 4]
# print(get_numpy_arr(a))
