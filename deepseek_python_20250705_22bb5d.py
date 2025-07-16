import pygame
import sys
import math
from pygame.locals import *

# Инициализация Pygame
pygame.init()

# Получаем информацию о дисплее
display_info = pygame.display.Info()
BASE_WIDTH, BASE_HEIGHT = 1400, 800
SCREEN_WIDTH, SCREEN_HEIGHT = display_info.current_w, display_info.current_h

# Создаем окно
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Организационная Структура ГБУЗ «Областная больница г. Троицк»")

# Цветовая схема
BACKGROUND = (240, 245, 255)
HEADER_COLOR = (30, 60, 120)
ACCENT_COLOR = (70, 130, 180)
TEXT_COLOR = (30, 30, 40)
BOX_COLOR = (255, 255, 255)
BOX_BORDER = (180, 200, 220)
HIGHLIGHT = (255, 245, 170)
CONNECTION_COLOR = (150, 170, 200)
SUBUNIT_COLOR = (230, 240, 250)
DEPARTMENT_COLOR = (220, 235, 255)

# Цвета для категорий узлов
COLORS = {
    "management": (70, 130, 180),      # Голубой - руководство
    "deputy": (65, 105, 225),           # Синий - заместители
    "admin": (95, 158, 160),            # Бирюзовый - административные
    "service": (72, 209, 204),          # Аквамарин - службы
    "medical": (60, 179, 113),          # Зеленый - медицинские
    "support": (255, 165, 0),           # Оранжевый - вспомогательные
}

# Цвета для направлений связей
CONNECTION_COLORS = {
    "medical": (60, 179, 113),          # Зеленый - медицинские связи
    "admin": (95, 158, 160),            # Бирюзовый - административные связи
    "finance": (218, 165, 32),          # Золотой - финансовые связи
    "support": (255, 140, 0),           # Темно-оранжевый - вспомогательные связи
}

# Шрифты (будут динамически масштабироваться)
def get_scaled_font(base_size, scale_factor=1.0):
    size = max(10, int(base_size * SCREEN_WIDTH / BASE_WIDTH * scale_factor))
    try:
        return pygame.font.SysFont("Arial", size)
    except:
        return pygame.font.Font(None, size)

