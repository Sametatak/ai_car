import pygame
import time
import math
import pickle
import neat
import os
from utils import scale_image, blit_rotate_center, blit_text_center
pygame.font.init()

GRASS = scale_image(pygame.image.load("ai_car/imgs/grass.jpg"), 2)
TRACK = scale_image(pygame.image.load("ai_car/imgs/track.png"), 0.9)
CROSS = scale_image(pygame.image.load("ai_car/imgs/cross.png"), 0.01)

UPP = scale_image(pygame.image.load("ai_car/imgs/fast_up.png"), 0.3)
LEFT = scale_image(pygame.image.load("ai_car/imgs/left_arrow.png"), 0.3)
RIGHT = scale_image(pygame.image.load("ai_car/imgs/right_arrow.png"), 0.3)
UP = scale_image(pygame.image.load("ai_car/imgs/up_arrow.png"), 0.3)


TRACK_BORDER = scale_image(pygame.image.load("ai_car/imgs/track-border.png"), 0.9)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)

FINISH = pygame.image.load("ai_car/imgs/finish.png")
FINISH_MASK = pygame.mask.from_surface(FINISH)
FINISH_POSITION = (130, 250)

RED_CAR = scale_image(pygame.image.load("ai_car/imgs/my_car.png"), 0.01)


WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Game!")

MAIN_FONT = pygame.font.SysFont("comicsans", 44)

FPS = 70




class PlayerCar:
    def __init__(self, max_vel, rotation_vel):
        self.odom = 0
        self.img = RED_CAR
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = 0
        self.angle = 0
        self.x, self.y = (170,200)
        self.acceleration = 0.1
    def draw(self, win):
        
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)
        self.lidar()
    def move_forward(self,x):
        self.vel = min(self.vel + x*self.acceleration, self.max_vel)
        self.move()

    def rotate(self, left=False, right=False):
        if left:
            self.angle += 5
        elif right:
            self.angle -= 5
        if self.angle > 360 or self.angle < -360:
            self.angle = 0
    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        
        return poi

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel
        self.odom += abs(vertical) + abs(horizontal)
        #print(self.odom)
        self.y -= vertical
        self.x -= horizontal
        


    def lidar(self):
        collision_point_x =  collision_point2_x = collision_point3_x = collision_point4_x = collision_point5_x= collision_point6_x = collision_point7_x= self.x 
        collision_point_y= collision_point2_y = collision_point3_y = collision_point4_y= collision_point5_y = collision_point6_y= collision_point7_y = self.y

        while not TRACK_BORDER_MASK.get_at((round(collision_point_x) ,round(collision_point_y))) and math.sqrt((collision_point_x-self.x)**2 + (collision_point_y-self.y)**2) <150 : 
            collision_point_x += math.cos(math.radians(self.angle+90))
            collision_point_y += math.sin(math.radians(self.angle-90))
        while not TRACK_BORDER_MASK.get_at((round(collision_point2_x) ,round(collision_point2_y))) and math.sqrt((collision_point2_x-self.x)**2 + (collision_point2_y-self.y)**2) <150: 
            collision_point2_x += math.cos(math.radians(self.angle+120))
            collision_point2_y += math.sin(math.radians(self.angle-60))
        while not TRACK_BORDER_MASK.get_at((round(collision_point3_x) ,round(collision_point3_y)))  and math.sqrt((collision_point3_x-self.x)**2 + (collision_point3_y-self.y)**2) <150: 
            collision_point3_x += math.cos(math.radians(self.angle+60))
            collision_point3_y += math.sin(math.radians(self.angle-120))
        
        while not TRACK_BORDER_MASK.get_at((round(collision_point4_x) ,round(collision_point4_y)))  and math.sqrt((collision_point4_x-self.x)**2 + (collision_point4_y-self.y)**2) <150: 
            collision_point4_x += math.cos(math.radians(self.angle+30))
            collision_point4_y += math.sin(math.radians(self.angle-150))
        while not TRACK_BORDER_MASK.get_at((round(collision_point5_x) ,round(collision_point5_y)))  and math.sqrt((collision_point5_x-self.x)**2 + (collision_point5_y-self.y)**2) <150: 
            collision_point5_x += math.cos(math.radians(self.angle+150))
            collision_point5_y += math.sin(math.radians(self.angle-30))
        while not TRACK_BORDER_MASK.get_at((round(collision_point6_x) ,round(collision_point6_y)))  and math.sqrt((collision_point6_x-self.x)**2 + (collision_point6_y-self.y)**2) <150: 
            collision_point6_x += math.cos(math.radians(self.angle+180))
            collision_point6_y += math.sin(math.radians(self.angle))
        while not TRACK_BORDER_MASK.get_at((round(collision_point7_x) ,round(collision_point7_y)))  and math.sqrt((collision_point7_x-self.x)**2 + (collision_point7_y-self.y)**2) <150: 
            collision_point7_x += math.cos(math.radians(self.angle))
            collision_point7_y += math.sin(math.radians(self.angle-180))
        
        
        WIN.blit(CROSS, (collision_point_x, collision_point_y))
        WIN.blit(CROSS, (collision_point2_x, collision_point2_y))
        WIN.blit(CROSS, (collision_point3_x, collision_point3_y))
        WIN.blit(CROSS, (collision_point4_x, collision_point4_y))
        WIN.blit(CROSS, (collision_point5_x, collision_point5_y))
        WIN.blit(CROSS, (collision_point6_x, collision_point6_y))
        WIN.blit(CROSS, (collision_point7_x, collision_point7_y))
        data_1 = math.sqrt((collision_point_x-self.x)**2 + (collision_point_y-self.y)**2)
        data_2 = math.sqrt((collision_point2_x-self.x)**2 + (collision_point2_y-self.y)**2)
        data_3 = math.sqrt((collision_point3_x-self.x)**2 +(collision_point3_y-self.y)**2)
        data_4 = math.sqrt((collision_point4_x-self.x)**2 + (collision_point4_y-self.y)**2)
        data_5 = math.sqrt((collision_point5_x-self.x)**2 + (collision_point5_y-self.y)**2)
        data_6 = math.sqrt((collision_point6_x-self.x)**2 + (collision_point6_y-self.y)**2)
        data_7 = math.sqrt((collision_point7_x-self.x)**2 + (collision_point7_y-self.y)**2)
        
        return(self.sigmoid2([data_1,data_2,data_3,data_4,data_5,data_6,data_7]))


    def sigmoid2(self,data):
        rt = []
        for i in range(len(data)):
            d = 1/(1+math.exp((-data[i]/15)+5))
            #print(data[i] , d)
            rt.append(d)


        
        return rt
    
        

    def train_ai(self,genomes, config,player_car):
        clock = pygame.time.Clock()
        images = [ (TRACK, (0, 0)),
                (FINISH, FINISH_POSITION), (TRACK_BORDER, (0, 0))]
        

        self.check = False
        run = True
        start_time = time.time()
        net = neat.nn.FeedForwardNetwork.create(genomes, config)

        while run:
            


            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                    break

            output = net.activate(self.lidar())

            #draw(WIN, images, player_car)
            if output[1] < 4:
                WIN.blit(LEFT, (500, 30))
                self.rotate(left=True)
            elif output[1] > 6:
                WIN.blit(RIGHT, (500, 30))
                self.rotate(right=True)
            else:
                pass
            if  output[0] < 5:
                WIN.blit(UP, (500, 30))
                self.move_forward(1)
            if output[0] > 5:
                WIN.blit(UPP, (500, 30))
                self.move_forward(2)
            #pygame.display.update()
            #player_car.draw(WIN)
            #pygame.display.update()
            #duration = time.time()- start_time


            
            if player_car.collide(TRACK_BORDER_MASK) != None:
                distance = math.sqrt((180-self.x)**2+(200-self.y)**2)

                genomes.fitness  = round(self.odom)


                return False
            




        return False
    
    
    def test_ai(self, net,player_car):
        clock = pygame.time.Clock()
        images = [(GRASS, (0, 0)), (TRACK, (0, 0)),
                (FINISH, FINISH_POSITION), (TRACK_BORDER, (0, 0))]
        

        
        run = True
        start_time = time.time()
         
        while run:
            
           
            #draw(WIN, images, player_car)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                    break
            
            output = net.activate(self.lidar())
            
            if output[1] < 4:
                #WIN.blit(LEFT, (500, 30))
                self.rotate(left=True)
            elif output[1] > 6:
                #WIN.blit(RIGHT, (500, 30))
                self.rotate(right=True)
            else:
                pass
            if  output[0] < 5:
                #WIN.blit(UP, (500, 30))
                self.move_forward(1)
            if output[0] > 5:
                #WIN.blit(UPP, (500, 30))
                self.move_forward(2)
            player_car.draw(WIN)
            #pygame.display.update()
            pygame.display.update()
            
            if player_car.collide(TRACK_BORDER_MASK) != None:
                
                return False







