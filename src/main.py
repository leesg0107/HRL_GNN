import pygame
from environments.rescue.rescue_env import RescueEnv
from agents.types.drone import DroneAgent
from agents.types.wheeled import WheeledAgent

def setup_agents(env):
    """에이전트 설정"""
    env.add_agent(DroneAgent((100, 100), 0))
    env.add_agent(DroneAgent((100, 130), 1))
    env.add_agent(WheeledAgent((100, 160), 2))

def main():
    # 환경 생성 및 설정
    env = RescueEnv()
    env.setup_default_environment()
    setup_agents(env)
    
    # 초기 상태
    state = env.reset()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # 각 에이전트의 행동 (지금은 정지 상태)
        actions = [(0, 0) for _ in env.agents]
        
        # 환경 진행
        state, observations, done, info = env.step(actions)
        env.render()
        
        if done:
            break
    
    pygame.quit()

if __name__ == "__main__":
    main() 