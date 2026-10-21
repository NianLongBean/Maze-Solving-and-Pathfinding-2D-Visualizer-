import pygame as pg

class Button:
    def __init__(self, x, y, width, height, text, bg_color=(220, 220, 220), hover_color=(190, 190, 190), text_color=(0, 0, 0)):
        self.rect = pg.Rect(x, y, width, height)
        self.text = text
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.selected = False

    def draw(self, surface, font):
        mouse_pos = pg.mouse.get_pos()
        color = self.hover_color if (self.rect.collidepoint(mouse_pos) or self.selected) else self.bg_color
        pg.draw.rect(surface, color, self.rect, border_radius=4)
        pg.draw.rect(surface, (80, 80, 80), self.rect, 2, border_radius=4)

        txt_surface = font.render(self.text, True, self.text_color)
        txt_rect = txt_surface.get_rect(center=self.rect.center)
        surface.blit(txt_surface, txt_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


class Slider:
    def __init__(self, x, y, width, min_val, max_val, initial_val, label="speed"):
        self.rect = pg.Rect(x, y, width, 6)
        self.min_val = min_val
        self.max_val = max_val
        self.val = initial_val
        self.label = label
        
        ratio = (initial_val - min_val) / (max_val - min_val)
        self.handle_x = x + int(ratio * width)
        self.handle_y = y + 3
        self.handle_radius = 7
        self.dragging = False

    def draw(self, surface, font):
        lbl_surf = font.render(f"{self.label}: {self.val}ms", True, (0, 0, 0))
        surface.blit(lbl_surf, (self.rect.x, self.rect.y + 12))

        pg.draw.rect(surface, (180, 180, 180), self.rect, border_radius=3)
        active_rect = pg.Rect(self.rect.x, self.rect.y, self.handle_x - self.rect.x, self.rect.height)
        pg.draw.rect(surface, (50, 150, 240), active_rect, border_radius=3)

        pg.draw.circle(surface, (30, 30, 30), (self.handle_x, self.handle_y), self.handle_radius)

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = event.pos
            if (mouse_x - self.handle_x)**2 + (mouse_y - self.handle_y)**2 <= (self.handle_radius + 5)**2:
                self.dragging = True
            elif self.rect.collidepoint(mouse_x, mouse_y):
                self.dragging = True
                self._update_pos(mouse_x)

        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False

        elif event.type == pg.MOUSEMOTION and self.dragging:
            self._update_pos(event.pos[0])

    def _update_pos(self, mouse_x):
        self.handle_x = max(self.rect.x, min(mouse_x, self.rect.x + self.rect.width))
        ratio = (self.handle_x - self.rect.x) / self.rect.width
        self.val = int(self.min_val + ratio * (self.max_val - self.min_val))


class Dropdown:
    def __init__(self, x, y, width, height, options):
        self.rect = pg.Rect(x, y, width, height)
        self.options = options
        self.selected_index = 0
        self.is_open = False

        # Tự động xếp các ô lựa chọn mở ngược lên phía trên (Fly-up)
        # để hiển thị nguyên vẹn cả 4 thuật toán mà không bị tràn viền hay cần cuộn
        self.option_rects = []
        num_opts = len(options)
        for i in range(num_opts):
            opt_y = y - (num_opts - i) * height
            self.option_rects.append(pg.Rect(x, opt_y, width, height))

    def draw(self, surface, font):
        # 1. Nút hiển thị chính
        pg.draw.rect(surface, (245, 245, 245), self.rect, border_radius=4)
        pg.draw.rect(surface, (0, 0, 0), self.rect, 2, border_radius=4)

        text = f"{self.options[self.selected_index]}  ▲" if self.is_open else f"{self.options[self.selected_index]}  ▼"
        txt_surf = font.render(text, True, (0, 0, 0))
        surface.blit(txt_surf, (self.rect.x + 10, self.rect.y + (self.rect.height - txt_surf.get_height()) // 2))

        # 2. Hiển thị danh sách 4 thuật toán mở ngược lên trên
        if self.is_open:
            for i, opt_rect in enumerate(self.option_rects):
                mouse_pos = pg.mouse.get_pos()
                color = (210, 230, 255) if opt_rect.collidepoint(mouse_pos) else (255, 255, 255)
                
                pg.draw.rect(surface, color, opt_rect)
                pg.draw.rect(surface, (0, 0, 0), opt_rect, 1)

                opt_surf = font.render(self.options[i], True, (0, 0, 0))
                surface.blit(opt_surf, (opt_rect.x + 10, opt_rect.y + (opt_rect.height - opt_surf.get_height()) // 2))

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            # Click vào nút bật/tắt menu
            if self.rect.collidepoint(event.pos):
                self.is_open = not self.is_open
                return True

            # Click chọn 1 trong các thuật toán
            if self.is_open:
                for i, opt_rect in enumerate(self.option_rects):
                    if opt_rect.collidepoint(event.pos):
                        self.selected_index = i
                        self.is_open = False
                        return True
                # Bấm ra ngoài thì đóng menu
                self.is_open = False

        return False

    def get_selected(self):
        return self.options[self.selected_index]