SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL';

DROP SCHEMA IF EXISTS `scheduler` ;
CREATE SCHEMA IF NOT EXISTS `scheduler` DEFAULT CHARACTER SET utf8 ;
USE `scheduler` ;

-- -----------------------------------------------------
-- Table `scheduler`.`curriculum`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `scheduler`.`curriculum` ;

CREATE  TABLE IF NOT EXISTS `scheduler`.`curriculum` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `Name` VARCHAR(128) NOT NULL ,
  `Abbreviation` VARCHAR(8) NOT NULL ,
  `FirstYear` INT NOT NULL ,
  `LastYear` INT NOT NULL ,
  `Url` VARCHAR(128) NULL ,
  PRIMARY KEY (`id`) ,
  INDEX `DeptAbbr` (`Abbreviation` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `scheduler`.`course`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `scheduler`.`course` ;

CREATE  TABLE IF NOT EXISTS `scheduler`.`course` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `Number` INT NOT NULL ,
  `Name` VARCHAR(128) NULL ,
  `Comment` VARCHAR(256) NULL ,
  `Description` VARCHAR(2048) NULL ,
  `idCurriculum` INT NOT NULL ,
  `GenEdReqs` INT NULL ,
  `FirstYear` INT NULL ,
  `FirstQuarter` CHAR(2) NULL ,
  `LastYear` INT NULL ,
  `LastQuarter` CHAR(2) NULL ,
  `MinCredits` INT NULL ,
  `MaxCredits` INT NULL ,
  PRIMARY KEY (`id`) ,
  INDEX `fk_Courses_Departments1` (`idCurriculum` ASC) ,
  INDEX `CourseNumber` (`Number` ASC) ,
  INDEX `CourseName` (`Name` ASC) ,
  INDEX `GenEdReqs` (`GenEdReqs` ASC) ,
  CONSTRAINT `fk_Courses_Departments1`
    FOREIGN KEY (`idCurriculum` )
    REFERENCES `scheduler`.`curriculum` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `scheduler`.`instructor`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `scheduler`.`instructor` ;

CREATE  TABLE IF NOT EXISTS `scheduler`.`instructor` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `Name` VARCHAR(64) NOT NULL ,
  PRIMARY KEY (`id`) ,
  INDEX `InstructorName` (`Name` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `scheduler`.`rating`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `scheduler`.`rating` ;

CREATE  TABLE IF NOT EXISTS `scheduler`.`rating` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `CourseWhole` DECIMAL(8,4) NULL ,
  `CourseContent` DECIMAL(8,4) NULL ,
  `InstructorContribution` DECIMAL(8,4) NULL ,
  `InstructorInterest` DECIMAL(8,4) NULL ,
  `InstructorEffectiveness` DECIMAL(8,4) NULL ,
  `AmountLearned` DECIMAL(8,4) NULL ,
  `Grading` DECIMAL(8,4) NULL ,
  `NumSurveyed` INT NOT NULL ,
  `NumEnrolled` INT NOT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `scheduler`.`section`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `scheduler`.`section` ;

CREATE  TABLE IF NOT EXISTS `scheduler`.`section` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `Quarter` CHAR(2) NOT NULL ,
  `Section` VARCHAR(4) NULL ,
  `idInstructor` INT NULL ,
  `idCourse` INT NOT NULL ,
  `idRating` INT NULL ,
  `InstructorTitle` VARCHAR(64) NULL ,
  `Year` INT NOT NULL ,
  `NumEnrolled` INT NULL ,
  `MaxEnrollment` INT NULL ,
  `ClassWebsite` VARCHAR(128) NULL ,
  `SLN` INT NULL ,
  PRIMARY KEY (`id`) ,
  INDEX `fk_Instances_Instructor` (`idInstructor` ASC) ,
  INDEX `fk_Instances_Courses1` (`idCourse` ASC) ,
  INDEX `fk_Instances_Ratings1` (`idRating` ASC) ,
  INDEX `SectionQuarter` (`Quarter` ASC) ,
  INDEX `SectionInstTitle` (`InstructorTitle` ASC) ,
  INDEX `SectionYear` (`Year` ASC) ,
  CONSTRAINT `fk_Instances_Instructor`
    FOREIGN KEY (`idInstructor` )
    REFERENCES `scheduler`.`instructor` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Instances_Courses1`
    FOREIGN KEY (`idCourse` )
    REFERENCES `scheduler`.`course` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Instances_Ratings1`
    FOREIGN KEY (`idRating` )
    REFERENCES `scheduler`.`rating` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `scheduler`.`building`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `scheduler`.`building` ;

CREATE  TABLE IF NOT EXISTS `scheduler`.`building` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `Abbreviation` VARCHAR(12) NOT NULL ,
  `Name` VARCHAR(128) NULL ,
  `Latitude` DECIMAL(16,8) NULL ,
  `Longitude` DECIMAL(16,8) NULL ,
  PRIMARY KEY (`id`) ,
  INDEX `abbrev` (`Abbreviation` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `scheduler`.`room`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `scheduler`.`room` ;

CREATE  TABLE IF NOT EXISTS `scheduler`.`room` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `Name` VARCHAR(45) NOT NULL ,
  `idBuilding` INT NOT NULL ,
  PRIMARY KEY (`id`) ,
  INDEX `fk_Room_Building1` (`idBuilding` ASC) ,
  INDEX `Index_Room_Name` (`Name` ASC) ,
  CONSTRAINT `fk_Room_Building1`
    FOREIGN KEY (`idBuilding` )
    REFERENCES `scheduler`.`building` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `scheduler`.`meetingtype`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `scheduler`.`meetingtype` ;

CREATE  TABLE IF NOT EXISTS `scheduler`.`meetingtype` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `Name` VARCHAR(64) NOT NULL ,
  PRIMARY KEY (`id`) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `scheduler`.`meeting`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `scheduler`.`meeting` ;

CREATE  TABLE IF NOT EXISTS `scheduler`.`meeting` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `Day` INT NULL ,
  `StartTime` INT NULL ,
  `EndTime` INT NULL ,
  `idSection` INT NOT NULL ,
  `idRoom` INT NULL ,
  `idMeetingType` INT NOT NULL ,
  PRIMARY KEY (`id`) ,
  INDEX `fk_Meetings_Instances1` (`idSection` ASC) ,
  INDEX `fk_Meeting_Room1` (`idRoom` ASC) ,
  INDEX `fk_Meeting_MeetingType1` (`idMeetingType` ASC) ,
  CONSTRAINT `fk_Meetings_Instances1`
    FOREIGN KEY (`idSection` )
    REFERENCES `scheduler`.`section` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Meeting_Room1`
    FOREIGN KEY (`idRoom` )
    REFERENCES `scheduler`.`room` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Meeting_MeetingType1`
    FOREIGN KEY (`idMeetingType` )
    REFERENCES `scheduler`.`meetingtype` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `scheduler`.`sectionrelation`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `scheduler`.`sectionrelation` ;

CREATE  TABLE IF NOT EXISTS `scheduler`.`sectionrelation` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `idSection` INT NOT NULL ,
  `idParent` INT NOT NULL ,
  PRIMARY KEY (`id`) ,
  INDEX `fk_SectionRelations_Instances1` (`idSection` ASC) ,
  INDEX `fk_SectionRelations_Instances2` (`idParent` ASC) ,
  CONSTRAINT `fk_SectionRelations_Instances1`
    FOREIGN KEY (`idSection` )
    REFERENCES `scheduler`.`section` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_SectionRelations_Instances2`
    FOREIGN KEY (`idParent` )
    REFERENCES `scheduler`.`section` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;



SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
