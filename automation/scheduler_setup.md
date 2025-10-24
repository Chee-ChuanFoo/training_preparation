# Scheduling Automated Reports

This guide explains how to schedule your Python scripts to run automatically without using Airflow.

---

## Windows: Task Scheduler

### Step 1: Create a Batch File

Create a file called `run_report.bat` in your project directory:

```batch
@echo off
cd C:\path\to\your\project\automation
python report_generator.py
pause
```

Or if using a virtual environment:

```batch
@echo off
cd C:\path\to\your\project
call .venv\Scripts\activate
cd automation
python report_generator.py
pause
```

### Step 2: Set Up Task Scheduler

1. **Open Task Scheduler**
   - Press `Win + R`
   - Type `taskschd.msc`
   - Press Enter

2. **Create Basic Task**
   - Click "Create Basic Task" in the right panel
   - Name: "Daily Sales Report"
   - Description: "Generates automated sales report every day"
   - Click "Next"

3. **Set Trigger**
   - Choose "Daily"
   - Click "Next"
   - Set start date and time (e.g., 8:00 AM)
   - Recur every: 1 days
   - Click "Next"

4. **Set Action**
   - Choose "Start a program"
   - Click "Next"
   - Program/script: Browse to your `run_report.bat` file
   - Click "Next"

5. **Finish**
   - Review settings
   - Check "Open the Properties dialog..." if you want to configure more options
   - Click "Finish"

### Step 3: Advanced Settings (Optional)

In the Properties dialog:

- **General Tab**
  - ☑ Run whether user is logged on or not
  - ☑ Run with highest privileges

- **Conditions Tab**
  - ☐ Start only if the computer is on AC power (uncheck if laptop)

- **Settings Tab**
  - ☑ Allow task to be run on demand
  - ☑ Run task as soon as possible after a scheduled start is missed

### Common Schedule Examples

| Schedule | Trigger Settings |
|----------|------------------|
| Every day at 8 AM | Daily, 8:00 AM, Recur every 1 days |
| Every Monday at 9 AM | Weekly, 9:00 AM, Monday |
| First day of month | Monthly, Day 1, 8:00 AM |
| Every hour | Daily, Start time, Repeat task every 1 hour for 1 day |

---

## Mac/Linux: Cron Jobs

### Step 1: Open Crontab

Open Terminal and run:

```bash
crontab -e
```

If this is your first time, it will create a new crontab file.

### Step 2: Add Cron Job

Add a line in the following format:

```
# minute hour day month day_of_week command
0 8 * * * cd /path/to/project && python automation/report_generator.py
```

Or with virtual environment:

```
0 8 * * * cd /path/to/project && source .venv/bin/activate && python automation/report_generator.py
```

### Step 3: Save and Exit

- **vim**: Press `Esc`, then type `:wq` and press Enter
- **nano**: Press `Ctrl+X`, then `Y`, then Enter

### Cron Syntax

```
┌───────────── minute (0 - 59)
│ ┌───────────── hour (0 - 23)
│ │ ┌───────────── day of month (1 - 31)
│ │ │ ┌───────────── month (1 - 12)
│ │ │ │ ┌───────────── day of week (0 - 6) (Sunday=0)
│ │ │ │ │
│ │ │ │ │
* * * * * command to execute
```

### Common Cron Examples

| Schedule | Cron Expression |
|----------|-----------------|
| Every day at 8 AM | `0 8 * * *` |
| Every Monday at 9 AM | `0 9 * * 1` |
| First day of month at 8 AM | `0 8 1 * *` |
| Every hour | `0 * * * *` |
| Every 30 minutes | `*/30 * * * *` |
| Every weekday at 8 AM | `0 8 * * 1-5` |
| Twice a day (8 AM and 8 PM) | `0 8,20 * * *` |

### View Existing Cron Jobs

```bash
crontab -l
```

### Remove All Cron Jobs

```bash
crontab -r
```

### Redirect Output to Log File

```bash
0 8 * * * cd /path/to/project && python automation/report_generator.py >> /path/to/logs/report.log 2>&1
```

---

## Python Alternative: Schedule Library

For a pure Python solution, you can use the `schedule` library.

