from typing import Tuple, Dict, Any, List
import numpy as np
import math

class Observer:
    def __init__(self, pos: Tuple[int, int], view_range: int = 800):
        self.pos = pos
        self.view_range = view_range
        self.rotation_speed = 2
        self.current_angle = 0
        self.fov = math.pi / 3
        self.detected_objects = []
        
    def scan(self, state: Dict[str, Any]) -> List[Dict[str, Any]]:
        self.current_angle = (self.current_angle + math.radians(self.rotation_speed)) % (2 * math.pi)
        
        detected = []
        
        if 'patients' in state:
            for obj_pos in state['patients']:
                if self._is_in_view_cone(obj_pos):
                    detected.append({
                        'type': 'patient',
                        'position': obj_pos,
                        'distance': self._calculate_distance(obj_pos),
                        'detection_time': state.get('time', 0)
                    })
        
        self.detected_objects.extend(detected)
        return detected
    
    def _is_in_view_cone(self, obj_pos: Tuple[int, int]) -> bool:
        dx = obj_pos[0] - self.pos[0]
        dy = obj_pos[1] - self.pos[1]
        
        angle = math.atan2(dy, dx)
        angle_diff = abs(self._normalize_angle(angle - self.current_angle))
        
        distance = self._calculate_distance(obj_pos)
        
        return angle_diff <= self.fov/2 and distance <= self.view_range
    
    def _calculate_distance(self, obj_pos: Tuple[int, int]) -> float:
        dx = obj_pos[0] - self.pos[0]
        dy = obj_pos[1] - self.pos[1]
        return math.sqrt(dx**2 + dy**2)
    
    def _normalize_angle(self, angle: float) -> float:
        while angle > math.pi:
            angle -= 2 * math.pi
        while angle < -math.pi:
            angle += 2 * math.pi
        return angle