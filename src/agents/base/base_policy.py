from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple

class BasePolicy(ABC):
    @abstractmethod
    def select_action(self, state: Dict[str, Any]) -> Tuple[int, int]:
        """상태를 받아서 행동을 선택"""
        pass
    
    @abstractmethod
    def update(self, experience: Dict[str, Any]):
        """경험을 통해 정책을 업데이트"""
        pass 