#!/usr/bin/env python

import argparse
import os
import glob
import matplotlib.pyplot as plt
from future.builtins import input
from os import path

def checkPlot():
    parser = argparse.ArgumentParser(description='Check plot of Reward vs Episode')
    parser.add_argument('--rewards', default="/home/sneha/uncertainty/Drone_RL/RL_exp/log/Results/reward.txt", help='Cumulative Rewards per episode')
    parser.add_argument('--irewards', default="/home/sneha/uncertainty/Drone_RL/RL_exp/log/Results/", help='Intermediate Rewards per episode')
    
    args = parser.parse_args()
    
    print("==== Args used:")
    print(args)
    print("Press 1 for rewards plot and 2 for intermediate rewards plot:")
    x = input()

    if(x == '1'):
        rewardsPlot(args.rewards)
    elif(x == '2'):
        irewardsPlot(args.irewards)

def rewardsPlot(path):
    
    f = open(path, "r")
    # print(f.read())
    Lines = f.readlines() 
    count = 0
    # Strips the newline character 
    x=[]
    y=[]
    for line in Lines: 
        # print("Line{}: {}".format(count, line.strip())) 
        values = line.split(",")
        y.append(float(values[0]))
        x.append(int(values[1]))
    plt.plot(x, y) 
  
    # naming the x axis 
    plt.xlabel('Episode') 
    # naming the y axis 
    plt.ylabel('Rewards') 
    plt.title('Cumulative reward vs episode') 
    
    # function to show the plot 
    plt.show() 

def irewardsPlot(pathr):
    count = 1
    # print(f.read())
     
    
    # Strips the newline character 
    x=[]
    y=[]
    
    while(path.exists(pathr+"/"+str(count)+".txt")):
        f = open(pathr+"/"+str(count)+".txt", "r")
        Lines = f.readlines()
        for line in Lines: 
            # print("Line{}: {}".format(count, line.strip())) 
            values = line.split(",")
            x.append(int(values[0].split(":")[1]))
            y.append(float(values[len(values)-1].split(":")[1]))
        count= count+1
        
    # print(x,y)
    plt.plot(x, y)  
    # naming the x axis 
    plt.xlabel('Episode') 
    # naming the y axis 
    plt.ylabel('Rewards') 
    plt.title('Intermediate reward vs episode')    
    # function to show the plot 
    plt.show() 



if __name__ == '__main__':
    checkPlot()
