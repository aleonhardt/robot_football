# -*- coding:utf-8 -*-
# Copyright (C) 2011 Renato de Pontes Pereira, renato.ppontes at gmail dot com
#
# This module is part of robotsoccer-python and is released under 
# the MIT  License: http://www.opensource.org/licenses/mit-license.php

"""
A small example of robotsoccer-python usage.

To run this module type in terminal::

   python example_simple.py host port

If host or port is omitted 'localhost' and 1024 are assumed as default
"""
import os
import sys
import math
import numpy

NUMBER_OF_POINTS = 180
BALL_ANGLE_RULES = 3
TARGET_ANGLE_RULES = 3
BALL_DISTANCE_RULES = 3

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from robotsoccer import SoccerClient

class fuzzySet:

    def __init__(self):
        self.set = 0

    def membership(self):
        raise NotImplementedError("Please Implement this method")

class fuzzyLambda(fuzzySet): #lambda(triangulo) herda da superclasse fuzzySet(conjunto fuzzy)

    def __init__(self, alpha, beta, gamma):
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma

        #inicializa vetor de pontos da função

        self.set = []
        for index in range(NUMBER_OF_POINTS):
            x = index*(math.pi/(NUMBER_OF_POINTS/2)) - math.pi
            if x < self.alpha or x >= self.gamma: 
                self.set.append(0);
            if x >= self.alpha and x < self.beta: 
                self.set.append((x - self.alpha)/(self.beta - self.alpha))
            if x >= self.beta and x < self.gamma: 
                self.set.append((self.gamma - x)/(self.gamma - self.beta))

    def membership(self, x):
        if x < self.alpha or x >= self.gamma: 
            return 0
        if x >= self.alpha and x < self.beta: 
            return (x - self.alpha)/(self.beta - self.alpha)
        if x >= self.beta and x < self.gamma: 
            return (self.gamma - x)/(self.gamma - self.beta)

class fuzzyLeftTrapezoid(fuzzySet):

    def __init__(self, alpha, beta):
        self.alpha = alpha;
        self.beta = beta;

        #inicializa vetor de pontos da função

        self.set = []
        for index in range(NUMBER_OF_POINTS):
            x = index*(math.pi/(NUMBER_OF_POINTS/2)) - math.pi
            if x < self.alpha: 
                self.set.append(1.0) 
            elif x >= self.alpha and x < self.beta: 
                self.set.append((self.beta - x)/(self.beta - self.alpha))
            elif x >= self.beta: 
                self.set.append(0.0)

    def membership(self, x):
        if x < self.alpha: 
            return 1 
        if x >= self.alpha and x < self.beta: 
            return (self.beta - x)/(self.beta - self.alpha)
        if x >= self.beta: 
            return 0

class fuzzyRightTrapezoid(fuzzySet):

    def __init__(self, alpha, beta):
        self.alpha = alpha;
        self.beta = beta;

        #inicializa vetor de pontos da função

        self.set = []
        for index in range(NUMBER_OF_POINTS):
            x = index*(math.pi/(NUMBER_OF_POINTS/2)) - math.pi
            if x < self.alpha: 
                self.set.append(0) 
            if x >= self.alpha and x < self.beta: 
                self.set.append((x - self.alpha)/(self.beta - self.alpha))
            if x >= self.beta: 
                self.set.append(1)

    def membership(self, x):
        if x < self.alpha: 
            return 0 
        if x >= self.alpha and x < self.beta: 
            return (x - self.alpha)/(self.beta - self.alpha)
        if x >= self.beta: 
            return 1

