import pygame as pg


class ControlsNote:

    def __init__(self, x=10, y=10, font_size=16):
        self.x = x
        self.y = y
        self.padding = 10
        self.font = pg.font.SysFont("Arial", font_size, bold=True)

        # List of controls/instructions to display
        self.controls = [
            "CONTROLS / SHORTCUTS",
            "[W] : Wall Mode",
            "[S] : Set Start Node",
            "[T] : Set Target Node",
            "[M] : Generate Maze",
            "[B] : Run BFS Algorithm",
            "[D] : Run DFS Algorithm",
            "[A] : Run Dijkstra Algorithm",
            "[Arrow_Up] : Speed Up",
            "[Arrow_down] : Speed Down",
            "[C] : Clear Path / Reset",
        ]

        # 1. Pre-render title button surface & calculate collapsed dimensions
        self.btn_text = self.font.render(
            "[?]", True, (255, 215, 0)
        )
        self.btn_rect = pg.Rect(
            self.x,
            self.y,
            self.btn_text.get_width() + self.padding * 2,
            self.btn_text.get_height() + self.padding * 2,
        )

        # 2. Pre-calculate expanded panel dimensions
        dummy_lines = [self.font.render(t, True, (0, 0, 0)) for t in self.controls]
        max_w = max(line.get_width() for line in dummy_lines)
        line_h = dummy_lines[0].get_height()
        spacing = 4
        total_h = len(dummy_lines) * (line_h + spacing)

        self.panel_rect = pg.Rect(
            self.x,
            self.y,
            max_w + self.padding * 2,
            total_h + self.padding * 2,
        )

    def draw(self, surface):
        mouse_pos = pg.mouse.get_pos()

        # Check if mouse is hovering over either the collapsed button or expanded panel area
        if self.panel_rect.collidepoint(mouse_pos) or self.btn_rect.collidepoint(
            mouse_pos
        ):
            self._draw_expanded_panel(surface)
        else:
            self._draw_collapsed_button(surface)

    def _draw_collapsed_button(self, surface):
        # Draw small dark badge when idle
        overlay = pg.Surface((self.btn_rect.width, self.btn_rect.height), pg.SRCALPHA)
        pg.draw.rect(overlay, (20, 20, 20, 210), overlay.get_rect(), border_radius=6)
        pg.draw.rect(overlay, (100, 100, 100, 255), overlay.get_rect(), width=2, border_radius=6)

        surface.blit(overlay, (self.x, self.y))
        surface.blit(self.btn_text, (self.x + self.padding, self.y + self.padding))

    def _draw_expanded_panel(self, surface):
        rendered_lines = []
        for i, text in enumerate(self.controls):
            color = (255, 215, 0) if i == 0 else (240, 240, 240)
            rendered_lines.append(self.font.render(text, True, color))

        line_height = rendered_lines[0].get_height()
        spacing = 4

        # Create panel overlay
        overlay = pg.Surface((self.panel_rect.width, self.panel_rect.height), pg.SRCALPHA)
        pg.draw.rect(overlay, (20, 20, 20, 230), overlay.get_rect(), border_radius=8)
        pg.draw.rect(overlay, (100, 100, 100, 255), overlay.get_rect(), width=2, border_radius=8)

        surface.blit(overlay, (self.x, self.y))

        # Blit text lines
        curr_y = self.y + self.padding
        for line in rendered_lines:
            surface.blit(line, (self.x + self.padding, curr_y))
            curr_y += line_height + spacing