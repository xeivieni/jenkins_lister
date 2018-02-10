from jenkinsapi import custom_exceptions
from jenkinsapi.jenkins import Jenkins
from utils import blue, green, red, format_data


class JenkinsHandler:
    def __init__(self, url, login, password):
        self.url = url
        self.server = Jenkins(url, timeout=2000, username=login, password=password)

    def job_list(self):
        print(blue('Fetching job list for %s...' % self.url))
        table_data = [
            ['Name', 'Status', 'Url']
        ]
        for job_name, job_instance in self.server.get_jobs():
            table_data.append([
                job_instance.name,
                green('RUNNING') if job_instance.is_running() else
                blue('STOPPED'),
                job_instance.url
            ])
        format_data(table_data)
        print("Jobs found: ", len(self.server.get_jobs_list()))

    def job_list_active(self):
        print(blue('Fetching job list for %s...' % self.url))
        table_data = [
            ['Name', 'Status', 'Url']
        ]
        count = 0
        for job_name, job_instance in self.server.get_jobs():
            if not job_instance.is_enabled():
                continue
            count += 1
            if count >= 10:
                break
            table_data.append([
                job_instance.name,
                self.job_status(job_instance),
                job_instance.url
            ])
        format_data(table_data)
        print("Jobs found: ", len(self.server.get_jobs_list()))

    def job_details(self, job_name):
        print(blue('Getting details for job %s on server %s ...' % (job_name, self.url)))
        table_data = [
            ['Name', 'Status', 'Url']
        ]
        try:
            job = self.server.get_job(job_name)
            table_data.append([
                job.name,
                self.job_status(job),
                job.url
            ])
            format_data(table_data)
        except custom_exceptions.UnknownJob:
            print('No job found : %s' % job_name)

    @staticmethod
    def job_status(job):
        status = blue("STOPPED")
        if not job.is_enabled():
            status = red("DISABLED")
        if job.is_running():
            status = green("RUNNING")
        return status

