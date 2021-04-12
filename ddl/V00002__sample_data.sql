-- insert sample data

INSERT INTO api.person (first_name, middle_name, last_name, email, age, meta_create_ts)
VALUES ('Joe', NULL, 'Shmoe', 'joeschmo@gmail.com', '31', NOW()),
       ('Janet', 'Wood', 'Reno', 'reno911@gmail.com', '42', NOW()),
       ('James', NULL, 'Gandolfini', 'soprano@gmail.com', '53', NOW()),
       ('Steve', 'J', 'Buschemi', 'buschemi@hotmail.com', '57', NOW()),
       ('Billy', 'Darrell', 'Mays', 'bmayso@gmail.com', '65', NOW()),
       ('Vince', NULL, 'Vaughn', 'oldschool@aol.com', '56', NOW());