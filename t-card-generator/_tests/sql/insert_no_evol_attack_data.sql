INSERT INTO pokemon_species VALUES
    (1, 'BASE', 1, 0, 2, 1, 10, 1, 1, 1, 1, 1, 1),
    (2, 'STADE 1', 1, 0, 3, 1, 20, 1, 1, 1, 1, 1, 1),
    (3, 'STADE 2', 1, 0, 0, null, null, 1, 1, 1, 1, 1, 1),
    (4, 'NO EVOL', 1, 0, 0, null, null, 1, 1, 1, 1, 1, 1);

INSERT INTO pokemon_owned VALUES
    (1, 1, 'POKEMON BASE', 1, 'M', 8, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 'http://127.0.0.1:5000/pokemon/1/456', 456, 456, null, 20, null, 0, 'a', null),
    (2, 1, 'POKEMON STADE 1', 2, 'M', 11, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 'http://127.0.0.1:5000/pokemon/1/456', 456, 456, null, 20, null, 0, 'a', null),
    (3, 1, 'POKEMON STADE 2', 3, 'M', 60, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 'http://127.0.0.1:5000/pokemon/1/456', 456, 456, null, 20, null, 0, 'a', null),
    (4, 1, 'POKEMON NO EVOL', 4, 'M', 5, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 'http://127.0.0.1:5000/pokemon/1/456', 456, 456, null, 20, null, 0, 'a', null);

INSERT INTO pokemon_attacks VALUES
    (1, 'ATTAQUE 1', 1, null, null, null, null, null, null, null, null, null, null, null, false),
    (2, 'ATTAQUE 2', 1, null, null, null, null, null, null, null, null, null, null, null, false),
    (3, 'ATTAQUE 3', 1, null, null, null, null, null, null, null, null, null, null, null, false),
    (4, 'ATTAQUE 4', 1, null, null, null, null, null, null, null, null, null, null, null, false),
    (5, 'ATTAQUE 5', 1, null, null, null, null, null, null, null, null, null, null, null, false),
    (6, 'ATTAQUE 6', 1, null, null, null, null, null, null, null, null, null, null, null, false),
    (7, 'ATTAQUE 7', 1, null, null, null, null, null, null, null, null, null, null, null, false),
    (8, 'ATTAQUE 8', 1, null, null, null, null, null, null, null, null, null, null, null, false),
    (9, 'ATTAQUE 9', 1, null, null, null, null, null, null, null, null, null, null, null, false),
    (10, 'ATTAQUE 10', 1, null, null, null, null, null, null, null, null, null, null, null, false);


INSERT INTO pokemon_species_attacks VALUES
    (1, 1, 1, 7, false, false, false, false),
    (2, 1, 2, 15, false, false, false, false),
    (3, 2, 2, 30, false, false, false, false),
    (4, 3, 3, 45, false, false, false, false),
    (5, 1, 4, 30, false, false, false, false),
    (6, 1, 5, null, true, false, false, false),
    (7, 1, 6, null, false, true, false, false),
    (8, 1, 7, null, false, false, true, false),
    (9, 1, 8, null, false, false, false, true),
    (10, 2, 9, 20, false, false, false, false),
    (11, 4, 9, 30, false, false, false, false),
    (12, 2, 10, 15, false, false, false, false),
    (13, 3, 10, 20, false, false, false, false);