def draw(win, images, player_car):
    for img, pos in images:
        win.blit(img, pos)



    player_car.draw(win)
    
    #pygame.display.update()


def move_player(player_car):
    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_a]:
        player_car.rotate(left=True)
    if keys[pygame.K_d]:
        player_car.rotate(right=True)
    if keys[pygame.K_w]:
        moved = True
        player_car.move_forward()
    if keys[pygame.K_s]:
        moved = True
        player_car.move_backward()

    if not moved:
        player_car.reduce_speed()

     
    

def eval_genomes(genomes, config):
    """
    Run each genome against eachother one time to determine the fitness.
    """
    #width, height = 700, 500
    #win = pygame.display.set_mode((width, height))
    #pygame.display.set_caption("Pong")
    for genome_id1, genome1 in genomes:
        #print(round(i/len(genomes) * 100), end=" ")
        genome1.fitness = 0 if genome1.fitness == None else genome1.fitness
        car = PlayerCar(4,4)
        force_quit = car.train_ai(genome1, config,car)
        #print(genome_id1)
        print("fitness:",genome1.fitness)
        #if  genome_id1 > 10:

            #print("fitness:",genome1.fitness)
            


def run_neat(config):
    p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-13954')
    #p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1000))

    winner = p.run(eval_genomes, 30000)
    print('\nBest genome:\n{!s}'.format(winner))
    
    with open("best.pickle_real", "wb") as f:
        pickle.dump(winner, f)
    


def test_best_network(config):
    with open("best.pickle_real", "rb") as f:
        winner = pickle.load(f)
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

   
    
    pygame.display.set_caption("testing")
    play = PlayerCar(4,4)
    play.test_ai(winner_net,play)





if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    #run_neat(config)
    test_best_network(config)


