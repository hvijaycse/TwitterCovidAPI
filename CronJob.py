# Package Scheduler.
from apscheduler.schedulers.blocking import BlockingScheduler
from scapebed import updateBed_job
# Main cronjob function.



# Create an instance of scheduler and add function.
scheduler = BlockingScheduler()
scheduler.add_job(updateBed_job, "interval",  minutes=10)

scheduler.start()
