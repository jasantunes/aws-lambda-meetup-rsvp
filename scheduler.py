from apscheduler.schedulers.blocking import BlockingScheduler
import meetup_rsvp
import logging

fmt = logging.Formatter('%(asctime)s %(levelname)s %(name)s - %(message)s')
h = logging.StreamHandler()
h.setFormatter(fmt)

log = logging.getLogger('scheduler')
log.setLevel(logging.INFO)
log.addHandler(h)

sched = BlockingScheduler()

@sched.scheduled_job('interval', seconds=3)
def timed_job():
    log.info('Running timed_job')
    meetup_rsvp.rsvp_for_group_events('contracostafc', [r'TUESDAY NIGHT: Small game'])

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
def scheduled_job():
    log('This job is run every weekday at 5pm.')

sched.start()
