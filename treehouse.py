import os
import sys
import argparse
import mechanize
import cookielib
from downloader import TreehouseDownloader


def main():
      # Set up expected command line arguments
      parser = argparse.ArgumentParser()
      parser.add_argument("course_url", help="URL of main course page")
      parser.add_argument("save_folder", help="subfolder of /downloads to save course videos in")
      parser.add_argument("email", help="your Treehouse account email")
      parser.add_argument("password", help="your Treehouse account password")
      parser.add_argument("-s", "--skip", action="store_true", help="skip already downloaded videos")

      # Set up browser
      browser = mechanize.Browser()
      cookie_jar = cookielib.LWPCookieJar()

      browser.set_cookiejar(cookie_jar)

      user_agent = 'Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36'
      browser.addheaders = [('User-agent', user_agent)]
      browser.set_handle_robots(False)

      # Extract command line arguments
      args = parser.parse_args()

      url = args.course_url
      folder = args.save_folder
      email = args.email
      password = args.password
      skip = args.skip

      # Run bot
      downloader = TreehouseDownloader(browser, url, folder, email, password, skip_downloaded=skip)

      try:
            downloader.download_videos()
      except KeyboardInterrupt:
            print '\nBye. See you soon :)'
            sys.exit(0)


if __name__ == '__main__':
    main()
