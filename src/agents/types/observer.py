from typing import Dict, Any, Tuple
from ..base.base_agent import BaseAgent
import math

class Observer(BaseAgent):
    def __init__(self, pos: Tuple[int, int], id: int):
        super().__init__(pos, id)
        self.view_range = 700
        self.fov = math.pi / 3.5 # 90도 시야각
        self.current_angle = 0
        self.rotation_speed = 0.01

    def get_observation(self, state: Dict[str, Any]) -> Dict[str, Any]:
        # Observer 특화 관찰 로직 구현
        visible_objects = {
            'patients': [],
            'obstacles': [],
            'agents': []
        }
        return visible_objects

    def scan(self, state: Dict[str, Any]) -> Dict[str, Any]:
        # 회전하면서 스캔하는 로직
        self.current_angle += self.rotation_speed
        if self.current_angle > 2 * math.pi:
            self.current_angle = 0
        return self.get_observation(state) 