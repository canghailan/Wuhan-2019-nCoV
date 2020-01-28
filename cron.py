from datetime import datetime
import subprocess
from apscheduler.schedulers.blocking import BlockingScheduler


def run():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cmds = [
        ["git", "pull"],
        ["git", "add", "."],
        ["git", "commit", "-m", f"""{now}自动更新"""],
        ["git", "push"]
    ]
    for cmd in cmds:
        print(" ".join(cmd))
        print(subprocess.check_output(cmd).decode())


run()

# scheduler = BlockingScheduler()
# scheduler.add_job(run, 'cron', second="3")
# scheduler.start()
