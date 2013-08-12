import pygame

class BaseClass(pygame.sprite.Sprite):

    allsprites = pygame.sprite.Group() #list containing every sprite in game
    def __init__(self, x, y, width, height, image_string):

        pygame.sprite.Sprite.__init__(self)#calling sprite classes init method
        BaseClass.allsprites.add(self)#adds sprite to allsprites list

        self.image = pygame.image.load(image_string)#image dealing with
        self.rect = self.image.get_rect()#the absolute rect of image
        self.rect.x = x#starting x position
        self.rect.y = y#starting y position

        self.width = width
        self.height = height

class Bug(BaseClass):

    List = pygame.sprite.Group()
    def __init__(self, x, y, width, height, image_string):

        BaseClass.__init__(self, x, y, width, height, image_string)
        Bug.List.add(self)
        self.velx = 3

    def motion(self):

        self.rect.x += self.velx