class fuzzyTrapezoid(fuzzySet):

    def __init__(self, alpha, beta, gamma, delta):
        self.alpha = alpha;
        self.beta = beta;       
        self.gamma = gamma;
        self.delta = delta;

        self.set = []
        for index in range(NUMBER_OF_POINTS):
            x = index*(math.pi/(NUMBER_OF_POINTS/2)) - math.pi
            if x < self.alpha or x >= self.delta: 
                self.set.append(0) 
            if x >= self.alpha and x < self.beta: 
                self.set.append((x - self.alpha)/(self.beta - self.alpha))
            if x >= self.beta and x < self.gamma: 
                self.set.append(1)      
            if x >= self.gamma and x < self.delta:
                self.set.append((self.delta - x)/(self.delta - self.gamma))

    def membership(self, x):
        if x < self.alpha or x >= self.delta: 
            return 0 
        if x >= self.alpha and x < self.beta: 
            return (x - self.alpha)/(self.beta - self.alpha)
        if x >= self.beta and x < self.gamma: 
            return 1      
        if x >= self.gamma and x < self.delta:
            return (self.delta - x)/(self.delta - self.gamma)



def fuzzyMaximum(firstVector, secondVector): #compõe o conjunto que é o resultado entre o máximo de dois conjuntos

    outputVector = []
    for index in range(NUMBER_OF_POINTS):
        outputVector.append(max(firstVector[index], secondVector[index]))

    return outputVector

def getFiringStrength(firstSet, firstValue, secondSet, secondValue, thirdSet, thirdValue):

    mi0 = firstSet.membership(firstValue)
    mi1 = secondSet.membership(secondValue)
    mi2 = thirdSet.membership(thirdValue)

    min1 = min(mi0, mi1)
    return min(min1, mi2)

def cutOutputVector(setVector, firingStrength):

    outputVector = []
    for index in range(NUMBER_OF_POINTS):
        if(setVector[index] > firingStrength):
            outputVector.append(firingStrength)
        else:
            outputVector.append(setVector[index])
    return outputVector

def defuzzification(setVector): #usando o metodo do centroide

    sumDen = 0; #denominador
    sumNum = 0; #numerador

    for index in range(len(setVector)):
        z = index*(math.pi/(NUMBER_OF_POINTS/2)) - math.pi
        sumNum = sumNum + z*setVector[index]
        sumDen = sumDen + setVector[index]

    centroid = sumNum/sumDen
    return centroid 

