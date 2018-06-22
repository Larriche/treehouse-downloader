import os
import re
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

    def get_step_urls(self):
        """
        Get the urls of the steps that have downloadable videos
        """
        pass

    def get_video_url(self):
        """
        Extract video url from a single tutorial page
        """
        pass

    def download_videos(self):
        """
        Main method to be called to handle video downloads
        """
        pass

    def login(self):
        """
        Log in the bot to treehouse
        """
        pass