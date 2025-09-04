import pygame
from settings import *


class Button:
    def __init__(self, x, y, width, height, text, on_click=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.on_click = on_click
        self.font = pygame.font.Font(None, 36)
        self.color = BUTTON_COLOR
        self.hover_color = BUTTON_HOVER_COLOR
        self.click_color = BUTTON_CLICK_COLOR
        self.is_hovered = False
        self.click_timer = 0

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered and event.button == 1:
                if self.on_click:
                    self.on_click()
                    self.click_timer = 0.2  # Show clicked color for 0.2 seconds
                return True
        return False

    def update(self, dt):
        if self.click_timer > 0:
            self.click_timer -= dt

    def draw(self, screen):
        current_color = self.color
        if self.click_timer > 0:
            current_color = self.click_color
        elif self.is_hovered:
            current_color = self.hover_color

        pygame.draw.rect(screen, current_color, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)

        text_surf = self.font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)


class TextInputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.text = text
        self.font = pygame.font.Font(None, 32)
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return self.text
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, WHITE)
        return None

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

