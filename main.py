import threading
import subprocess

def run_bot_media():
    subprocess.run(["python", "bot_media.py"])

def run_247():
    subprocess.run(["python", "run_247.py"])

t1 = threading.Thread(target=run_bot_media)
t2 = threading.Thread(target=run_247)

t1.start()
t2.start()

t1.join()
t2.join()
