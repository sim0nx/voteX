-- 
-- Created by SQL::Translator::Producer::PostgreSQL
-- Created on Wed Sep 26 13:13:53 2012
-- 
--
-- Table: answer.
--
CREATE TABLE "answer" (
  "id" bigserial NOT NULL,
  "question_id" bigint NOT NULL,
  "name" character varying(255) NOT NULL,
  PRIMARY KEY ("id")
);

--
-- Table: participant.
--
CREATE TABLE "participant" (
  "id" bigserial NOT NULL,
  "poll_id" bigint NOT NULL,
  "key" character varying(64) NOT NULL,
  "update_date" timestamp DEFAULT NULL,
  "mail_sent" smallint NOT NULL DEFAULT 0,
  PRIMARY KEY ("id")
);

--
-- Table: poll.
--
CREATE TABLE "poll" (
  "id" bigserial NOT NULL,
  "name" character varying(255) NOT NULL,
  "owner" character varying(64) NOT NULL,
  "instructions" text NOT NULL,
  "expiration_date" timestamp NOT NULL,
  "public" smallint NOT NULL,
  "running" smallint NOT NULL,
  PRIMARY KEY ("id")
);

--
-- Table: question.
--
CREATE TABLE "question" (
  "id" bigserial NOT NULL,
  "poll_id" bigint NOT NULL,
  "question" character varying(255) NOT NULL,
  "type" smallint NOT NULL,
  "mandatory" smallint NOT NULL,
  PRIMARY KEY ("id")
);

--
-- Table: session.
--
CREATE TABLE "session" (
  "id" serial NOT NULL,
  "namespace" character varying(255) NOT NULL,
  "accessed" timestamp NOT NULL,
  "created" timestamp NOT NULL,
  "data" bytea NOT NULL,
  PRIMARY KEY ("id"),
  CONSTRAINT "namespace" UNIQUE ("namespace")
);

--
-- Table: submission.
--
CREATE TABLE "submission" (
  "id" bigserial NOT NULL,
  "poll_id" bigint NOT NULL,
  "question_id" bigint NOT NULL,
  "participant_id" bigint NOT NULL,
  "answer_id" bigint NOT NULL,
  "update_date" timestamp DEFAULT NULL,
  "answer_text" text,
  "answer_bool" smallint DEFAULT NULL,
  PRIMARY KEY ("id")
);
