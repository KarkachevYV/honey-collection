import pygame
import random
import math

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
FLOWER_SIZE = 70
BEE_SIZE = 30
NUM_FLOWERS = 4
TRIGGER_DISTANCE = 50  # Расстояние до курсора, при котором пчела перемещается

# Цвета
GREY = (128, 128, 128)
WHITE = (255, 255, 255)
ORANGE = (255, 165, 0)

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

# Загрузка изображения пчелы
bee_image = pygame.transform.scale(pygame.image.load("img/bee.png").convert_alpha(), (BEE_SIZE, BEE_SIZE))

# Функция для генерации случайной позиции цветка
def generate_random_position(existing_positions):
    while True:
        x = random.randint(0, WIDTH - FLOWER_SIZE)
        y = random.randint(0, HEIGHT - FLOWER_SIZE)
        if all(not (pos[0] < x < pos[0] + FLOWER_SIZE and pos[1] < y < pos[1] + FLOWER_SIZE) for pos in existing_positions):
            return x, y

# Генерируем начальные позиции и типы для четырех цветков
flower_positions = [generate_random_position([]) for _ in range(NUM_FLOWERS)]
flower_types = [random.choice(list(flower_images.keys())) for _ in range(NUM_FLOWERS)]

# Словарь для хранения количества собранного меда
honey_collected = {flower_type: 0 for flower_type in flower_images.keys()}

# Начальная позиция пчелы в центре случайного цветка
bee_index = random.randint(0, NUM_FLOWERS - 1)
bee_position = (flower_positions[bee_index][0] + FLOWER_SIZE // 2 - BEE_SIZE // 2,
                flower_positions[bee_index][1] + FLOWER_SIZE // 2 - BEE_SIZE // 2)

visited_flowers = set()

running = True

while running:
    screen.fill(GREY)

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            # Изменение цветков
            for i, (flower_pos, flower_type) in enumerate(zip(flower_positions, flower_types)):
                if (flower_pos[0] <= mouse_pos[0] <= flower_pos[0] + FLOWER_SIZE and
                    flower_pos[1] <= mouse_pos[1] <= flower_pos[1] + FLOWER_SIZE):
                    flower_positions[i] = generate_random_position(flower_positions)
                    flower_types[i] = random.choice(list(flower_images.keys()))

    # Получаем позицию курсора
    mouse_pos = pygame.mouse.get_pos()

    # Проверка на расстояние до курсора
    distance = math.sqrt((bee_position[0] - mouse_pos[0]) ** 2 + (bee_position[1] - mouse_pos[1]) ** 2)
    if distance < TRIGGER_DISTANCE:
        # Перемещаем пчелу на новый случайный цветок
        bee_index = random.randint(0, NUM_FLOWERS - 1)
        bee_position = (flower_positions[bee_index][0] + FLOWER_SIZE // 2 - BEE_SIZE // 2,
                        flower_positions[bee_index][1] + FLOWER_SIZE // 2 - BEE_SIZE // 2)

    # Рисуем цветки
    for flower_pos, flower_type in zip(flower_positions, flower_types):
        screen.blit(flower_images[flower_type], flower_pos)

    # Рисуем пчелу
    screen.blit(bee_image, bee_position)

    # Проверка, собрала ли пчела мед
    for flower_pos, flower_type in zip(flower_positions, flower_types):
        if bee_position == (flower_pos[0] + FLOWER_SIZE // 2 - BEE_SIZE // 2,
                            flower_pos[1] + FLOWER_SIZE // 2 - BEE_SIZE // 2) and (flower_pos, flower_type) not in visited_flowers:
            honey_collected[flower_type] += 5
            visited_flowers.add((flower_pos, flower_type))

    # Отображение количества меда
    font = pygame.font.Font(None, 18)
    y_offset = 10
    for flower_type, honey in honey_collected.items():
        text = font.render(f" Вы с пчелой собрали мёд с '{flower_type}': {honey} mg", True, ORANGE)
        screen.blit(text, (10, y_offset))
        y_offset += 30

    # Обновляем дисплей
    pygame.display.flip()

pygame.quit()