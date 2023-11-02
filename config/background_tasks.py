import glob
import os
from threading import Lock

lock = Lock()

def empty_log_cleaner():

    log_directory = "logs"
    log_files = glob.glob(os.path.join(log_directory, "*.log"))
    if lock.acquire(blocking=False):
        try:
            for log_file in log_files:
                if os.path.getsize(log_file) == 0:
                    os.remove(log_file)
                    print(f"Removed log file: {log_file}")
                # if os.path.basename(log_file).startswith("info"):
                #     with open(log_file, 'r') as f:
                #         for line in f:
                #             if "Cache Hits:" in line:
                #                 os.remove(log_file)
                #                 print(f"Removed log file: {log_file}")
                #                 print(50*"=")
                #                 break
                #     os.remove(log_file)
                #     print(50*"=")
        finally:
            lock.release()
    else:
        print("Another instance is already running. Skipping.")