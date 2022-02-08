import string
import random

def random_dict_list_creation():
    # Initionalithation random list of dictionaries (2 - 10 dictionaries; 1 - 26 keys as ascii_lowercase, values as 0 -100)
    dictionaries_list = []
    for numder in range(0, random.randint(2, 10)):
        n_dict = {}
        key_list = random.sample(string.ascii_lowercase, random.randint(1, 26))
        for n_key in key_list:
            n_dict[n_key] = random.randint(0, 100)
        dictionaries_list.append(n_dict)
    return dictionaries_list
    #print(dictionaries_list)   # dictionaries_list test.

def dict_list_concatenation(dictionaries_list):
    # Initialization a dictionary showing the quantity for each key.
    matrix = {}
    for dict in dictionaries_list:
        for key in dict.keys():
            if key not in matrix.keys():
                matrix[key] = 1
            else:
                matrix[key] += 1
    #print(matrix)  # matrix test

    # Initialization a dictionary filled with MAX value for each key.
    result = {}
    for dict in dictionaries_list:
        for key in dict.keys():
            if matrix[key] == 1:
                result[key] = dict[key]
            else:
                if key not in result.keys():
                    result[key] = dict[key]
                else:
                    if result[key] < dict[key]:
                        result[key] = dict[key]
    #print(result)  # result (no index) test.

    # Indexing non-unique keys
    for id, dict in enumerate(dictionaries_list):
        for key in dict.keys():
            if matrix[key] != 1:
                if key in result.keys():
                    if result[key] == dict[key]:
                        result.pop(key)
                        result[str(key + '_' + str(id + 1))] = dict[key]
    return result

dictionaries_list = random_dict_list_creation()
#print(dictionaries_list) #dictionaries_list creation test.
print(dict_list_concatenation(dictionaries_list));
