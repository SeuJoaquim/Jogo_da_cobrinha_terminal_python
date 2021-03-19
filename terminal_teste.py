import time
import os
import random
from win32api import GetKeyState
import threading


class Game():
    def __init__(self):
        # Game stats
        self.matrix     = [[-1 for i in range(10)] for i in range(10)] 
        self.velocity   = 0.5


        self.emoji_table = [
            [-2,"\U0001F5A4"],
            [-1,"\U0001F90E"],
            [ 1,"\U0001F34E"],
            [ 2,"\U0001F438"],
            [ 3, "\U0001F49A"]
        ]
        # Game Objects
        self.apple      = self.Apple() 
        self.apple.create_new_apple()
        self.player     = self.Player()
    
    class Apple():
        def __init__(self):
            self.exists = False
        
        def create_new_apple(self):
            self.exists = True
            self.x = random.randint(1,8)
            self.y = random.randint(1,8)
            

    class Player():
        def __init__(self):
            self.keyTABLE               = {}  
            self.keyTABLE["UP"]         = [-1, 0]
            self.keyTABLE["DOWN"]       = [ 1, 0]
            self.keyTABLE["LEFT"]       = [ 0,-1]
            self.keyTABLE["RIGHT"]      = [ 0, 1]    


            self.x = self.y     = 5
            self.continuos_move = "UP"
            self.length         = 0

            self.body = []
        
        def move(self, moviment,isPressed):
            if not isPressed:
                self.continuos_move = moviment
                self.x += self.keyTABLE[f"{moviment}"][0]
                self.y += self.keyTABLE[f"{moviment}"][1]
        
        def move_body(self):
            if self.body:
                n = len(self.body) - 1
                while n>=0:
                    if n != 0:
                        self.body[n][2] = self.body[n-1][2]
                    else:
                        self.body[n][2] = self.continuos_move
                        

                    self.body[n][0] += self.keyTABLE[f"{self.body[n][2]}"][0]
                    self.body[n][1] += self.keyTABLE[f"{self.body[n][2]}"][1]
                    n -= 1

        def increase(self):
            self.length += 1
            if self.length != 1:
                last            = len(self.body) - 1
                x               = self.body[last][0] 
                y               = self.body[last][1] 
                continuos_move  = self.body[last][2]

                content = [
                    x - self.keyTABLE[f"{continuos_move}"][0],
                    y - self.keyTABLE[f"{continuos_move}"][1],
                    continuos_move
                ]
                self.body.append(content)
            
            else:
                content = [
                    self.x - self.keyTABLE[f"{self.continuos_move}"][0],
                    self.y - self.keyTABLE[f"{self.continuos_move}"][1],
                    self.continuos_move]
                self.body.append(content)
    

    def execute(self):
        def key_down(key):
            state = GetKeyState(key)
            if (state != 0) and (state != 1):
                return True
            else:
                return False

        def generate_table():
            def set_apple():
                self.matrix[self.apple.x][self.apple.y] = 1
                        
            def set_player_position():
                self.matrix[self.player.x][self.player.y] = 2
            
            def set_body_position():
                if self.player.body:
                    for item in self.player.body:
                        self.matrix[item[0]][item[1]] = 3

            def clear_table():
                for i in range(10):
                    for j in range(10):
                        self.matrix[i][j] = -1
                        if (i == 0) or (i == 9) or (j== 0) or (j == 9):
                            self.matrix[i][j] = -2

            def print_table():
                os.system("cls")
                for i in range(10):
                    for j in range(10):
                        for item in self.emoji_table:
                            if self.matrix[i][j] == item[0]:
                                value = item[1]
                        print(value, end= "")
                        if j == 9:
                            print()

                print("\n\n") 

            if not self.apple.exists:
                self.apple.create_new_apple()  
                    
            clear_table()
            set_apple()
            set_body_position()
            set_player_position()
            self.player.move_body()

            print_table()

        def starter():
            running = True
            while running:
                move = False


                if key_down(0x57) or key_down(0x77):
                    self.player.move("UP",move)
                    move = True

                if key_down(0x53) or key_down(0x73):
                    self.player.move("DOWN",move)
                    move = True

                if key_down(0x41) or key_down(0x61):
                    self.player.move("LEFT",move)
                    move = True

                if key_down(0x44) or key_down(0x64):
                    self.player.move("RIGHT",move)
                    move = True

                if key_down(0x20):
                    exit()
                    
                if not move:
                    self.player.move(self.player.continuos_move, move)


                if (self.player.x == self.apple.x) and (self.player.y == self.apple.y):
                    self.apple.exists = False
                    self.player.increase()
                    self.apple.create_new_apple()
                
                if self.player.body:
                    for item in self.player.body:
                        if (self.player.x == item[0]) and (self.player.y == item[1]):
                            print("Você perdeu \U0001F633")
                            exit()

                if (self.player.x == 0) or (self.player.x == 9) or (self.player.y == 0) or (self.player.y == 9):
                    print("Você perdeu \U0001F633")
                    exit()

                generate_table()
                
                time.sleep(self.velocity)
                
                # Controlled game loops
                
        def in_new_thread():
            th = threading.Thread(target=starter)
            th.start()

        in_new_thread()




game = Game()
game.execute()