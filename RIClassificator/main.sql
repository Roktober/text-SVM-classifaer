CREATE TABLE classification_data (
    id serial primary key,
    stemm_util text NOT NULL unique
);

CREATE TABLE classes (
    id serial primary key,
    stemm_ulit_id serial REFERENCES classification_data(id),
    class_id int NOT NULL,
    source int NOT NULL
);