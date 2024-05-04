CREATE TABLE "user" (
    id UUID PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255)
);

CREATE TABLE "account" (
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
    amount FLOAT,
    FOREIGN KEY (sender_id) REFERENCES "account"(id),
    FOREIGN KEY (receiver_id) REFERENCES "account"(id)
)
