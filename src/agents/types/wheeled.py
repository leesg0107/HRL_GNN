from typing import Dict, Any, Tuple
from ..base.base_agent import BaseAgent

class WheeledAgent(BaseAgent):
    def __init__(self, pos: Tuple[int, int], id: int):
        super().__init__(pos, id)
        self.speed = 1
        self.view_range = 100
        
    def get_observation(self, state: Dict[str, Any]) -> Dict[str, Any]:
        visible_objects = {
            'patients': [],
            'obstacles': [],
            'rescue_signals': []
        }
        # 바퀴 달린 에이전트 특화 관찰 로직 구현
        return visible_objects 