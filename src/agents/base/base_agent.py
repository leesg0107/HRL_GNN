from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple

class BaseAgent(ABC):
    def __init__(self, pos: Tuple[int, int], id: int):
        self.pos = pos
        self.id = id
        self.policy = None
        self.observation_history = []
    
    @abstractmethod
    def get_observation(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """환경을 관찰하여 에이전트의 관점에서의 상태를 반환"""
        pass
    
    def step(self, state: Dict[str, Any]) -> Tuple[int, int]:
        """환경 상태를 받아서 행동을 결정"""
        if self.policy:
            return self.policy.select_action(self.get_observation(state))
        return (0, 0)  # 기본 행동
    
    def set_policy(self, policy):
        """정책 설정"""
        self.policy = policy
    
    def update(self, experience: Dict[str, Any]):
        """경험을 통한 정책 업데이트"""
        if self.policy:
            self.policy.update(experience) 