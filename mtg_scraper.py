from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import regex as re


class Scraper:

    def __init__(self):
        options = Options()
        options.headless = True
        options.add_argument("--window-size=1920,1200")
        self.driver = webdriver.Chrome(executable_path="chromedriver.exe")
        self.card_list = None
        self.deck_list = None

    def reopen_driver(self):
        self.driver = webdriver.Chrome(executable_path="chromedriver.exe")

    """
    TODO:
    - Inputs for deck themes
    """
    def find_commander(self):
        commander = input("Commander name: ")
        commander = re.split(r'[\- ,]', commander)
        cleaned_commander = []
        for word in commander:
            word = ''.join(e for e in word if e.isalnum() and e not in [" ", "-"])
            cleaned_commander += [word]
        commander = cleaned_commander
        commander = "-".join(commander)

        pricing = input("Expensive, budget, or none: ")
        path = f"https://edhrec.com/average-decks/{commander}"
        if pricing.lower() != "none":
            path += f"/{pricing}"

        self.driver.get(path)
        self.driver.implicitly_wait(1)
        body = self.driver.find_elements_by_class_name("card-body")
        self.card_list = body[-1].text
        self.driver.quit()

        ERROR = "The error has been recorded. New cards take a few days to show up on EDHREC. Otherwise, you can also" \
                " report a bug to help us fix it faster."
        if self.card_list == ERROR:
            print("Commander Not Found")
            print("Please Try again")
            self.reopen_driver()
            self.find_commander()

        print("Commander Found")

    def scrape_list(self):
        print("Scraping List")
        card_list = self.card_list.split("\n")
        cleaned_list = []
        for card in card_list:
            if not any(char.isdigit() for char in card):
                continue
            cleaned_list += [card]

        card_list = cleaned_list
        self.deck_list = {}  # card name: number
        for card in card_list:
            pieces = card.split(" ")
            self.deck_list[pieces[1]] = pieces[0]
        print("Finished")

    def export_to_file(self, filepath):
        with open(filepath, "w", encoding="utf-8") as f:
            for k in self.deck_list:
                f.write(f"{k} {self.deck_list[k]}\n")
