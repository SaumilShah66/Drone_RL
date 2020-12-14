
Skip to content
Pull requests
Issues
Marketplace
Explore
@varunasthana92
SaumilShah66 /
Drone_RL

2
0

    0

Code
Issues
Pull requests
Actions
Projects
Wiki
Security

    Insights

Drone_RL/blender_scripts/plot.py /
@snehanyk05
snehanyk05 Slight changes to close file
Latest commit e91409d 5 hours ago
History
1 contributor
85 lines (68 sloc) 2.16 KB
#!/usr/bin/env python

import argparse
import os
import glob
import matplotlib.pyplot as plt
from future.builtins import input
from os import path

def checkPlot():
    parser = argparse.ArgumentParser(description='Check plot of Reward vs Episode')
    parser.add_argument('--rewards', default="/home/varun/Drone_RL/Drone_RL/RL_exp/log/", help='Cumulative Rewards per episode')
    parser.add_argument('--irewards', default="/home/varun/Drone_RL/Drone_RL/RL_exp/log/", help='Intermediate Rewards per episode')
    
    args = parser.parse_args()

    folders = glob.glob(args.rewards + 'blender*')
    folders.sort()
    folders = folders[-1]
    args.rewards = folders + '/Results/reward.txt'
    args.irewards = folders + '/Results/'
    
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
    f.close()
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
    
    while(path.exists(pathr + str(count)+".txt")):
        f = open(pathr + str(count)+".txt", "r")
        Lines = f.readlines()
        for line in Lines: 
            values = line.split(",")
            x.append(int(values[0].split(":")[1]))
            y.append(float(values[len(values)-1].split(":")[1]))
        f.close()
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