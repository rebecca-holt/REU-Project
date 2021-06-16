#Rebecca Holt
#REU simple model 2/28/21

#import functions to calc integral & produce random #s
import numpy as np
import sympy as sy
import matplotlib.pyplot as plt

import scipy.integrate as integrate
from scipy.integrate import quad
from scipy.integrate import dblquad
from scipy.integrate import nquad

import random

#define global variables
HOUSES = 100
MAX_KWH = 2800
PRICE = .5
BUDGET = 5

#define main function
def main():
    house_eng_list, total_eng, total_eng_list, power_eqn_list = get_power()
    print(house_eng_list)
    print("\n")
    print("\n")
    print(power_eqn_list)


#function to calculate total power
def get_power():
    #initialize total energy (this can be user defined if need be)
    total_eng = 0

    #initialize list of total energy list 
    total_eng_list = []

    #initialize list of eqn for power of # of houses
    power_eqn_list = []

    #initialize list to add energy of each house to
    house_eng_list = []

    #initialize list of budget of # of houses
    budget_list = []

    #initialize list of index of removed equations
    removed_index_list = []

    #initialize list of removed equations
    removed_eqn_list = []

    #populate a list with budget of 100 houses
    for i in range (0, HOUSES + 1):
        budget_list.append(BUDGET)

    #populate a list with initial energy output of 100 houses
    for i in range (0, HOUSES + 1):
        house_eng_list.append(0)

 #populate a list with randomly generated power curve equation of 100 houses
    thing = []
    for i in range(0, HOUSES + 1):
        #get random factor for each house to scale power curve
        r = random.randint(1, 10)
        result = lambda x: (-((x/3)-2)**2 + 4)

        #add power curve equation to list
        power_eqn_list.append(result)
    

    for i in range(0, HOUSES + 1):
        #get equation of house from power_eqn_list
        pwr_eqn = power_eqn_list[i]

        #calculate area up until given time of specific house
        energy = quad(pwr_eqn, 0, 4)

        #add power of that house to house_pwr_list
        house_eng_list[i] = energy[0]

        #add houses power to total energy
        total_eng += energy[0]

        #add total energy to total_eng_list
        total_eng_list.append(total_eng)

    #return total energy
    return house_eng_list, total_eng, total_eng_list, power_eqn_list, 

        
#call main function
main()
