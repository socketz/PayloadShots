# PayloadShots

This application is made to automate the task of reporting many XSS vulnerabilities, and to take a screenshot of each one.

It is a very simple script, and it could be improved a lot, although for the task that has been created it is enough.

If you have suggestions for improvements, do not hesitate to open an issue.

***IMPORTANT NOTE**: Headless execution is not possible, as the alert popup blocks the ability to capture screenshots using Selenium (get_screenshot_as_file and other methods), so this script provides the functionality to be able to capture all the window including the alert popup.*

At the moment it only works with the drivers below:
- [x] Geckodriver
- [x] Chromedriver
- [ ] OperaChromiumDriver
- [ ] Safari WebDriver
- [ ] InternetExplorerDriver
- [ ] Microsoft Edge WebDriver
- [ ] Microsoft Edge Legacy WebDriver

## Requirements
First install the necessary packages with the following command:
```
python -m pip install -U -r requirements.txt
```

Then, download the driver supported from official webpage:
- [Geckodriver](https://github.com/mozilla/geckodriver/releases)
- [Chromedriver](https://chromedriver.chromium.org/downloads) - Please, if you doubt the version to choose, look at the [version-selection](https://chromedriver.chromium.org/downloads/version-selection) page


## Quickstart
This example takes two screenshots from `example_list.txt` included in this repository:
```
python payloadshots.py -b firefox -l example_list.txt
```

## Help
```
usage: payloadshots.py [-h] --browser {firefox,chrome} [--window-size WINDOW_SIZE] [--maximized] [--url URL] [--path PATH] [--name NAME] [--list URL_LIST] [--show]

PayloadShots it's an automation tool for pentesters to reporting previously exploited XSS URLs

optional arguments:
  -h, --help            show this help message and exit
  --browser {firefox,chrome}, -b {firefox,chrome}
                        The webdriver to use. This require a compatible browser installed
  --window-size WINDOW_SIZE, -w WINDOW_SIZE
                        The window size, should be specified by a comma separator. For example: 1024,768 (width, height)
  --maximized, -m       Window size maximized at run. NOTE: If this option it is set, overrides window-size option.
  --url URL, -u URL     The URL to be requested by the browser and take an screenshot
  --path PATH, -p PATH  Output path to save the screenshots
  --name NAME, -n NAME  Screenshot prefix name
  --list URL_LIST, -l URL_LIST
                        URL list file to make the requests by the browser and take an screenshot
  --show, -s            Shows all the screenshots taken, not recommended for multiple URLs
  ```

## TODO
- [ ] Add pip pakage support
- [ ] Add support for more WebDrivers
- [ ] Add support for other type of exploitations (screenshots without alerts, inject scripts on webpages, connect with debugger, etc)

## Credits
Software used by this application:
- [Selenium](https://github.com/SeleniumHQ/selenium/blob/master/LICENSE)
- [PyAutoGUI](https://github.com/asweigart/pyautogui/blob/master/LICENSE.txt)
- [pywin32](https://github.com/mhammond/pywin32)