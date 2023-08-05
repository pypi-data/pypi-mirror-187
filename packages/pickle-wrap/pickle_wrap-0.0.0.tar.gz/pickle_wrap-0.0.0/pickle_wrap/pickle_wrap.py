import pickle
import os
from time import time

def getVariableName(variable, globalVariables):
    # from: https://stackoverflow.com/questions/18425225/getting-the-name-of-a-variable-as-a-string
    """ Get Variable Name as String by comparing its ID to globals() Variables' IDs
        args:
            variable(var): Variable to find name for (Obviously this variable has to exist)
        kwargs:
            globalVariables(dict): Copy of the globals() dict (Adding to Kwargs allows this function to work properly when imported from another .py)
    """
    for globalVariable in globalVariables:
        if id(variable) == id(globalVariables[globalVariable]): # If our Variable's ID matches this Global Variable's ID...
            return globalVariable # Return its name from the Globals() dict

def pickle_wrap(filepath, callback, args=None, kwargs=None, easy_override=False, verbose=0):
    '''
    :param filepath: File to which the callback output should be loaded (if already created)
                     or where the callback output should be saved 
    :param callback: Function to be pickle_wrapped
    :param args: Arguments passed to function (often not necessary)
    :param kwargs: Kwargs passed to the function (often not necessary)
    :param easy_override: If true, then the callback will be performed and the previous .pkl
                          save will be overwritten (if it exists)
    :param verbose: If true, then some additional details will be printed (the name of the callback,
                    and the time needed to perform the function or load the .pkl)
    :return: Returns the output of the callback or the output saved in filepath
    '''
    if verbose:
        print('filepath:', filepath)
        print('Function:', getVariableName(callback, globalVariables=globals().copy()))
    if os.path.isfile(filepath) and not easy_override:
        if verbose: print('Loading...')
        start = time()
        with open(filepath, "rb") as file:
            pk = pickle.load(file)
            if verbose: print('Load time:', time()-start)
            return pk
    else:
        if verbose: print('Callback:', getVariableName(callback, globalVariables=globals().copy()))
        start = time()
        if args:
            output = callback(*args)
        elif kwargs:
            output = callback(**kwargs)
        else:
            output = callback()
        if verbose:
            print('Function time:', time()-start)
            print('Dumping to file name:', filepath)
        start = time()
        with open(filepath, "wb") as new_file:
            pickle.dump(output, new_file)
        if verbose: print('Dump time:', time()-start)
        return output