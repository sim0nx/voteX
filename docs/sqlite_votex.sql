PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;

CREATE TABLE "answer" (
  "id" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL,
  "question_id" INTEGER NOT NULL,
  "name" VARCHAR NOT NULL
);

CREATE TABLE "participant" (
  "id" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL,
  "poll_id" INTEGER NOT NULL,
  "participant" VARCHAR NOT NULL,
  "key" VARCHAR NOT NULL,
  "update_date" DATETIME
);

CREATE TABLE "poll" (
  "id" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL,
  "name" VARCHAR NOT NULL,
  "owner" VARCHAR NOT NULL,
  "instructions" TEXT NOT NULL,
  "expiration_date" DATETIME NOT NULL,
  "public" INTEGER NOT NULL,
  "running" INTEGER NOT NULL
);

CREATE TABLE "question" (
  "id" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL,
  "poll_id" INTEGER NOT NULL,
  "question" VARCHAR NOT NULL,
  "type" INTEGER NOT NULL,
  "mandatory" INTEGER NOT NULL
);

CREATE TABLE "submission" (
  "id" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL,
  "poll_id" INTEGER NOT NULL,
  "question_id" INTEGER NOT NULL,
  "participant_id" INTEGER NOT NULL,
  "answer_id" INTEGER NOT NULL,
  "update_date" DATETIME,
  "answer_text" TEXT,
  "answer_bool" INTEGER
);

CREATE TABLE "login" (
  "id" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL,
  "username" VARCHAR NOT NULL,
  "password" VARCHAR NOT NULL,
  "email" VARCHAR NOT NULL,
  "last_login" DATETIME NOT NULL
);

COMMIT;
