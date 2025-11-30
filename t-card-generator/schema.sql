DROP TABLE IF EXISTS mp_character;
CREATE TABLE mp_character(
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   firstname VARCHAR(20) NOT NULL,
   lastname VARCHAR(20) NOT NULL,
   original_char_name VARCHAR(50) NOT NULL,
   original_game VARCHAR(50) NOT NULL,
   age SMALLINT UNSIGNED NOT NULL,
   status VARCHAR(20) NOT NULL,
   sex VARCHAR(10) NOT NULL,
   region VARCHAR(30) NOT NULL,
   starter VARCHAR(100) NOT NULL,
   id_number VARCHAR(4) NOT NULL
);

DROP TABLE IF EXISTS physical;
CREATE TABLE physical (
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   character_id INTEGER UNSIGNED NOT NULL,
   description VARCHAR(100) NOT NULL,
   FOREIGN KEY(character_id) REFERENCES mp_character(id)
);

DROP TABLE IF EXISTS mental;
CREATE TABLE mental (
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   character_id INTEGER UNSIGNED NOT NULL,
   description VARCHAR(100) NOT NULL,
   FOREIGN KEY(character_id) REFERENCES mp_character(id)
);

DROP TABLE IF EXISTS object;
CREATE TABLE object (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(25) NOT NULL,
    category VARCHAR(25) NOT NULL
);

INSERT INTO object VALUES
    (NULL, 'Poké Ball', 'balls'),
    (NULL, 'Super Ball', 'balls'),
    (NULL, 'Hyper Ball', 'balls'),
    (NULL, 'Faiblo Ball', 'balls'),
    (NULL, 'Bis Ball', 'balls'),
    (NULL, 'Filet Ball', 'balls'),
    (NULL, 'Speed Ball', 'balls'),
    (NULL, 'Masse Ball', 'balls'),
    (NULL, 'Sombre Ball', 'balls'),
    (NULL, 'Scuba Ball', 'balls'),
    (NULL, 'Master Ball', 'balls'),
    (NULL, 'Potion', 'heal'),
    (NULL, 'Super Potion', 'heal'),
    (NULL, 'Hyper Potion', 'heal'),
    (NULL, 'Potion Max', 'heal'),
    (NULL, 'Eau Fraîche', 'heal'),
    (NULL, 'Soda Cool', 'heal'),
    (NULL, 'Limonade', 'heal'),
    (NULL, 'Lait Meumeu', 'heal'),
    (NULL, 'Anti-Brûle', 'heal'),
    (NULL, 'Anti-Para', 'heal'),
    (NULL, 'Antidote', 'heal'),
    (NULL, 'Antigel', 'heal'),
    (NULL, 'Réveil', 'heal'),
    (NULL, 'Total Soin', 'heal'),
    (NULL, 'Guérison', 'heal'),
    (NULL, 'Rappel', 'heal'),
    (NULL, 'Rappel Max', 'heal'),
    (NULL, 'Pierre Feu', 'evol'),
    (NULL, 'Pierre Eau', 'evol'),
    (NULL, 'Pierre Plante', 'evol'),
    (NULL, 'Pierre Foudre', 'evol'),
    (NULL, 'Pierre Glace', 'evol'),
    (NULL, 'Pierre Soleil', 'evol'),
    (NULL, 'Pierre Lune', 'evol'),
    (NULL, 'Pierre Stase', 'evol'),
    (NULL, 'CT Acier', 'ct'),
    (NULL, 'CT Combat', 'ct'),
    (NULL, 'CT Dragon', 'ct'),
    (NULL, 'CT Eau', 'ct'),
    (NULL, 'CT Electrik', 'ct'),
    (NULL, 'CT Fée', 'ct'),
    (NULL, 'CT Feu', 'ct'),
    (NULL, 'CT Glace', 'ct'),
    (NULL, 'CT Insecte', 'ct'),
    (NULL, 'CT Normal', 'ct'),
    (NULL, 'CT Plante', 'ct'),
    (NULL, 'CT Poison', 'ct'),
    (NULL, 'CT Psy', 'ct'),
    (NULL, 'CT Roche', 'ct'),
    (NULL, 'CT Sol', 'ct'),
    (NULL, 'CT Spectre', 'ct'),
    (NULL, 'CT Ténèbres', 'ct'),
    (NULL, 'CT Vol', 'ct'),
    (NULL, 'Baie Oran', 'berry'),
    (NULL, 'Baie Ceriz', 'berry'),
    (NULL, 'Baie Maron', 'berry'),
    (NULL, 'Baie Pêcha', 'berry'),
    (NULL, 'Baie Fraive', 'berry'),
    (NULL, 'Baie Willia', 'berry'),
    (NULL, 'Baie Kika', 'berry'),
    (NULL, 'Baie Sitrus', 'berry'),
    (NULL, 'Baie Prine', 'berry'),
    (NULL, 'Baie Siam', 'berry'),
    (NULL, 'Baie Mangou', 'berry'),
    (NULL, 'Baie Rabuta', 'berry'),
    (NULL, 'Baie Tronci', 'berry'),
    (NULL, 'Baie Kiwan', 'berry'),
    (NULL, 'Baie Charti', 'berry'),
    (NULL, 'Baie Micle', 'berry'),
    (NULL, 'Super Bonbon', 'other'),
    (NULL, 'Gelée Rouge', 'other'),
    (NULL, 'Pokébloc Violet', 'other'),
    (NULL, 'Pomme d''Or', 'other'),
    (NULL, 'Miel', 'other'),
    (NULL, 'CM', 'other'),
    (NULL, 'GM', 'other'),
    (NULL, 'PV Plus', 'other'),
    (NULL, 'Carbone', 'other'),
    (NULL, 'Protéine', 'other'),
    (NULL, 'Calcium', 'other'),
    (NULL, 'Fer', 'other'),
    (NULL, 'Zinc', 'other'),
    (NULL, 'Appât fade', 'other'),
    (NULL, 'Appât rustique', 'other'),
    (NULL, 'Appât sophistiqué', 'other'),
    (NULL, 'Appât 5 étoiles', 'other'),
    (NULL, 'Pokéflûte', 'rare'),
    (NULL, 'Pokéflûte bleue', 'rare'),
    (NULL, 'Pokéflûte rouge', 'rare'),
    (NULL, 'Pokéflûte noire', 'rare'),
    (NULL, 'Pokéflûte violette', 'rare'),
    (NULL, 'Canne', 'rare'),
    (NULL, 'Super-canne', 'rare'),
    (NULL, 'Méga-canne', 'rare'),
    (NULL, 'CS Anti-brûme', 'rare'),
    (NULL, 'CS Vol', 'rare'),
    (NULL, 'CS Éclate-Roc', 'rare'),
    (NULL, 'CS Force', 'rare'),
    (NULL, 'CS Coupe', 'rare'),
    (NULL, 'CS Cascade', 'rare'),
    (NULL, 'CS Surf', 'rare'),
    (NULL, 'Pass Almia', 'rare'),
    (NULL, 'Sérum M', 'rare'),
    (NULL, 'Sérum S', 'rare');


