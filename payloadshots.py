#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: socketz

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException, NoAlertPresentException
from selenium.webdriver.firefox.options import Options as fOptions
from selenium.webdriver.chrome.options import Options as cOptions
import sys
import time

from pathlib import Path
import pyautogui
import argparse
from argparse import HelpFormatter

from win32 import win32gui
from win32 import win32process
import sys

class PayloadShots(object):
    '''
    PayloadShots it's a simple script for taking automated screenshots, including alert payloads.
    '''
    class bcolors:
        OKBLUE = '\033[94m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
        BLUE = '\033[34m'
        WHITE = '\033[97m'
        BACK_WHITE = '\033[107m'
        BACK_BLACK = '\033[40m'

    def __init__(self, args=None):
        if args == None:
            self.parser = self.argument_parser()
            self.args = self.parser.parse_args()
        else:
            self.args = args
        self.browser = self.args.browser.lower()
        self.maximized = self.args.maximized
        self.driver_setup(self.args.window_size)
        self.screenshots_path = self.args.path
        self.screenshots_prefix = self.args.name
        self.show = self.args.show

    def run(self):
        if self.args.url != None:
            self.capture_payloads([self.args.url])
        elif self.args.url_list != None:
            for url_file in self.args.url_list:
                url_list = [line.rstrip('\n') for line in url_file.readlines()]
                self.capture_payloads(url_list)
        else:
            self.printc('URL list not defined. Exiting...', 'warn')

        # Exiting
        self.quit_driver()

    def argument_parser(self):
        self.parser = argparse.ArgumentParser(
            description="PayloadShots it's an automation tool for pentesters to reporting previously exploited XSS URLs")
        self.parser.add_argument('--browser', '-b', required=True, dest='browser', default="firefox", choices=[
                                 'firefox', 'chrome'], help='The webdriver to use. This require a compatible browser installed')
        self.parser.add_argument('--window-size', '-w', dest='window_size', default="1024,768",
                                 help='The window size, should be specified by a comma separator. For example: 1024,768 (width, height)')
        self.parser.add_argument('--maximized', '-m', dest='maximized', action='store_true',
                                 help='Window size maximized at run. `NOTE`: If this option it is set, overrides window-size option.')
        self.parser.add_argument(
            '--url', '-u', dest='url', help='The URL to be requested by the browser and take an screenshot')
        self.parser.add_argument(
            '--path', '-p', dest='path', default='payloads_screenshots', help='Output path to save the screenshots')
        self.parser.add_argument(
            '--name', '-n', dest='name', default='vuln', help='Screenshot prefix name')
        self.parser.add_argument('--list', '-l', dest='url_list', nargs=1, type=argparse.FileType(
            'r'), default=sys.stdin, help='URL list file to make the requests by the browser and take an screenshot')
        self.parser.add_argument('--show', '-s', dest='show', action='store_true',
                                 help='Shows all the screenshots taken, not recommended for multiple URLs')
        return self.parser

    def driver_setup(self, window_size=None):
        if(self.browser == 'chrome'):
            self.driver = webdriver.Chrome(
                desired_capabilities=self.chrome_caps(), options=self.chrome_setup(window_size))
        elif(self.browser == 'firefox'):
            self.driver = webdriver.Firefox(
                firefox_profile=self.firefox_profile(), options=self.firefox_setup(window_size))
            if self.maximized == True:
                self.driver.maximize_window()

    def firefox_setup(self, window_size):
        options = fOptions()
        # Set the window size of browser
        options.add_argument(f"--window-size={window_size}")
        options.accept_insecure_certs = True
        return options

    def firefox_profile(self):
        cProfile = webdriver.FirefoxProfile()
        cProfile.set_preference(
            'browser.download.manager.showWhenStarting', 'false')
        cProfile.set_preference('browser.urlbar.trimURLs', 'false')
        return cProfile

    def chrome_setup(self, window_size=None):
        options = cOptions()
        if self.maximized == True:
            options.add_argument(f"--start-maximized")
        else:
            options.add_argument(f"--window-size={window_size}")

        return options

    def chrome_caps(self):
        caps = webdriver.DesiredCapabilities.CHROME.copy()
        caps['acceptInsecureCerts'] = True
        return caps

    def get_window_PID(self):
        if(self.browser == 'Chrome'):
            import psutil
            p = psutil.Process(self.driver.service.process.pid)
            return p.children()[0].pid
        else:
            return self.driver.capabilities['moz:processID']

    def screenshot_by_pid(self, procid, maximized=False):
        """
        Method to take the screenshot by PID, this makes the magic works
        """
        self.__HWND = None

        def getHwnd(hwnd, procid):
            if procid in win32process.GetWindowThreadProcessId(hwnd):
                if win32gui.IsWindowVisible(hwnd):
                    self.__HWND = hwnd
        win32gui.EnumWindows(getHwnd, procid)
        if self.__HWND != None:
            win32gui.SetForegroundWindow(self.__HWND)
            x, y, x1, y1 = win32gui.GetClientRect(self.__HWND)
            if maximized == False:
                # Fix only for not maximized window
                x, y = win32gui.ClientToScreen(self.__HWND, (x, y))
            x1, y1 = win32gui.ClientToScreen(self.__HWND, (x1 - x, y1 - y))
            im = pyautogui.screenshot(region=(x, y, x1, y1))
            return im
        else:
            printc("Error taking screenshot", "error")

    def quit_driver(self):
        '''
        Closes the browser and shutdown the driver
        '''
        self.driver.quit()

    def printc(self, msg, msg_type='info'):
        '''
        Prints application messages with colors
        '''
        if msg_type == 'info':
            prefix = f"{self.bcolors.OKBLUE}[+]{self.bcolors.ENDC} "
            print(prefix, msg)
        elif msg_type == 'warn':
            prefix = f"{self.bcolors.WARNING}[+]{self.bcolors.ENDC} "
            print(prefix, msg)
        elif msg_type == 'error':
            prefix = f"{self.bcolors.FAIL}[+]{self.bcolors.ENDC} "
            print(prefix, msg)
        elif msg_type == 'success':
            prefix = f"{self.bcolors.OKGREEN}[+]{self.bcolors.ENDC} "
            print(prefix, msg)
        else:
            print(msg)

    def capture_payloads(self, urls: list):
        """
        Method that iterates over URL's with XSS payload, and capture the window. \n
        To work well, should not perform other tasks at the same time. 
        The only way to capture the result of a payload, was by capturing
        the screen in a specific region that matched the browser window.\n
        NOTE: At the moment, only XSS alert payloads supported

        `urls`: List of URL's with included payload
        """
        # Window PID
        pid = self.get_window_PID()

        # Path to save screenshots
        Path(self.screenshots_path).mkdir(parents=True, exist_ok=True)

        for idx, url in enumerate(urls):
            self.printc("Execution of URL: " + url)
            try:
                self.driver.get(url)
                time.sleep(0.5)  # Wait for correct screenshot
                im = self.screenshot_by_pid(pid, self.maximized)

                if im:
                    if self.show == True:
                        self.printc("Showing screenshot of URL: " + url)
                        im.show()

                    screenshot_filepath = f'{self.screenshots_path}/{self.screenshots_prefix}_{idx:02d}.png'
                    with open(screenshot_filepath, 'wb') as img:
                        self.printc("Saving screenshot at: " +
                                    screenshot_filepath, "success")
                        im.save(img)

                # Needed for next payload execution
                alert = self.driver.switch_to.alert
                alert.dismiss()
            except (UnexpectedAlertPresentException, TimeoutException) as e:
                pass


if __name__ == "__main__":
    # Python version check
    if sys.version_info < (3, 0):
        print("Sorry, this program requires Python 3.x, not Python 2.x\n")
        sys.exit(1)
    
    # Setup and run
    pshots = PayloadShots()
    pshots.run()
