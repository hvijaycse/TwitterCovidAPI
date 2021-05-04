# Package Scheduler.
from apscheduler.schedulers.blocking import BlockingScheduler
from scrapebed import updateBed_job, callServer
# Main cronjob function.


# Create an instance of scheduler and add function.
scheduler = BlockingScheduler()

# Service to update live bed database
scheduler.add_job(updateBed_job, "interval",  minutes=10)

# Calling heroku api to keep free dyno running
scheduler.add_job(callServer, "interval",  minutes=2)

scheduler.start()