DROP TABLE IF EXISTS inventory;
CREATE TABLE inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    character_id INTEGER UNSIGNED NOT NULL,
    object_id INTEGER UNSIGNED NOT NULL,
    quantity INTEGER UNSIGNED NOT NULL DEFAULT 0,
    FOREIGN KEY(object_id) REFERENCES object(id),
    FOREIGN KEY(character_id) REFERENCES mp_character(id)
);

DROP TABLE IF EXISTS money;
CREATE TABLE money (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    character_id INTEGER UNSIGNED NOT NULL,
    amount INTEGER UNSIGNED NOT NULL,
    statement_date TEXT NOT NULL,
    FOREIGN KEY(character_id) REFERENCES mp_character(id)
);

DROP TABLE IF EXISTS ct;
CREATE TABLE ct (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    character_id INTEGER UNSIGNED NOT NULL,
    object_id INTEGER UNSIGNED NOT NULL,
    name VARCHAR(50) NOT NULL,
    quantity INTEGER UNSIGNED NOT NULL,
    reserved VARCHAR(255) NULL,
    FOREIGN KEY(character_id) REFERENCES mp_character(id),
    FOREIGN KEY(object_id) REFERENCES object(id)
);

DROP TABLE IF EXISTS cs_history;
CREATE TABLE cs_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    character_id INTEGER UNSIGNED NOT NULL,
    object_id INTEGER UNSIGNED NOT NULL,
    last_used VARCHAR(10) NULL,
    link VARCHAR(255) NULL,
    frequency VARCHAR(15) NOT NULL,
    FOREIGN KEY(character_id) REFERENCES mp_character(id),
    FOREIGN KEY(object_id) REFERENCES object(id)
);

