from apscheduler.schedulers.background import BackgroundScheduler
from django.core.management import call_command
import logging

logger = logging.getLogger(__name__)

def start_scheduler():
    scheduler = BackgroundScheduler()
    
    # Update daily stats every day at 5 AM
    scheduler.add_job(
        lambda: call_command('update_daily_stats'),
        'cron',
        hour=5,
        minute=0,
        id='update_daily_stats',
        name='Update daily stats',
        replace_existing=True,
    )
    
    # Update weekly stats every Monday at 5 AM
    scheduler.add_job(
        lambda: call_command('update_weekly_stats'),
        'cron',
        day_of_week='mon',
        hour=5,
        minute=0,
        id='update_weekly_stats',
        name='Update weekly stats',
        replace_existing=True,
    )
    
    scheduler.start()
    logger.info("Scheduler started with jobs")