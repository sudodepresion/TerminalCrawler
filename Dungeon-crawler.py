from os import execlp
import sys
import json
import io
import math
import random
import time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def vectorAdd(vec1,vec2):
    return [vec1[0] + vec2[0], vec1[1] + vec2[1]]


def main(xLimit, yLimit):
    global currentRoom
    global Player
    global goal

    Player = [1,3]
    goal = [-1,-1]
    startingTime = time.time()

    generateWalls("Start")
    while Player != goal:
        print(displayPoints(xLimit, yLimit, Player, walls))
        print(f"Current: {Player} Last: {lastPlayerPosition} Room: {currentRoom}")
        getInput(xLimit, yLimit)
        collisionHandler(xLimit, yLimit)
    print(displayPoints(xLimit, yLimit, Player, walls))
    timer = time.time() - startingTime 
    print(f"You won! Your time: {round(timer,2)}s")
    showAndEditHighscore(timer)
    print("-" * 30)
    if input("Play again? (y/n)") == "y":
        main(xLimit, yLimit)
         

def displayPoints(xLimit, yLimit, Player, walls):
    output = ""
    for y in range(0,yLimit):
        for x in range(0,xLimit):
            targetPoint = [x, y]
            if Player == targetPoint:
                output += " 🤖 "
            elif walls.count(targetPoint) > 0:
                output += " 🧱 "
            elif goal == targetPoint:
                output += " 🏆 "
            else: output += " ⚪ "
        output += "\n"
    return output

def getInput(xLimit, yLimit):
        playerInput = input(f"\nYour Move: ")
    
        if playerInput == "":
            getInput(xLimit, yLimit)
        elif playerInput == "w":
            Player[1] -= 1
        elif playerInput == "a":
            Player[0] -= 1
        elif playerInput == "s":
            Player[1] += 1
        elif playerInput == "d":
            Player[0] += 1
        elif playerInput == "h":
            showAndEditHighscore()
        elif playerInput[0:2] == "r-":
            if int(playerInput[2:]) < xLimit * yLimit:
                try:
                    global walls
                    walls = []
                    generateRandomWalls(int(playerInput[2:]))
                except: print(f"Invalid command | Your Input: {playerInput[2:]}")
            else: print("To big")
        elif playerInput[0:2] == "g-":
            generateWalls(playerInput[2:])
        else: print(f"invalid command | Your Input: {playerInput}")

def collisionHandler(xLimit, yLimit):
    global Player
    global lastPlayerPosition
    if Player in walls:
        print("You can't go through solid stone!")
        Player = lastPlayerPosition.copy()
    else:
        lastPlayerPosition = Player.copy()
    roomTransition(xLimit, yLimit)

def generateRandomWalls(amount):
    for i in range(amount):
        global Player
        pos = [random.randint(0,6),random.randint(0,6)]
        while walls.count(pos) > 0 or pos == Player:
            pos = [random.randint(0,6),random.randint(0,6)]
        walls.append(pos)
             
def generateWalls(Room): 
    with open("rooms.json") as json_data:
        data = json.load(json_data)
        vectors = data['Rooms'][0][Room]
    global walls
    walls = vectors

def roomTransition(xLimit, yLimit):
    global Player
    global currentRoom
    global goal
    if Player[0] >= xLimit or Player[1] >= yLimit or Player[0] < 0 or Player[1] < 0:
        choosenRoom = currentRoom
        while choosenRoom == currentRoom:
            goal = [-1,-1] # despawn the goal as a standart in rooms
            diceThrow = random.randint(1,5)
            if diceThrow == 1:
                choosenRoom = "Room-1"
            elif diceThrow == 2:
                choosenRoom = "Room-2"
            elif diceThrow == 3:
                choosenRoom = "Room-3"
                goal = [3, 1] # bringing the goal back
            elif diceThrow == 4:
                choosenRoom = "Room-4"
            elif diceThrow == 5:
                choosenRoom = "Room-5"
                goal = [4,3]
        generateWalls(choosenRoom)
        currentRoom = choosenRoom
        Player = [0,3]

def showAndEditHighscore(time):
    with open("Highscores.json", "r") as json_data:
        dataHighscore = json.load(json_data)
        topPlayer = dataHighscore["Highscores"][0]["Top"][0]["Name"]
        topTime   = dataHighscore["Highscores"][0]["Top"][0]["Time"]
        print(f"Current Highscore: {topPlayer} -- {round(topTime,2)}s")

        if time < int(topTime):
            if input("You have a new best Time! Want to save it? (y/n)") == "y":
                dataHighscore["Highscores"][0]["Top"][0]["Time"] = time
                dataHighscore["Highscores"][0]["Top"][0]["Name"] = input("Your Name:    ")
                with open("Highscores.json", "w") as file:
                    json.dump(dataHighscore, file, indent=2)
    


Player = [1,3]
lastPlayerPosition = [1,3]

currentRoom = "Start"
goal = [-1,-1]
walls = []

main(7, 7)


