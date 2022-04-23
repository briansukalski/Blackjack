def add_dictionaries(dict_1, dict_2, dict_2_factor):
    #Checks that dictionaries have identical keys
    if len(dict_1.keys()) != len(dict_2.keys()):
        print("Dictionary keys do not match; they do not have the same number of keys")
        return
    for key in dict_1.keys():
        if key not in dict_2.keys():
            print(f"Dictionary keys do not match: key {key} not found in dictionary 2")
            return
    
    print ("Match!")
    return

score_probabilities = {17: 0, 18: 0, 19: 0, 20: 0, 21: 0, 22: 0}

score_probabilites_2 = {17: 0, 18: 0, 19: 0, 20: 0, 21: 0, 22: 0}

add_dictionaries(score_probabilities, score_probabilites_2, 1)