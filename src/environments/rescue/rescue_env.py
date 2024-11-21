import pygame
import math
from typing import List, Tuple, Dict, Any, TYPE_CHECKING
from environments.base.base_environment import BaseEnvironment
from environments.rescue.constants import ObstacleType, Colors, RescueConfig
from agents.types.drone import DroneAgent
from agents.types.wheeled import WheeledAgent
from agents.types.observer import Observer
from environments.rescue.communication_channel import CommunicationChannel

if TYPE_CHECKING:
    from agents.base.base_agent import BaseAgent

class RescueEnv(BaseEnvironment):
    def __init__(self, width: int = RescueConfig.DEFAULT_WIDTH, 
                 height: int = RescueConfig.DEFAULT_HEIGHT,
                 grid_size: int = RescueConfig.DEFAULT_GRID_SIZE):
        super().__init__()
        pygame.init()
        self.width = width
        self.height = height
        self.grid_size = grid_size
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Rescue Mission")
        
        # Environment specific state
        self.patients = []
        self.obstacles = {}
        self.observer = Observer((100, 300), -1)  # Observer 추가
        self.comm_channel = CommunicationChannel()
        
    def reset(self) -> Dict[str, Any]:
        """환경을 초기화하고 초기 상태를 반환"""
        # 기존 상태는 유지하고 time만 초기화
        self.time = 0
        return self._get_state()
        
    def step(self, actions: List[Any]) -> Tuple[Dict[str, Any], List[Dict[str, Any]], bool, Dict[str, Any]]:
        # Observer 스캔
        detected_objects = self.observer.scan(self._get_state())
        
        # Observer 정보 공유
        detected_info = self.observer.scan(self._get_state())
        self.comm_channel.broadcast(-1, {
            'type': 'observation',
            'data': detected_info
        })
        
        # 각 에이전트의 행동 및 통신 처리
        for agent, action in zip(self.agents, actions):
            # 행동 실행
            movement, message = action  # 행동과 통신 메시지 분리
            if message:
                self.comm_channel.broadcast(agent.id, message)
                
            # 다른 에이전트들의 메시지 수신
            received_msgs = self.comm_channel.receive(agent.id)
            agent.process_messages(received_msgs)
            
            current_pos = agent.pos
            dx, dy = movement
            new_x = max(0, min(self.width, current_pos[0] + dx))
            new_y = max(0, min(self.height, current_pos[1] + dy))
            new_pos = (new_x, new_y)
            
            if self._is_valid_move(agent, new_pos):
                agent.pos = new_pos
        
        self.time += 1
        observations = [agent.get_observation(self._get_state()) for agent in self.agents]
        done = False
        
        return self._get_state(), observations, done, {
            'time': self.time,
            'detected_objects': detected_objects
        }
    
    def render(self):
        """환경을 시각화"""
        self.screen.fill(Colors.WHITE)
        
        # Observer의 시야각 영역 그리기
        surface = pygame.Surface((self.width * 2, self.height * 2), pygame.SRCALPHA)
        points = [(self.observer.pos[0], self.observer.pos[1])]
        num_points = 50
        start_angle = self.observer.current_angle - self.observer.fov/2
        end_angle = self.observer.current_angle + self.observer.fov/2
        
        for i in range(num_points + 1):
            angle = start_angle + (end_angle - start_angle) * i / num_points
            x = self.observer.pos[0] + math.cos(angle) * self.observer.view_range
            y = self.observer.pos[1] + math.sin(angle) * self.observer.view_range
            points.append((x, y))
        
        if len(points) > 2:
            pygame.draw.polygon(surface, (0, 0, 255, 30), points)
        self.screen.blit(surface, (-self.width//2, -self.height//2))
        
        # Observer의 시야각 경계선 표시
        pygame.draw.line(self.screen, Colors.BLUE, self.observer.pos,
                        (self.observer.pos[0] + math.cos(start_angle) * self.observer.view_range,
                         self.observer.pos[1] + math.sin(start_angle) * self.observer.view_range))
        pygame.draw.line(self.screen, Colors.BLUE, self.observer.pos,
                        (self.observer.pos[0] + math.cos(end_angle) * self.observer.view_range,
                         self.observer.pos[1] + math.sin(end_angle) * self.observer.view_range))
        
        # 각 요소 그리기
        self._draw_grid()        # 그리드 그리기
        self._draw_patients()    # 환자 그리기
        self._draw_obstacles()   # 장애물 그리기
        self._draw_agents()      # 에이전트 그리기
        
        # Observer 그리기
        font = pygame.font.Font(None, 20)
        observer_text = font.render("Observer", True, Colors.BLUE)
        self.screen.blit(observer_text, 
                        (self.observer.pos[0] - 30, self.observer.pos[1] - 25))
        pygame.draw.circle(self.screen, Colors.BLUE, self.observer.pos, RescueConfig.OBSERVER_RADIUS)
        
        pygame.display.flip()  # 화면 업데이트
    
    def _draw_grid(self):
        """그리드 그리기"""
        for x in range(0, self.width, self.grid_size):
            pygame.draw.line(self.screen, Colors.BLACK, (x, 0), (x, self.height))
        for y in range(0, self.height, self.grid_size):
            pygame.draw.line(self.screen, Colors.BLACK, (0, y), (self.width, y))
    
    def _draw_patients(self):
        """환자 그리기"""
        font = pygame.font.Font(None, 20)
        for i, patient_pos in enumerate(self.patients):
            pygame.draw.circle(self.screen, Colors.RED, 
                             (int(patient_pos[0]), int(patient_pos[1])), 
                             RescueConfig.PATIENT_RADIUS)
            text = font.render(f"Patient {i+1}", True, Colors.RED)
            self.screen.blit(text, 
                            (patient_pos[0] - 30, patient_pos[1] - 20))
    
    def _draw_obstacles(self):
        """장애물 그리기"""
        font = pygame.font.Font(None, 20)
        for i, (pos, obs_type) in enumerate(self.obstacles.items()):
            color = Colors.PURPLE if obs_type == ObstacleType.AERIAL else Colors.BLACK
            rect = pygame.Rect(int(pos[0] - RescueConfig.OBSTACLE_SIZE/2),
                             int(pos[1] - RescueConfig.OBSTACLE_SIZE/2),
                             RescueConfig.OBSTACLE_SIZE,
                             RescueConfig.OBSTACLE_SIZE)
            pygame.draw.rect(self.screen, color, rect)
            
            text = font.render(
                f"{'Aerial' if obs_type == ObstacleType.AERIAL else 'Normal'} Obs",
                True, color
            )
            self.screen.blit(text, (pos[0] - 35, pos[1] - 25))
    
    def _draw_agents(self):
        """에이전트 그리기"""
        font = pygame.font.Font(None, 20)
        for i, agent in enumerate(self.agents):
            pygame.draw.circle(self.screen, Colors.GREEN, agent.pos, RescueConfig.AGENT_RADIUS)
            text = font.render(f"{type(agent).__name__} {i+1}", True, Colors.GREEN)
            self.screen.blit(text, (agent.pos[0] - 35, agent.pos[1] - 20))
    
    def _is_valid_move(self, agent, new_pos: Tuple[int, int]) -> bool:
        """이동 가능 여부 확인"""
        for obs_pos, obs_type in self.obstacles.items():
            if self._is_collision(new_pos, obs_pos):
                if not (isinstance(agent, DroneAgent) and obs_type == ObstacleType.AERIAL):
                    return False
        return True
    
    def _is_collision(self, pos1: Tuple[int, int], pos2: Tuple[int, int], 
                     threshold: int = RescueConfig.OBSTACLE_SIZE/2) -> bool:
        """두 위치 간의 충돌 여부를 확인"""
        dx = abs(pos1[0] - pos2[0])
        dy = abs(pos1[1] - pos2[1])
        return dx < threshold and dy < threshold
    
    def _get_state(self) -> Dict[str, Any]:
        """현재 환경 상태를 딕셔너리로 반환"""
        return {
            'time': self.time,
            'patients': self.patients,
            'obstacles': [(pos, type.value) for pos, type in self.obstacles.items()],
            'agents': [(agent.pos, type(agent).__name__) for agent in self.agents]
        }
    
    def get_observation_space(self) -> Dict[str, Any]:
        return {
            'width': self.width,
            'height': self.height,
            'grid_size': self.grid_size,
            'features': ['patients', 'obstacles', 'agents']
        }
    
    def get_action_space(self) -> Dict[str, Any]:
        return {
            'type': 'continuous',
            'shape': (2,),  # (dx, dy)
            'range': (-1, 1)  # 정규화된 이동 범위
        }
    
    def add_patient(self, pos: Tuple[int, int]):
        """환자의 위치를 추가"""
        self.patients.append(pos)
    
    def add_obstacle(self, pos: Tuple[int, int], obstacle_type: ObstacleType):
        """장애물의 위치와 타입을 추가"""
        self.obstacles[pos] = obstacle_type
    
    def add_agent(self, agent: 'BaseAgent'):
        """에이전트를 환경에 추가"""
        self.agents.append(agent)
    
    def setup_default_environment(self):
        """기본 환경 설정 (환자, 장애물 배치 등)"""
        # 환자 추가 (5명)
        self.add_patient((200, 300))  # 왼쪽
        self.add_patient((600, 400))  # 오른쪽 아래
        self.add_patient((500, 150))  # 오른쪽 위
        self.add_patient((650, 250))  # 오른쪽 중앙
        self.add_patient((350, 450))  # 중앙 아래
        
        # 장애물 배치
        # 1. 중앙 세로 벽 (일반 장애물)
        for y in range(100, 501, 40):
            self.add_obstacle((400, y), ObstacleType.NORMAL)
        
        # 2. 오른쪽 위 환자 주변 (드론만 통과 가능)
        for x in range(460, 541, 40):
            self.add_obstacle((x, 110), ObstacleType.AERIAL)
            self.add_obstacle((x, 190), ObstacleType.AERIAL)
        for y in range(110, 191, 40):
            self.add_obstacle((460, y), ObstacleType.AERIAL)
            self.add_obstacle((540, y), ObstacleType.AERIAL)
        
        # 3. 오른쪽 중앙 환자 주변 (드론만 통과 가능)
        for x in range(610, 691, 40):
            self.add_obstacle((x, 210), ObstacleType.AERIAL)
            self.add_obstacle((x, 290), ObstacleType.AERIAL)
        for y in range(210, 291, 40):
            self.add_obstacle((610, y), ObstacleType.AERIAL)
            self.add_obstacle((690, y), ObstacleType.AERIAL)
        
        # 4. 중앙 아래 환자 주변 (일반 장애물)
        for x in range(310, 391, 40):
            self.add_obstacle((x, 410), ObstacleType.NORMAL)
        for y in range(410, 491, 40):
            self.add_obstacle((310, y), ObstacleType.NORMAL)
            self.add_obstacle((390, y), ObstacleType.NORMAL)