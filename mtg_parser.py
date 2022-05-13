import requests
import time
import json
import pandas as pd
import urllib


class Parser:

    def __init__(self, card_list):
        if type(card_list) == dict:
            card_list = list(card_list.keys())
        self.decklist = card_list
        self.ATTRIBUTE_NAMES = ["name", "color_indicator", "cmc", "type_line", "layout", "keywords",
                                "color_identity", "rarity", "oracle_text"]
        self.POTENTIAL_NAMES = ["name", "cmc", "color_indicator", "type_line", "layout", "oracle_text"]

    def parse_list(self):
        print("Parsing unique cards")
        cards_info = []
        idx = 0
        for card in self.decklist:
            card = urllib.parse.quote(card)
            response = requests.get(f"https://api.scryfall.com/cards/search?q={card}")
            time.sleep(0.5)
            card_object = response.content
            card_json = json.loads(card_object.decode("utf-8"))
            card_data = card_json["data"][0]
            card_components = dict()
            card_components["idx"] = idx
            for attr in self.ATTRIBUTE_NAMES:
                if attr in card_data.keys():
                    card_components[attr] = card_data[attr]
                else:
                    card_components[attr] = "NA"
            if "card_faces" in card_data.keys():
                faces = card_data['card_faces']
                for face in faces:
                    for attr in self.POTENTIAL_NAMES:
                        if attr in face.keys():
                            card_components[attr] = face[attr]
                        else:
                            card_components[attr] = "NA"

                    cards_info += [list(card_components.values())]
            else:
                cards_info += [list(card_components.values())]

            idx += 1
            if idx % 5 == 0:
                print (f"Progress ... {idx}/{len(self.decklist)}")
        print("Finished")
        return cards_info

    def export_frame(self, data, filepath):
        df = pd.DataFrame(data, columns=["idx"]+self.ATTRIBUTE_NAMES)
        df.to_csv(filepath)
        print("Exported")
