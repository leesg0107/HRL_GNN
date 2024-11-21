from typing import Dict, Any, Tuple
from ..base.base_agent import BaseAgent

class DroneAgent(BaseAgent):
    def __init__(self, pos: Tuple[int, int], id: int):
        super().__init__(pos, id)
        self.speed = 2
        self.view_range = 150
        
    def get_observation(self, state: Dict[str, Any]) -> Dict[str, Any]:
        visible_objects = {
            'patients': [],
            'obstacles': [],
            'rescue_signals': []
        }
        # 드론 특화 관찰 로직 구현
        return visible_objects 