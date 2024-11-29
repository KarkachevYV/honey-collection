import pygame
import random

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
FLOWER_SIZE = 70
NUM_FLOWERS = 4

# Цвета
GREY = (128,128,128)

# Создаем окно
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Медоносы")

# Загрузка изображений цветов
flower_images = {
    'sunflower': pygame.transform.scale(pygame.image.load("img/flower.png").convert_alpha(), (FLOWER_SIZE, FLOWER_SIZE)),
    'buckwheat': pygame.transform.scale(pygame.image.load("img/buckwheat.png").convert_alpha(), (FLOWER_SIZE, FLOWER_SIZE)),
    'melilot': pygame.transform.scale(pygame.image.load("img/melilot.png").convert_alpha(), (FLOWER_SIZE, FLOWER_SIZE)),
    'colza': pygame.transform.scale(pygame.image.load("img/colza.png").convert_alpha(), (FLOWER_SIZE, FLOWER_SIZE)),
}

# Функция для генерации случайной позиции цветка
def generate_random_position(existing_positions):
    while True:
        x = random.randint(0, WIDTH - FLOWER_SIZE)
        y = random.randint(0, HEIGHT - FLOWER_SIZE)
        # Проверяем, что новая позиция не пересекается с существующими
        if all(not (pos[0] < x < pos[0] + FLOWER_SIZE and pos[1] < y < pos[1] + FLOWER_SIZE) for pos in existing_positions):
            return x, y

# Генерируем начальные позиции и типы для четырех цветков
flower_positions = [generate_random_position([]) for _ in range(NUM_FLOWERS)]
flower_types = [random.choice(list(flower_images.keys())) for _ in range(NUM_FLOWERS)]

running = True

while running:
  screen.fill(GREY)

  # Обработка событий
  for event in pygame.event.get():
      if event.type == pygame.QUIT:
          running = False
      elif event.type == pygame.MOUSEBUTTONDOWN:
          mouse_pos = event.pos
          for i, (flower_pos, flower_type) in enumerate(zip(flower_positions, flower_types)):
              if (flower_pos[0] <= mouse_pos[0] <= flower_pos[0] + FLOWER_SIZE and
                      flower_pos[1] <= mouse_pos[1] <= flower_pos[1] + FLOWER_SIZE):
                  # Перемещаем цветок на новую случайную позицию и меняе его тип
                  flower_positions[i] = generate_random_position(flower_positions)
                  flower_types[i] = random.choice(list(flower_images.keys()))

  # Рисуем цветки
  for flower_pos, flower_type in zip(flower_positions, flower_types):
      screen.blit(flower_images[flower_type], flower_pos)

  # Обновляем дисплей
  pygame.display.flip()

pygame.quit()