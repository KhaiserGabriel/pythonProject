class Character:
    def __init__(self, player_name="", character_name="", experience=0, level=1):
        self.player_name = player_name
        self.character_name = character_name
        self.experience = experience
        self.level = level
    
    def to_dict(self):
        return {
            "player_name": self.player_name,
            "character_name": self.character_name,
            "experience": self.experience,
            "level": self.level
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            data.get("player_name", ""),
            data.get("character_name", ""),
            data.get("experience", 0),
            data.get("level", 1)
        )

class Campaign:
    def __init__(self, name=""):
        self.name = name
        self.characters = []
    
    def add_character(self, character):
        self.characters.append(character)
    
    def to_dict(self):
        return {
            "name": self.name,
            "characters": [char.to_dict() for char in self.characters]
        }
    
    @classmethod
    def from_dict(cls, data):
        campaign = cls(data.get("name", ""))
        for char_data in data.get("characters", []):
            campaign.add_character(Character.from_dict(char_data))
        return campaign