# Структура данных для главной диаграммы (координаты будут рассчитываться динамически)
diagrams = {
    "main": {
        "title": "Основная организационная структура",
        "nodes": [
            # Руководство (верхний уровень)
            {"id": "director", "label": "Главный врач", "size": (250, 50), 
             "color": COLORS["management"],
             "info": "Руководитель учреждения. Отвечает за общее управление больницей, стратегическое планирование, финансово-хозяйственную деятельность и взаимодействие с вышестоящими органами здравоохранения."},
            
            # Заместители (второй уровень)
            {"id": "deputy1", "label": "Зам. по акушерству", "size": (200, 35),
             "color": COLORS["deputy"],
             "info": "Курирует родильное отделение, гинекологию, женскую консультацию и неонатологию. Отвечает за организацию помощи беременным и роженицам."},
            {"id": "deputy2", "label": "Зам. по детству", "size": (180, 35),
             "color": COLORS["deputy"],
             "info": "Руководит педиатрической службой, включая детский стационар, поликлинику и отделение новорожденных. Отвечает за здоровье детей от 0 до 18 лет."},
            {"id": "deputy3", "label": "Зам. по экспертизе", "size": (200, 35),
             "color": COLORS["deputy"],
             "info": "Курирует медико-социальную экспертизу, врачебные комиссии, оформление инвалидности и больничных листов."},
            {"id": "deputy4", "label": "Зам. по контролю", "size": (220, 35),
             "color": COLORS["deputy"],
             "info": "Отвечает за внутренний контроль качества медицинской помощи, эпидемиологическую безопасность и соблюдение санэпидрежима."},
            {"id": "deputy5", "label": "Зам. по экономике", "size": (200, 35),
             "color": COLORS["deputy"],
             "info": "Руководит финансово-экономической службой, бухгалтерией, закупками и материально-техническим обеспечением."},
            {"id": "deputy6", "label": "Зам. по поликлинике", "size": (200, 35),
             "color": COLORS["deputy"],
             "info": "Курирует взрослую поликлинику, дневной стационар, сельские амбулатории и профилактическую работу."},
            {"id": "deputy7", "label": "Зам. по хирургии", "size": (200, 35),
             "color": COLORS["deputy"],
             "info": "Руководит хирургической службой, включая операционный блок, отделения гнойной и пластической хирургии, травматологию."},
            
            # Административные подразделения (третий уровень)
            {"id": "accounting", "label": "Главный бухгалтер", "size": (200, 35),
             "color": COLORS["admin"],
             "info": "Отвечает за финансовую деятельность больницы: бухгалтерский учет, расчет зарплат, отчетность в налоговые органы и фонды."},
            {"id": "nurse", "label": "Главная медсестра", "size": (180, 35),
             "color": COLORS["admin"],
             "info": "Руководит средним и младшим медицинским персоналом, организует сестринский уход, контролирует выполнение процедур."},
            {"id": "org_method", "label": "Орг.-метод. кабинет", "size": (200, 35),
             "color": COLORS["admin"],
             "info": "Занимается организацией лечебного процесса, внедрением новых методик, повышением квалификации персонала."},
            {"id": "statistics", "label": "Мед. статистика", "size": (180, 35),
             "color": COLORS["admin"],
             "info": "Ведет учет медицинской документации, формирует статистические отчеты, анализирует показатели здоровья населения."},
            {"id": "pharmacy", "label": "Лекарственное обесп.", "size": (200, 35),
             "color": COLORS["service"],
             "info": "Обеспечивает больницу лекарственными средствами, изделиями медицинского назначения, ведет их учет и хранение."},
            {"id": "transfusiology", "label": "Трансфузиология", "size": (180, 35),
             "color": COLORS["service"],
             "info": "Отвечает за заготовку, хранение и обеспечение безопасности донорской крови и ее компонентов."},
            {"id": "it", "label": "Информ. технологии", "size": (200, 35),
             "color": COLORS["service"],
             "info": "Поддерживает работу компьютерных систем, медицинских информационных систем, сетей и оборудования."},
            
            # Основные подразделения (четвертый уровень)
            {"id": "hospital", "label": "Стационар", "size": (180, 40), 
             "subunits": ["Терапевтический", "Хирургический", "Акушерство", "Педиатрия"],
             "color": COLORS["medical"],
             "info": "Основное лечебное подразделение для круглосуточного лечения пациентов. Включает 4 профильных отделения."},
            {"id": "clinic", "label": "Поликлиника", "size": (160, 40), 
             "subunits": ["Взрослая", "Детская"],
             "color": COLORS["medical"],
             "info": "Оказание амбулаторной помощи населению, профилактические осмотры, диспансеризация."},
            {"id": "emergency", "label": "Скорая помощь", "size": (180, 40), 
             "subunits": ["Городские посты", "Сельские посты", "Мобильные бригады"],
             "color": COLORS["medical"],
             "info": "Оказание экстренной медицинской помощи, транспортировка пациентов в стационар."},
            {"id": "diagnostics", "label": "Диагностика", "size": (180, 40), 
             "subunits": ["Лаборатория", "УЗИ", "Рентген", "Эндоскопия"],
             "color": COLORS["medical"],
             "info": "Проведение лабораторных и инструментальных исследований для диагностики заболеваний."},
            {"id": "women", "label": "Жен. консультация", "size": (200, 40), 
             "subunits": ["Пренатальная диагностика", "Школа материнства"],
             "color": COLORS["support"],
             "info": "Оказание помощи беременным, планирование семьи, наблюдение за женским здоровьем."},
            {"id": "day_hospital", "label": "Дневной стац.", "size": (160, 40), 
             "subunits": ["Терапевтический", "Офтальмологический", "Диализ"],
             "color": COLORS["support"],
             "info": "Лечение пациентов без круглосуточного пребывания в стационаре."},
            {"id": "support", "label": "Вспом. службы", "size": (180, 40), 
             "subunits": ["Физиотерапия", "ЛФК", "Массаж"],
             "color": COLORS["support"],
             "info": "Обеспечивает восстановительное лечение и реабилитацию пациентов."},
            
            # Детское и сельское направление (нижний уровень)
            {"id": "children", "label": "Дет. поликлиника", "size": (200, 35), 
             "subunits": ["Педиатрия", "Профилактика", "Школьная медицина"],
             "color": COLORS["medical"],
             "info": "Специализированная помощь детям, вакцинация, патронаж новорожденных."},
            {"id": "rural", "label": "Сельск. амбулатории", "size": (200, 35), 
             "subunits": ["Бобровская", "Родиновская", "ФАПы"],
             "color": COLORS["medical"],
             "info": "Обеспечение медицинской помощью жителей сельской местности, выездные бригады."},
        ],
        "connections": [
            # Связи руководства
            ("director", "deputy1", "admin"),
            ("director", "deputy2", "admin"),
            ("director", "deputy3", "admin"),
            ("director", "deputy4", "admin"),
            ("director", "deputy5", "admin"),
            ("director", "deputy6", "admin"),
            ("director", "deputy7", "admin"),
            
            # Связи заместителей с подразделениями
            ("deputy1", "hospital", "medical"),
            ("deputy1", "women", "medical"),
            ("deputy2", "children", "medical"),
            ("deputy3", "diagnostics", "medical"),
            ("deputy4", "emergency", "medical"),
            ("deputy5", "accounting", "finance"),
            ("deputy5", "support", "finance"),
            ("deputy6", "clinic", "medical"),
            ("deputy6", "day_hospital", "medical"),
            ("deputy6", "rural", "medical"),
            ("deputy7", "it", "admin"),
            
            # Связи административных
            ("deputy4", "nurse", "admin"),
            ("deputy4", "org_method", "admin"),
            ("deputy4", "statistics", "admin"),
            ("deputy5", "pharmacy", "admin"),
            ("deputy5", "transfusiology", "admin"),
            
            # Связи между подразделениями
            ("hospital", "clinic", "medical"),
            ("hospital", "emergency", "medical"),
            ("hospital", "diagnostics", "medical"),
            ("clinic", "rural", "medical"),
            ("diagnostics", "support", "medical"),
        ]
    }
}

