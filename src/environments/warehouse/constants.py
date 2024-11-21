from typing import Tuple

class Colors:
    WHITE: Tuple[int, int, int] = (255, 255, 255)
    BLACK: Tuple[int, int, int] = (0, 0, 0)
    BLUE: Tuple[int, int, int] = (0, 0, 255)
    YELLOW: Tuple[int, int, int] = (255, 255, 0)
    GRAY: Tuple[int, int, int] = (128, 128, 128)

class WarehouseConfig:
    DEFAULT_WIDTH = 1000
    DEFAULT_HEIGHT = 800
    DEFAULT_GRID_SIZE = 20
    SHELF_SIZE = 40
    ITEM_SIZE = 15
    CHARGING_STATION_SIZE = 30 