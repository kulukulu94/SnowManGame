import pygame


class Scorer:
      
        
    def __init__(self, window):
        self.window = window
        self.health = 100 # health
        self.points = 0 # points
        self.life_loss_rate = 2 # rate at which health falls
        
    # Increases points
    def add_points(self):
        self.points += 1

    # When a snowflake is collected, points, health increase and life loss rate increase to make it more difficult
    def snowflake_calc(self):
        self.points += 3
        self.health += 5 
        self.life_loss_rate += 0.5 ** self.life_loss_rate 
        
        # Health cannot be greater than 100
        if self.health > 100:
            self.health = 100
    
    # Health decreases (and at a faster rate) over time
    def update(self):
        self.health -= self.life_loss_rate * self.window.delta_time()
    
    # Snowie dies if health is zero
    def snowie_alive(self):
        return self.health > 0 

    def get_points(self):
        return self.points

    # Shows health bar and number of points
    def draw(self):
        pygame.draw.rect(self.window.get_screen(), (105, 105, 105), (512 / 2 - 66, 8, 132, 34), 0)  # 2px gray border
        pygame.draw.rect(self.window.get_screen(), (255, 0, 0), (512 / 2 - 64, 10, 128, 30), 0)  # Red bar
        pygame.draw.rect(self.window.get_screen(), (0, 255, 0), (512 / 2 - 64, 10,  self.health / 100 * 128, 30), 0) # Green bar
        self.window.draw_text('points: {}'.format(self.points), 512 / 2 - 64, 12, color=(0, 0, 255), font_file='font.TTF', size=24)