### Install Schedule

```bash
pip install schedule
```

### Create Scheduler Script

Create `scheduler.py`:

```python
import schedule
import time
from report_generator import main as generate_report

def job():
    """Run the report generation"""
    print(f"Starting scheduled job at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    generate_report()
    print(f"Job completed at {time.strftime('%Y-%m-%d %H:%M:%S')}")

# Schedule the job
schedule.every().day.at("08:00").do(job)

# Or other schedule options:
# schedule.every().hour.do(job)
# schedule.every().monday.at("09:00").do(job)
# schedule.every(10).minutes.do(job)

print("Scheduler started. Press Ctrl+C to stop.")

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(60)  # Check every minute
```

### Run the Scheduler

```bash
python scheduler.py
```

**Note**: This script must keep running. On Windows, you can run it as a background service or use Task Scheduler to start it on boot.

---

## Testing Your Scheduled Task

Before scheduling, test your script manually:

### Windows

```batch
cd C:\path\to\your\project\automation
python report_generator.py
```

### Mac/Linux

```bash
cd /path/to/your/project/automation
python report_generator.py
```

---

## Troubleshooting

### Windows Task Scheduler

**Problem**: Task shows as running but doesn't produce output

**Solutions**:
1. Check the "Last Run Result" code:
   - `0x0`: Success
   - `0x1`: Incorrect function
   - `0x41301`: Task currently running
   
2. Ensure the working directory is correct in your batch file

3. Check that Python is in the system PATH or use full path:
   ```batch
   C:\Python39\python.exe report_generator.py
   ```

4. Enable "Run whether user is logged on or not" and provide credentials

### Mac/Linux Cron

**Problem**: Cron job doesn't run

**Solutions**:
1. Check cron logs:
   ```bash
   # On Mac
   tail -f /var/log/system.log | grep cron
   
   # On Linux
   tail -f /var/log/syslog | grep CRON
   ```

2. Use absolute paths in cron commands

3. Set up environment variables in crontab:
   ```bash
   SHELL=/bin/bash
   PATH=/usr/local/bin:/usr/bin:/bin
   
   0 8 * * * cd /path/to/project && python automation/report_generator.py
   ```

4. Redirect output to a log file to see errors:
   ```bash
   0 8 * * * cd /path && python script.py >> /path/to/log.txt 2>&1
   ```

---

## Best Practices

1. **Test First**: Always test your script manually before scheduling

2. **Use Absolute Paths**: Avoid relative paths in scheduled scripts

3. **Log Everything**: Write logs to track execution and debug issues

4. **Error Handling**: Ensure your script handles errors gracefully

5. **Notifications**: Consider adding email notifications for failures

6. **Monitor**: Regularly check that scheduled tasks are running successfully

7. **Documentation**: Document what each scheduled task does and when it runs

---

## Email Notifications (Optional)

To get email notifications when reports are generated, you can add email functionality to your scripts.

### Example with Gmail

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def send_email_with_attachment(subject, body, to_email, attachment_path):
    """Send email with attachment"""
    from_email = "your_email@gmail.com"
    password = "your_app_password"  # Use App Password, not regular password
    
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'plain'))
    
    # Attach file
    with open(attachment_path, 'rb') as f:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename={attachment_path}')
    msg.attach(part)
    
    # Send email
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(from_email, password)
        server.send_message(msg)
    
    print(f"Email sent to {to_email}")
```

**Note**: For Gmail, you need to create an "App Password" in your Google Account settings.

---

## Resources

- **Windows Task Scheduler**: [Microsoft Docs](https://docs.microsoft.com/en-us/windows/win32/taskschd/task-scheduler-start-page)
- **Cron**: [Crontab.guru](https://crontab.guru/) - Cron expression generator
- **Python Schedule**: [schedule Documentation](https://schedule.readthedocs.io/)

---

## Summary

- **Windows**: Use Task Scheduler with batch files
- **Mac/Linux**: Use cron jobs
- **Python Alternative**: Use `schedule` library with a long-running script
- Always test manually first
- Use absolute paths and proper error handling
- Monitor your scheduled tasks regularly

Happy automating! 🤖

