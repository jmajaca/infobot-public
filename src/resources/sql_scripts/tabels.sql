DROP TABLE IF EXISTS "user" CASCADE;
DROP TABLE IF EXISTS channel CASCADE;
DROP TABLE IF EXISTS course CASCADE;
DROP TABLE IF EXISTS author CASCADE;
DROP TABLE IF EXISTS notification CASCADE;
DROP TABLE IF EXISTS reminder CASCADE;
DROP TABLE IF EXISTS pin CASCADE;
DROP TABLE IF EXISTS slack_user CASCADE;
DROP TABLE IF EXISTS filter CASCADE;
DROP TABLE IF EXISTS reaction CASCADE;

CREATE TABLE "user"(
    id SERIAL PRIMARY KEY,
    name VARCHAR (64) UNIQUE NOT NULL,
    password VARCHAR(256) NOT NULL
);

CREATE TABLE slack_user(
    id VARCHAR(64) UNIQUE NOT NULL,
    name VARCHAR(64) NOT NULL
);

CREATE TABLE channel(
    id VARCHAR(64) PRIMARY KEY,
    tag VARCHAR(64) UNIQUE NOT NULL,
    creator_id VARCHAR(64) NOT NULL REFERENCES slack_user(id),
    created TIMESTAMP NOT NULL
);

CREATE TABLE course(
    id SERIAL PRIMARY KEY,
    name VARCHAR(64) UNIQUE NOT NULL,
    channel_tag VARCHAR(64) REFERENCES channel(tag),
    url VARCHAR(64) DEFAULT NULL
);

CREATE TABLE author(
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(64) NOT NULL,
    last_name VARCHAR(64) NOT NULL
);

CREATE TABLE notification(
    id SERIAL PRIMARY KEY,
    title VARCHAR(256) NOT NULL,
    site INT REFERENCES course(id),
    author INT REFERENCES author(id),
    publish_date TIMESTAMP NOT NULL,
    text VARCHAR(2048) NOT NULL,
    link varchar(256) NOT NULL
);

CREATE TABLE reminder(
    id SERIAL PRIMARY KEY,
    text VARCHAR(1024) NOT NULL,
    end_date TIMESTAMP NOT NULL,
    timer INTERVAL NOT NULL,
    notification INT NOT NULL REFERENCES notification(id),
    posted BOOLEAN DEFAULT FALSE,
    CONSTRAINT check_timer_positive CHECK(timer > '0 hours')
);

CREATE TABLE pin(
    id SERIAL PRIMARY KEY,
    creation_date TIMESTAMP NOT NULL,
    timer INTERVAL NOT NULL,
    channel VARCHAR(64) REFERENCES channel(id),
    timestamp FLOAT NOT NULL,
    done BOOLEAN DEFAULT FALSE
);

-- TODO make this table
CREATE TABLE Filter(
    id SERIAL PRIMARY KEY,
    ban_title VARCHAR(64) NOT NULL
);

CREATE TABLE reaction(
    id SERIAL PRIMARY KEY,
    name VARCHAR (64) NOT NULL,
    timestamp FLOAT,
    channel VARCHAR(64) REFERENCES channel(id),
    sender VARCHAR(64) NOT NULL REFERENCES slack_user(id),
    receiver VARCHAR(64) NOT NULL REFERENCES slack_user(id)
);