DROP TABLE IF EXISTS flute_history;
CREATE TABLE flute_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    character_id INTEGER UNSIGNED NOT NULL,
    object_id INTEGER UNSIGNED NOT NULL,
    last_used VARCHAR(10) NULL,
    link VARCHAR(255) NULL,
    frequency VARCHAR(15) NOT NULL,
    FOREIGN KEY(character_id) REFERENCES mp_character(id),
    FOREIGN KEY(object_id) REFERENCES object(id)
);

DROP TABLE IF EXISTS history;
CREATE TABLE history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    character_id INTEGER UNSIGNED NOT NULL,
    movement VARCHAR(10) NOT NULL,
    movement_date VARCHAR(10) NOT NULL,
    objects VARCHAR(255) NULL,
    objects_in_exchange VARCHAR(255) NULL,
    objects_out_exchange VARCHAR(255) NULL,
    link VARCHAR(255) NOT NULL,
    link_title VARCHAR(100) NOT NULL,
    FOREIGN KEY(character_id) REFERENCES mp_character(id)
);

DROP TABLE IF EXISTS justificatif_link;
CREATE TABLE justificatif_link (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    character_id INTEGER UNSIGNED NOT NULL,
    object_id INTEGER UNSIGNED NOT NULL,
    link VARCHAR(255) NOT NULL,
    link_title VARCHAR(100) NOT NULL,
    FOREIGN KEY(character_id) REFERENCES mp_character(id),
    FOREIGN KEY(object_id) REFERENCES object(id)
);

DROP TABLE IF EXISTS social;
CREATE TABLE social (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    character_id INTEGER UNSIGNED NOT NULL,
    full_name VARCHAR(50) NOT NULL,
    bond VARCHAR(50) NOT NULL,
    description TEXT NOT NULL,
    pj TINYINT UNSIGNED NOT NULL,
    hexa_text VARCHAR(25) NULL,
    FOREIGN KEY(character_id) REFERENCES mp_character(id)
);

DROP TABLE IF EXISTS social_subject;
CREATE TABLE social_subject (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    social_id INTEGER UNSIGNED NOT NULL,
    link VARCHAR(255) NOT NULL,
    FOREIGN KEY(social_id) REFERENCES social(id)
);

DROP TABLE IF EXISTS social_pokemon;
CREATE TABLE social_pokemon (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    social_id INTEGER UNSIGNED NOT NULL,
    pokemon VARCHAR(25) NOT NULL,
    pokemon_name VARCHAR(25) NOT NULL,
    FOREIGN KEY(social_id) REFERENCES social(id)
);

DROP TABLE IF EXISTS journey_chapter;
CREATE TABLE journey_chapter (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    character_id INTEGER UNSIGNED NOT NULL,
    name VARCHAR(25) NOT NULL,
    after INTEGER UNSIGNED NOT NULL,
    FOREIGN KEY(character_id) REFERENCES mp_character(id)
);

DROP TABLE IF EXISTS journey;
CREATE TABLE journey (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    journey_chapter_id INTEGER UNSIGNED NOT NULL,
    name VARCHAR(100) NOT NULL,
    link VARCHAR(255) NULL,
    after INTEGER UNSIGNED NOT NULL,
    status VARCHAR(20) NOT NULL,
    feat VARCHAR(100) NOT NULL,
    FOREIGN KEY(journey_chapter_id) REFERENCES journey_chapter(id)
);

DROP TABLE IF EXISTS goals;
CREATE TABLE goals (
     id INTEGER PRIMARY KEY AUTOINCREMENT,
     character_id INTEGER UNSIGNED NOT NULL,
     description VARCHAR(100) NOT NULL,
     category INTEGER UNSIGNED NOT NULL,
     done BOOLEAN NOT NULL DEFAULT false,
     FOREIGN KEY(character_id) REFERENCES mp_character(id)
);

