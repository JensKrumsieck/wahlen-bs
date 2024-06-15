from harvester import Harvester
import asyncio

async def main():
    harvester = Harvester()
    await harvester.db.connect()
    await harvester.harvest() 
    
asyncio.run(main())