from django.apps import AppConfig


class ResumeConfig(AppConfig):
    name = 'resume'
   
    def ready(self):
        import resume.signals 

