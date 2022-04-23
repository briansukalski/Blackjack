def add_dictionaries(dict_1, dict_2, dict_2_factor):
    #Checks that dictionaries have identical keys
    if len(dict_1.keys()) != len(dict_2.keys()):
        print("Dictionary keys do not match; they do not have the same number of keys")
        return
    for key in dict_1.keys():
        if key not in dict_2.keys():
            print(f"Dictionary keys do not match: key {key} not found in dictionary 2")
            return
    
    #Checks that all values in each dictionary are numeric
    for val in dict_1.values():
        if not isinstance(val, (int, float)):
            print(f"Value {val} is not a number")
            return
    for val in dict_2.values():
        if not isinstance(val, (int, float)):
            print(f"Value {val} is not a number")
            return
    
    #If values match, adds values from dict_2 into dict_1, modified by the provided factor
    for key in dict_1.keys():
        dict_1[key] += dict_2[key] * dict_2_factor
    
    return