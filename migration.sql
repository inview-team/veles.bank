CREATE TABLE "user" (
    id UUID PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    phone_number VARCHAR(255) UNIQUE,
    password VARCHAR(255)
);

CREATE TABLE "company" (
    id UUID PRIMARY KEY,
    name VARCHAR(255),
    balance FLOAT,
    email VARCHAR(255)
);

CREATE TABLE "wallet" (
    id UUID PRIMARY KEY,
    balance FLOAT DEFAULT 0.0,
    type VARCHAR(255),
    number VARCHAR(255),
    status BOOLEAN,
    user_id UUID,
    FOREIGN KEY (user_id) REFERENCES "user"(id)
);


CREATE TABLE "transaction" (
    id UUID PRIMARY KEY,
    sender_id UUID,
    receiver_id UUID,
    type VARCHAR(255),
    amount FLOAT
);

CREATE TABLE "authtoken" (
    id UUID PRIMARY KEY,
    token VARCHAR(255),
    type VARCHAR(255),
    user_id UUID,
    FOREIGN KEY (user_id) REFERENCES "user"(id)
);