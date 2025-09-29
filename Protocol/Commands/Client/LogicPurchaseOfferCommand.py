from ByteStream.Reader import Reader
from Logic.Home.LogicShopData import LogicShopData
from Protocol.Messages.Server.AvailableServerCommandMessage import AvailableServerCommandMessage
from Protocol.Commands.Server.LogicGiveDeliveryItemsCommand import LogicGiveDeliveryItemsCommand

class LogicPurchaseOfferCommand(Reader):
    def __init__(self, client, player, initial_bytes):
        super().__init__(initial_bytes)
        self.player = player
        self.client = client
        self.offer_index: int = 0
        self.brawler: int = 0

    def decode(self):
        self.readVInt()
        self.readVInt()
        self.readLogicLong()
        self.offer_index = self.readVInt()
        self.brawler = self.readDataReference()[1]

    def process(self, db):
        offer = LogicShopData.offers[self.offer_index]
        if offer.get("Claimed", False):
            return  # Already claimed

        self.player.delivery_items = {"DeliveryTypes": [100], "Items": []}

        # Dispatch map: OfferID -> handler function
        def handle_gems(item):
            amt = item.get("Amount", 1)
            self.player.delivery_items["Items"].append({"Amount": amt, "Value": 8})
            self.player.gems += amt

        def handle_tokens(item):
            amt = item.get("Amount", 1)
            self.player.delivery_items["Items"].append({"Amount": amt, "DataRef": [0, 0], "Value": 2})
            self.player.token_doubler += amt

        def handle_resources(item):
            self.player.coins += item.get("Amount", 1)
            self.player.delivery_items["Items"].append({"Amount": item.get("Amount", 1), "Value": 7})

        def handle_skins(item):
            iid = item.get("ItemID", 0)
            self.player.delivery_items["Items"].append({"Amount": 1, "Value": 9, "ItemID": [29, iid]})
            if iid not in self.player.unlocked_skins:
                self.player.unlocked_skins.append(iid)

        def handle_brawlers(item):
            dr = item.get("CharacterID", [16, 0])
            self.player.delivery_items["Items"].append({"Amount": item.get("Amount", 1), "DataRef": dr, "Value": 1})
            if dr not in self.player.brawlers_unlocked:
                self.player.brawlers_unlocked.append(dr)

        def handle_brawler_pp(item):
            dr = item.get("CharacterID", [16, 0])
            amt = item.get("Amount", 1)
            self.player.delivery_items["Items"].append({"Amount": amt, "DataRef": dr, "Value": 6})
            key = str(dr[1])
            self.player.brawlers_powerpoints[key] = self.player.brawlers_powerpoints.get(key, 0) + amt

        def handle_delivery_types(item, dtype):
            for _ in range(item.get("Amount", 1)):
                self.player.delivery_items["DeliveryTypes"].append(dtype)
            self.player.delivery_items["Count"] = item.get("Amount", 1)

        # Map OfferID to handler
        dispatch = {
            1: handle_resources,
            3: handle_brawlers,
            4: handle_skins,
            8: handle_brawler_pp,
            9: handle_tokens,
            12: handle_brawler_pp,
            16: handle_gems,
            0: lambda item: handle_delivery_types(item, 10),
            6: lambda item: handle_delivery_types(item, 10),
            10: lambda item: handle_delivery_types(item, 11),
            14: lambda item: handle_delivery_types(item, 12),
        }

        # Process items
        for item in offer["Items"]:
            handler = dispatch.get(item["OfferID"])
            if handler:
                handler(item)
            else:
                print(f"Unsupported offer ID: {item['OfferID']}")

        # Apply cost
        resource_type = offer.get("Currency", 0)
        cost = offer["Cost"]
        if resource_type == 0:
            self.player.gems -= cost
        elif resource_type == 1:
            self.player.coins -= cost
        elif resource_type == 3:
            self.player.resources[3]["Amount"] -= cost

        self.player.db = db
        AvailableServerCommandMessage(self.client, self.player, LogicGiveDeliveryItemsCommand).send()