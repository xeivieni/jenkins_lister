from jenkinsapi import custom_exceptions
from jenkinsapi.jenkins import Jenkins
from utils import COLORS, format_data


class JenkinsHandler:
    def __init__(self, url, login, password):
        self.url = url
        self.server = Jenkins(url, timeout=2000, username=login, password=password)

    def job_list(self):
        print('%sFetching job list for %s %s...' % (COLORS["blue"], self.url, COLORS['reset']))
        table_data = [
            ['Name', 'Status', 'Url']
        ]
        count = 0
        for job_name, job_instance in self.server.get_jobs():
            count += 1
            if count >= 10:
                break
            table_data.append([
                job_instance.name,
                COLORS["yellow"] + 'RUNNING' + COLORS["reset"] if job_instance.is_running() else
                COLORS["red"] + 'STOPPED' + COLORS["reset"],
                job_instance.url
            ])
        format_data(table_data)
        print("Jobs found: ", len(self.server.get_jobs_list()))

    def job_details(self, job_name):
        print('%sGetting details for job %s on server %s %s...'
              % (COLORS["blue"], job_name, self.url, COLORS['reset']))
        try:
            job = self.server.get_job(job_name)
            print('Got Job %s. Running: %s. Enabled: %s' % (job, job.is_running(), job.is_enabled()))
        except custom_exceptions.UnknownJob:
            print('No job found : %s' % job_name)


