-- CreateEnum
CREATE TYPE "ElectionType" AS ENUM ('bundestagswahl', 'landtagswahl', 'europawahl', 'ratswahl', 'buergermeisterwahl');

-- CreateEnum
CREATE TYPE "VoteType" AS ENUM ('primary_vote', 'secondary_vote');

-- CreateTable
CREATE TABLE "Election" (
    "election_id" SERIAL NOT NULL,
    "election_name" TEXT NOT NULL,
    "election_date" TIMESTAMP(3) NOT NULL,
    "election_type" "ElectionType" NOT NULL,

    CONSTRAINT "Election_pkey" PRIMARY KEY ("election_id")
);

-- CreateTable
CREATE TABLE "District" (
    "district_id" SERIAL NOT NULL,
    "district_name" TEXT NOT NULL,
    "city" TEXT,
    "state" TEXT,
    "registered_voters" INTEGER NOT NULL,
    "voters_voted" INTEGER NOT NULL,
    "election_id" INTEGER,

    CONSTRAINT "District_pkey" PRIMARY KEY ("district_id")
);

-- CreateTable
CREATE TABLE "Party" (
    "party_id" SERIAL NOT NULL,
    "party_name" TEXT NOT NULL,

    CONSTRAINT "Party_pkey" PRIMARY KEY ("party_id")
);

-- CreateTable
CREATE TABLE "Vote" (
    "vote_id" SERIAL NOT NULL,
    "district_id" INTEGER NOT NULL,
    "party_id" INTEGER NOT NULL,
    "election_id" INTEGER NOT NULL,
    "vote_type" "VoteType" NOT NULL,
    "vote_count" INTEGER NOT NULL,

    CONSTRAINT "Vote_pkey" PRIMARY KEY ("vote_id")
);

-- AddForeignKey
ALTER TABLE "District" ADD CONSTRAINT "District_election_id_fkey" FOREIGN KEY ("election_id") REFERENCES "Election"("election_id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Vote" ADD CONSTRAINT "Vote_election_id_fkey" FOREIGN KEY ("election_id") REFERENCES "Election"("election_id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Vote" ADD CONSTRAINT "Vote_district_id_fkey" FOREIGN KEY ("district_id") REFERENCES "District"("district_id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Vote" ADD CONSTRAINT "Vote_party_id_fkey" FOREIGN KEY ("party_id") REFERENCES "Party"("party_id") ON DELETE RESTRICT ON UPDATE CASCADE;
