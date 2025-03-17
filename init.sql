-- Required to be able to user gen_random_uuid
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Delete data if exists
DELETE FROM review;
DELETE FROM book;
DELETE FROM "user";

-- Reset the ID to start with 1
ALTER SEQUENCE user_id_seq RESTART WITH 1;
ALTER SEQUENCE review_id_seq RESTART WITH 1;

-- Insert data
-- All users have the same password (Bookhive1234)
INSERT INTO "user" (username, email, first_name, last_name, password_hash, is_verified, role, created_at, updated_at)
VALUES
    ('user1', 'johndoe89@example.com', 'John', 'Doe', '$5$rounds=535000$GUfl71a9h8pJj8Sg$TzyBL5pYQ2JQfrf.h18PBqR40dyXUMVcAfoeWCKn.HA', TRUE, 'user', NOW(), NOW()),
    ('user2', 'janesmith22@outlook.com', 'Jane', 'Smith', '$5$rounds=535000$GUfl71a9h8pJj8Sg$TzyBL5pYQ2JQfrf.h18PBqR40dyXUMVcAfoeWCKn.HA', FALSE, 'admin', NOW(), NOW()),
    ('user3', 'alexjohnson77@gmail.com', 'Alice', 'Johnson', '$5$rounds=535000$GUfl71a9h8pJj8Sg$TzyBL5pYQ2JQfrf.h18PBqR40dyXUMVcAfoeWCKn.HA', TRUE, 'user', NOW(), NOW()),
    ('user4', 'emily.brown@companymail.com', 'Bob', 'Brown', '$5$rounds=535000$GUfl71a9h8pJj8Sg$TzyBL5pYQ2JQfrf.h18PBqR40dyXUMVcAfoeWCKn.HA', FALSE, 'moderator', NOW(), NOW()),
    ('user5', 'michael.white@yahoo.com', 'Charlie', 'Davis', '$5$rounds=535000$GUfl71a9h8pJj8Sg$TzyBL5pYQ2JQfrf.h18PBqR40dyXUMVcAfoeWCKn.HA', TRUE, 'user', NOW(), NOW()),
    ('user6', 'katie.miller@domain.org', 'Daniel', 'Martinez', '$5$rounds=535000$GUfl71a9h8pJj8Sg$TzyBL5pYQ2JQfrf.h18PBqR40dyXUMVcAfoeWCKn.HA', TRUE, 'admin', NOW(), NOW()),
    ('user7', 'robert.james@webmail.com', 'Emily', 'Harris', '$5$rounds=535000$GUfl71a9h8pJj8Sg$TzyBL5pYQ2JQfrf.h18PBqR40dyXUMVcAfoeWCKn.HA', FALSE, 'user', NOW(), NOW()),
    ('user8', 'lisa.jones@email.co', 'Frank', 'Wilson', '$5$rounds=535000$GUfl71a9h8pJj8Sg$TzyBL5pYQ2JQfrf.h18PBqR40dyXUMVcAfoeWCKn.HA', TRUE, 'moderator', NOW(), NOW()),
    ('user9', 'brian.clark@mybusiness.com', 'Grace', 'Taylor', '$5$rounds=535000$GUfl71a9h8pJj8Sg$TzyBL5pYQ2JQfrf.h18PBqR40dyXUMVcAfoeWCKn.HA', FALSE, 'user', NOW(), NOW()),
    ('user10', 'sarah.williams@university.edu', 'Henry', 'Anderson', '$5$rounds=535000$GUfl71a9h8pJj8Sg$TzyBL5pYQ2JQfrf.h18PBqR40dyXUMVcAfoeWCKn.HA', TRUE, 'user', NOW(), NOW()),
    ('user11', 'mark.taylor@personalmail.com', 'Isla', 'Thomas', '$5$rounds=535000$GUfl71a9h8pJj8Sg$TzyBL5pYQ2JQfrf.h18PBqR40dyXUMVcAfoeWCKn.HA', TRUE, 'admin', NOW(), NOW()),
    ('user12', 'olivia.anderson@companymail.org', 'Jack', 'Moore', '$5$rounds=535000$GUfl71a9h8pJj8Sg$TzyBL5pYQ2JQfrf.h18PBqR40dyXUMVcAfoeWCKn.HA', FALSE, 'user', NOW(), NOW()),
    ('user13', 'james.wilson@techmail.com', 'Katie', 'Lee', '$5$rounds=535000$GUfl71a9h8pJj8Sg$TzyBL5pYQ2JQfrf.h18PBqR40dyXUMVcAfoeWCKn.HA', TRUE, 'moderator', NOW(), NOW()),
    ('user14', 'charlotte.moore@outlook.net', 'Liam', 'Clark', '$5$rounds=535000$GUfl71a9h8pJj8Sg$TzyBL5pYQ2JQfrf.h18PBqR40dyXUMVcAfoeWCKn.HA', FALSE, 'user', NOW(), NOW()),
    ('user15', 'george.thompson@gmail.com', 'Mia', 'Lewis', '$5$rounds=535000$GUfl71a9h8pJj8Sg$TzyBL5pYQ2JQfrf.h18PBqR40dyXUMVcAfoeWCKn.HA', TRUE, 'user', NOW(), NOW()),
    ('user16', 'lucy.scott@domain.co', 'Noah', 'Walker', '$5$rounds=535000$GUfl71a9h8pJj8Sg$TzyBL5pYQ2JQfrf.h18PBqR40dyXUMVcAfoeWCKn.HA', TRUE, 'admin', NOW(), NOW()),
    ('user17', 'adam.davis@mailbox.com', 'Olivia', 'Hall', '$5$rounds=535000$GUfl71a9h8pJj8Sg$TzyBL5pYQ2JQfrf.h18PBqR40dyXUMVcAfoeWCKn.HA', FALSE, 'user', NOW(), NOW()),
    ('user18', 'grace.martinez@workemail.com', 'Peter', 'Allen', '$5$rounds=535000$GUfl71a9h8pJj8Sg$TzyBL5pYQ2JQfrf.h18PBqR40dyXUMVcAfoeWCKn.HA', TRUE, 'moderator', NOW(), NOW()),
    ('user19', 'peter.kim@businessmail.com', 'Quinn', 'Young', '$5$rounds=535000$GUfl71a9h8pJj8Sg$TzyBL5pYQ2JQfrf.h18PBqR40dyXUMVcAfoeWCKn.HA', FALSE, 'user', NOW(), NOW()),
    ('user20', 'hannah.lee@webservice.org', 'Ryan', 'King', '$5$rounds=535000$GUfl71a9h8pJj8Sg$TzyBL5pYQ2JQfrf.h18PBqR40dyXUMVcAfoeWCKn.HA', TRUE, 'user', NOW(), NOW());


