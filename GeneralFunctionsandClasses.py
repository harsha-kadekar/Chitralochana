'''
Name:           GeneralFunctionsandClasses
Description:    This file has all the functions and classes which can be used by all the modules
Developer:      Harsha Kadekar
References:     http://stackoverflow.com/questions/6760685/creating-a-singleton-in-python -> For singleton classes
'''


class SingleTonClassCreator(object):
    '''
    Name: SingleTonClassCreator
    Description: This class is responsible for creation of singleton class. Any class which wants to be a singleton
                 can use this class parent object.
    '''
    _instances = []

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingleTonClassCreator, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

