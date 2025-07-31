import pygame  # وارد کردن کتابخانه pygame برای ساخت بازی
import sys     # وارد کردن sys برای استفاده از خروج از برنامه (sys.exit)

pygame.init()  # راه‌اندازی تمام ماژول‌های pygame (ضروری برای شروع)

# تنظیمات پنجره بازی
WIDTH, HEIGHT = 700, 600  # تعیین عرض و ارتفاع پنجره
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # ایجاد پنجره با اندازه مشخص
pygame.display.set_caption("Snakes and Ladders - Menu")  # تنظیم عنوان پنجره

# فونت‌ها
FONT = pygame.font.SysFont("arial", 28)       # فونت بزرگ برای تیترها
SMALL_FONT = pygame.font.SysFont("arial", 22) # فونت کوچک برای نوشته‌های بازیکنان

# رنگ‌ها
WHITE = (255, 255, 255)  # سفید
GRAY = (200, 200, 200)   # خاکستری
BLACK = (0, 0, 0)        # مشکی
BUTTON_COLOR = (100, 180, 255)  # رنگ دکمه‌ها (آبی روشن)
PLAYER_COLORS = [             # لیست رنگ‌هایی که بازیکنان می‌توانند انتخاب کنند
    (255, 0, 0),    # قرمز
    (0, 0, 255),    # آبی
    (0, 128, 0),    # سبز
    (255, 165, 0)   # نارنجی
]

# وضعیت‌های اولیه بازی
menu_state = "main"      # وضعیت منو (main = صفحه اول، form = فرم بازیکنان)
input_boxes = []         # لیست جعبه‌های ورودی برای نام بازیکنان
players = []             # لیست بازیکنان نهایی (نام و رنگ)
num_players = 2          # تعداد بازیکنان پیش‌فرض
selected_color = [0, 1, 2, 3]  # انتخاب رنگ برای هر بازیکن (اشاره به اندیس PLAYER_COLORS)

# کلاس InputBox برای گرفتن نام بازیکن
class InputBox:
    def __init__(self, x, y, w, h, text=''):  # سازنده با موقعیت و اندازه و متن اولیه
        self.rect = pygame.Rect(x, y, w, h)  # تعریف مستطیل ورودی
        self.base_color = GRAY              # رنگ پیش‌فرض خاکستری
        self.active_color = (0, 120, 255)    # رنگ فعال آبی
        self.color = self.base_color         # رنگ فعلی با مقدار پیش‌فرض
        self.text = text                     # متن داخل باکس
        self.txt_surface = FONT.render(text, True, BLACK)  # ایجاد سطح متن برای نمایش
        self.active = False                  # مشخص می‌کند که آیا باکس فعال است یا نه

    def handle_event(self, event):  # تابع مدیریت رویدادها
        if event.type == pygame.MOUSEBUTTONDOWN:  # اگر کلیک شد
            if self.rect.collidepoint(event.pos):  # اگر روی این باکس کلیک شده بود
                self.active = True               # فعال شود
                self.color = self.active_color   # رنگ به آبی تغییر کند
            else:
                self.active = False              # در غیر این صورت غیرفعال شود
                self.color = self.base_color     # و به خاکستری برگردد
        if event.type == pygame.KEYDOWN and self.active:  # اگر کلید زده شد و باکس فعال بود
            if event.key == pygame.K_RETURN:     # اگر Enter زده شد
                self.active = False              # باکس غیرفعال شود
                self.color = self.base_color     # رنگ به خاکستری تغییر کند
            elif event.key == pygame.K_BACKSPACE:  # اگر Backspace زده شد
                self.text = self.text[:-1]         # یک حرف از انتها حذف شود
            elif len(self.text) < 12:              # اگر طول متن کمتر از ۱۲ کاراکتر بود
                self.text += event.unicode         # حرف جدید به متن اضافه شود
            self.txt_surface = FONT.render(self.text, True, BLACK)  # متن دوباره رسم شود

    def draw(self, screen):  # تابع رسم باکس روی صفحه
        pygame.draw.rect(screen, self.color, self.rect, 2)  # کشیدن مستطیل با رنگ
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 1))  # نمایش متن داخل باکس

# تابع برای رسم دکمه‌ها
def draw_button(text, x, y, w, h):
    rect = pygame.Rect(x, y, w, h)                    # ایجاد مستطیل دکمه
    pygame.draw.rect(screen, BUTTON_COLOR, rect)     # کشیدن زمینه دکمه با رنگ آبی روشن
    pygame.draw.rect(screen, BLACK, rect, 2)         # کشیدن کادر مشکی دور دکمه
    label = FONT.render(text, True, BLACK)           # نوشتن متن روی دکمه
    screen.blit(label, (x + 15, y + 10))              # نمایش متن روی دکمه
    return rect                                       # بازگرداندن مستطیل دکمه برای بررسی کلیک