DROP TABLE IF EXISTS pokemon_species;
CREATE TABLE pokemon_species (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    species VARCHAR(50) NOT NULL UNIQUE,
    type_1_id INTEGER UNSIGNED NOT NULL,
    type_2_id INTEGER UNSIGNED NULL,
    evolution_id INTEGER UNSIGNED NULL,
    evolution_way INTEGER UNSIGNED NULL,
    evolution_level INTEGER UNSIGNED NULL,
    pv INTEGER UNSIGNED NOT NULL,
    atk INTEGER UNSIGNED NOT NULL,
    atk_special INTEGER UNSIGNED NOT NULL,
    defense INTEGER UNSIGNED NOT NULL,
    defense_special INTEGER UNSIGNED NOT NULL,
    speed INTEGER UNSIGNED NOT NULL
);

DROP TABLE IF EXISTS pokemon_attacks;
CREATE TABLE pokemon_attacks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL,
    type_id INTEGER UNSIGNED NOT NULL,
    informations VARCHAR(255) NULL,
    power INTEGER UNSIGNED NULL,
    precision INTEGER UNSIGNED NULL,
    useless BOOLEAN NOT NULL DEFAULT false,
    burn_percentage INTEGER UNSIGNED NULL,
    freeze_percentage INTEGER UNSIGNED NULL,
    paralyse_percentage INTEGER UNSIGNED NULL,
    scare_percentage INTEGER UNSIGNED NULL,
    poison_percentage INTEGER UNSIGNED NULL,
    sleep_percentage INTEGER UNSIGNED NULL,
    boost VARCHAR(250) NULL,
    critique_attack BOOLEAN NOT NULL DEFAULT false
);

DROP TABLE IF EXISTS pokemon_species_attacks;
CREATE TABLE pokemon_species_attacks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    species_id INTEGER UNSIGNED NOT NULL,
    attack_id INTEGER UNSIGNED NOT NULL,
    level INTEGER UNSIGNED NULL,
    ct BOOLEAN NOT NULL DEFAULT false,
    cs BOOLEAN NOT NULL DEFAULT false,
    gm BOOLEAN NOT NULL DEFAULT false,
    cm BOOLEAN NOT NULL DEFAULT false,
    FOREIGN KEY(species_id) REFERENCES pokemon_species(id),
    FOREIGN KEY(attack_id) REFERENCES pokemon_attacks(id)
);

DROP TABLE IF EXISTS pokemon_category;
CREATE TABLE pokemon_category (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    character_id INTEGER UNSIGNED NOT NULL,
    name VARCHAR(50) NOT NULL
);

INSERT INTO pokemon_category (character_id, name) VALUES (0, 'Stockage');

DROP TABLE IF EXISTS pokemon_owned;
CREATE TABLE pokemon_owned (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    character_id INTEGER UNSIGNED NOT NULL,
    name VARCHAR(100) NOT NULL,
    species_id INTEGER UNSIGNED NOT NULL,
    sex VARCHAR(1) NOT NULL,
    level INTEGER UNSIGNED NOT NULL,
    shiny BOOLEAN NOT NULL DEFAULT false,
    pv INTEGER UNSIGNED NOT NULL DEFAULT 0,
    atk INTEGER UNSIGNED NOT NULL DEFAULT 0,
    atk_special INTEGER UNSIGNED NOT NULL DEFAULT 0,
    defense INTEGER UNSIGNED NOT NULL DEFAULT 0,
    def_special INTEGER UNSIGNED NOT NULL DEFAULT 0,
    speed INTEGER UNSIGNED NOT NULL DEFAULT 0,
    exp_point INTEGER UNSIGNED NOT NULL DEFAULT 0,
    exp_point_per_level INTEGER UNSIGNED NOT NULL DEFAULT 1,
    hp_up INTEGER UNSIGNED NOT NULL DEFAULT 0,
    zinc INTEGER UNSIGNED NOT NULL DEFAULT 0,
    calcium INTEGER UNSIGNED NOT NULL DEFAULT 0,
    carbos INTEGER UNSIGNED NOT NULL DEFAULT 0,
    iron INTEGER UNSIGNED NOT NULL DEFAULT 0,
    protein INTEGER UNSIGNED NOT NULL DEFAULT 0,
    obtention_link VARCHAR(255) NOT NULL,
    obtention_name VARCHAR(255) NOT NULL,
    nature VARCHAR(20) NOT NULL,
    sprite_credits VARCHAR(255) NULL,
    category_id INTEGER UNSIGNED NOT NULL,
    pension VARCHAR(30) NULL,
    egg BOOLEAN NOT NULL DEFAULT false,
    background VARCHAR(100) NOT NULL,
    banner_credit VARCHAR(100) NULL,
    FOREIGN KEY(species_id) REFERENCES pokemon_species(id),
    FOREIGN KEY(character_id) REFERENCES mp_character(id),
    FOREIGN KEY(category_id) REFERENCES pokemon_category(id)
);

