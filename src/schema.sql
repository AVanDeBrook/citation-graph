-- uncomment this line if you want to refresh your database on next run
DROP TABLE IF EXISTS paper;
CREATE TABLE IF NOT EXISTS paper (
  `sequence_id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  `paper_id` VARCHAR(255) NOT NULL,
  `has_bib` BOOLEAN NOT NULL DEFAULT 0,
  `has_tex` BOOLEAN NOT NULL DEFAULT 0,
  `title_bib` VARCHAR(255),
  `title_tex` VARCHAR(255),
  `author_bib` VARCHAR(255),
  `author_tex` VARCHAR(255),
  `year` INTEGER,
  `month` VARCHAR(255),
  `volume` VARCHAR(255),
  `number` VARCHAR(255),
  `pages` VARCHAR(255),
  `publisher` VARCHAR(255),
  `journal` VARCHAR(255),
  `last_accessed` VARCHAR(255),
  `address` VARCHAR(255),
  `abstract` VARCHAR(255),
  `index_terms` VARCHAR(255),
  `bib` VARCHAR(255)
);

-- uncomment this line if you want to refresh your database on next run
-- DROP TABLE IF EXISTS citation ;
CREATE TABLE IF NOT EXISTS citation (
  `sequence_id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
  `paper_id` VARCHAR(255) NOT NULL,
  `reference_paper_id` VARCHAR(255) NOT NULL
);