from prisma import Prisma

from util_types import Election

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