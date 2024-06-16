from prisma import Prisma

from util_types import District, Election

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