from agents import RunHooks, AgentHooks
from context import UserSessionContext
from datetime import datetime
import json

class HealthWellnessRunHooks(RunHooks[UserSessionContext]):
    """Global lifecycle hooks for the health wellness system"""
    
    def on_agent_start(self, agent_name: str, context: UserSessionContext):
        print(f"🚀 [Hook] Agent '{agent_name}' started for user {context.name}")
        
    def on_agent_end(self, agent_name: str, context: UserSessionContext):
        print(f"✅ [Hook] Agent '{agent_name}' completed")
        
    def on_tool_start(self, tool_name: str, context: UserSessionContext):
        print(f"🔧 [Hook] Tool '{tool_name}' started")
        
    def on_tool_end(self, tool_name: str, context: UserSessionContext):
        print(f"🔧 [Hook] Tool '{tool_name}' completed")
        
    def on_handoff(self, from_agent: str, to_agent: str, context: UserSessionContext):
        print(f"🔄 [Hook] Handoff from '{from_agent}' to '{to_agent}'")
        
        # Log handoff in context
        handoff_entry = {
            "from": from_agent,
            "to": to_agent,
            "message": f"Handoff at {datetime.now().isoformat()}",
            "timestamp": datetime.now().isoformat()
        }
        context.add_handoff_log(handoff_entry)

class HealthWellnessAgentHooks(AgentHooks[UserSessionContext]):
    """Agent-specific lifecycle hooks"""
    
    def on_start(self, context: UserSessionContext):
        print(f"🎯 [Agent Hook] Health wellness agent started for {context.name}")
        
    def on_end(self, context: UserSessionContext):
        print(f"🎯 [Agent Hook] Health wellness agent session ended")
        
        # Log session summary
        session_summary = {
            "user": context.name,
            "goal": context.goal,
            "handoffs": len(context.handoff_logs),
            "progress_entries": len(context.progress_logs),
            "timestamp": datetime.now().isoformat()
        }
        print(f"📊 [Session Summary] {json.dumps(session_summary, indent=2)}")
