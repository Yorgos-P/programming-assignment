#!/usr/bin/env python3
"""Analyse a given dataset of sick people and their contacts. Identify
characteristics related to disease spreading as set out in the coursework
brief.
Student number: 20122963
"""

import sys
import os.path
from format_list import format_list

def file_exists(file_name):

    return os.path.isfile(str(file_name))


def parse_file(file_name):
    #In each line of the input file I use the first name to be the key and all names to the right as values
    #I do this for each line and each time I add it to the empty dictionary called infect_dict using the 'update' command
    
    infect_dict = {}
    data_set = open(str(file_name), "r")
    line = str(file_name)
    while line != "":
        line = data_set.readline().rstrip()
        infect_dict.update({line.split(',')[0]: sorted(line.split(',')[1:])})
    data_set.close()
    infect_dict.pop('', None)
    #The above line is simply a precaution as sometimes one extra line on the file which is empty might be added. The above removes it from dictionary.
    return infect_dict


def dic_values(contacts_dic):

    """Return all people who have been contacted by a zombie.

    Args:
        contacts_dic (dic): each entry is a sick person's name and their list
        of contacts.

    Returns:
        list: all names (repetitions included) in all values associated 
        with every key of the input dictionary.
    """
    
    dic_values = []
    for sublist in list(contacts_dic.values()):
        for element in sublist:
            dic_values.append(element)
    return dic_values

def find_patients_zero(contacts_dic):

# MAIN IDEA: The people who do not appear in any sick person's contacts have to be in the keys of the dictionary, hence it is sufficient if each key is not in all the values.
    patients_zero = []
    dict_values = dic_values(contacts_dic)

    for key in range(len(contacts_dic)):
        if list(contacts_dic.keys())[key] not in dict_values:
            patients_zero.append(list(contacts_dic.keys())[key])
    return sorted(patients_zero)
    


def find_potential_zombies(contacts_dic):

    potential_zombies = []
    dict_values = dic_values(contacts_dic)
    for element in dict_values:
        if element not in list(contacts_dic.keys()):
            potential_zombies.append(element)
    return sorted(list(set(potential_zombies)))


def find_not_zombie_nor_zero(contacts_dic, patients_zero_list, zombie_list):

#combined_dic is the list containing all names in the inputed dataset
#combined_zombie is the list containing patient zeroe(s) and potential zombies
#Finally, the list returned is all the names (combined_dic) minus the names in combined_zombie
    
    dict_values = dic_values(contacts_dic)
    combined_zombie = list(set(zombie_list + patients_zero_list))
    combined_dic = list(set(list(contacts_dic.keys()) + dict_values))
    return sorted([x for x in combined_dic if x not in combined_zombie])

    


def find_most_viral(contacts_dic):

    keys = list(contacts_dic.keys())
    maximum = max([len(x) for x in list(contacts_dic.values())])
    return sorted([x for x in keys if len(contacts_dic[str(x)]) == maximum])



def find_most_contacted(contacts_dic):

    values = dic_values(contacts_dic)
    dict_values = list(set(dic_values(contacts_dic)))

#Retrieve the maximum count
#Finally return the names in dic_values that appear 'maximum' times

    maximum = max([dict_values.count(dict_values[x]) for x in range(dict_values)])
    return sorted(list(set([x for x in values if values.count(x) == maximum])))
    



def auxiliary_recursion_func(contacts_dic, zombie_list, dict_names):
    
    """Return the contact or contacts who appear in the most sick persons'
    contact list.

    Args:
        contacts_dic (dic): each entry is a sick person's name and their list
        of contacts.
        zombie_list (list): list of potential zombies
        dict_names (dic): The keys are all names in a data set and the values empty lists

    Returns:
        dictionary: contains the names of everyone in the dataset as keys and
        a list as value containing the number of people contacted including their height.
    """

    #Recursive solution to SECTION 10
    if len(contacts_dic) == 0:
        for i in dict_names:
            dict_names[str(i)] = max(dict_names[str(i)], default = 0)
        return dict_names
        
    else:
        for i in zombie_list:
            for j in contacts_dic:
                if i in contacts_dic[str(j)]:
                    dict_names[str(j)].append(max(dict_names[str(i)], default = 0) + 1)
        for i in contacts_dic:
            for j in zombie_list:
                if j in contacts_dic[str(i)]:
                    del(contacts_dic[str(i)][contacts_dic[str(i)].index(str(j))])
        contacts = {key: value for key, value in contacts_dic.items() if value}
        zombie_list = find_potential_zombies(contacts)
        return auxiliary_recursion_func(contacts, zombie_list, dict_names)


