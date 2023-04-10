# timesheet app

timesheet app with Falcon Rest API Demo application


"""
class TimeEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    task = models.CharField(max_length=200)
"""

## Start server
```bash
  gunicorn -b 127.0.0.1:5000 --reload app.main:application
  ```
