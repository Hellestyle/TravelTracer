USE `stud_v23_she199`;


SET FOREIGN_KEY_CHECKS = 0;

TRUNCATE TABLE achievement; 
TRUNCATE TABLE achievement_meta; 
TRUNCATE TABLE age_category;
TRUNCATE TABLE city;
TRUNCATE TABLE city_meta;
TRUNCATE TABLE country;
TRUNCATE TABLE country_meta;
TRUNCATE TABLE friend;
TRUNCATE TABLE `group`;
TRUNCATE TABLE `language`;
TRUNCATE TABLE page_element;
TRUNCATE TABLE page_element_meta;
TRUNCATE TABLE password_recovery;
TRUNCATE TABLE sight;
TRUNCATE TABLE sight_has_achievement;
TRUNCATE TABLE sight_has_sight_type;
TRUNCATE TABLE sight_meta;
TRUNCATE TABLE sight_photo;
TRUNCATE TABLE sight_type;
TRUNCATE TABLE sight_type_meta;
TRUNCATE TABLE `user`;
TRUNCATE TABLE user_in_group;
TRUNCATE TABLE user_system_meta;
TRUNCATE TABLE verification;
TRUNCATE TABLE visited_list;
TRUNCATE TABLE wishlist;

SET FOREIGN_KEY_CHECKS = 1;


INSERT INTO `language` (name, flag, `default`) VALUES
	('English', 'en.ico', 1), ('Norsk', 'no.ico', 0);

INSERT INTO page_element (name, system_name) VALUES
	('Header Title', 'header_title'), ('Login Page Title', 'login_page_title'), ('Registration Page Title', 'registration_page_title'), ('Logout Button', 'logout_button');

INSERT INTO page_element_meta (page_element_id, language_id, text) VALUES
	(1, 1, 'TraverTracer'), (1, 2, 'TraverTracer'),
	(2, 1, 'Login'), (2, 2, 'Logg Inn'),
	(3, 1, 'Registration'), (3, 2, 'Registrering'),
	(4, 1, 'Logout'), (4, 2, 'Logg ut');

INSERT INTO country () VALUES (), ();

INSERT INTO country_meta (country_id, language_id, name) VALUES
	(1, 1, 'Norway'), (1, 2, 'Norge'),
	(2, 1, 'USA'), (2, 2, 'USA');

INSERT INTO city (country_id) VALUES (1), (1), (1), (2);

INSERT INTO city_meta (city_id, language_id, name) VALUES
	(1, 1, 'Oslo'), (1, 2, 'Oslo'),
	(2, 1, 'Narvik'), (2, 2, 'Narvik'),
	(3, 1, 'Tromso'), (3, 2, 'Tromsø'),
	(4, 1, 'New York'), (4, 2, 'New York');

INSERT INTO sight_type (points) VALUES (5), (8), (4), (10), (4);

INSERT INTO sight_type_meta (sight_type_id, language_id, name, description) VALUES
	(1, 1, 'Restaurants', 'Restaurants and cafes'), (1, 2, 'Restauranter', 'Restauranter og kafeer'),
	(2, 1, 'Museums', 'Art, historical, and scientific museums'), (2, 2, 'Museer', 'Kunstmuseer, historiske og vitenskapelige museer'),
	(3, 1, 'Parks', 'Parks and alleys'), (3, 2, 'Parker', 'Parker og smug'),
	(4, 1, 'Natural attractions', 'Mountains, lakes, and other natural places'), (4, 2, 'Naturlig attraksjoner', 'Fjell, innsjøer og andre naturlige steder'),
	(5, 1, 'Monuments', 'Famous monuments'), (5, 2, 'Monumenter', 'Kjente monumenter');

INSERT INTO age_category (min_age, max_age) VALUES
	(NULL, NULL), (NULL, 6), (6, 13), (13, 18), (18, 25), (25, 45), (45, 65), (65, NULL);

