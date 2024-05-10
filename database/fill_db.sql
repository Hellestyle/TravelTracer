USE `stud_v23_she199`;


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

INSERT INTO sight_type (points) VALUES (1), (10), (6), (8), (7), (4), (9), (2), (5), (3);

INSERT INTO sight_type_meta (sight_type_id, language_id, name, description) VALUES
	(1, 1, 'Restaurants', 'Restaurants and cafes'), (1, 2, 'Restauranter', 'Restauranter og kafeer'),
	(2, 1, 'Museums', 'Art, historical, and scientific museums'), (2, 2, 'Museer', 'Kunstmuseer, historiske og vitenskapelige museer'),
	(3, 1, 'Parks', 'Parks and alleys'), (3, 2, 'Parker', 'Parker og smug'),
	(4, 1, 'Natural attractions', 'Mountains, lakes, and other natural places'), (4, 2, 'Naturlig attraksjoner', 'Fjell, innsjøer og andre naturlige steder'),
	(5, 1, 'Monuments', 'Famous monuments'), (5, 2, 'Monumenter', 'Kjente monumenter'),
    (6, 1, 'Libraries', NULL),
    (7, 1, 'Cathedrals', NULL),
    (8, 1, 'Trams', NULL),
    (9, 1, 'Aquariums', NULL),
    (10, 1, 'Ski & Snowboard Areas', NULL);

INSERT INTO age_category () VALUES (), (), (), (), (), (), ();

INSERT INTO age_category_meta (age_category_id, language_id, name) VALUES
	(1, 1, 'Children (0-12 years)'), 
    (2, 1, 'Family-friendly'), 
    (3, 1, 'Teenagers (13-19 years)'), 
    (4, 1, 'Young Adults (20-30 years)'), 
    (5, 1, 'Adults (31-60 years)'), 
    (6, 1, 'Seniors (60+ years)'),
    (7, 1, 'All ages');