def find_maximum_distance_from_zombie(contacts_dic, zombie_list):

    #Initialize dictionary with all names of a dataset as keys
    #this serves to catalogue the data used in the recursion

    values = set(list(set(dic_values(contacts_dic))))
    keys = set(list(contacts_dic.keys()))
    dict_names_list = list(values) + list(keys)
    dict_names = {}
    for i in range(len(dict_names_list)):
        dict_names.update({dict_names_list[i]: []})
    
    return auxiliary_recursion_func(contacts_dic, zombie_list, dict_names)








    



def main():
    """Main logic for the program.
    """
    filename = ""
    # Get the file name from the command line or ask the user for a file name
    args = sys.argv[1:]
    if len(args) == 0:
        filename = input("Please enter the name of the file: ")
    elif len(args) == 1:
        filename = args[0]
    else:
        print("""\n\nUsage\n\tTo run the program type:
        \tpython contact.py infile
        where infile is the name of the file containing the data.\n""")
        sys.exit()

    #This produces a list of all the names given a dataset (repetitions included)

    # Section 2. Check that the file exists
    if not file_exists(filename):
        print("File does not exist, ending program.")
        sys.exit()

    # Section 3. Create contacts dictionary from the file
    contacts_dic = parse_file(filename)

    


    # Section 4. Print contact records
    # Add your code here.
    for key in range(len(contacts_dic)):
        keys = list(contacts_dic.keys())
        contacts_names =  format_list(contacts_dic[keys[key]])
        print(f"{keys[key]} had contact with {contacts_names}")

    # Section 5. Identify the possible patients zero. Patient(s) zero are those
    #    people who do not appear in another's contact list.
    # Complete function find_patients_zero() and add code here to print the
    # output as specified in the brief.
    patients_zero_list = find_patients_zero(contacts_dic)
    print("Patient Zero(s): " + format_list(patients_zero_list))

    # Section 6. Find potential zombies. Potential zombies are those people who
    # have been in contact with a sick person but have not yet been identified
    # as sick.
    # Complete function find_potential_zombies() and add code here to print the
    # output as specified in the brief.
    zombie_list = find_potential_zombies(contacts_dic)
    print(f"Potential Zombies: {format_list(zombie_list)}")

    # Section 7. Find people who are neither patient zero(s) nor potential
    # zombies.
    # Complete function find_not_zombie_nor_zero() and add code here to print
    # the output as specified in the brief.
    not_zombie_nor_zero = find_not_zombie_nor_zero(contacts_dic,
                                    patients_zero_list, zombie_list)
    print(f"Neither Patient Zero of Potential Zombie: {format_list(not_zombie_nor_zero)}")


    # Section 8. Find the most viral people.
    # Complete function find_most_viral() and add code here to print the
    # output as specified in the brief.
    most_viral_list = find_most_viral(contacts_dic)
    print(f"Most Viral People: {format_list(most_viral_list)}")


    # Section 9. Find most contacted. The people who appear in the most sick
    # persons' lists.
    # Complete function find_most_contacted() and add code here to print the
    # output as specified in the brief.
    most_contacted = find_most_contacted(contacts_dic)
    print(f"Most Contacted: {format_list(most_contacted)}")



    # Section 10. Maximum Distance from Zombie
    # Complete function find_maximum_distance_from_zombie() and add code here
    # to print the output as specified in the brief.
    heights_dic = find_maximum_distance_from_zombie(contacts_dic, zombie_list)
    for i in range(len(heights_dic)):
        print(f"{list(heights_dic.keys())[i]}: {list(heights_dic.values())[i]}")


    ######
    # Extra functionality - no function headers provided.
    ######
    

if __name__ == "__main__":
    main()


