import os, shutil
import datetime as dt

def make_report_dir():
    now = dt.datetime.now().strftime("%m_%d_%H_%M_%S")

    if not os.path.exists("reports"):
        os.makedirs("reports")

    report_dir=f"reports/{now}"
    os.mkdir(report_dir)

    shutil.copyfile("scripts/templates/css/style.css", f"{report_dir}/style.css")
    return report_dir