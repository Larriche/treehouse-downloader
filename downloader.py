import os
import re
import time
import sqlite3
from bs4 import BeautifulSoup

class TreehouseDownloader:
    def __init__(self, browser, landing_page_url, folder, email, password):
        """
        Create a new instance of this class
        """
        # A mechanize object that will handle our browsing
        self.browser = browser

        # URL for main page of a course
        self.landing_page_url = landing_page_url

        # Treehouse user email
        self.email = email

        # Treehouse user password
        self.password = password

        # Main directory for downloads
        self.downloads_folder = folder

        # Base treehouse url
        self.base_url = 'https://teamtreehouse.com'

        # Sqlite database connection handle
        self.conn = None

    def get_step_urls(self):
        """
        Get the urls of the steps that have downloadable videos
        """
        # Visit the page to get course steps
        res = self.browser.open(self.landing_page_url + "/stages")
        html = res.read()

        # Holds url of steps that involve a video tutorial
        # URLs are grouped by course stages
        video_page_urls = {}

        soup = BeautifulSoup(html, "html.parser")

        # Divs housing each stage content
        stage_divs = soup.findAll('div', {'class': 'featurette'})

        for div in stage_divs:
            stage_title = str(div.find('h2').getText()).strip()

            # Links and headings for tutorials in a stage are stored as lists
            for li in div.findAll('li'):
                p = li.find('p')
                a = li.find('a')
                if not p or not a:
                    continue

                # Extract text from the paragraph that may be a duration for
                # video content or otherwise for objectives and question pages
                time_text = str(p.getText()).strip()

                if not hasattr(a, 'href'):
                    continue

                url = a['href']

                # We are adding only URLs whose corresponding info look like durations
                if re.match(r'^(\d+)\:(\d+)$', time_text):
                    video_page_urls.setdefault(stage_title, [])
                    video_page_urls[stage_title].append(url)

        return video_page_urls

    def get_video_url(self, url):
        """
        Extract the HD video url from a single tutorial page
        """
        url = self.base_url + url

        res = self.browser.open(url)
        html = res.read()

        soup = BeautifulSoup(html, "html.parser")
        a = soup.find('a', href=re.compile('.\?hd=yes'))

        if hasattr(a, 'href'):
            return a['href']

        return None

    def download_videos(self):
        """
        Main method to be called to handle video downloads
        """
        setup = self.setup()

        if not setup:
            print "Unable to create connection to cache database. Aborting.."
            return

        login = self.login()

        if not login:
            print 'Log in failed. Aborting..'
            return

        print 'Log in was successful'

        # Create base folder
        if not os.path.exists(self.downloads_folder):
            os.makedirs(self.downloads_folder)

        # Course step urls grouped by stage
        step_urls = self.get_step_urls()

        for stage in step_urls:
            print 'Current stage: ' + stage

            urls = step_urls[stage]
            stage_folder = os.path.join(self.downloads_folder, stage)
            path = self.downloads_folder + '/' + stage + '/'

            # Create sub-directory for a stage
            if not os.path.exists(stage_folder):
                os.makedirs(stage_folder)

            # Video count, will be used in naming videos
            count = 1

            for url in urls:
                # Get the url for the HD content for this course step
                video_url = self.get_video_url(url)

                if not video_url:
                    continue

                video_url = self.base_url + video_url

                # Download the mp4 file as a binary stream and write it out
                print "Downloading and saving video " + str(count)

                res = self.browser.open(video_url)
                data = res.read()
                file_path = path + "video_{}.mp4".format(str(count))

                with open(file_path, 'wb') as file_handle:
                    file_handle.write(data)

                self.save_url(video_url)

                count += 1

                print "Catching my breath :)"
                time.sleep(5)

    def login(self):
        """
        Log in the bot to treehouse
        """
        # URL for logging in
        url = self.base_url + '/signin?return_to=%2F'

        # Get login form, fill it and submit it
        res = self.browser.open(url)
        self.browser.select_form(nr=0)
        self.browser.form['user_session[email]'] = self.email
        self.browser.form['user_session[password]'] = self.password

        self.browser.submit()

        # Check for successful login
        res = self.browser.open(self.landing_page_url)
        html = res.read()

        if "/logout" in html:
            return True

        return False

    def setup(self):
        """
        Check whether urls database exists, if not create it
        """
        # Create the database for storing the video urls
        conn = sqlite3.connect('urls.db')

        table_sql = """
                    CREATE TABLE IF NOT EXISTS urls(
                        url TEXT
                    );
                    """
        if conn is not None:
            try:
                c = conn.cursor()
                c.execute(table_sql)
            except Exception as e:
                return False
        else:
            return False

        self.conn = conn

        return True

    def save_url(self, url):
        """
        Keep track of url of an already downloaded video
        """
        sql = """INSERT INTO urls(url) VALUES(?)"""
        values = (url,)

        with self.conn:
            cur = self.conn.cursor()
            cur.execute(sql, values)

        return



