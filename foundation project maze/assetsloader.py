import pygame as pg

from cell import Cell

class AssetLoader:

    def __init__(self, cell_size):
        self.cell_size = cell_size

        try:
            self.wall_img = pg.transform.scale(
                pg.image.load("assets/wall.png"), (cell_size, cell_size)
            )
            self.start_img = pg.transform.scale(
                pg.image.load("assets/start.png"), (cell_size, cell_size)
            )
            self.target_img = pg.transform.scale(
                pg.image.load("assets/target.png"), (cell_size, cell_size)
            )
            self.empty_img = pg.transform.scale(
                pg.image.load("assets/empty.png"), (cell_size, cell_size)
            )
            self.has_assets = True
        except pg.error:
            # Trường hợp chưa có file ảnh, hệ thống sẽ tự fallback về vẽ màu mặc định
            self.has_assets = False

    # Hàm vẽ nhận tham số screen, cell, x, y từ ngoài truyền vào
    def draw_cell(self, screen, cell, x, y):
        if not self.has_assets:
            return False  # Trả về False để vẽ màu bằng rect mặc định

        if cell.state == Cell.WALL:
            screen.blit(self.wall_img, (x, y))
            return True
        elif cell.state == Cell.START:
            screen.blit(self.start_img, (x, y))
            return True
        elif cell.state == Cell.TARGET:
            screen.blit(self.target_img, (x, y))
            return True
        elif cell.state == Cell.EMPTY:  # Bổ sung vẽ asset cho ô EMPTY
            screen.blit(self.empty_img, (x, y))
            return True

        return False  # Với VISITED, PATH... vẽ màu mặc định