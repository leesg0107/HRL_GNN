from abc import ABC, abstractmethod
from typing import Dict, Any, List, Tuple, Optional
from agents.base.agent import BaseAgent

class BaseEnvironment(ABC):
    """다양한 환경에서 사용할 수 있는 기본 환경 클래스"""
    
    def __init__(self):
        self.agents: List[BaseAgent] = []
        self.state: Dict[str, Any] = {}
        self.time: int = 0
        
    @abstractmethod
    def reset(self) -> Dict[str, Any]:
        """환경을 초기화하고 초기 상태를 반환"""
        pass
    
    @abstractmethod
    def step(self, actions: List[Any]) -> Tuple[Dict[str, Any], List[Dict[str, Any]], bool, Dict[str, Any]]:
        """환경을 한 스텝 진행"""
        pass
    
    @abstractmethod
    def render(self):
        """환경을 시각화"""
        pass
    
    @abstractmethod
    def add_agent(self, agent: BaseAgent):
        """에이전트를 환경에 추가"""
        pass
    
    @abstractmethod
    def get_observation_space(self) -> Dict[str, Any]:
        """관찰 공간의 정보를 반환"""
        pass
    
    @abstractmethod
    def get_action_space(self) -> Dict[str, Any]:
        """행동 공간의 정보를 반환"""
        pass 