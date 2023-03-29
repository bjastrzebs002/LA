import sched
import time

s = sched.scheduler(time.time, time.sleep)


def start_scheduler(job, interval):
    def schedule_job(sc):
        job()
        s.enter(interval * 60, 1, schedule_job, (sc,))

    s.enter(interval * 60, 1, schedule_job, (s,))
    s.run()
