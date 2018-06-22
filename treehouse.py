import sys
import mechanize
import cookielib
from downloader import TreehouseDownloader


def printUsage():
    print """
          Usage:
             python treehouse.py course_url save_folder email password
         """

inputs = sys.argv

if len(inputs) < 5:
      printUsage()
else:
      browser = mechanize.Browser()
      cookie_jar = cookielib.LWPCookieJar()

      browser.set_cookiejar(cookie_jar)

      user_agent = 'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36'
      browser.addheaders = [('User-agent', user_agent)]
      browser.set_handle_robots(False)

      url, folder, email, password = inputs[1:]

      downloader = TreehouseDownloader(browser, url, folder, email, password)
      downloader.download_videos()