INSERT INTO book (id, title, author, publisher, published_date, page_count, language, created_at, updated_at, user_id)
VALUES
    (gen_random_uuid(), 'The Great Gatsby', 'F. Scott Fitzgerald', 'Scribner', '1925-04-10', 218, 'en', NOW(), NOW(), 1),
    (gen_random_uuid(), 'To Kill a Mockingbird', 'Harper Lee', 'J.B. Lippincott & Co.', '1960-07-11', 281, 'en', NOW(), NOW(), 2),
    (gen_random_uuid(), '1984', 'George Orwell', 'Secker & Warburg', '1949-06-08', 328, 'en', NOW(), NOW(), 3),
    (gen_random_uuid(), 'Pride and Prejudice', 'Jane Austen', 'T. Egerton', '1813-01-28', 279, 'en', NOW(), NOW(), 4),
    (gen_random_uuid(), 'Moby-Dick', 'Herman Melville', 'Harper & Brothers', '1851-10-18', 635, 'en', NOW(), NOW(), 5),
    (gen_random_uuid(), 'War and Peace', 'Leo Tolstoy', 'The Russian Messenger', '1869-01-01', 1225, 'ru', NOW(), NOW(), 6),
    (gen_random_uuid(), 'The Odyssey', 'Homer', 'Penguin Classics', '800-01-01', 541, 'gr', NOW(), NOW(), 7),
    (gen_random_uuid(), 'The Catcher in the Rye', 'J.D. Salinger', 'Little, Brown and Company', '1951-07-16', 214, 'en', NOW(), NOW(), 8),
    (gen_random_uuid(), 'Brave New World', 'Aldous Huxley', 'Chatto & Windus', '1932-01-01', 268, 'en', NOW(), NOW(), 9),
    (gen_random_uuid(), 'Crime and Punishment', 'Fyodor Dostoevsky', 'The Russian Messenger', '1866-01-01', 671, 'ru', NOW(), NOW(), 10),
    (gen_random_uuid(), 'The Hobbit', 'J.R.R. Tolkien', 'George Allen & Unwin', '1937-09-21', 310, 'en', NOW(), NOW(), 11),
    (gen_random_uuid(), 'The Lord of the Rings', 'J.R.R. Tolkien', 'George Allen & Unwin', '1954-07-29', 1178, 'en', NOW(), NOW(), 12),
    (gen_random_uuid(), 'Frankenstein', 'Mary Shelley', 'Lackington, Hughes, Harding, Mavor & Jones', '1818-01-01', 280, 'en', NOW(), NOW(), 13),
    (gen_random_uuid(), 'Dracula', 'Bram Stoker', 'Archibald Constable and Company', '1897-05-26', 418, 'en', NOW(), NOW(), 14),
    (gen_random_uuid(), 'The Alchemist', 'Paulo Coelho', 'HarperOne', '1988-01-01', 208, 'pt', NOW(), NOW(), 15),
    (gen_random_uuid(), 'Don Quixote', 'Miguel de Cervantes', 'Francisco de Robles', '1605-01-16', 863, 'es', NOW(), NOW(), 16),
    (gen_random_uuid(), 'The Divine Comedy', 'Dante Alighieri', 'Niccolò di Lorenzo della Magna', '1320-01-01', 798, 'it', NOW(), NOW(), 17),
    (gen_random_uuid(), 'Les Misérables', 'Victor Hugo', 'A. Lacroix, Verboeckhoven & Cie.', '1862-01-01', 1463, 'fr', NOW(), NOW(), 18),
    (gen_random_uuid(), 'Ulysses', 'James Joyce', 'Shakespeare and Company', '1922-02-02', 730, 'en', NOW(), NOW(), 19),
    (gen_random_uuid(), 'Anna Karenina', 'Leo Tolstoy', 'The Russian Messenger', '1878-01-01', 864, 'ru', NOW(), NOW(), 20);


