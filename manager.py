import json
import os
from .models import Campaign, Character

class CharacterManager:
    def __init__(self):
        self.campaigns = []
        self.current_campaign_index = -1
        self.load_data()
    
    def create_campaign(self, name):
        new_campaign = Campaign(name)
        self.campaigns.append(new_campaign)
        self.current_campaign_index = len(self.campaigns) - 1
        self.save_data()
        return new_campaign
    
    def get_current_campaign(self):
        if 0 <= self.current_campaign_index < len(self.campaigns):
            return self.campaigns[self.current_campaign_index]
        return None
    
    def add_character(self, character):
        campaign = self.get_current_campaign()
        if campaign:
            campaign.add_character(character)
            self.save_data()
            return True
        return False
    
    def update_character(self, index, character):
        campaign = self.get_current_campaign()
        if campaign and 0 <= index < len(campaign.characters):
            campaign.characters[index] = character
            self.save_data()
            return True
        return False
    
    def save_data(self):
        os.makedirs("data", exist_ok=True)
        with open("data/characters.json", "w", encoding='utf-8') as f:
            json.dump({
                "campaigns": [camp.to_dict() for camp in self.campaigns],
                "current_campaign_index": self.current_campaign_index
            }, f, indent=4, ensure_ascii=False)
    
    def load_data(self):
        try:
            with open("data/characters.json", "r", encoding='utf-8') as f:
                data = json.load(f)
                self.campaigns = [Campaign.from_dict(camp) for camp in data.get("campaigns", [])]
                self.current_campaign_index = data.get("current_campaign_index", -1)
                
                if not self.campaigns:
                    self.current_campaign_index = -1
                elif self.current_campaign_index >= len(self.campaigns):
                    self.current_campaign_index = 0
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            self.campaigns = []
            self.current_campaign_index = -1