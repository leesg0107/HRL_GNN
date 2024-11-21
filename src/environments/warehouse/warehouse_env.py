import pygame
from typing import List, Dict, Any, Tuple
from ..base.base_environment import BaseEnvironment
from .constants import Colors, WarehouseConfig

class WarehouseEnv(BaseEnvironment):
    def __init__(self, width: int = WarehouseConfig.DEFAULT_WIDTH, 
                 height: int = WarehouseConfig.DEFAULT_HEIGHT):
        super().__init__()
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Warehouse Management")
        
        # Environment specific state
        self.items = {}  # 창고 내 물품 위치
        self.shelves = []  # 선반 위치
        self.charging_stations = []  # 충전소 위치
        
    def reset(self) -> Dict[str, Any]:
        self.items.clear()
        self.shelves.clear()
        self.charging_stations.clear()
        self.time = 0
        return self._get_state()
        
    def step(self, actions: List[Any]) -> Tuple[Dict[str, Any], List[Dict[str, Any]], bool, Dict[str, Any]]:
        # 각 에이전트의 행동 처리
        for agent, action in zip(self.agents, actions):
            if action[0] == 'move':
                dx, dy = action[1]
                new_x = max(0, min(self.width, agent.pos[0] + dx))
                new_y = max(0, min(self.height, agent.pos[1] + dy))
                if self._is_valid_move((new_x, new_y)):
                    agent.pos = (new_x, new_y)
            elif action[0] == 'pickup':
                self._handle_pickup(agent)
            elif action[0] == 'drop':
                self._handle_drop(agent)
            elif action[0] == 'charge':
                self._handle_charge(agent)
                
        self.time += 1
        observations = [agent.get_observation(self._get_state()) for agent in self.agents]
        done = False  # 나중에 종료 조건 추가
        
        return self._get_state(), observations, done, {'time': self.time}
    
    def render(self):
        """환경을 시각화"""
        self.screen.fill(Colors.WHITE)
        self._draw_shelves()
        self._draw_items()
        self._draw_charging_stations()
        self._draw_agents()
        pygame.display.flip()
        
    def _draw_shelves(self):
        """선반 그리기"""
        for shelf in self.shelves:
            pygame.draw.rect(self.screen, Colors.GRAY,
                           (shelf[0]-WarehouseConfig.SHELF_SIZE//2,
                            shelf[1]-WarehouseConfig.SHELF_SIZE//2,
                            WarehouseConfig.SHELF_SIZE,
                            WarehouseConfig.SHELF_SIZE))
            
    def _draw_items(self):
        """물품 그리기"""
        for pos, item_info in self.items.items():
            pygame.draw.circle(self.screen, Colors.BLUE, pos, 
                             WarehouseConfig.ITEM_SIZE)
            
    def _draw_charging_stations(self):
        """충전소 그리기"""
        for station in self.charging_stations:
            pygame.draw.rect(self.screen, Colors.YELLOW,
                           (station[0]-WarehouseConfig.CHARGING_STATION_SIZE//2,
                            station[1]-WarehouseConfig.CHARGING_STATION_SIZE//2,
                            WarehouseConfig.CHARGING_STATION_SIZE,
                            WarehouseConfig.CHARGING_STATION_SIZE))
            
    def _draw_agents(self):
        """에이전트 그리기"""
        for agent in self.agents:
            pygame.draw.circle(self.screen, Colors.BLACK, agent.pos, 10)
            
    def _is_valid_move(self, pos: Tuple[int, int]) -> bool:
        """이동 가능 여부 확인"""
        # 선반과 충전소와의 충돌 체크
        for shelf in self.shelves:
            if self._is_collision(pos, shelf, WarehouseConfig.SHELF_SIZE):
                return False
        return True
    
    def _is_collision(self, pos1: Tuple[int, int], pos2: Tuple[int, int], 
                     threshold: int) -> bool:
        """두 위치 간의 충돌 여부를 확인"""
        return (abs(pos1[0] - pos2[0]) < threshold and 
                abs(pos1[1] - pos2[1]) < threshold)
    
    def _get_state(self) -> Dict[str, Any]:
        """현재 환경 상태를 딕셔너리로 반환"""
        return {
            'time': self.time,
            'items': self.items,
            'shelves': self.shelves,
            'charging_stations': self.charging_stations,
            'agents': [(agent.pos, type(agent).__name__) for agent in self.agents]
        }
    
    def get_observation_space(self) -> Dict[str, Any]:
        return {
            'width': self.width,
            'height': self.height,
            'features': ['items', 'shelves', 'charging_stations', 'agents']
        }
        
    def get_action_space(self) -> Dict[str, Any]:
        return {
            'type': 'discrete',
            'actions': ['move', 'pickup', 'drop', 'charge']
        }
    
    def add_shelf(self, pos: Tuple[int, int]):
        """선반 추가"""
        self.shelves.append(pos)
        
    def add_item(self, pos: Tuple[int, int], item_info: Dict[str, Any]):
        """물품 추가"""
        self.items[pos] = item_info
        
    def add_charging_station(self, pos: Tuple[int, int]):
        """충전소 추가"""
        self.charging_stations.append(pos) 