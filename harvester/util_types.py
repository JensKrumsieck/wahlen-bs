class Endpoint:
    def __init__(self, id: str, name: str, state: str, baseUrl: str):
        self.id = id
        self.name = name
        self.state = state
        self.baseUrl = baseUrl

    def __init__(self, dict):
        for key in dict:
            setattr(self, key, dict[key])

class ElectionDate:
    def __init__(self, name: str, date: str, url: str, url_alt: str):
        self.name = name
        self.date = date
        self.url = url
        self.url_alt = url_alt

    def __init__(self, dict):
        for key in dict:
            setattr(self, key, dict[key])

    def __repr__(self):
        return f"{self.date} ({self.name})"
    
class Election:
    def __init__(self):
        pass
    def __init__(self, election_date: str, election_name: str, election_type: str):
        self.election_date = election_date
        self.election_name = election_name
        self.election_type = election_type

    def __repr__(self) -> str:
        return f"{self.election_name} ({self.election_date, self.election_type})"