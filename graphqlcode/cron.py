from crontab import CronTab

def __init__(self):
    self.cron = CronTab(user=True)

def add_minutely(self, name, user, command, environment=None):
	"""
	Add an hourly cron task
	"""
    	cron_job = self.cron.new(command='puppet agent' , user='harish')
    	cron_job.minute.every(2)
    	cron_job.enable()
   	self.cron.write()
    	if self.cron.render():
        	print self.cron.render()
        	return True
add_minutely()
