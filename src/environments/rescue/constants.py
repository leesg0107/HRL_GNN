from enum import Enum
from typing import Tuple

class ObstacleType(Enum):
    NORMAL = "NORMAL"
    AERIAL = "AERIAL"

class Colors:
    WHITE: Tuple[int, int, int] = (255, 255, 255)
    BLACK: Tuple[int, int, int] = (0, 0, 0)
    RED: Tuple[int, int, int] = (255, 0, 0)
    GREEN: Tuple[int, int, int] = (0, 255, 0)
    BLUE: Tuple[int, int, int] = (0, 0, 255)
    PURPLE: Tuple[int, int, int] = (128, 0, 128)

class RescueConfig:
    DEFAULT_WIDTH = 800
    DEFAULT_HEIGHT = 600
    DEFAULT_GRID_SIZE = 20
    AGENT_RADIUS = 8
    OBSTACLE_SIZE = 20
    PATIENT_RADIUS = 8
    OBSERVER_RADIUS = 10 