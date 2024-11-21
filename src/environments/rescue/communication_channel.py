from typing import List, Dict, Any

class CommunicationChannel:
    """에이전트 간 통신을 관리하는 클래스"""
    
    def __init__(self):
        self.messages = []  # 메시지 저장소
        
    def broadcast(self, sender_id: int, message: Dict[str, Any]):
        """모든 에이전트에게 메시지 전달"""
        self.messages.append((sender_id, message))
        
    def receive(self, agent_id: int) -> List[Dict[str, Any]]:
        """특정 에이전트가 수신할 메시지 반환"""
        # 자신이 보낸 메시지를 제외한 모든 메시지 반환
        return [msg for sender, msg in self.messages if sender != agent_id]
        
    def clear(self):
        """메시지 저장소 초기화"""
        self.messages.clear() 