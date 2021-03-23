SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema citation_graph
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `citation_graph` ;

-- -----------------------------------------------------
-- Schema citation_graph
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `citation_graph` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `citation_graph` ;

-- -----------------------------------------------------
-- Table `citation_graph`.`CHECKS_PAPER_REFRENCES`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `citation_graph`.`CHECKS_PAPER_REFRENCES` ;

CREATE TABLE IF NOT EXISTS `citation_graph`.`CHECKS_PAPER_REFRENCES` (
  `checkingID` INT NOT NULL,
  `PaperName` VARCHAR(45) NOT NULL,
  `PublisherName` VARCHAR(45) NOT NULL,
  `RefrenceWebsites` VARCHAR(45) NOT NULL,
  `PercentageDependency` DOUBLE NOT NULL,
  `CheckingTotalTime` DATETIME NOT NULL,
  PRIMARY KEY (`checkingID`),
  UNIQUE INDEX `checkingID_UNIQUE` (`checkingID` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `citation_graph`.`CITATION_GRAPH_TOOL`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `citation_graph`.`CITATION_GRAPH_TOOL` ;

CREATE TABLE IF NOT EXISTS `citation_graph`.`CITATION_GRAPH_TOOL` (
  `ToolProductionID` INT NOT NULL,
  `ToolName` VARCHAR(45) NOT NULL,
  `VisualOperations` TINYINT NOT NULL,
  `StorageCapacity` INT NOT NULL,
  `TypesOfGraphs` VARCHAR(45) NOT NULL,
  `TypesOfCitations` INT NOT NULL,
  `MaxUsersLoadAtOneTime` INT NOT NULL,
  PRIMARY KEY (`ToolProductionID`),
  UNIQUE INDEX `ToolProductionID_UNIQUE` (`ToolProductionID` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `citation_graph`.`EDIT_VISUAL_DEPENDENCY`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `citation_graph`.`EDIT_VISUAL_DEPENDENCY` ;

CREATE TABLE IF NOT EXISTS `citation_graph`.`EDIT_VISUAL_DEPENDENCY` (
  `updationID` INT NOT NULL,
  `updateNumber` INT NOT NULL,
  `publisherID` INT NOT NULL,
  `updatedLocation` VARCHAR(45) NOT NULL,
  `updatedFileSize` INT NOT NULL,
  `updationDate` DATE NOT NULL,
  PRIMARY KEY (`updationID`, `updateNumber`, `publisherID`),
  UNIQUE INDEX `updationID_UNIQUE` (`updationID` ASC) VISIBLE,
  UNIQUE INDEX `updateNumber_UNIQUE` (`updateNumber` ASC) VISIBLE,
  UNIQUE INDEX `publisherID_UNIQUE` (`publisherID` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `citation_graph`.`INPUT_PAPER`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `citation_graph`.`INPUT_PAPER` ;

CREATE TABLE IF NOT EXISTS `citation_graph`.`INPUT_PAPER` (
  `paperID` INT NOT NULL,
  `Title` VARCHAR(45) NOT NULL,
  `No_of_publishers` INT NOT NULL,
  `Page_length` INT NOT NULL,
  `ResearchTopic` VARCHAR(45) NOT NULL,
  `NoOfRefrences` INT NOT NULL,
  `SubmissionDate` DATE NOT NULL,
  `NoOfRevisions` INT NOT NULL,
  `FIleFormat` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`paperID`),
  UNIQUE INDEX `paperID_UNIQUE` (`paperID` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `citation_graph`.`OUTPUT_VISUAL_DEPENDENCY`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `citation_graph`.`OUTPUT_VISUAL_DEPENDENCY` ;

CREATE TABLE IF NOT EXISTS `citation_graph`.`OUTPUT_VISUAL_DEPENDENCY` (
  `outputID` INT NOT NULL,
  `paperID` INT NOT NULL,
  `outputTime` DATETIME NOT NULL,
  `qualityIndex` VARCHAR(45) NOT NULL,
  `noOfResearchers` INT NOT NULL,
  `fileFormat` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`outputID`, `paperID`),
  UNIQUE INDEX `outputID_UNIQUE` (`outputID` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `citation_graph`.`SAVE_VISUAL_DEPENDENCY`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `citation_graph`.`SAVE_VISUAL_DEPENDENCY` ;

CREATE TABLE IF NOT EXISTS `citation_graph`.`SAVE_VISUAL_DEPENDENCY` (
  `savingID` INT NOT NULL,
  `sizeOfFile` INT NOT NULL,
  `noOfCopies` INT NOT NULL,
  `totalSizeLeft` INT NOT NULL,
  `savingLocation` VARCHAR(45) NOT NULL,
  `userAccessNo` INT NOT NULL,
  `userContact` INT NOT NULL,
  PRIMARY KEY (`savingID`),
  UNIQUE INDEX `savingID_UNIQUE` (`savingID` ASC) VISIBLE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `citation_graph`.`USER`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `citation_graph`.`USER` ;

CREATE TABLE IF NOT EXISTS `citation_graph`.`USER` (
  `idUSER` INT NOT NULL,
  `User_Name` VARCHAR(45) NOT NULL,
  `User_Age` INT NOT NULL,
  `ResearcherNo` INT NOT NULL,
  `CollegeID` INT NOT NULL,
  `NoOfPublishedPapers` INT NOT NULL,
  `DOB` DATE NOT NULL,
  `Address` VARCHAR(45) NOT NULL,
  `Email` VARCHAR(15) NOT NULL,
  `PhoneNo` INT NOT NULL,
  PRIMARY KEY (`idUSER`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