# صفحه اصلی منو (اول بازی)
def draw_main_menu():
    screen.fill(WHITE)  # پاک کردن صفحه و سفید کردن پس‌زمینه
    title = FONT.render(" Snakes and Ladders", True, BLACK)  # نوشتن عنوان بازی
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 150))  # وسط‌چین کردن عنوان
    return draw_button("Start Game", WIDTH // 2 - 100, 300, 200, 60)  # رسم دکمه شروع بازی

# فرم ورود اطلاعات بازیکنان
def draw_player_form():
    global input_boxes, selected_color  # استفاده از متغیرهای سراسری
    screen.fill(WHITE)  # سفید کردن پس‌زمینه

    label = FONT.render("Number of players:", True, BLACK)  # نوشتن برچسب تعداد بازیکن
    screen.blit(label, (50, 30))  # قرار دادن روی صفحه

    for i in range(2, 5):  # دکمه‌های ۲ تا ۴ بازیکن
        btn = draw_button(str(i), 250 + (i - 2) * 60, 25, 45, 55)  # رسم دکمه
        if num_players == i:
            pygame.draw.rect(screen, BLACK, btn, 3)  # اگر انتخاب شده، با کادر ضخیم مشخص شود

    for i in range(num_players):  # برای هر بازیکن
        name_label = SMALL_FONT.render(f"Player {i + 1} name:", True, BLACK)  # برچسب نام بازیکن
        screen.blit(name_label, (30, 100 + i * 100))  # نمایش برچسب
        input_boxes[i].draw(screen)  # رسم باکس ورودی

        color_label = SMALL_FONT.render("Color:", True, BLACK)  # برچسب رنگ
        screen.blit(color_label, (300, 100 + i * 100))  # نمایش برچسب

        for j, color in enumerate(PLAYER_COLORS):  # برای هر رنگ قابل انتخاب
            color_rect = pygame.Rect(360 + j * 50, 100 + i * 100, 30, 30)  # مستطیل رنگ
            pygame.draw.rect(screen, color, color_rect)  # رسم رنگ
            if selected_color[i] == j:
                pygame.draw.rect(screen, BLACK, color_rect, 3)  # اگر انتخاب شده، کادر مشکی دورش

    return draw_button("Start Game", WIDTH // 2 - 100, 500, 200, 50)  # دکمه شروع بازی

# تابع اصلی بازی
def main():
    global menu_state, input_boxes, num_players, selected_color
    clock = pygame.time.Clock()  # ساعت برای کنترل نرخ فریم

    input_boxes = [InputBox(160, 100 + i * 100, 120, 35) for i in range(4)]  # ساخت باکس‌های ورودی اولیه

    while True:  # حلقه اصلی بازی
        screen.fill(WHITE)  # پاک کردن صفحه

        if menu_state == "main":  # اگر در منوی اصلی هستیم
            start_btn = draw_main_menu()  # نمایش صفحه منو
        elif menu_state == "form":  # اگر در فرم بازیکنان هستیم
            start_game_btn = draw_player_form()  # نمایش فرم بازیکنان

        for event in pygame.event.get():  # بررسی تمام رویدادها
            if event.type == pygame.QUIT:  # اگر روی ضربدر کلیک شد
                pygame.quit()
                sys.exit()

            if menu_state == "main":  # اگر در صفحه اول هستیم
                if event.type == pygame.MOUSEBUTTONDOWN and start_btn.collidepoint(event.pos):
                    menu_state = "form"  # به فرم برو

            elif menu_state == "form":  # اگر در فرم بازیکنان هستیم
                if event.type == pygame.MOUSEBUTTONDOWN:  # کلیک شد
                    for i in range(2, 5):  # بررسی دکمه تعداد بازیکنان
                        btn = pygame.Rect(220 + (i - 2) * 60, 25, 50, 40)
                        if btn.collidepoint(event.pos):
                            num_players = i  # تنظیم تعداد بازیکن
                            input_boxes = [InputBox(160, 100 + i * 100, 120, 35) for i in range(num_players)]  # ساخت باکس‌ها
                            selected_color = [i % 4 for i in range(num_players)]  # رنگ اولیه

                    for i in range(num_players):  # انتخاب رنگ
                        for j in range(4):
                            color_rect = pygame.Rect(360 + j * 50, 100 + i * 100, 30, 30)
                            if color_rect.collidepoint(event.pos):
                                selected_color[i] = j

                    if start_game_btn.collidepoint(event.pos):  # اگر روی "Start Game" کلیک شد
                        players = []  # لیست بازیکنان را بساز
                        for i in range(num_players):
                            name = input_boxes[i].text.strip() or f"Player {i + 1}"  # نام وارد شده یا پیش‌فرض
                            color = PLAYER_COLORS[selected_color[i]]  # رنگ انتخابی
                            players.append((name, color))  # ذخیره بازیکن
                        print("🎉 Players:")  # چاپ بازیکنان روی کنسول
                        for p in players:
                            print(f"{p[0]} - Color: {p[1]}")
                        pygame.quit()  # بستن pygame
                        sys.exit()     # خروج از برنامه

                for box in input_boxes:  # بررسی تایپ در باکس‌ها
                    box.handle_event(event)

        pygame.display.flip()  # به‌روزرسانی صفحه
        clock.tick(30)         # محدود کردن نرخ فریم به ۳۰ فریم در ثانیه

# اجرای برنامه
if __name__ == "__main__":
    main()  # اجرای تابع اصلی
