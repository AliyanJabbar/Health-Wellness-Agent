from agents import function_tool, RunContextWrapper
from context import UserSessionContext
from .tracker import ProgressTrackerTool
from typing import Optional

# Initialize the progress tracker
progress_tracker = ProgressTrackerTool()

@function_tool()
async def progress_tracker_tool(
    ctx: RunContextWrapper[UserSessionContext],
    metric_type: str,
    value: float,
    unit: str,
    notes: Optional[str] = None
) -> str:
    """
    Track user's progress towards their health goals.
    
    Args:
        metric_type: Type of metric (weight, measurements, workout_completed, etc.)
        value: The measured value
        unit: Unit of measurement (kg, lbs, cm, etc.)
        notes: Optional notes about the progress
    """
    print("-" * 50)
    print(f"[Tool] Tracking progress: {value} {unit} {metric_type}")
    
    try:
        # Record progress
        summary = progress_tracker.run(
            metric_type=metric_type,
            value=value,
            unit=unit,
            notes=notes,
            context=ctx.context
        )
        
        print(f"[Tool] Progress recorded. {summary.progress_percentage}% complete")
        print("-" * 50)
        
        return f"""
        📊 **Progress Update Recorded!**
        
        **Current Progress:** {summary.current_progress} / {summary.target_progress}
        **Completion:** {summary.progress_percentage}%
        **Days Remaining:** {summary.days_remaining}
        **Status:** {"✅ On Track" if summary.on_track else "⚠️ Needs Attention"}
        
        **Recommendations:**
        {chr(10).join([f"• {rec}" for rec in summary.recommendations])}
        """
        
    except Exception as e:
        return f"❌ Error tracking progress: {str(e)}"

@function_tool()
async def get_progress_summary(ctx: RunContextWrapper[UserSessionContext]) -> str:
    """Get a summary of user's current progress."""
    
    if not ctx.context.progress_logs:
        return "No progress data recorded yet. Start tracking your progress!"
    
    # Get recent progress entries
    recent_entries = ctx.context.progress_logs[-5:]  # Last 5 entries
    
    summary = "📈 **Recent Progress:**\n"
    for entry in recent_entries:
        summary += f"• {entry['date'][:10]}: {entry['value']} {entry['unit']} ({entry['metric_type']})\n"
    
    return summary