INSERT INTO sight (city_id, age_category_id, google_maps_url, active, open_time, close_time) VALUES
	(1, 1, 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2000.365925839628!2d10.740637377483424!3d59.90947417490049!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x46416e88f67085cd%3A0xdcf2357905a03761!2sStatholdergaarden!5e0!3m2!1sno!2sno!4v1709823648099!5m2!1sno!2sno', 1, '6:00:00', '22:00:00'),
	(2, 5, 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d1466.3510485544261!2d17.421929099192013!3d68.43704862923146!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x45dbbfb7ea6d0a83%3A0x3b144d7377078f89!2sFuru%20Gastropub!5e0!3m2!1sno!2sno!4v1709823114173!5m2!1sno!2sno', 1, '12:00:00', '23:00:00'),
	(3, 1, 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d1386.3987020284865!2d18.968909578055616!3d69.66648738114753!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x45df105e7e017a9b%3A0x451a9b89b8677a2f!2sRestaurant%20Smak%20AS!5e0!3m2!1sno!2sno!4v1709823360328!5m2!1sno!2sno', 1, '6:00:00', '18:00:00'),
	(3, 6, 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d1387.329332266788!2d18.96074607805482!3d69.65223428113663!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x45c4c4538f889c73%3A0x7072e24b8fa74ca8!2sPolarmuseet%20i%20Troms%C3%B8!5e0!3m2!1sno!2sno!4v1709823417696!5m2!1sno!2sno', 1, '11:00:00', '17:00:00'),
	(3, 1, 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d1386.5696721282113!2d18.944414978055505!3d69.6638689811456!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x45c4c445e2ebeb71%3A0x210cefa26c302f6f!2sCharlottenlund%20aktivitets-%20og%20friluftspark!5e0!3m2!1sno!2sno!4v1709823533949!5m2!1sno!2sno', 0, NULL, NULL),
	(4, 1, 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3025.2676073911716!2d-74.04788002347213!3d40.69010357139694!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x89c251435afe5fdd%3A0x961a3af922a7eeae!2sStatue%20of%20Liberty%20Museum!5e0!3m2!1sno!2sno!4v1709823582662!5m2!1sno!2sno', 1, NULL, NULL);

INSERT INTO sight_meta (sight_id, language_id, name, address, description) VALUES
	(1, 1, 'Statholdergaarden', 'Raadhusgata 11, Oslo 0151 Norway', 'Statholdergaarden is Bent Stiansen\'s gourmet restaurant. In 1993, Bent Stiansen became the world master of the culinary contest, Bocuse d`Or. He and his team have developed Statholdergaarden into one of Oslo\'s and Norway\'s best restaurants.'), -- https://statholdergaarden.no/en/home?mobile=no
	(2, 1, 'Furu Gastropub', 'Kongens gate 36, Narvik 8514 Norway', NULL),
	(3, 1, 'Restaurant Smak', 'Skippergata 16B, Tromso 9008 Norway', 'At Restaurant Smak located in Tromso, guests can enjoy delightful culinary creations made from locally sourced ingredients. The menu showcases the unique and diverse natural elements of Northern Norway and consists of the finest seasonal ingredients sourced from the region.'), -- https://www.restaurant-smak.no/en/
	(4, 1, 'The Polar Museum', 'Sondre Tollbugt. 11B, Tromso 9008 Norway', 'The Polar Museum opened on June 18, 1978, 50 years to the day after Roald Amundsen left Tromsø on his last expedition, to search for Umberto Nobile and the airship ”Italy”. The museum is situated in an historic Customs warehouse, which dates back to 1830 and has an idyllic location on the waterfront in the historic Skansen area.'), -- https://uit.no/tmu/art?p_document_id=398471
	(5, 1, 'Charlottenlund park', 'Conrad Holmboes veg 89, 9011 Tromso, Norway', NULL),
	(6, 1, 'Statue of Liberty', 'Liberty Island, New York City, NY 10004', 'The Statue of Liberty Enlightening the World was a gift of friendship from the people of France to the people of the United States and is a universal symbol of freedom and democracy. The Statue of Liberty was dedicated on October 28, 1886, designated as a National Monument in 1924 and restored for her centennial on July 4, 1986.'); -- https://www.tripadvisor.com/Attraction_Review-g60763-d103887-Reviews-Statue_of_Liberty-New_York_City_New_York.html

INSERT INTO sight_has_sight_type (sight_id, sight_type_id) VALUES
	(1, 1),
	(2, 1),
	(3, 1),
	(4, 2), (4, 4),
	(5, 3), (5, 4),
	(6, 5);

INSERT INTO sight_photo (sight_id, photo) VALUES
	(1, '1_1.jpg'), (1, '1_2.jpg'),
	(2, '2_1.jpeg'), (2, '2_2.jpeg'), (2, '2_3.jpeg'),
	(3, '3_1.webp'), (3, '3_2.jpg'), (3, '3_3.jpg'),
	(4, '4_1.webp'), (4, '4_2.jpg'),
	(5, '5_1.JPG'),
	(6, '6_1.webp'), (6, '6_2.jpg'), (6, '6_3.jpeg');

INSERT INTO achievement (icon) VALUES ('1.png'), ('2.png'), ('3.png'), ('4.png'), ('5.png');

INSERT INTO achievement_meta (achievement_id, language_id, name, description) VALUES
	(1, 1, 'Traveler', 'Travel to some outstanding place'),
	(1, 2, 'Reisende', 'Reis til et enestående sted'),
	(2, 1, 'Explorer', 'Walk and enjoy the view'),
	(2, 2, 'Utforsker', 'Gå og nyt utsikten'),
	(3, 1, 'Adventurer', 'Visit some unusual place'),
	(3, 2, 'Eventyrer', 'Besøk et uvanlig sted'),
	(4, 1, 'Gourmet', 'Visit a restaurant'),
	(4, 2, 'Gourmet', 'Besøk en restaurant'),
	(5, 1, 'Coffee Lover', 'Drink some coffee'),
	(5, 2, 'Kaffeelsker', 'drikke litt kaffe');

INSERT INTO sight_has_achievement (achievement_id, sight_id) VALUES
	(4, 1),
	(4, 2), (5, 2),
	(4, 3), (5, 3),
	(1, 4), (2, 4), (3, 4),
	(2, 5),
	(1, 6), (2, 6);

-- Імена згенеровані за допомогою Python бібліотеки Faker (fake_names.py)
INSERT INTO `user` (username, email, firstname, lastname, avatar, admin, password) VALUES
	('tetiana2024', 'tetiana.v@example.com', 'Tetiana', 'V', '1.png', 1, 'pbkdf2:sha256:600000$HQ3uN5G0VQOyzKKId8hSslCW5CNk0uUd$87a2a0112338f66e7f52f332042b88df6e9adf8279117d48030c0d7844f80e91'), -- Password: 12345
	('jm12345', 'jammil@test.com', 'James', 'Miller', NULL, 0, 'pbkdf2:sha256:600000$lGJbCpHVxZhz9EXLmCWawhsOAAy0vm4F$ab3d9defab1ba7a3f65392019173eab7c6dec08ceeb60fe15a0bf8cd7998c773'), -- Password: abc111
	('cole.ow', 'cole.ow@example.com', 'Cole', 'Owens', '3.jpg', 0, 'pbkdf2:sha256:600000$V7Y8pBswMzxDzmZS1cjbieW4qPknOyvN$12906af4a65dd4ed984f72b6180512c8921dd7735b9785fa51a0a8a4fd7a0f60'), -- Password: password2024
	('den2024', 'denshaw@example.com', 'Denise', 'Shaw', '4.jpeg', 0, 'pbkdf2:sha256:600000$PRQZGCEAkCRTQNvAJLMmsjGu2HubvA5i$a71cce403ec9903f932c7c8dfe5bf97296166c0841dd38825f7f159b08b0b7e4'), -- Password: den2024
	('mark_sandoval', 'mark.sandoval@test.com', 'Mark', 'Sandoval', NULL, 0, 'pbkdf2:sha256:600000$urlE71cfZ9h11U66JzSnUkWjKfddXb6Z$e483d473cf11f6be6776b9c0761273abfb91f5484c1c052b8fca8375896d3a85'), -- Password: anbufve12jed23
	('abrown', 'abrown@example.com', 'Abigail', 'Brown', NULL, 0, 'pbkdf2:sha256:600000$xoIGGrf0H9Dgb8395i2KqeEiwKsPxDe2$59a5155db5edd5f7efbfd7979e5c93055d45ed5cdc1cdd49dac5454cae333e42'); -- Password: abcde_zyxwv

INSERT INTO user_system_meta (user_id, verified, open_profile, show_real_name, show_friend_list, current_language, current_city) VALUES
	(1, 1, 1, 1, 1, 1, 3),
	(2, 0, 1, 1, 1, NULL, NULL),
	(3, 1, 0, 1, 1, 2, 1),
	(4, 1, 1, 0, 1, 2, 2),
	(5, 1, 0, 0, 0, 1, NULL),
	(6, 1, 1, 1, 0, NULL, 4);

INSERT INTO verification (user_id, uuid) VALUES (2, 'b115b82c-e613-4ce2-aab0-4df632b8e70d');

INSERT INTO password_recovery (user_id, uuid) VALUES (4, 'a7f8788f-fde3-49ed-961e-601b62427a8f');

INSERT INTO friend (follower, following) VALUES
	(1, 2), (1, 3), (1, 5),
	(2, 1), (2, 4),
	(3, 2), (3, 4), (3, 6),
	(4, 1), (4, 3), (4, 6),
	(5, 1), (5, 2),
	(6, 3), (6, 4), (6, 5);

INSERT INTO `group` (name, description, avatar, open) VALUES
	('Travellers', 'Group of travellers', '1.png', 1),
	('Test', 'Test group', NULL, 0);

INSERT INTO user_in_group (user_id, group_id, leader) VALUES
	(1, 1, 1), (2, 1, 0), (5, 1, 0),
	(3, 2, 1), (4, 2, 0);

INSERT INTO wishlist (user_id, group_id, sight_id) VALUES
	(1, NULL, 1), (1, NULL, 3),
	(5, NULL, 2),
	(NULL, 1, 5), (NULL, 1, 6),
	(NULL, 2, 1), (NULL, 2, 4);

INSERT INTO visited_list (user_id, group_id, sight_id) VALUES
	(NULL, 1, 4),
	(NULL, 2, 5),
	(1, NULL, 4), (1, NULL, 2),
	(2, NULL, 4),
	(5, NULL, 4),
	(3, NULL, 5),
	(4, NULL, 5);