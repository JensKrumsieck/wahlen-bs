-- CreateTable
CREATE TABLE "Version" (
    "id" SERIAL NOT NULL,
    "city" TEXT NOT NULL,
    "timestamp" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "Version_pkey" PRIMARY KEY ("id")
);