def main():

    host = sys.argv[1] if len(sys.argv) > 1 else 'localhost'    
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 1024
    
    sc = SoccerClient()
    sc.connect(host, port)

    #conjuntos fuzzy de distância da bola
    ballClose = fuzzyLeftTrapezoid(70,100)
    ballFar = fuzzyRightTrapezoid(50, 250)
	
    #conjuntos fuzzy do ângulo em relação à bola

    ballLeftBack = fuzzyLeftTrapezoid(-math.pi, -math.pi/2)
    ballLeftFront = fuzzyLambda(-math.pi/4, -math.pi/2, 0)
    ballForward = fuzzyLambda(-math.pi/2, 0, math.pi/2)
    ballRightFront = fuzzyLambda(0, math.pi/2, math.pi/4)
    ballRightBack = fuzzyRightTrapezoid(math.pi/2, math.pi)

    #conjuntos fuzzy do ângulo em relação ao gol

    targetLeft = fuzzyLeftTrapezoid(-math.pi, 0)
    targetForward = fuzzyLambda(-math.pi/2, 0, math.pi/2)
    targetRight = fuzzyRightTrapezoid(0, math.pi)

    #conjuntos fuzzy do ângulo do robô(saída)

    robotLeft= fuzzyLambda(- math.pi, -math.pi/4, -math.pi/2)
    robotLeftFront = fuzzyLambda(-math.pi/4, -math.pi/2, 0)
    robotForward = fuzzyLambda(-math.pi/2, 0, math.pi/2)
    robotRightFront = fuzzyLambda(0, math.pi/2, math.pi/4)
    robotRight = fuzzyLambda(math.pi/2, math.pi/4, math.pi)
    
    rulesMatrix = numpy.zeros((2,5,3), dtype=object) # Make a 2 by 5 by 3 rules matrix
    #[distância, angulo bola, angulo gol]
    #close
    rulesMatrix[0][0][0] = robotLeft
    rulesMatrix[0][0][1] = robotLeft
    rulesMatrix[0][0][2] = robotLeftFront
    
    rulesMatrix[0][1][0] = robotLeft
    rulesMatrix[0][1][1] = robotLeft
    rulesMatrix[0][1][2] = robotLeftFront
    
    rulesMatrix[0][2][0] = robotRightFront
    rulesMatrix[0][2][1] = robotForward
    rulesMatrix[0][2][2] = robotLeftFront
    
    rulesMatrix[0][3][0] = robotRightFront
    rulesMatrix[0][3][1] = robotRightFront
    rulesMatrix[0][3][2] = robotRight
    
    rulesMatrix[0][4][0] = robotRightFront
    rulesMatrix[0][4][1] = robotRight
    rulesMatrix[0][4][2] = robotRight

    #far
    rulesMatrix[1][0][0] = robotLeft
    rulesMatrix[1][0][1] = robotLeft
    rulesMatrix[1][0][2] = robotLeft
    
    rulesMatrix[1][1][0] = robotLeftFront
    rulesMatrix[1][1][1] = robotLeftFront
    rulesMatrix[1][1][2] = robotLeftFront
    
    rulesMatrix[1][2][0] = robotForward
    rulesMatrix[1][2][1] = robotForward
    rulesMatrix[1][2][2] = robotForward
    
    rulesMatrix[1][3][0] = robotRightFront
    rulesMatrix[1][3][1] = robotRightFront
    rulesMatrix[1][3][2] = robotRightFront
    
    rulesMatrix[1][4][0] = robotRight
    rulesMatrix[1][4][1] = robotRight
    rulesMatrix[1][4][2] = robotRight
    
    

    distanceFuzzySets =[ballClose, ballFar]
    ballFuzzySets = [ballLeftBack, ballLeftFront, ballForward, ballRightFront, ballRightBack]
    targetFuzzySets = [targetLeft, targetForward, targetRight]
    robotFuzzySets = [robotLeft, robotLeftFront, robotForward, robotRightFront, robotRight]

    # Action loop
    while True:
        # Gets the angle between robot and ball
        ball_angle = sc.get_ball_angle()

        # Gets the angle between goal and robot
        target_angle = sc.get_target_angle()

	#gets the distance to the ball
        ball_distance = sc.get_ball_distance()

        inferedVector = [0]*180

        #laço para determinar a força de disparo de cada regra e calcular o conjunto de inferencia fuzzy

        for i in range(len(distanceFuzzySets)): 
            for j in range(len(ballFuzzySets)):
                for k in range(len(targetFuzzySets)):
                    mi0 = distanceFuzzySets[i].membership(ball_distance)
                    print(mi0)
                    if mi0 > 0:
                        mi1 = ballFuzzySets[j].membership(ball_angle)
                        print(mi1)
                        if mi1 > 0:
                            mi2=targetFuzzySets[k].membership(target_angle)
                            print(mi2)
                            if mi2 > 0:
                                firingStrength = getFiringStrength(distanceFuzzySets[i], ball_distance, ballFuzzySets[j], ball_angle, targetFuzzySets[k], target_angle)
                                inferedVector = fuzzyMaximum(inferedVector, cutOutputVector(rulesMatrix[i][j][k].set, firingStrength))

        out = defuzzification(inferedVector)

        # converte ângulo do robô na força dos dois motores

        force_left = math.cos(out) - math.sin(out)
        force_right = math.cos(out) + math.sin(out)

        # Sends the action of robot to simulator
        sc.act(force_left*0.5, force_right*0.5)

    # Disconnects from match simulator (actually this line is never called)
    sc.disconnect()

if __name__ == '__main__':
    main() 

    