# Коэффициент масштабирования
SCALE_FACTOR = min(SCREEN_WIDTH / BASE_WIDTH, SCREEN_HEIGHT / BASE_HEIGHT)

# Функция для масштабирования размеров
def scale_size(size):
    return (int(size[0] * SCALE_FACTOR), int(size[1] * SCALE_FACTOR))

# Функция для масштабирования позиций
def scale_pos(pos):
    return (int(pos[0] * SCALE_FACTOR), int(pos[1] * SCALE_FACTOR))

# Функция для масштабирования значений
def scale_value(value):
    return int(value * SCALE_FACTOR)

# Текущая диаграмма
current_diagram = "main"
scroll_offset = 0
scroll_speed = scale_value(30)
dragging = False
drag_start_pos = (0, 0)
selected_node = None
zoom_level = 0.85
info_panel_width = scale_value(300)
show_info_panel = False
min_zoom = 0.7
max_zoom = 1.5
show_instructions = True
show_legend = True
show_all_subunits = False
fullscreen = False

# Рассчитываем позиции узлов на основе разрешения экрана
def calculate_node_positions():
    diagram = diagrams["main"]
    nodes = diagram["nodes"]
    
    # Рассчитываем базовые позиции в зависимости от разрешения
    base_x = SCREEN_WIDTH // 2
    vertical_spacing = scale_value(80)
    
    # Руководство (верхний уровень)
    nodes[0]["pos"] = (base_x, scale_value(70))
    
    # Заместители (второй уровень)
    deputy_count = 7
    deputy_spacing = scale_value(150)
    start_x = base_x - (deputy_count - 1) * deputy_spacing // 2
    
    for i in range(7):
        nodes[1+i]["pos"] = (start_x + i * deputy_spacing, scale_value(150))
    
    # Административные подразделения (третий уровень)
    admin_count = 7
    admin_spacing = scale_value(150)
    start_x = base_x - (admin_count - 1) * admin_spacing // 2
    
    for i in range(7):
        nodes[8+i]["pos"] = (start_x + i * admin_spacing, scale_value(230))
    
    # Основные подразделения (четвертый уровень)
    main_count = 7
    main_spacing = scale_value(150)
    start_x = base_x - (main_count - 1) * main_spacing // 2
    
    for i in range(7):
        nodes[15+i]["pos"] = (start_x + i * main_spacing, scale_value(320))
    
    # Детское и сельское направление (нижний уровень)
    nodes[22]["pos"] = (base_x - scale_value(300), scale_value(410))
    nodes[23]["pos"] = (base_x + scale_value(300), scale_value(410))

# Инициализируем позиции
calculate_node_positions()

# Функция для преобразования координат с учетом масштаба и скролла
def transform_pos(x, y):
    return (x * zoom_level, (y + scroll_offset) * zoom_level)