DROP TABLE IF EXISTS pokemon_owned_attacks;
CREATE TABLE pokemon_owned_attacks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pokemon_owned_id INTEGER UNSIGNED NOT NULL,
    species_attack_id INTEGER UNSIGNED NOT NULL,
    FOREIGN KEY(pokemon_owned_id) REFERENCES pokemon_owned(id),
    FOREIGN KEY(species_attack_id) REFERENCES pokemon_species_attacks(id)
);

DROP TABLE IF EXISTS ndm_months;
CREATE TABLE ndm_months (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    month VARCHAR NOT NULL,
    year INTEGER UNSIGNED NOT NULL
);

DROP TABLE IF EXISTS ndm_subjects;
CREATE TABLE ndm_subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    character_id INTEGER UNSIGNED NOT NULL,
    name VARCHAR(255) NOT NULL,
    url VARCHAR(255) NOT NULL,
    info VARCHAR(255) NOT NULL,
    closed BOOLEAN NOT NULL DEFAULT false,
    FOREIGN KEY(character_id) REFERENCES mp_character(id)
);

DROP TABLE IF EXISTS ndm_posts;
CREATE TABLE ndm_posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    character_id INTEGER UNSIGNED NOT NULL,
    month_id INTEGER UNSIGNED NOT NULL,
    subject_id INTEGER UNSIGNED NOT NULL,
    words INTEGER UNSIGNED NOT NULL,
    FOREIGN KEY(character_id) REFERENCES mp_character(id),
    FOREIGN KEY(month_id) REFERENCES ndm_months(id),
    FOREIGN KEY(subject_id) REFERENCES ndm_subjects(id)
);

DROP TABLE IF EXISTS ndm_rewards;
CREATE TABLE ndm_rewards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    character_id INTEGER UNSIGNED NOT NULL,
    month_id INTEGER UNSIGNED NOT NULL,
    level_winned INTEGER UNSIGNED NOT NULL,
    level_winned_justif VARCHAR(255) NOT NULL,
    distribution VARCHAR(255) NULL,
    FOREIGN KEY(character_id) REFERENCES mp_character(id),
    FOREIGN KEY(month_id) REFERENCES ndm_months(id)
);

DROP TABLE IF EXISTS cookies_months;
CREATE TABLE cookies_months (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    character_id INTEGER UNSIGNED NOT NULL,
    month VARCHAR(5) NOT NULL,
    win_cookies INTEGER UNSIGNED NOT NULL,
    FOREIGN KEY(character_id) REFERENCES mp_character(id)
);

DROP TABLE IF EXISTS cookies_used;
CREATE TABLE cookies_used (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cookies_months_id INTEGER UNSIGNED NOT NULL,
    pokemon_id INTEGER NULL,
    before_lvl VARCHAR(15) NULL,
    after_lvl VARCHAR(15) NULL,
    FOREIGN KEY(cookies_months_id) REFERENCES cookies_months(id),
    FOREIGN KEY(pokemon_id) REFERENCES pokemon_owned(id)
);

-- DROP TABLE IF EXISTS dex;
-- CREATE TABLE dex (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     character_id INTEGER UNSIGNED NOT NULL,
--     name VARCHAR(25) NOT NULL,
--     start_date VARCHAR(10) NOT NULL,
--     end_date VARCHAR(10) NOT NULL,
--     FOREIGN KEY(character_id) REFERENCES mp_character(id)
-- );
--
-- DROP TABLE IF EXISTS dex_experience;
-- CREATE TABLE dex_experience (
--     id INTEGER PRIMARY KEY AUTOINCREMENT,
--     dex_id INTEGER UNSIGNED NOT NULL,
--     month VARCHAR(10) NOT NULL,
--     pokemon_id INTEGER UNSIGNED NOT NULL,
--     base_lvl INTEGER UNSIGNED NOT NULL,
--     end_lvl INTEGER UNSIGNED NOT NULL,
--     give BOOLEAN NOT NULL DEFAULT false,
--     FOREIGN KEY(dex_id) REFERENCES dex(id),
--     FOREIGN KEY(pokemon_id) REFERENCES pokemon(id)
-- );
