use ApDB;
insert into boeken values ('De geschiedenis van Rock 'n Roll', 'De Hasque', 2011');
drop table if exists Liedjes;
CREATE TABLE Liedjes(Titel VARCHAR(100), Duurtijd tinyint UNSIGNED);
-- het liedje duurt vijf minuten
insert into liedjes values ('Ain't talkin' 'bout Love', 5 * 60);