# Функция для отрисовки диаграммы
def draw_diagram(diagram_key):
    diagram = diagrams[diagram_key]
    
    # Отрисовка заголовка
    title_font = get_scaled_font(28, zoom_level)
    title = title_font.render(diagram["title"], True, HEADER_COLOR)
    screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, scale_value(10)))
    
    # Отрисовка соединений
    for connection in diagram["connections"]:
        node1 = next((n for n in diagram["nodes"] if n["id"] == connection[0]), None)
        node2 = next((n for n in diagram["nodes"] if n["id"] == connection[1]), None)
        color_type = connection[2] if len(connection) > 2 else "default"
        color = CONNECTION_COLORS.get(color_type, CONNECTION_COLOR)
        
        if node1 and node2:
            # Преобразуем координаты с учетом масштаба и скролла
            x1, y1 = transform_pos(*node1["pos"])
            x2, y2 = transform_pos(*node2["pos"])
            
            # Рассчитываем среднюю точку по Y
            mid_y = (y1 + y2) / 2
            
            # Рисуем соединение в виде трех сегментов
            pygame.draw.line(screen, color, (x1, y1), (x1, mid_y), scale_value(2))
            pygame.draw.line(screen, color, (x1, mid_y), (x2, mid_y), scale_value(2))
            pygame.draw.line(screen, color, (x2, mid_y), (x2, y2), scale_value(2))
            
            # Рисуем стрелку на последнем сегменте
            arrow_size = scale_value(8) * zoom_level
            angle = math.pi/2 if y2 > mid_y else -math.pi/2
            
            pygame.draw.polygon(screen, color, [
                (x2, y2),
                (x2 - arrow_size, y2 - arrow_size * (1 if angle > 0 else -1)),
                (x2 + arrow_size, y2 - arrow_size * (1 if angle > 0 else -1))
            ])
    
    # Отрисовка узлов
    for node in diagram["nodes"]:
        # Преобразуем координаты с учетом масштаба и скролла
        x, y = transform_pos(*node["pos"])
        width, height = scale_size(node["size"])
        width *= zoom_level
        height *= zoom_level
        
        # Цвет узла
        node_color = node.get("color", BOX_COLOR)
        
        # Рисуем прямоугольник узла
        color = HIGHLIGHT if selected_node == node["id"] else node_color
        pygame.draw.rect(screen, color, (x - width//2, y - height//2, width, height), 0, scale_value(6))
        pygame.draw.rect(screen, BOX_BORDER, (x - width//2, y - height//2, width, height), scale_value(1), scale_value(6))
        
        # Рисуем текст узла
        node_font = get_scaled_font(14, zoom_level)
        label = node["label"]
        
        # Разбиваем длинные названия на две строки
        if len(label) > 15:
            parts = label.split()
            if len(parts) > 1:
                # Разделяем на две строки по последнему пробелу
                split_index = len(parts) // 2
                line1 = " ".join(parts[:split_index])
                line2 = " ".join(parts[split_index:])
                
                label1 = node_font.render(line1, True, TEXT_COLOR)
                label2 = node_font.render(line2, True, TEXT_COLOR)
                
                screen.blit(label1, (x - label1.get_width()//2, y - height//4))
                screen.blit(label2, (x - label2.get_width()//2, y + height//8))
            else:
                label_text = node_font.render(label, True, TEXT_COLOR)
                text_rect = label_text.get_rect(center=(x, y))
                screen.blit(label_text, text_rect)
        else:
            label_text = node_font.render(label, True, TEXT_COLOR)
            text_rect = label_text.get_rect(center=(x, y))
            screen.blit(label_text, text_rect)
        
        # Рисуем подразделения, если они есть и узел выбран или включен режим показа всех
        if "subunits" in node and (selected_node == node["id"] or show_all_subunits):
            subunit_y = y + height//2 + scale_value(10)
            small_font = get_scaled_font(11, zoom_level)
            
            for subunit in node["subunits"]:
                sub_width = scale_value(160) * zoom_level
                sub_height = scale_value(22) * zoom_level
                
                pygame.draw.rect(screen, SUBUNIT_COLOR, 
                                (x - sub_width//2, subunit_y, sub_width, sub_height), 0, scale_value(4))
                pygame.draw.rect(screen, BOX_BORDER, 
                                (x - sub_width//2, subunit_y, sub_width, sub_height), scale_value(1), scale_value(4))
                
                sub_label = small_font.render(subunit, True, TEXT_COLOR)
                screen.blit(sub_label, (x - sub_label.get_width()//2, subunit_y + scale_value(3)))
                subunit_y += scale_value(26) * zoom_level
    
    return len(diagram["nodes"]) * scale_value(80)

# Функция для проверки попадания в узел
def check_node_hit(diagram_key, pos):
    diagram = diagrams[diagram_key]
    for node in diagram["nodes"]:
        # Преобразуем координаты с учетом масштаба и скролла
        x, y = transform_pos(*node["pos"])
        width, height = scale_size(node["size"])
        width *= zoom_level
        height *= zoom_level
        
        rect = pygame.Rect(x - width//2, y - height//2, width, height)
        if rect.collidepoint(pos):
            return node
    return None

# Функция для отрисовки информационной панели
def draw_info_panel(node):
    if not node or not show_info_panel:
        return
    
    # Шрифты
    header_font = get_scaled_font(20)
    info_font = get_scaled_font(13)
    small_font = get_scaled_font(11)
    
    # Рассчитываем ширину панели
    panel_width = scale_value(300)
    
    # Рисуем фон панели
    pygame.draw.rect(screen, (250, 250, 255), (SCREEN_WIDTH - panel_width, 0, panel_width, SCREEN_HEIGHT))
    pygame.draw.rect(screen, HEADER_COLOR, (SCREEN_WIDTH - panel_width, 0, panel_width, scale_value(35)))
    
    # Заголовок панели
    title = header_font.render("Информация", True, BOX_COLOR)
    screen.blit(title, (SCREEN_WIDTH - panel_width + scale_value(10), scale_value(5)))
    
    # Название отдела
    name_label = info_font.render(node['label'], True, TEXT_COLOR)
    pygame.draw.rect(screen, (240, 240, 250), 
                    (SCREEN_WIDTH - panel_width + scale_value(10), scale_value(40), 
                     panel_width - scale_value(20), scale_value(30)))
    pygame.draw.rect(screen, BOX_BORDER, 
                    (SCREEN_WIDTH - panel_width + scale_value(10), scale_value(40), 
                     panel_width - scale_value(20), scale_value(30)), scale_value(1), scale_value(4))
    screen.blit(name_label, (SCREEN_WIDTH - panel_width + scale_value(15), scale_value(45)))
    
    # Дополнительная информация
    if "info" in node:
        info_text = node["info"]
    else:
        info_text = "Подробная информация об этом подразделении."
    
    # Рендерим текст с переносами
    y_pos = scale_value(85)
    info_label = info_font.render("Описание:", True, HEADER_COLOR)
    screen.blit(info_label, (SCREEN_WIDTH - panel_width + scale_value(10), y_pos))
    y_pos += scale_value(25)
    
    words = info_text.split()
    line = ""
    for word in words:
        test_line = line + word + " "
        if info_font.size(test_line)[0] < panel_width - scale_value(20):
            line = test_line
        else:
            rendered = info_font.render(line, True, TEXT_COLOR)
            screen.blit(rendered, (SCREEN_WIDTH - panel_width + scale_value(10), y_pos))
            y_pos += scale_value(20)
            line = word + " "
    
    if line:
        rendered = info_font.render(line, True, TEXT_COLOR)
        screen.blit(rendered, (SCREEN_WIDTH - panel_width + scale_value(10), y_pos))
        y_pos += scale_value(25)
    
    # Подразделения
    if "subunits" in node:
        y_pos += scale_value(10)
        sub_title = info_font.render("Подразделения:", True, HEADER_COLOR)
        screen.blit(sub_title, (SCREEN_WIDTH - panel_width + scale_value(10), y_pos))
        y_pos += scale_value(25)
        
        for subunit in node["subunits"]:
            pygame.draw.rect(screen, SUBUNIT_COLOR, 
                           (SCREEN_WIDTH - panel_width + scale_value(15), y_pos, 
                            panel_width - scale_value(25), scale_value(22)), 0, scale_value(4))
            pygame.draw.rect(screen, BOX_BORDER, 
                           (SCREEN_WIDTH - panel_width + scale_value(15), y_pos, 
                            panel_width - scale_value(25), scale_value(22)), scale_value(1), scale_value(4))
            sub_label = small_font.render(subunit, True, TEXT_COLOR)
            screen.blit(sub_label, (SCREEN_WIDTH - panel_width + scale_value(20), y_pos + scale_value(3)))
            y_pos += scale_value(28)

# Функция для отрисовки легенды
def draw_legend():
    if not show_legend:
        return None
    
    # Шрифты
    header_font = get_scaled_font(20)
    info_font = get_scaled_font(13)
    small_font = get_scaled_font(11)
    
    # Оптимальные размеры для читаемости
    legend_width = scale_value(260)
    legend_height = scale_value(300)
    legend_x = scale_value(20)
    legend_y = scale_value(60)
    
    # Фон легенды
    pygame.draw.rect(screen, (250, 250, 255), (legend_x, legend_y, legend_width, legend_height))
    pygame.draw.rect(screen, HEADER_COLOR, (legend_x, legend_y, legend_width, scale_value(30)))
    pygame.draw.rect(screen, BOX_BORDER, (legend_x, legend_y, legend_width, legend_height), scale_value(1), scale_value(4))
    
    # Заголовок легенды
    title = small_font.render("Легенда организационной структуры", True, BOX_COLOR)
    screen.blit(title, (legend_x + legend_width//2 - title.get_width()//2, legend_y + scale_value(8)))
    
    # Содержимое легенды
    y_pos = legend_y + scale_value(40)
    
    # Легенда для узлов
    node_title = info_font.render("Категории узлов:", True, HEADER_COLOR)
    screen.blit(node_title, (legend_x + scale_value(15), y_pos))
    y_pos += scale_value(25)
    
    categories = [
        ("Руководство", COLORS["management"]),
        ("Заместители", COLORS["deputy"]),
        ("Административные", COLORS["admin"]),
        ("Службы", COLORS["service"]),
        ("Медицинские", COLORS["medical"]),
        ("Вспомогательные", COLORS["support"])
    ]
    
    for name, color in categories:
        pygame.draw.rect(screen, color, (legend_x + scale_value(15), y_pos, scale_value(18), scale_value(18)), 0, scale_value(4))
        pygame.draw.rect(screen, BOX_BORDER, (legend_x + scale_value(15), y_pos, scale_value(18), scale_value(18)), scale_value(1), scale_value(4))
        label = small_font.render(name, True, TEXT_COLOR)
        screen.blit(label, (legend_x + scale_value(40), y_pos))
        y_pos += scale_value(25)
    
    # Легенда для связей
    y_pos += scale_value(10)
    conn_title = info_font.render("Типы связей:", True, HEADER_COLOR)
    screen.blit(conn_title, (legend_x + scale_value(15), y_pos))
    y_pos += scale_value(25)
    
    connections = [
        ("Медицинские", CONNECTION_COLORS["medical"]),
        ("Административные", CONNECTION_COLORS["admin"]),
        ("Финансовые", CONNECTION_COLORS["finance"]),
        ("Вспомогательные", CONNECTION_COLORS["support"])
    ]
    
    for name, color in connections:
        pygame.draw.line(screen, color, (legend_x + scale_value(15), y_pos + scale_value(9)), 
                        (legend_x + scale_value(70), y_pos + scale_value(9)), scale_value(3))
        label = small_font.render(name, True, TEXT_COLOR)
        screen.blit(label, (legend_x + scale_value(80), y_pos))
        y_pos += scale_value(25)
    
    # Кнопка закрытия
    close_btn = pygame.Rect(legend_x + legend_width - scale_value(35), legend_y + scale_value(5), 
                          scale_value(30), scale_value(20))
    pygame.draw.rect(screen, (220, 100, 100), close_btn, 0, scale_value(4))
    close_text = small_font.render("X", True, BOX_COLOR)
    screen.blit(close_text, (close_btn.centerx - close_text.get_width()//2, 
                            close_btn.centery - close_text.get_height()//2))
    
    return close_btn

# Функция для отрисовки инструкций
def draw_instructions():
    if not show_instructions:
        return None
    
    # Шрифты
    header_font = get_scaled_font(20)
    info_font = get_scaled_font(13)
    small_font = get_scaled_font(11)
    
    # Оптимальные размеры для читаемости
    inst_width = scale_value(300)
    inst_height = scale_value(300)
    inst_x = SCREEN_WIDTH - inst_width - scale_value(20)
    inst_y = scale_value(20)
    
    # Фон инструкций
    pygame.draw.rect(screen, (250, 250, 255), (inst_x, inst_y, inst_width, inst_height))
    pygame.draw.rect(screen, HEADER_COLOR, (inst_x, inst_y, inst_width, scale_value(30)))
    pygame.draw.rect(screen, BOX_BORDER, (inst_x, inst_y, inst_width, inst_height), scale_value(1), scale_value(4))
    
    # Заголовок инструкций
    title = small_font.render("Управление диаграммой", True, BOX_COLOR)
    screen.blit(title, (inst_x + inst_width//2 - title.get_width()//2, inst_y + scale_value(8)))
    
    # Содержимое инструкций
    y_pos = inst_y + scale_value(40)
    
    instructions = [
        "Колесо мыши: Прокрутка",
        "Правая кнопка: Перетаскивание",
        "+/-: Масштабирование",
        "R: Сброс вида",
        "Левая кнопка: Выбор узла",
        "I: Информация",
        "L: Легенда",
        "H: Инструкции",
        "S: Подразделения",
        "F: Полный экран",
        "ESC: Выход"
    ]
    
    # Используем увеличенный шрифт для читаемости
    for text in instructions:
        instruction = small_font.render(text, True, TEXT_COLOR)
        screen.blit(instruction, (inst_x + scale_value(20), y_pos))
        y_pos += scale_value(25)
    
    # Кнопка закрытия
    close_btn = pygame.Rect(inst_x + inst_width - scale_value(35), inst_y + scale_value(5), 
                          scale_value(30), scale_value(20))
    pygame.draw.rect(screen, (220, 100, 100), close_btn, 0, scale_value(4))
    close_text = small_font.render("X", True, BOX_COLOR)
    screen.blit(close_text, (close_btn.centerx - close_text.get_width()//2, 
                            close_btn.centery - close_text.get_height()//2))
    
    return close_btn

# Функция для отрисовки кнопок управления
def draw_control_buttons():
    buttons = []
    
    # Шрифт для кнопок
    button_font = get_scaled_font(14)
    
    # Кнопка сброса масштаба
    reset_btn = pygame.Rect(SCREEN_WIDTH - scale_value(140), SCREEN_HEIGHT - scale_value(40), 
                          scale_value(130), scale_value(30))
    pygame.draw.rect(screen, ACCENT_COLOR, reset_btn, 0, scale_value(5))
    reset_text = button_font.render("Сбросить вид", True, BOX_COLOR)
    screen.blit(reset_text, (reset_btn.centerx - reset_text.get_width()//2, 
                           reset_btn.centery - reset_text.get_height()//2))
    buttons.append(("reset", reset_btn))
    
    # Кнопка показа/скрытия подразделений
    sub_btn = pygame.Rect(SCREEN_WIDTH - scale_value(140), SCREEN_HEIGHT - scale_value(80), 
                        scale_value(130), scale_value(30))
    btn_color = (60, 179, 113) if show_all_subunits else ACCENT_COLOR
    pygame.draw.rect(screen, btn_color, sub_btn, 0, scale_value(5))
    btn_text = "Скрыть подразделения" if show_all_subunits else "Показать подразделения"
    sub_text = button_font.render(btn_text, True, BOX_COLOR)
    screen.blit(sub_text, (sub_btn.centerx - sub_text.get_width()//2, 
                         sub_btn.centery - sub_text.get_height()//2))
    buttons.append(("subunits", sub_btn))
    
    # Кнопка полноэкранного режима
    fullscreen_btn = pygame.Rect(SCREEN_WIDTH - scale_value(140), SCREEN_HEIGHT - scale_value(120), 
                               scale_value(130), scale_value(30))
    btn_color = (180, 100, 220) if fullscreen else ACCENT_COLOR
    pygame.draw.rect(screen, btn_color, fullscreen_btn, 0, scale_value(5))
    btn_text = "Оконный режим" if fullscreen else "Полный экран"
    fullscreen_text = button_font.render(btn_text, True, BOX_COLOR)
    screen.blit(fullscreen_text, (fullscreen_btn.centerx - fullscreen_text.get_width()//2, 
                                fullscreen_btn.centery - fullscreen_text.get_height()//2))
    buttons.append(("fullscreen", fullscreen_btn))
    
    return buttons

# Функция для переключения полноэкранного режима
def toggle_fullscreen():
    global fullscreen, screen, SCREEN_WIDTH, SCREEN_HEIGHT
    
    fullscreen = not fullscreen
    if fullscreen:
        # Получаем размеры основного дисплея
        info = pygame.display.Info()
        SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
    else:
        # Возвращаемся к обычному размеру
        SCREEN_WIDTH, SCREEN_HEIGHT = display_info.current_w, display_info.current_h
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    
    # Пересчитываем позиции узлов
    calculate_node_positions()
    
    # Обновляем масштаб
    global SCALE_FACTOR
    SCALE_FACTOR = min(SCREEN_WIDTH / BASE_WIDTH, SCREEN_HEIGHT / BASE_HEIGHT)

# Функция для обработки изменения размера окна
def handle_resize(event):
    global SCREEN_WIDTH, SCREEN_HEIGHT, SCALE_FACTOR
    
    if not fullscreen:
        SCREEN_WIDTH, SCREEN_HEIGHT = event.w, event.h
        SCALE_FACTOR = min(SCREEN_WIDTH / BASE_WIDTH, SCREEN_HEIGHT / BASE_HEIGHT)
        calculate_node_positions()

# Основной цикл
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Обработка изменения размера окна
        if event.type == pygame.VIDEORESIZE:
            handle_resize(event)
        
        # Обработка прокрутки
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Прокрутка вверх
                scroll_offset = max(-SCREEN_HEIGHT//2, scroll_offset - scroll_speed)
            if event.button == 5:  # Прокрутка вниз
                scroll_offset = min(SCREEN_HEIGHT//2, scroll_offset + scroll_speed)
            if event.button == 1:  # Левая кнопка мыши
                pos = pygame.mouse.get_pos()
                
                # Проверка клика по узлу
                node = check_node_hit(current_diagram, pos)
                if node:
                    selected_node = node["id"]
                    show_info_panel = True
                else:
                    selected_node = None
                    show_info_panel = False
                
                # Проверка клика по кнопке закрытия легенды
                if show_legend:
                    close_btn = draw_legend()
                    if close_btn and close_btn.collidepoint(pos):
                        show_legend = False
                
                # Проверка клика по кнопке закрытия инструкций
                if show_instructions:
                    close_btn = draw_instructions()
                    if close_btn and close_btn.collidepoint(pos):
                        show_instructions = False
                
                # Проверка клика по кнопкам управления
                control_buttons = draw_control_buttons()
                for btn_id, btn_rect in control_buttons:
                    if btn_rect.collidepoint(pos):
                        if btn_id == "reset":
                            zoom_level = 0.85
                            scroll_offset = 0
                        elif btn_id == "subunits":
                            show_all_subunits = not show_all_subunits
                        elif btn_id == "fullscreen":
                            toggle_fullscreen()
        
        # Обработка перетаскивания
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  # Правая кнопка мыши
            dragging = True
            drag_start_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            dragging = False
        if event.type == pygame.MOUSEMOTION and dragging:
            current_pos = pygame.mouse.get_pos()
            dx = current_pos[0] - drag_start_pos[0]
            dy = current_pos[1] - drag_start_pos[1]
            drag_start_pos = current_pos
            scroll_offset += dy / zoom_level
        
        # Обработка масштабирования и других клавиш
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                zoom_level = min(max_zoom, zoom_level + 0.1)
            if event.key == pygame.K_MINUS:
                zoom_level = max(min_zoom, zoom_level - 0.1)
            if event.key == pygame.K_i:
                show_info_panel = not show_info_panel
                if not show_info_panel:
                    selected_node = None
            if event.key == pygame.K_r:  # Сброс масштаба и позиции
                zoom_level = 0.85
                scroll_offset = 0
            if event.key == pygame.K_h:  # Показать/скрыть инструкции
                show_instructions = not show_instructions
            if event.key == pygame.K_l:  # Показать/скрыть легенду
                show_legend = not show_legend
            if event.key == pygame.K_s:  # Показать/скрыть все подразделения
                show_all_subunits = not show_all_subunits
            if event.key == pygame.K_f:  # Переключение полноэкранного режима
                toggle_fullscreen()
            if event.key == pygame.K_ESCAPE:  # Выход по ESC
                running = False
    
    # Отрисовка
    screen.fill(BACKGROUND)
    
    # Отрисовка диаграммы
    draw_diagram(current_diagram)
    
    # Информационная панель
    if show_info_panel and selected_node:
        node = next((n for n in diagrams[current_diagram]["nodes"] if n["id"] == selected_node), None)
        if node:
            draw_info_panel(node)
    
    # Отрисовка легенды
    if show_legend:
        draw_legend()
    
    # Отрисовка инструкций
    if show_instructions:
        draw_instructions()
    else:
        # Отображение подсказки о вызове инструкций
        hint_font = get_scaled_font(11)
        hint = hint_font.render("H: Инструкции, L: Легенда, S: Подразделения, F: Полный экран", True, (100, 100, 120))
        screen.blit(hint, (scale_value(10), SCREEN_HEIGHT - scale_value(20)))
    
    # Отрисовка кнопок управления
    draw_control_buttons()
    
    # Отображение масштаба
    hint_font = get_scaled_font(11)
    zoom_text = hint_font.render(f"Масштаб: {zoom_level:.1f}x", True, (100, 100, 120))
    screen.blit(zoom_text, (scale_value(10), SCREEN_HEIGHT - scale_value(40)))
    
    # Отображение смещения
    offset_text = hint_font.render(f"Смещение: {scroll_offset:.0f}", True, (100, 100, 120))
    screen.blit(offset_text, (scale_value(10), SCREEN_HEIGHT - scale_value(60)))
    
    # Отображение режима экрана
    mode_text = hint_font.render(f"Режим: {'Полный экран' if fullscreen else 'Оконный'}", True, (100, 100, 120))
    screen.blit(mode_text, (scale_value(10), SCREEN_HEIGHT - scale_value(80)))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()