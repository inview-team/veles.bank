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
    email VARCHAR(255)
);

CREATE TABLE "wallet" (
    id UUID PRIMARY KEY,
    balance FLOAT DEFAULT 0.0,
    type VARCHAR(255),
    number VARCHAR(255),
    status BOOLEAN,
    holder_id UUID
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


INSERT INTO "user" (id, first_name, last_name, email, phone_number, password)
VALUES ('123e4567-e89b-12d3-a456-426614174000', 'Ivan', 'Ivanov', 'ivanovmts@gmail.com', '+79991112233', '$2b$12$7BhL8PRvMxQapKNwnEpw3el/4m4ZLG0vfYWg10Of8HZLt8PkQTSqW');

INSERT INTO "user" (id, first_name, last_name, email, phone_number, password)
VALUES ('614ff9b4-4770-4cf4-acbe-c98d9db151e2', 'Artem', 'Artemov', 'jane.smith@example.com', '+79522470099', '$2b$12$7BhL8PRvMxQapKNwnEpw3el/4m4ZLG0vfYWg10Of8HZLt8PkQTSqW');

INSERT INTO "wallet" (id, balance, type, number, status, holder_id) VALUES ('a1552892-2381-446e-9a13-2a0ec5605a77', 10000, 'debet', '5436600395847640', true, '123e4567-e89b-12d3-a456-426614174000');

INSERT INTO "wallet" (id, balance, type, number, status, holder_id) VALUES ('1395ca4a-2c89-491b-b74c-86f41b5eb15e', 10000, 'debet', '2820583798920165 ', true, '614ff9b4-4770-4cf4-acbe-c98d9db151e2');


INSERT INTO "company" (id, name, email) VALUES ('d0f0926a-9ed2-4474-8e6e-94793eb6654f', 'SkyNet', 'skynet@gmail.com');

INSERT INTO "company" (id, name, email) VALUES ('81edfc20-caf1-477d-add7-2a6ab64fe998', 'Васильчуки', 'vasilchuki@gmail.com');

INSERT INTO "wallet" (id, balance, type, number, status, holder_id) VALUES ('9296dfb5-aa5d-4442-ae74-8addcd5e2fd4', 10000, 'debet', '5454958162571065', true, 'd0f0926a-9ed2-4474-8e6e-94793eb6654f');

INSERT INTO "wallet" (id, balance, type, number, status, holder_id) VALUES ('eeb27a90-5009-498b-8087-a807d426cad5', 10000, 'debet', '2026050757500486 ', true, '81edfc20-caf1-477d-add7-2a6ab64fe998');
