INSERT INTO pokemon_species VALUES
    (1, 'BASE', 1, 0, 2, 1, 10, 1, 1, 1, 1, 1, 1),
    (2, 'STADE 1', 1, 0, 0, 1, 20, 1, 1, 1, 1, 1, 1);

INSERT INTO pokemon_owned VALUES
    (1, 1, 'POKEMON BASE', 1, 'M', 15, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 'http://127.0.0.1:5000/pokemon/1/456', 456, 456, null, 20, 'Toto', 0, 'a', null),
    (2, 1, 'POKEMON STADE 1', 2, 'M', 11, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 'http://127.0.0.1:5000/pokemon/1/456', 456, 456, null, 20, null, 0, 'a', null);

INSERT INTO pokemon_attacks VALUES
    (1, 'ATTAQUE 1', 1, null, null, null, null, null, null, null, null, null, null, null, false),
    (2, 'ATTAQUE 2', 1, null, null, null, null, null, null, null, null, null, null, null, false),
    (3, 'ATTAQUE 3', 1, null, null, null, null, null, null, null, null, null, null, null, false),
    (4, 'ATTAQUE 4', 1, null, null, null, null, null, null, null, null, null, null, null, false),
    (5, 'ATTAQUE 5', 1, null, null, null, null, null, null, null, null, null, null, null, false),
    (6, 'ATTAQUE 6', 1, null, null, null, null, null, null, null, null, null, null, null, false);

INSERT INTO pokemon_species_attacks VALUES
    (1, 1, 1, 15, false, false, false, false),
    (2, 1, 2, 7, false, false, false, false),
    (3, 1, 6, 50, false, false, false, false),
    (4, 1, 4, 19, false, false, false, false),
    (5, 1, 5, 21, false, false, false, false),
    (6, 1, 4, null, true, false, false, false),
    (7, 2, 3, 35, false, false, false, false),
    (8, 2, 4, 20, true, false, false, false),
    (9, 2, 5, null, false, true, false, false),
    (10, 2, 6, 40, false, false, false, false);
