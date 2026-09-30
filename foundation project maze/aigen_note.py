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
            "[C] : Clear Path / Reset",
        ]

    def draw(self, surface):
        # 1. Render all text surfaces
        rendered_lines = []
        for i, text in enumerate(self.controls):
            # Highlight title header in yellow, rest in white
            color = (255, 215, 0) if i == 0 else (240, 240, 240)
            rendered_lines.append(self.font.render(text, True, color))

        # 2. Calculate panel dimensions
        max_width = max(line.get_width() for line in rendered_lines)
        line_height = rendered_lines[0].get_height()
        spacing = 4
        total_height = len(rendered_lines) * (line_height + spacing)

        # 3. Create transparent overlay surface for background
        panel_rect = pg.Rect(
            0,
            0,
            max_width + self.padding * 2,
            total_height + self.padding * 2,
        )
        overlay = pg.Surface(
            (panel_rect.width, panel_rect.height), pg.SRCALPHA
        )

        # Semi-transparent dark background (RGBA: 20, 20, 20, 210)
        pg.draw.rect(
            overlay,
            (20, 20, 20, 210),
            overlay.get_rect(),
            border_radius=8,
        )
        pg.draw.rect(
            overlay,
            (100, 100, 100, 255),
            overlay.get_rect(),
            width=2,
            border_radius=8,
        )

        # 4. Blit overlay panel onto main surface
        surface.blit(overlay, (self.x, self.y))

        # 5. Draw text lines on top of the panel
        curr_y = self.y + self.padding
        for line in rendered_lines:
            surface.blit(line, (self.x + self.padding, curr_y))
            curr_y += line_height + spacing