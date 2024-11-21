from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple, List
from .policy import BasePolicy

class BaseAgent(ABC):
    def __init__(self, pos: Tuple[int, int], id: int):
        self.pos = pos
        self.id = id
        self.policy = None
        self.observation_history = []
        
    @abstractmethod
    def set_policy(self, policy: BasePolicy):
        """에이전트의 정책 설정"""
        pass
        
    @abstractmethod
    def get_observation(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """환경으로부터 관찰 획득"""
        pass
        
    @abstractmethod
    def step(self, state: Dict[str, Any]) -> Tuple[int, int]:
        """정책에 따른 행동 선택"""
        pass
        
    @abstractmethod
    def update(self, experience: Dict[str, Any]):
        """경험을 통한 정책 업데이트"""
        pass 