INSERT INTO sight (city_id, age_category_id, google_maps_url, active, open_time, close_time) VALUES
	(1, 1, 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2000.365925839628!2d10.740637377483424!3d59.90947417490049!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x46416e88f67085cd%3A0xdcf2357905a03761!2sStatholdergaarden!5e0!3m2!1sno!2sno!4v1709823648099!5m2!1sno!2sno', 1, '6:00', '22:00'),
	(2, 5, 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d1466.3510485544261!2d17.421929099192013!3d68.43704862923146!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x45dbbfb7ea6d0a83%3A0x3b144d7377078f89!2sFuru%20Gastropub!5e0!3m2!1sno!2sno!4v1709823114173!5m2!1sno!2sno', 1, '12:00', '23:00'),
	(3, 1, 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d1386.3987020284865!2d18.968909578055616!3d69.66648738114753!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x45df105e7e017a9b%3A0x451a9b89b8677a2f!2sRestaurant%20Smak%20AS!5e0!3m2!1sno!2sno!4v1709823360328!5m2!1sno!2sno', 1, '6:00', '18:00'),
	(3, 6, 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d1387.329332266788!2d18.96074607805482!3d69.65223428113663!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x45c4c4538f889c73%3A0x7072e24b8fa74ca8!2sPolarmuseet%20i%20Troms%C3%B8!5e0!3m2!1sno!2sno!4v1709823417696!5m2!1sno!2sno', 1, '11:00', '17:00'),
	(3, 1, 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d1386.5696721282113!2d18.944414978055505!3d69.6638689811456!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x45c4c445e2ebeb71%3A0x210cefa26c302f6f!2sCharlottenlund%20aktivitets-%20og%20friluftspark!5e0!3m2!1sno!2sno!4v1709823533949!5m2!1sno!2sno', 0, NULL, NULL),
	(4, 1, 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3025.2676073911716!2d-74.04788002347213!3d40.69010357139694!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x89c251435afe5fdd%3A0x961a3af922a7eeae!2sStatue%20of%20Liberty%20Museum!5e0!3m2!1sno!2sno!4v1709823582662!5m2!1sno!2sno', 1, NULL, NULL),
    (3, 7, 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d1387.4295674942782!2d18.952586477539178!3d69.65069904657312!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x45c4c452d961edcf%3A0xb55f80bb0e84519c!2sTroms%C3%B8%20bibliotek%20og%20byarkiv!5e0!3m2!1sno!2sno!4v1712367327454!5m2!1sno!2sno', 1, '09:00', '19:00'),
    (3, 7, 'https://www.google.com/maps/embed?pb=!1m14!1m8!1m3!1d2775.1893727644406!2d18.987263!3d69.64817!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x45c4c4e4d949bb99%3A0xbaf6c8e4e9ccd3f4!2sArctic%20Cathedral!5e0!3m2!1sen!2sno!4v1712367443446!5m2!1sen!2sno', 1, '11:00', '17:00'),
    (3, 7, 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d731145.2660063057!2d16.90304103704268!3d69.02776090650379!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x45c4c503e5cd6803%3A0x4c8c4f3c4c21549d!2sFjellheisen!5e0!3m2!1sno!2sno!4v1715281177166!5m2!1sno!2sno', 1, '10:00', '22:00'),
    (3, 7, 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d1387.3903053406011!2d18.952035288854972!3d69.65130039999998!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x45c4c4531c14bc57%3A0x178af8af99249f3c!2sRaketten%20Bar%20%26%20P%C3%B8lse!5e0!3m2!1sno!2sno!4v1715284852687!5m2!1sno!2sno', 1, '12:00', '19:00'),
    (3, 2, 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d1387.8887382026544!2d18.947268877538665!3d69.64366604718515!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x45c4c5ae8001d221%3A0xc7ec699ee0c7ce7f!2sPolaria!5e0!3m2!1sno!2sno!4v1715286624812!5m2!1sno!2sno', 1, '10:00', '16:00'),
    (3, 7, 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d1387.32318419682!2d18.95665877753932!3d69.65232844643137!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x45c4c453077b532d%3A0x4ab62ac6cc5fd432!2sPerspektivet%20Museum!5e0!3m2!1sno!2sno!4v1715289021806!5m2!1sno!2sno', 1, '10:00', '16:00'),
    (3, 7, 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d58614.67624783167!2d18.878537884562807!3d69.61468825078992!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x45c4c5826e3d8a33%3A0xca90b9da7a08270f!2sTroms%C3%B8%20Forsvarsmuseum!5e0!3m2!1sno!2sno!4v1715290115403!5m2!1sno!2sno', 1, '12:00', '16:00'),
    (3, 7, 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d1387.5571619871534!2d18.954235377539035!3d69.64874474674316!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x45c4c5acb77d2a8f%3A0xde8cb7984e588950!2sTroms%C3%B8%20domkirke!5e0!3m2!1sno!2sno!4v1715291601278!5m2!1sno!2sno', 1, '12:00', '16:00'),
    (3, 7, 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d1387.3886351538454!2d18.956368078136567!3d69.65132598113594!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x45c4c45310f3497b%3A0xec77855881569573!2sFangstmonument%20(Arctic%20Hunter)!5e0!3m2!1sno!2sno!4v1715294567083!5m2!1sno!2sno', 1, NULL, NULL),
    (3, 2, 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d1385.7384575933381!2d19.066850678138!3d69.67659858115532!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x45c4c498b6d456db%3A0xebde0189e5fa8324!2sTroms%C3%B8%20Alpinpark!5e0!3m2!1sno!2sno!4v1715295367876!5m2!1sno!2sno', 1, '10:00', '20:30'),
    (3, 7, 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3183.5293726830164!2d18.973332611103523!3d69.677009457329!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x45c4c46896595cef%3A0xb631fce0bed01755!2sTroms%C3%B8%20arktisk-alpine%20botanisk%20hage!5e0!3m2!1sno!2sno!4v1715296835320!5m2!1sno!2sno', 1, NULL, NULL),
    (3, 7, 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d1387.559497076841!2d18.958592278136386!3d69.64870898113391!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x45c4c5a97e522b57%3A0xcf0687b87677301b!2sTroll%20Museum!5e0!3m2!1sno!2sno!4v1715297500668!5m2!1sno!2sno', 1, '09:00', '18:00');

INSERT INTO sight_meta (sight_id, language_id, name, address, description) VALUES
	(1, 1, 'Statholdergaarden', 'Raadhusgata 11, Oslo 0151 Norway', 'Statholdergaarden is Bent Stiansen\'s gourmet restaurant. In 1993, Bent Stiansen became the world master of the culinary contest, Bocuse d`Or. He and his team have developed Statholdergaarden into one of Oslo\'s and Norway\'s best restaurants.'), -- https://statholdergaarden.no/en/home?mobile=no
	(2, 1, 'Furu Gastropub', 'Kongens gate 36, Narvik 8514 Norway', NULL),
	(3, 1, 'Restaurant Smak', 'Skippergata 16B, Tromso 9008 Norway', 'At Restaurant Smak located in Tromso, guests can enjoy delightful culinary creations made from locally sourced ingredients. The menu showcases the unique and diverse natural elements of Northern Norway and consists of the finest seasonal ingredients sourced from the region.'), -- https://www.restaurant-smak.no/en/
	(4, 1, 'The Polar Museum', 'Sondre Tollbugt. 11B, Tromso 9008 Norway', 'The Polar Museum opened on June 18, 1978, 50 years to the day after Roald Amundsen left Tromsø on his last expedition, to search for Umberto Nobile and the airship ”Italy”. The museum is situated in an historic Customs warehouse, which dates back to 1830 and has an idyllic location on the waterfront in the historic Skansen area.'), -- https://uit.no/tmu/art?p_document_id=398471
	(5, 1, 'Charlottenlund park', 'Conrad Holmboes veg 89, 9011 Tromso, Norway', NULL),
	(6, 1, 'Statue of Liberty', 'Liberty Island, New York City, NY 10004', 'The Statue of Liberty Enlightening the World was a gift of friendship from the people of France to the people of the United States and is a universal symbol of freedom and democracy. The Statue of Liberty was dedicated on October 28, 1886, designated as a National Monument in 1924 and restored for her centennial on July 4, 1986.'), -- https://www.tripadvisor.com/Attraction_Review-g60763-d103887-Reviews-Statue_of_Liberty-New_York_City_New_York.html
	(7, 1, 'Arctic Cathedral', 'Hans Nilsens veg 41, Tromsdalen 9020 Norway', 'Tromsdalen Church, also known as Ishavskatedralen (The Arctic Cathedral) was dedicated on November 19, 1965. Architect Jan Inge Hovig succeeded in creating a masterpiece. The cathedral is a landmark visible from the Tromsø Sound, the Tromsø Bridge and when landing in Tromsø by aircraft. The 11 aluminium-coated concrete panels on each side of the roof provide the cathedral’s form.'), -- https://www.ishavskatedralen.no/en/the-arctic-cathedral/
    (8, 1, 'Public library and City Archives', 'Groennegata 94, Tromso 9008 Norway', 'The library counts its year of establishment as 1871. At that time, Tromsø Municipality and Tromsø Savings Bank joined forces to form Tromsø Municipal Library. Over the years, the library has been located in several premises around the city. In 2005, the main library moved from its old premises in Storgatbakken to the spectacular building in Fokuskvartalet.'), -- https://tromso.kommune.no/bibliotek/om-biblioteket 
    (9, 1, 'Fjellheisen Tromsø', 'Sollivegen 12, Tromsdalen 9020 Norway', 'Fjell­hei­sen ble byg­get i 1961 av Brød­rene Jakob­sens Rederi, et rederi som drev stort innen polar fangst, fiske og eks­pe­di­sjo­ner i Ark­tis og Antark­tis. Gondo­lene bærer stolt rederiets to symboler; isbjørnen og selen. Fjellheisen strekker seg fra Solliveien i Tromsdalen opp til fjellhyllen Storsteinen. Nedre stasjon ligger på Tromsøs fastland, 50 meter over havet. Øvre stasjon, Fjellstua, ligger 421 m over havet.'), -- https://no.tripadvisor.com/Attraction_Review-g190475-d1889657-Reviews-Fjellheisen_Tromso-Tromso_Troms_Northern_Norway.html 
    (10, 1, 'Raketten', 'Storgata 94B Stortorget, Tromso 9008 Norway', '1 of 20 Quick Bites in Tromso. Quick Bites, Fast Food, Scandinavian.'), -- https://no.tripadvisor.com/Restaurant_Review-g190475-d7035146-Reviews-Raketten-Tromso_Troms_Northern_Norway.html
    (11, 1, 'Polaria', 'Hjalmar Johansens Gate 12, Tromso 9296 Norway', 'Polaria is an Arctic Experience Centre and Aquarium located in the heart of Tromsø. Learn about Climate Change through our brand-new interactive exhibitions, reflect over how all life in the Arctic is connected, and discover how you can make a difference. In our aquarium you will find unique species of fish and crustations from the northern regions, as well as our five seals. Join in on the daily feeding and training sessions of the seals at 10:30, 12:30 and 15:30.'), -- https://www.tripadvisor.com/Attraction_Review-g190475-d319306-Reviews-Polaria-Tromso_Troms_Northern_Norway.html
    (12, 1, 'Perspektivet Museum', 'Storgata 95, Tromso 9008 Norway', 'Temporary exhibitions about contemporary life and society. Situated in the centre of Tromsø in a magnificent 1838 villa, we often show documentary photography and we have a changing events programme. We also operate the Folkeparken open air museum south on the island (buildings open in summer).'), -- https://www.tripadvisor.com/Attraction_Review-g190475-d3476809-Reviews-Perspektivet_Museum-Tromso_Troms_Northern_Norway.html
    (13, 1, 'Tromso Defence Museum', 'Solstrandvegen 370, Tromsdalen 9020 Norway', 'Tromsø War Museum was founded in 1993 to take care of the citys war history from early times - around 1250 - until today.'), -- http://www.tromsoforsvarsmuseum.no/english.html, https://no.tripadvisor.com/Attraction_Review-g190475-d10687810-Reviews-Tromso_Defence_Museum-Tromso_Troms_Northern_Norway.html
    (14, 1, 'Tromso Domkirke', 'Kirkegata 7, Troms0 9008 Norway', 'Tromsø Cathedral (Norwegian: Tromsø domkirke) is a cathedral of the Church of Norway located in the city of Tromsø in Tromsø. The cathedral is the church for the Tromsø Domkirkens parish. It is the headquarters for the Tromsø domprosti (arch-deanery) and the Diocese of Nord-Hålogaland. This cathedral is notable since it is the only Norwegian protestant cathedral made of wood.'), -- https://www.tripadvisor.com/Attraction_Review-g190475-d319297-Reviews-Tromso_Domkirke-Tromso_Troms_Northern_Norway.html, https://no.wikipedia.org/wiki/Tromsø_domkirke 
    (15, 1, 'Fangstmonument Arctic Hunter', 'Stortorget, 9008 Tromso, Norway', 'A statue of a whaler in a boat – Fangstmonument (Arctic Hunter). He is battling rough seas while trying to spear a sea creature.'), -- https://www.tripadvisor.com/Attraction_Review-g190475-d19284578-Reviews-Fangstmonument_Arctic_Hunter-Tromso_Troms_Northern_Norway.html, https://www.waymarking.com/waymarks/WMHKCP_Fangstmonument_Arctic_Hunter_Troms_Norway, https://traveltail.co/country/Norway/Tromsø/activities/4264 
    (16, 1, 'Tromso Alpinpark', 'Jadevegen 129, 9022 Tromso, Norway', 'Tromsø Alpinpark is a ski resort for everyone. The facility has for a number of decades housed alpine sports for all, families with children, tourists and the everyday skier. Tromsø Alpinpark is centrally located just 10 minutes to everywhere, the airport and the city center of Tromsø. You will find the resort right in the heart of the Kroken district on the mainland.'), -- https://tromsoalpinpark.no/en/, https://www.facebook.com/tromsoalpinpark?locale=nb_NO
    (17, 1, 'Tromso Arctic-Alpine Botanic Garden', 'Stakkevollvegen 200, Tromso 9019 Norway', 'The combination of rare plants from the Arctic and from mountains around the world gives Tromso Arctic-Alpine Botanic Garden a distinctive character that cannot be found in any other botanical garden. International media and plant experts recognize the garden as one of the worlds finest.'), -- https://www.tripadvisor.com/Attraction_Review-g190475-d19113499-Reviews-Tromso_Arctic_Alpine_Botanic_Garden-Tromso_Troms_Northern_Norway.html, https://www.tripadvisor.com/Attraction_Review-g190475-d319303-Reviews-Tromso_Botaniske_Hage-Tromso_Troms_Northern_Norway.html, https://www.visittromso.no/book/to-do/881848/tromsø-arctic-alpine-botanical-garden/showdetails 
    (18, 1, 'Troll Museum', 'Kaigata 3, Tromso 9008 Norway', 'Welcome to the first Troll Museum with augmented reality. This is the first and only museum about trolls and fairytales in Norway, and must-do experience. Centrally located in Tromsø city, the Troll Museum is the only place where you can meet with the trolls and discover the magic world of norwegian tales.'); -- https://www.tripadvisor.com/Attraction_Review-g190475-d23625083-Reviews-Troll_Museum-Tromso_Troms_Northern_Norway.html
    
INSERT INTO sight_has_sight_type (sight_id, sight_type_id) VALUES
	(1, 1),
	(2, 1),
	(3, 1),
	(4, 2), (4, 4),
	(5, 3), (5, 4),
	(6, 5),
    (7, 6),
    (8, 7),
    (9, 8),
    (10, 1),
    (11, 9),
    (12, 2),
    (13, 2),
    (14, 7),
    (15, 5),
    (16, 10),
    (17, 3), (17, 4),
    (18, 2);

INSERT INTO sight_photo (sight_id, photo) VALUES
	(1, '1/1.jpg'), (1, '1/2.jpg'),
	(2, '2/1.jpeg'), (2, '2/2.jpeg'), (2, '2/3.jpeg'),
	(3, '3/1.webp'), (3, '3/2.jpg'), (3, '3/3.jpg'),
	(4, '4/1.webp'), (4, '4/2.jpg'),
	(5, '5/1.JPG'),
	(6, '6/1.webp'), (6, '6/2.jpg'), (6, '6/3.jpeg'),
    (7, '7/1.jpg'), (7, '7/2.jpg'), (7, '7/3.jpg'),
    (8, '8/1.jpg'), (8, '8/2.jpeg'), (8, '8/3.jpg'), (8, '8/4.jpeg'),
    (9, '9/1.jpg'), (9, '9/2.jpg'), (9, '9/3.jpg'),
    (10, '10/1.jpg'), (10, '10/2.jpg'), (10, '10/3.jpg'), (10, '10/4.jpg'),
    (11, '11/1.jpg'), (11, '11/2.jpg'), (11, '11/3.jpg'), (11, '11/4.jpg'), (11, '11/5.jpg'),
    (12, '12/1.jpg'), (12, '12/2.jpg'), (12, '12/3.jpg'), (12, '12/4.jpg'),
    (13, '13/1.jpg'), (13, '13/2.jpg'),
    (14, '14/1.jpg'), (14, '14/2.jpg'), (14, '14/3.jpg'),
    (15, '15/1.webp'), (15, '15/2.jpg'),
    (16, '16/1.jpg'), (16, '16/2.jpg'), (16, '16/3.jpg'), (16, '16/4.jpg'),
    (17, '17/1.jpg'), (17, '17/2.jpg'), (17, '17/3.jpg'), (17, '17/4.jpg'),
    (18, '18/1.jpg'), (18, '18/2.jpg'), (18, '18/3.jpg');

INSERT INTO achievement (icon) VALUES ('1.png'), ('2.png'), ('3.png'), ('4.png'), ('5.png'), ('6.png'), ('7.png'), ('8.png'), ('9.png');

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
	(5, 2, 'Kaffeelsker', 'Drikke litt kaffe'),
    (6, 1, 'Between shelves', 'Explore. Learn. Be inspired'),
    (7, 1, 'Echo of the Vaults', 'Learn about history and architecture through visiting cathedrals'),
    (8, 1, 'Conqueror of the Peaks', 'Conquer the heights and take a birds eye view of the world.'),
    (9, 1, 'Lord of the Depths', 'Immerse yourself in a world of underwater flora and fauna revealing the secrets of the ocean depths.');

INSERT INTO sight_has_achievement (achievement_id, sight_id) VALUES
	(4, 1),
	(4, 2), (5, 2),
	(4, 3), (5, 3),
	(1, 4), (2, 4), (3, 4),
	(2, 5),
	(1, 6), (2, 6),
    (6, 7),
    (7, 8),
    (2, 9), (4, 9),
    (4, 10), (5, 10),
    (9, 11), (3, 11),
    (1, 12), (3, 12),
    (3, 13),
    (7, 14),
    (1, 15), (2, 15),
    (8, 16), (2, 16), (3, 16),
    (2, 17), (3, 17),
    (1, 18), (3, 18);

-- Navn generert ved hjelp av Faker Python-biblioteket (fake_names.py)
INSERT INTO `user` (username, email, firstname, lastname, avatar, admin, password) VALUES
	('tetiana2024', 'tetiana.v@example.com', 'Tetiana', 'V', '1.png', 1, 'pbkdf2:sha256:260000$IoGMsP32mSUxsqO7$36e01a1751342caa90bd3e2a540df2387aae463d69a6e188aea0d12e38a9ac09'), -- Password: 123456789
	('jm12345', 'jammil@test.com', 'James', 'Miller', NULL, 0, 'pbkdf2:sha256:260000$IoGMsP32mSUxsqO7$36e01a1751342caa90bd3e2a540df2387aae463d69a6e188aea0d12e38a9ac09'),  -- Password: 123456789
	('cole.ow', 'cole.ow@example.com', 'Cole', 'Owens', '3.jpg', 0, 'pbkdf2:sha256:260000$Ycm39vW9YqX7HjV7$30dc06b7640b2569f536685ce7f9dd4a32403dc185bcebdd7eeb320635e14131'),  -- Password: 123456789
	('den2024', 'denshaw@example.com', 'Denise', 'Shaw', '4.jpeg', 0, 'pbkdf2:sha256:260000$tmCV8uhQYtn8mm4R$6c0daac42b8f17ad05f1817f1705ff6500f7b6b51a137353c1808f1539b7979a'),  -- Password: 123456789
	('mark_sandoval', 'mark.sandoval@test.com', 'Mark', 'Sandoval', NULL, 0, 'pbkdf2:sha256:260000$YsNMbKSbfEUQnEmN$c5cfe6efc879e76d3277e3a50b2c123523533bc059e66aaf2fdb2c2d4c65e2c3'),  -- Password: 123456789
	('abrown', 'abrown@example.com', 'Abigail', 'Brown', NULL, 0, 'pbkdf2:sha256:260000$LIbxJ2uys4OAUNTi$40748d70e16cb95c7dd3cfae70441d68cc166f0675f00f36a2942e31d6a8af00');  -- Password: 123456789

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

INSERT INTO visited_list (user_id, group_id, sight_id, liked) VALUES
	(NULL, 1, 4, 1),
	(NULL, 2, 5, 0),
	(1, NULL, 4, 1), (1, NULL, 2, 0),
	(2, NULL, 4, NULL),
	(5, NULL, 4, NULL),
	(3, NULL, 5, 1),
	(4, NULL, 5, 1);