INSERT INTO review (text, rating, created_at, user_id, book_id) 
VALUES
    ('Great read!', floor(random() * 4 + 1), current_timestamp, (SELECT id FROM "user" ORDER BY random() LIMIT 1), (SELECT id FROM "book" ORDER BY random() LIMIT 1)),
    ('Good, but a bit slow at times.', floor(random() * 4 + 1), current_timestamp, (SELECT id FROM "user" ORDER BY random() LIMIT 1), (SELECT id FROM "book" ORDER BY random() LIMIT 1)),
    ('Loved the ending!', floor(random() * 4 + 1), current_timestamp, (SELECT id FROM "user" ORDER BY random() LIMIT 1), (SELECT id FROM "book" ORDER BY random() LIMIT 1)),
    ('Could not put it down!', floor(random() * 4 + 1), current_timestamp, (SELECT id FROM "user" ORDER BY random() LIMIT 1), (SELECT id FROM "book" ORDER BY random() LIMIT 1)),
    ('It was just okay.', floor(random() * 4 + 1), current_timestamp, (SELECT id FROM "user" ORDER BY random() LIMIT 1), (SELECT id FROM "book" ORDER BY random() LIMIT 1)),
    ('Really enjoyed the plot twists!', floor(random() * 4 + 1), current_timestamp, (SELECT id FROM "user" ORDER by random() LIMIT 1), (SELECT id FROM "book" ORDER BY random() LIMIT 1)),
    ('A decent story, but predictable.', floor(random() * 4 + 1), current_timestamp, (SELECT id FROM "user" ORDER BY random() LIMIT 1), (SELECT id FROM "book" ORDER BY random() LIMIT 1)),
    ('Amazing character development.', floor(random() * 4 + 1), current_timestamp, (SELECT id FROM "user" ORDER BY random() LIMIT 1), (SELECT id FROM "book" ORDER BY random() LIMIT 1)),
    ('The pacing was off, but it was good overall.', floor(random() * 4 + 1), current_timestamp, (SELECT id FROM "user" ORDER BY random() LIMIT 1), (SELECT id FROM "book" ORDER BY random() LIMIT 1)),
    ('The plot was a bit too complicated.', floor(random() * 4 + 1), current_timestamp, (SELECT id FROM "user" ORDER BY random() LIMIT 1), (SELECT id FROM "book" ORDER BY random() LIMIT 1)),
    ('Good writing, but I expected more action.', floor(random() * 4 + 1), current_timestamp, (SELECT id FROM "user" ORDER BY random() LIMIT 1), (SELECT id FROM "book" ORDER BY random() LIMIT 1)),
    ('Not my favorite, but still interesting.', floor(random() * 4 + 1), current_timestamp, (SELECT id FROM "user" ORDER BY random() LIMIT 1), (SELECT id FROM "book" ORDER BY random() LIMIT 1)),
    ('Well-written, but the ending was predictable.', floor(random() * 4 + 1), current_timestamp, (SELECT id FROM "user" ORDER BY random() LIMIT 1), (SELECT id FROM "book" ORDER BY random() LIMIT 1)),
    ('Interesting premise, but the execution lacked depth.', floor(random() * 4 + 1), current_timestamp, (SELECT id FROM "user" ORDER BY random() LIMIT 1), (SELECT id FROM "book" ORDER BY random() LIMIT 1)),
    ('Very immersive world-building.', floor(random() * 4 + 1), current_timestamp, (SELECT id FROM "user" ORDER BY random() LIMIT 1), (SELECT id FROM "book" ORDER BY random() LIMIT 1)),
    ('Good, but I did not feel emotionally connected.', floor(random() * 4 + 1), current_timestamp, (SELECT id FROM "user" ORDER BY random() LIMIT 1), (SELECT id FROM "book" ORDER BY random() LIMIT 1)),
    ('The storyline was captivating, though slow in parts.', floor(random() * 4 + 1), current_timestamp, (SELECT id FROM "user" ORDER BY random() LIMIT 1), (SELECT id FROM "book" ORDER BY random() LIMIT 1)),
    ('Well-paced and enjoyable.', floor(random() * 4 + 1), current_timestamp, (SELECT id FROM "user" ORDER BY random() LIMIT 1), (SELECT id FROM "book" ORDER BY random() LIMIT 1)),
    ('A light and fun read.', floor(random() * 4 + 1), current_timestamp, (SELECT id FROM "user" ORDER BY random() LIMIT 1), (SELECT id FROM "book" ORDER BY random() LIMIT 1)),
    ('The dialogue was a highlight.', floor(random() * 4 + 1), current_timestamp, (SELECT id FROM "user" ORDER BY random() LIMIT 1), (SELECT id FROM "book" ORDER BY random() LIMIT 1)),
    ('Great start but dragged in the middle.', floor(random() * 4 + 1), current_timestamp, (SELECT id FROM "user" ORDER BY random() LIMIT 1), (SELECT id FROM "book" ORDER BY random() LIMIT 1)),
    ('Thoroughly enjoyed it.', floor(random() * 4 + 1), current_timestamp, (SELECT id FROM "user" ORDER BY random() LIMIT 1), (SELECT id FROM "book" ORDER BY random() LIMIT 1));


SELECT 'Table user has ' || count(*) || ' records' FROM "user";
SELECT 'Table book has ' || count(*) || ' records' FROM "book";
SELECT 'Table review has ' || count(*) || ' records' FROM "review";
