from datetime import datetime
import numpy as np
from prisma import Prisma
from pytz import utc
from util_types import District, Election, Vote

class Database:
    def __init__(self):
        pass

    prisma: Prisma = Prisma()

    async def connect(self):
        await self.prisma.connect()

    async def insertElection(self, election: Election):
        dbo =  await self.prisma.election.find_first(where={"election_name": election.election_name, "election_date" : election.election_date})
        if not dbo:
            dbo = await self.prisma.election.create({
                "election_name": election.election_name,
                "election_date": election.election_date,
                "election_type": election.election_type
            })
        return dbo
    
    async def insertDistrict(self, district: District):
        dbo = await self.prisma.district.find_first(where={"district_name": district.district_name, "city": district.city, "election_id": district.election_id})
        if not dbo:
            dbo = await self.prisma.district.create({
                "district_name": district.district_name,
                "city": district.city,
                "state": district.state,
                "registered_voters": district.registered_voters,
                "voters_voted": district.voters_voted,
                "election_id": district.election_id
            })
        return dbo
    async def getParty(self, partyName: str):
        return await self.prisma.party.find_first(where={"party_name": partyName})

    async def insertParty(self, partyName: str):
        dbo = await self.getParty(partyName)
        if not dbo:
            dbo = await self.prisma.party.create({
                "party_name": partyName
            })
        return dbo
    
    async def insertVote(self, vote: Vote):
        if np.isnan(vote.vote_count):
            vote.vote_count = 0
            
        dbo = await self.prisma.vote.find_first(where={"party_id": vote.party_id, "district_id": vote.district_id, "election_id": vote.election_id, "vote_type": vote.vote_type})
        if not dbo:
            dbo = await self.prisma.vote.create({
                "party_id": vote.party_id,
                "district_id": vote.district_id,
                "election_id": vote.election_id,
                "vote_count": int(vote.vote_count),
                "vote_type": vote.vote_type
            })
        return dbo
    
    async def getVersion(self, city: str):
        return await self.prisma.version.find_first(where={"city": city})
    
    async def isUpToDate(self, city: str, endpoint_version: str) -> bool:
        dbo = await self.getVersion(city)
        if not dbo:
            return False
        date_endpoint_version = datetime.strptime(endpoint_version, "%d.%m.%Y %H:%M:%S %f")
        return dbo.timestamp >= utc.localize(date_endpoint_version)
    
    async def updateVersion(self, city: str, endpoint_version: str):
        dbo = await self.getVersion(city)
        if not dbo:
            await self.prisma.version.create({
                "city": city,
                "timestamp": datetime.strptime(endpoint_version, "%d.%m.%Y %H:%M:%S %f")
            })
        else:
            await self.prisma.version.update({
                "where": {"city": city},
                "data": {"timestamp": datetime.strptime(endpoint_version, "%d.%m.%Y %H:%M:%S %f")}
            })