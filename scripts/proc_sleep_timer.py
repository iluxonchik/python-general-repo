# Kills process by image name after a specified timeout
# Useful as a sleep timer for some apps that don't support it natively, like VLC
# Works only on Windows!
# Example usage: python proc_sleep_timer vlc.exe 3600
import sched, time, subprocess, sys

if (len(sys.argv) != 3):
	print("Usage: python proc_sleep_timer.py IMAGE_NAME TIMEOUT")
	sys.exit(1)

image_name = sys.argv[1]
timeout = int(sys.argv[2])

def taskkill_img(image_name):
	p = subprocess.Popen(['taskkill', '/IM', image_name])

s = sched.scheduler(time.monotonic, time.sleep)
s.enter(timeout, 1, taskkill_img, argument=(image_name,))
a=s.run()