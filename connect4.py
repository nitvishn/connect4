#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 13 11:10:15 2017
V8.3

@author: vishnuvnittoor
"""
import pygame, sys
import random
from copy import deepcopy
import numpy as np
import json
import os

clean=False

moveFile='memo.txt'

depth = 5

player1='0'
player2='1'
random.seed()
red = (255,0,0)
green = (197,234,124)
blue = (0,0,255)
darkBlue = (0,0,128)
white = (255,255,255)
black = (0,0,0)
pink = (255,200,200)
grey=(0, 0, 0)
light_grey=(58, 58, 58)

def say(string, badMouth=False):
    if(badMouth):
        string+=' Hahah, nice game!'

    os.system('say '+'"'+string+'"')

def cls():
    screen.fill(white)

def getColumns(matrix):
    rows=[]
    for i in range(len(matrix[0])):
        row=[]
        for column in matrix:
            row.append(column[i])
        rows.append(row)
    return rows

def getDiagonals(matrix):
    a = np.array(matrix)
    diags = [a[::-1,:].diagonal(i) for i in range(-a.shape[0]+1,a.shape[1])]
    diags.extend(a.diagonal(i) for i in range(a.shape[1]-1,-a.shape[0],-1))
    return [n.tolist() for n in diags]

def isFourConnected(myList):
    L=myList[:]
    item=L.pop()
    streak=0
    for element in myList:
        if(element==item):
            streak+=1
            if(streak==4 and item!=None):
                return item
        else:
            item=element
            streak=1
    return False

# def isFourConnectedv2(myList):
#     L=myList[:]
#     item=L.pop()
#     streak=0
#     streaki=0
#     for i in range(len(myList)):
#         element=m
#         if(element==item):
#             streak+=1
#             if(streak==4 and item!=None):
#                 return streaki
#         else:
#             item=element
#             streak=1
#             streaki=i
#     return False

depth=abs(depth)
if(depth==0):
    depth+=1

def drawBoard(inpt):
    def findFour():
        columns=inpt.columns
        indexes=[]
        for columni in range(len(columns)):
            column=columns[columni]
            if(isFourConnected(column)!=False):
                streaki=isFourConnected(column)
                indexes.append((columni, streaki))
                indexes.append((columni, streaki+1))
                indexes.append((columni, streaki+2))
                indexes.append((columni, streaki+3))
                return indexes
        return None
    
    cls()
    board=deepcopy(inpt.columns)
    for item in board:
        item.reverse()
    alternate=False
    for y in range(0, 550, 100):
        if(alternate):
            start=100
        else:
            start=200
        for x in range(start-100, 675, 200):
            pygame.draw.rect(screen, light_grey, (x, y, 100, 100), 0)
        alternate=not(alternate)
    
    alternate=True
    for y in range(0, 600, 100):
        if(alternate):
            start=100
        else:
            start=200
        for x in range(start-100, 675, 200):
            pygame.draw.rect(screen, grey, (x, y, 100, 100), 0)
        alternate=not(alternate)
    
    points=[(0, 0), (700, 0), (700, 600), (0, 600)]
    pygame.draw.lines(screen, black, True, points, 2)
    for x in range(len(board)):
        col=board[x]
        x=100*(x) + 50
        for y in range(len(col)):
            thing=col[y]
            y=100*(y) + 50
            if(thing=='1'):
                fill=red
            elif(thing=='0'):
                fill=green
            else:
                continue
            pygame.draw.circle(screen, fill, (x, y), 25, 0)
    pygame.display.update()
#    if(findFour()!=False):
#        print(findFour())
#        pygame.draw.lines(screen, black, False, findFour(), 2)
        
    
def difference(board1, board2):
    for i in range(0, len(board1.columns)):
        column1=board1.columns[i]
        column2=board2.columns[i]
        for j in range(len(column1)):
            if(column1[j]!=column2[j]):
                return i+1
    return None

def getInputAndUpdate(board, moveMade):
    cls()
    drawBoard(board)
    print("\nComputer played:", moveMade)
    inpt=input("\n\nColumn number: ")
    while(not(inpt.isnumeric() and board.move(int(inpt), player2))):
        cls()
        drawBoard(board)
        print("\nInvalid Input.")
        inpt=input("\n\nColumn number: ")

def minimax(node, depth, isMaximisingPlayer, orig_depth, alpha, beta):
    
    if(depth==0 or node.hasWon()!=False):
        return node.evaluation()
    
    if(isMaximisingPlayer):
        bestNode=None
        bestVal=alpha
        for child in node.childs(player1):
            v = minimax(child, depth-1, False, orig_depth, alpha, beta)
            if(bestVal<v):
                bestVal=v
                bestNode=deepcopy(child)
            alpha=max(alpha, bestVal)
            if(beta<=alpha):
                break
        if(depth==orig_depth):
            return bestNode
        return bestVal
    else:
        bestNode=None
        bestVal=beta
        for child in node.childs(player2):
            v = minimax(child, depth-1, True, orig_depth, alpha, beta)
            if(bestVal>v):
                bestVal=v
                bestNode=deepcopy(child)
            beta = min( beta, bestVal)
            if beta <= alpha:
                break
        if(depth==orig_depth):
            return bestNode
        return bestVal
    
def copyBoard(src, dest):
    cols=src.columns
    dest=Board(cols)

def boardFromString(string):
    columns=[[]]
    for char in string:
        if(len(columns[-1])==6):
            columns.append([])
        if(char=='_'):
            columns[-1].append(None)
        else:
            columns[-1].append(char)
    return columns

def makeMove(board):
    strings=stringsFromFile(moveFile)
    for key in strings.keys():
        if(boardToString(board)==key):
            prevBoard=Board(board.columns)
            board.columns=boardFromString(strings[key])
            return difference(prevBoard, board)
    print("moving...")
    best=minimax(board, depth, True, depth, -10000000, 10000000)
    print(best)
    if(best!=None):
        strings = stringsFromFile(moveFile)
        file = open("memo.txt", 'a')
        if (boardToString(board) not in strings):
            file.write(boardToString(board) + ' ' + boardToString(best) + '\n')
        prevBoard=Board(board.columns)
        board.columns=best.columns
        return difference(prevBoard, board)
    else:
        board.move(random.choice(board.getChoices()), player1)
        return "random"

def possibleFours(bigboard, player):
    def possWins(L):
        List=L[:]
        for i in range(len(List)):
            if(List[i]==None):
                List[i]=player
        num=0
        for i in range(0, len(List), 1):
            visual=[]
            try:
                visual=List[i:i+4]
            except:
                break
            if(len(visual)==4 and isFourConnected(visual)==player):
                num+=1
        return num
    
    board=bigboard.columns
    num=0
    for row in getColumns(board):
        num+=possWins(row)
    for column in board:
        num+=possWins(column)
    for diag in getDiagonals(board):
        num+=possWins(diag)
    return num


class Board(object):
    def __init__(self, col=None):
        if(col==None):
            self.columns=[]
            L=[None]*6
            for i in range(7):
                self.columns.append(L[:])
        else:
            self.columns=deepcopy(col)
    
    def hasWon(self):
        columns=self.columns
        
        if(self.getChoices==[]):
            return True
        
        for column in columns:
            if(isFourConnected(column)!=False):
                return isFourConnected(column)
        
        for row in getColumns(columns):
            if(isFourConnected(row)!=False):
                return isFourConnected(row)
        
        for diag in getDiagonals(columns):
            if(isFourConnected(diag)!=False):
                return isFourConnected(diag)
        
        
        return False
    
    def evaluation(self):

        def numThreats(player):


            def isThreat(L, player):

                def contains(small, big):
                    for i in range(len(big) - len(small) + 1):
                        for j in range(len(small)):
                            if big[i + j] != small[j]:
                                break
                        else:
                            return True
                    return False

                templates = [[None, player, player, player], [player, player, player, None]]

                if(contains(templates[0], L) and contains(templates[1], L)):
                    return 10
                elif(contains(templates[0], L)):
                    return 6
                elif(contains(templates[1], L)):
                    return 6
                return 0

            num=0
            for row in getColumns(self.columns):
                num+=isThreat(row, player)

            for row in self.columns:
                num+=isThreat(row, player)

            for row in getDiagonals(self.columns):
                num+=isThreat(row, player)

            return num

        def xInARow(player):
            def longest_run(L, thing):
                longest=1
                n=1
                for item in L[1:]:
                    if(item!=thing):
                        longest=max(n, longest)
                        n=0
                    else:
                        n+=1
                return longest
            tot=0
            for row in getColumns(self.columns):
                if(longest_run(row, player)==2):
                    tot+=3
                elif(longest_run(row, player)==3):
                    tot+=5
#                else:
#                    tot-=1

            for row in self.columns:
                if(longest_run(row, player)==2):
                    tot+=2
                elif(longest_run(row, player)==3):
                    tot+=4
#                else:
#                    tot-=1

            for row in getDiagonals(self.columns):
                if(longest_run(row, player)==2):
                    tot+=3
                elif(longest_run(row, player)==3):
                    tot+=5
#                else:
#                    tot-=1
            return tot

        # def numThreats(player):
        #     num=0
        #     threats=[[None, player, player, player], [player, player, player, None]]
        #     for row in getColumns(board.columns):
        #         for threat in threats:
        #             if(threat in row):
        #                 num+=1
        #         if(threat[0] in row and threat[1] in row):
        #             num+=5

        #     for row in board.columns:
        #         for threat in threats:
        #             if(threat in row):
        #                 num+=1
        #         if(threat[0] in row and threat[1] in row):
        #             num+=5

        #     for row in getDiagonals(board.columns):
        #         for threat in threats:
        #             if(threat in row):
        #                 num+=1
        #         if(threat[0] in row and threat[1] in row):
        #             num+=5
        #     return num

        if(self.hasWon()==True):
            return 0
        elif(self.hasWon()==player2):
            return -1000000000
        elif(self.hasWon()==player1):
            return 1000000000

        acc=(possibleFours(self, player1)-possibleFours(self, player2))*2
        # print(acc)

        #45-63
        acc+=numThreats(player1)*3
        acc-=numThreats(player2)*3

        acc+=xInARow(player1)
        acc-=xInARow(player2)
        # acc+=numThreats(player1)*30
        # acc-=numThreats(player2)*30
        return acc
    
    def getChoices(self):
        choices=[]
        for i in range(len(self.columns)):
            for thing in self.columns[i]:
                if(thing==None):
                    choices.append(i+1)
                    break
        return choices
    
    def getLastIndex(self, column):
        for i in range(len(column)):
            if(column[i]==None):
                return i
    
    def move(self, columnno, player):
        if(columnno not in self.getChoices()):
            return False
        columnno-=1
        self.columns[columnno][self.getLastIndex(self.columns[columnno])]=player
        return True

    def childs(self, player):
        myBoard=deepcopy(self.columns)
        kids=[]
        for move in self.getChoices():
            self.move(move, player)
            kids.append(Board(self.columns))
            self.columns=deepcopy(myBoard)
        return kids

#board=Board()
#moveMade=None
#if(input("Does computer start?\nY/N: ").lower()[0]=='y'):
#    drawBoard(board)
#    moveMade=makeMove(board)
#while(board.hasWon()==False):
#    getInputAndUpdate(board, moveMade)
#    cls()
#    drawBoard(board)
#    print()
#    if(board.hasWon()==False):
#        moveMade=makeMove(board)
#    cls()
#    drawBoard(board)
#cls()
#drawBoard(board)
#if(board.hasWon()==player1):
#    print("\n\nYou lost. Better luck next time.")
#elif(board.hasWon()==player2):
#    print("\n\nIm...impossible!")
#else:
#    print("\n\nDraw.")
#print()

def boardToString(board):
    string=""
    for column in board.columns:
        for item in column:
            if(item==None):
                string+='_'
            else:
                string+=item
    return string

def stringsFromFile(filename):
    file=open(filename, "r")
    strings={}
    for line in file:
        key=""
        val=""
        spacePassed=False
        for char in line:
            if(char=='\n'):
                break
            if(char==' '):
                spacePassed=True
                continue
            if(spacePassed):
                val+=char
            else:
                key+=char
        strings[key]=val
    return strings

def play(board):
    boardToString(board)
    global moveMade
    moveMade=makeMove(board)
    print("Computer played: ", moveMade)
    drawBoard(board)
    pygame.display.update()

crashed=False
toMove=False
board=Board()


# while(board.hasWon()==False):
#     drawBoard(board)
#     pygame.display.update()
#     if(board.hasWon()==False and toMove):
#         play(board)
#         toMove=False
#     drawBoard(board)
#     pygame.display.update()
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#              pygame.quit(); sys.exit();
#         elif(event.type==pygame.KEYDOWN):
#             string=chr(event.key)
#             if(not(string.isnumeric())):
#                 continue
#             string=int(string)
#             if(string>7 or string <1):
#                 continue
#             if(not(board.move(string, player2))):
#                 continue
#             print("You played", string)
#             drawBoard(board)
#             pygame.display.update()
#             toMove=True

#GAME CODE
os.system('say "Do I start?"')
inpt=input("Does computer start? Y/N: ")
inpt.replace(' ', '')
while(len(inpt)!=0 and inpt.upper()[0]!='Y' and inpt.upper()[0]!='N'):
    os.system('say "again, Do I start?"')
    inpt = input("Does computer start? Y/N")
    inpt.replace(' ', '')

if(inpt.upper()[0]=='Y'):
    moveMade=makeMove(board)
    say("I played " + str(moveMade))

crashed=False
loops=0

pygame.init()
clock=pygame.time.Clock()
screen = pygame.display.set_mode((700,600))
drawBoard(board)
pygame.display.update()

played=False

pygame.display.update()
while not crashed:
    outfile = open('outfile.json', 'w')
    json.dump(board.columns, outfile, indent=4)
    if(board.hasWon()!=False):
        crashed=True
        continue
    if(played):
        say("I played " + str(moveMade))
        played=False
        pygame.event.clear()
        continue
    drawBoard(board)
    pygame.display.update()
    if(toMove and loops==1):
        play(board)
        played=True
        toMove=False
        pygame.time.wait(500)
        pygame.event.clear()
        continue
    else:
        loops+=1
    for event in pygame.event.get():
        if(event.type==pygame.QUIT):
            pygame.quit(); sys.exit()

        elif event.type==pygame.KEYDOWN:
            string=chr(event.key)
            if(not(string.isnumeric())):
                continue
            string=int(string)

            if(string>7 or string<1):
                continue
            
            if(not(board.move(string, player2))):
                continue
            if(board.hasWon()!=False):
                crashed=True
            else:
                print("You played", string)
                toMove=True
                loops=0

        elif event.type==pygame.MOUSEBUTTONUP:
            x=pygame.mouse.get_pos()[0]
            x/=100
            x=int(str(x)[0])+1

            if (not (board.move(x, player2))):
                continue
            if (board.hasWon() != False):
                crashed = True
            else:
                print("You played", x)
                toMove = True
                loops = 0

    clock.tick(60)

pygame.display.update()
if(board.hasWon()==player1):
    print('\n\nYou lost. Better luck next time.\n')
    say("I won.", not(clean))
elif(board.hasWon()==player2):
    print("\n\nYou won....? Impos-impossi-impossible!!!\n")
    say("You won?!??!", not(clean))
else:
    print("\n\nYou drew. Good job.\n")
    say("DRAW!", not(clean))
while(True):
    drawBoard(board)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
             pygame.quit(); sys.exit();
