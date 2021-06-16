#Rebecca Holt
#REU simple model 2/28/21

#how to use atom--- tips
#using real data? access to data? how will model differ?
#what do you use to graph with atom?

#since there are 100 houses, should I just pick a few to look at the graph of?
#or should I do the total energy?

#how do you think I should change the graph because I have a set function
#and then I make it zero and then I set it back, so how would I graph this?

#import functions to calc integral & produce random #s
import numpy as np
import sympy as sy
import matplotlib.pyplot as plt

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
    eng_list, bud_list = get_power()
    print(eng_list)
    print(bud_list)

    #call graph function to make graph of power
    #graph()

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
    for i in range(0, HOUSES + 1):
        #get random factor for each house to scale power curve
        factor = random.uniform(.5, 2)

        #calculate power curve
        f = lambda x: factor * (-((x/3)-2)**2 + 4)

        #add power curve equation to list
        power_eqn_list.append(f)

    #now, check if curtailment is necissary:
    #for a time step
    x = 0
    for x in range(13):
        #change curtailed power equations back to normal
        if len(removed_index_list) != 0:
            for i in range(0, len(removed_index_list) + 1):
                power_eqn_list.insert(removed_index_list[i], removed_eqn_list[i])
               
        #define ideal power curve
        ideal = lambda x: -((x/3)-2)**2 + 4
        #get area of ideal curve up until time x
        ideal_eng = quad(ideal, 0, x)
        #multiply ideal_eng by HOUSES to get total ideal energy of all houses
        ideal_total_eng = ideal_eng * HOUSES

        #get energy list and total energy for first time step
        house_eng_list, total_eng, total_eng_list = calc_power(power_eqn_list, house_eng_list, total_eng, total_eng_list, x)
                               
        #if total energy of houses is greater than maximum, stop random house from adding power to grid
        while total_eng > ideal_total_eng[0]:
            #get random house number 
            num_house = random.randint(0, HOUSES)
            
            #check if house has acceptable budget to curtail power
            if budget_list[num_house] > 0:
                #save the initial equations 
                #add index of num_house to removed_index_list
                removed_index_list.append(num_house)

                #append eqn of num_house to removed_eqn_list
                removed_eqn_list.append(power_eqn_list[num_house])

                #replace old eqn with 0 
                power_eqn_list[num_house] = 0
                
                #subtract curtailed energy from houses budget 
                budget_list[num_house] = budget_list[num_house] - PRICE

                #send to the calc_power function to calculate new power
                house_eng_list, total_eng, total_eng_list = calc_power(power_eqn_list, house_eng_list, total_eng, total_eng_list, x)

    return house_eng_list, budget_list

def calc_power(power_eqn_list, house_eng_list, total_eng, total_eng_list, x):
    #calculate the power of each house over time step
    for i in range(0, HOUSES + 1):
        #get equation of house from power_eqn_list
        pwr_eqn = power_eqn_list[i]

        #calculate area up until given time of specific house
        energy = quad(pwr_eqn, 0, x)

        #add power of that house to house_pwr_list
        house_eng_list[i] = energy[0]

        #add houses power to total energy
        total_eng += energy[0]

        #add total energy to total_eng_list
        total_eng_list.append(total_eng)

    #return total energy
    return house_eng_list, total_eng, total_eng_list

        
#call main function
main()
