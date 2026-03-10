import pygame


class ImageButton(pygame.sprite.Sprite):

    def __init__(self, name : str, image : pygame.image, resizeScale : float, position):
       pygame.sprite.Sprite.__init__(self)

       self.name = name

       self.image = pygame.transform.rotozoom(image, 0, resizeScale)
       self.rect = self.image.get_rect()
       self.rect = self.rect.move(position)
    
    def isClicked(self, mouseClicked : bool):
        if mouseClicked and self.rect.collidepoint(pygame.mouse.get_pos()):
            return True
        return False


class LogicGatesMenu():
    def __init__(self, LG_Types):
        # Fonts and colors
        self.consolasFont = pygame.font.SysFont('Consolas', 24)
        self.headingRectColor = (125, 125, 125)
        self.headingTextColor = (0, 0, 0)
        self.backgroundRectColor = (150, 150, 150)

        # Graphics objects
        self.headingRect = pygame.Rect(1050, 0,  150, 50)
        self.headingText = self.consolasFont.render('Logic Gates', True, self.headingTextColor)
        self.backgroundRect = pygame.Rect(1050, 50,  150, 750)
        self.LG_ImageButtons = pygame.sprite.Group()

        # Append the Logic Gate ImageButtons
        for i in range(len(LG_Types)):
            LG_Image = pygame.image.load("LogicGateImages/" + LG_Types[i] + ".png")
            self.LG_ImageButtons.add(ImageButton(LG_Types[i], LG_Image, 0.8, (1070, 83.3*i + 50)))
    
    def Draw(self, screen):
        pygame.draw.rect(screen, self.headingRectColor, self.headingRect)
        pygame.draw.rect(screen, self.backgroundRectColor, self.backgroundRect)
        screen.blit(self.headingText, (1055, 15))
        self.LG_ImageButtons.draw(screen)
    
    # Returns tuple of (isClicked, LG_Type)
    def isClicked(self, mouseClicked : bool) -> tuple[bool, str]:
        for LG_ImageButton in self.LG_ImageButtons:
            if LG_ImageButton.isClicked(mouseClicked):
                return (True, LG_ImageButton.name)
        return (False, '')
