from typing import Dict, Any, Tuple
from ..base.agent import BaseAgent
from ..base.policy import BasePolicy
import numpy as np

class WheeledAgent(BaseAgent):
    def __init__(self, pos: Tuple[int, int], id: int):
        super().__init__(pos, id)
        self.speed = 1  # 드론보다 느린 이동
        self.view_range = 100  # 더 좁은 시야
        
    def set_policy(self, policy: BasePolicy):
        self.policy = policy
        
    def get_observation(self, state: Dict[str, Any]) -> Dict[str, Any]:
        visible_objects = {
            'patients': [],
            'obstacles': [],
        }
        
        for key in ['patients', 'obstacles']:
            if key in state:
                for obj in state[key]:
                    if self._is_in_view_range(obj[0] if isinstance(obj, tuple) else obj):
                        visible_objects[key].append(obj)
        
        return visible_objects
        
    def step(self, state: Dict[str, Any]) -> Tuple[int, int]:
        if self.policy:
            return self.policy.select_action(self.get_observation(state))
        # 임시로 랜덤 행동 반환
        return (
            np.random.randint(-self.speed, self.speed + 1),
            np.random.randint(-self.speed, self.speed + 1)
        )
        
    def update(self, experience: Dict[str, Any]):
        if self.policy:
            self.policy.update(experience)
            
    def _is_in_view_range(self, obj_pos: Tuple[int, int]) -> bool:
        dx = obj_pos[0] - self.pos[0]
        dy = obj_pos[1] - self.pos[1]
        distance = np.sqrt(dx**2 + dy**2)
        return distance <= self.view_range
        
# ... (나머지 코드는 동일) 