from typing import Type, Dict, Any

class Registry:
    def __init__(self):
        self._agents = {}
        self._environments = {}
        self._policies = {}

    def register_agent(self, name: str, agent_class: Any):
        self._agents[name] = agent_class

    def register_environment(self, name: str, env_class: Any):
        self._environments[name] = env_class

    def register_policy(self, name: str, policy_class: Any):
        self._policies[name] = policy_class

    def get_agent(self, name: str) -> Any:
        if name not in self._agents:
            raise KeyError(f"Agent '{name}' not found in registry")
        return self._agents[name]

    def get_environment(self, name: str) -> Any:
        if name not in self._environments:
            raise KeyError(f"Environment '{name}' not found in registry")
        return self._environments[name]

    def get_policy(self, name: str) -> Any:
        if name not in self._policies:
            raise KeyError(f"Policy '{name}' not found in registry")
        return self._policies[name]

# 전역 레지스트리 인스턴스
registry = Registry() 