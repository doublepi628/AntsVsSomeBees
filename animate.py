import pygame
import math


class ShiningText:
    """Change the transparency of the text over time"""
    def __init__(self, font, text, position):
        self.font = font
        self.text = text
        self.position = position
        self.alpha = 255
        self.increasing = False

    def update(self):
        if self.increasing:
            self.alpha += 2
            if self.alpha >= 255:
                self.alpha = 255
                self.increasing = False
        else:
            self.alpha -= 2
            if self.alpha <= 0:
                self.alpha = 0
                self.increasing = True

    def draw(self, screen):
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.center = self.position
        text_surface.set_alpha(self.alpha)
        screen.blit(text_surface, text_rect)


class ShiningObjects:
    """Save and display all shining objects on the screen"""
    def __init__(self):
        self.all_objects = []

    def add_object(self, obj):
        self.all_objects.append(obj)

    def remove_object(self, obj):
        self.all_objects.remove(obj)

    def draw_all(self, screen):
        for obj in self.all_objects:
            obj.update()
            obj.draw(screen)


class MovingImage:
    """Change the location of image over time"""
    def __init__(self, image_path, start_pos, end_pos):
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.speed = 2  # 移动速度
        self.distance = math.sqrt((end_pos[0] - start_pos[0])**2 + (end_pos[1] - start_pos[1])**2)
        self.direction = ((end_pos[0] - start_pos[0]) / self.distance, (end_pos[1] - start_pos[1]) / self.distance)
        self.current_distance = 0

    def update(self):
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed
        if math.sqrt((self.rect.x - self.start_pos[0])**2 + (self.rect.y - self.start_pos[1])**2) > self.distance:
            self.rect = self.end_pos
        self.current_distance += self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)


class MovingObjects:
    """Save and display all moving objects on the screen"""
    def __init__(self):
        self.all_objects = []

    def add_object(self, obj):
        self.all_objects.append(obj)

    def draw_all(self, screen):
        for obj in self.all_objects:
            obj.update()
            obj.draw(screen)


class FadingImage:
    """Change the transparency of image over time"""
    def __init__(self, image_path, position, size):
        self.image = pygame.transform.scale(pygame.image.load(image_path), size)
        self.position = position
        self.alpha = 255  # 初始透明度

    def update(self):
        self.alpha -= 5
        if self.alpha < 0:
            self.alpha = 0
        self.image.set_alpha(self.alpha)

    def draw(self, surface):
        surface.blit(self.image, self.position)


class FadingObjects:
    """Save and display all fading objects on the screen"""
    def __init__(self):
        self.all_objects = []

    def add_object(self, obj):
        self.all_objects.append(obj)

    def draw_all(self, screen):
        for obj in self.all_objects:
            obj.update()
            if obj.alpha <= 0:
                self.all_objects.remove(obj)
                return
            obj.draw(screen)
