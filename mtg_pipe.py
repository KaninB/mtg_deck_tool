from mtg_scraper import Scraper
from mtg_parser import Parser

if __name__ == "__main__":
    scraper = Scraper()
    card_list = scraper.find_commander()
    scraper.scrape_list()
    scraper.export_to_file("deck_list.txt")

    parser = Parser(scraper.deck_list)
    data = parser.parse_list()
    parser.export_frame(data, "deck_list.csv")