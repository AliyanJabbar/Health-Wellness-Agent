from pydantic import BaseModel
from typing import Optional, List, Dict, Literal


class UserSessionContext(BaseModel):
    """user session context provider"""

    # attributes
    name: str
    uid: int
    history: Optional[List[Dict[Literal["role", "content"], str]]]
    current_agent: Optional[str] = "health_wellness_agent"
    goal: Optional[dict] = None
    diet_preferences: Optional[str] = None
    workout_plan: Optional[dict] = None
    meal_plan: Optional[List[str]] = None
    injury_notes: Optional[str] = None
    handoff_logs: List[Dict[Literal["from", "to", "message"], str]] = []
    progress_logs: List[Dict] = []

    # methods
    def add_handoff_log(self, log_entry: Dict[Literal["from", "to", "message"], str]):
        """Add a handoff log entry"""
        self.handoff_logs.append(log_entry)

    def add_progress_log(self, log_entry: Dict[str, str]):
        """Add a progress log entry"""
        self.progress_logs.append(log_entry)
