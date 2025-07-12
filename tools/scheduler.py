from agents import function_tool, RunContextWrapper
from context import UserSessionContext
from .scheduler import CheckinSchedulerTool
from typing import Optional

# Initialize the scheduler
scheduler = CheckinSchedulerTool()

@function_tool()
async def schedule_checkin_tool(
    ctx: RunContextWrapper[UserSessionContext],
    reminder_type: str = "checkin",
    frequency: str = "weekly"
) -> str:
    """
    Schedule progress check-ins and reminders.
    
    Args:
        reminder_type: Type of reminder (checkin, workout, meal_prep, weigh_in)
        frequency: How often to remind (daily, weekly, monthly)
    """
    print("-" * 50)
    print(f"[Tool] Scheduling {frequency} {reminder_type} reminders")
    
    try:
        response = scheduler.run(
            reminder_type=reminder_type,
            frequency=frequency,
            context=ctx.context
        )
        
        print(f"[Tool] Scheduled {len(response.scheduled_reminders)} reminders")
        print("-" * 50)
        
        next_reminder_info = ""
        if response.next_reminder:
            next_date = response.next_reminder.scheduled_date[:10]
            next_reminder_info = f"\n**Next Reminder:** {next_date} - {response.next_reminder.title}"
        
        return f"""
        ⏰ **Reminders Scheduled!**
        
        {response.message}
        {next_reminder_info}
        
        You'll receive {frequency} reminders to help you stay on track with your goals!
        """
        
    except Exception as e:
        return f"❌ Error scheduling reminders: {str(e)}"

@function_tool()
async def get_upcoming_reminders(ctx: RunContextWrapper[UserSessionContext]) -> str:
    """Get upcoming reminders for the user."""
    
    upcoming = scheduler.get_upcoming_reminders(ctx.context, days_ahead=7)
    
    if not upcoming:
        return "No upcoming reminders scheduled."
    
    reminder_list = "\n".join([
        f"• {reminder.scheduled_date[:10]}: {reminder.title}"
        for reminder in upcoming
    ])
    
    return f"📅 **Upcoming Reminders:**\n{reminder_list}"
