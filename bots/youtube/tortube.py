# A *SCRATCH* of a bot that watches YouTube videos through tor using selenium and stem
from stem import Signal
from stem.control import Controller
import stem.process
import time, random, signal, sys
from selenium import webdriver
from selenium.webdriver.common.proxy import *

myProxy = "localhost:9150"

proxy = Proxy({
    'proxyType': ProxyType.MANUAL,
    'socksProxy': myProxy,
    'noProxy': ''
    })

def print_bootstrap_lines(line):
  if "Bootstrapped " in line:
    print(line)


print("Starting Tor:\n")

tor_process = stem.process.launch_tor_with_config(
  tor_cmd = "[TOR.EXE_PATH]",
  config = {
    'SocksPort': "9150",
    'ControlPort':"9151"
    },
  init_msg_handler = print_bootstrap_lines,
)
driver = webdriver.Firefox(proxy=proxy)

total_views = 0

try:
    while True:
        driver.get("https://www.atagar.com/echo.php")
        print(driver.find_element_by_tag_name('body').text)

        driver.get("[YoutTube Video Link]")

        watch_time = random.choice(range(20, 41))
        print("Watching video for: " + str(watch_time) + " seconds")
        time.sleep(watch_time)

        with Controller.from_port(port = 9151) as controller:
          controller.authenticate()
          controller.signal(Signal.NEWNYM)

        driver.delete_all_cookies()

        total_views += 1
        print("Views: " + str(total_views))
finally:
    print("Exiting...")
    driver.close()
    tor_process.kill()