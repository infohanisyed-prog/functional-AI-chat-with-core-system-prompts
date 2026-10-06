from collections import defaultdict
from typing import Dict, List


class ConversationMemory:
    """Simple in-memory conversation store for the prototype."""

    def __init__(self, max_messages: int = 20):
        self._sessions: Dict[str, List[dict]] = defaultdict(list)
        self.max_messages = max_messages

    def get(self, session_id: str) -> List[dict]:
        return list(self._sessions[session_id])

    def add(self, session_id: str, role: str, content: str) -> None:
        self._sessions[session_id].append(
            {"role": role, "content": content}
        )
        self._sessions[session_id] = self._sessions[session_id][-self.max_messages:]

    def clear(self, session_id: str) -> None:
        self._sessions.pop(session_id, None)

    def count(self, session_id: str) -> int:
        return len(self._sessions[session_id])
