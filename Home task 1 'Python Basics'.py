import random
# Creatintg a list with 1000 random numbers in range 0 to 1000.
random_num_list = [random.randint(0, 1000) for i in range(100)]

# Defining a function which performs sort operation. 
# Based on realpython.com/sorting-algorithms-python.
def sorting(list):
    # Loop from the second element of the list until the last element.
    for item in range(1, len(list)):
        # This is the element we want to position in its correct place.
        key_item = list[item]
        # Initialize the variable that will be used to find the correct position of the element referenced by `key_item`.
        x = item - 1
        # Run through the list of items (the left portion of the list) and find the correct position of the element referenced by `key_item`. 
        # Do this only if `key_item` is smaller than its adjacent values.
        while x >= 0 and list[x] > key_item:
            # Shift the value one position to the left and reposition X to point to the next element (from right to left).
            list[x + 1] = list[x]
            x -= 1
        # When shifting the elements is finished, `key_item` is placed in its correct location
        list[x + 1] = key_item
    return list
    
# Sorting executed.
random_num_list = sorting(random_num_list)

# Defining a function which performs print out an AVG for odd and even numbers from provided list.
def print_avg_for_even_and_odd(list):
    # Initialize the variables that will be used to find AVG.
    odd_list = []
    even_list = []
    # Loop to fill out odd and even variables that will be used to find AVG.
    for item in list:
        # Excluding zeros, since they are not even and are not odd.
        if item != 0:
            # Parity check. 
            if item % 2 == 0:
                # Filling even_list
                even_list.append(item)
            # If number isn't 0 and isn't even then it is odd.
            else:
                # Filling odd_list
                odd_list.append(item)
    # try/except to avoid dividing by 0 error if len(odd_or_even_list) = 0.
    try:
        print('Average odd number = ' + str( (sum(odd_list) / len(odd_list))))
    except:
        print('Error in AVG odd calculation')
    try:
        print('Average even number = ' + str( (sum(even_list) / len(even_list))))
    except:
        print('Error in AVG even calculation')

print_avg_for_even_and_odd(random_num_list);

