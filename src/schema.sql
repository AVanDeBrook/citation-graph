-- uncomment this line if you want to refresh your database on next run
-- DROP TABLE IF EXISTS paper;
CREATE TABLE IF NOT EXISTS paper (
  `paper_id` VARCHAR(255) PRIMARY KEY NOT NULL,
  `title` VARCHAR(512),
  `author` VARCHAR(255),
  `year` VARCHAR(255),
  `abstract` VARCHAR(255),
  `bib_references` VARCHAR(255)
);

-- uncomment this line if you want to refresh your database on next run
-- DROP TABLE IF EXISTS citation ;
-- CREATE TABLE IF NOT EXISTS citation (
--   `sequence_id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
--   `paper_id` VARCHAR(255) NOT NULL,
--   `reference_paper_id` VARCHAR(255) NOT NULL
-- );
