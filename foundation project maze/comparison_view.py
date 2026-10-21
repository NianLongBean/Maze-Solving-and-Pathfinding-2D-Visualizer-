
import pygame as pg


class ComparisonView:
    def __init__(self):
        self.visible = False
        self.font = pg.font.SysFont("Arial", 14)
        self.title_font = pg.font.SysFont("Arial", 20, bold=True)

    def draw(self, screen, results):
        if not self.visible:
            return

        overlay = pg.Surface(screen.get_size(), pg.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        panel = pg.Rect(20, 50, screen.get_width() - 40, 320)
        pg.draw.rect(screen, (250, 250, 250), panel)
        pg.draw.rect(screen, (30, 30, 30), panel, 2)

        title = self.title_font.render(
            "Algorithm Comparison", True, (20, 20, 20)
        )
        screen.blit(title, (panel.x + 15, panel.y + 12))

        headers = [
            ("Algorithm", 15),
            ("Runs", 130),
            ("Success", 190),
            ("Time(ms)", 280),
            ("Visited", 390),
            ("Path", 500),
        ]

        header_y = panel.y + 55

        for label, offset in headers:
            text = self.font.render(label, True, (0, 0, 0))
            screen.blit(text, (panel.x + offset, header_y))

        pg.draw.line(
            screen, (100, 100, 100),
            (panel.x + 10, header_y + 25),
            (panel.right - 10, header_y + 25), 1
        )

        for index, result in enumerate(results):
            y = header_y + 35 + index * 35
            path = result["avg_path_length"]

            values = [
                result["algorithm"],
                str(result["total_runs"]),
                f'{result["success_rate"]:.1f}%',
                f'{result["avg_runtime_ms"]:.3f}',
                f'{result["avg_visited_count"]:.1f}',
                f"{path:.1f}" if path is not None else "N/A",
            ]

            for value_index, value in enumerate(values):
                text = self.font.render(value, True, (20, 20, 20))
                screen.blit(
                    text,
                    (panel.x + headers[value_index][1], y)
                )

        hint = self.font.render(
            "Press ESC to close", True, (70, 70, 70)
        )
        screen.blit(hint, (panel.x + 15, panel.bottom - 30))
