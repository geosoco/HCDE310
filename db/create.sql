SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL';

DROP SCHEMA IF EXISTS `scheduler` ;
CREATE SCHEMA IF NOT EXISTS `scheduler` DEFAULT CHARACTER SET utf8 ;
USE `scheduler` ;

-- -----------------------------------------------------
-- Table `scheduler`.`Curriculum`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `scheduler`.`Curriculum` ;

CREATE  TABLE IF NOT EXISTS `scheduler`.`Curriculum` (
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
-- Table `scheduler`.`Course`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `scheduler`.`Course` ;

CREATE  TABLE IF NOT EXISTS `scheduler`.`Course` (
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
    REFERENCES `scheduler`.`Curriculum` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `scheduler`.`Instructor`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `scheduler`.`Instructor` ;

CREATE  TABLE IF NOT EXISTS `scheduler`.`Instructor` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `Name` VARCHAR(64) NOT NULL ,
  PRIMARY KEY (`id`) ,
  INDEX `InstructorName` (`Name` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `scheduler`.`Rating`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `scheduler`.`Rating` ;

CREATE  TABLE IF NOT EXISTS `scheduler`.`Rating` (
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
-- Table `scheduler`.`Section`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `scheduler`.`Section` ;

CREATE  TABLE IF NOT EXISTS `scheduler`.`Section` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `Quarter` CHAR(2) NOT NULL ,
  `Section` VARCHAR(4) NULL ,
  `idInstructor` INT NOT NULL ,
  `idCourses` INT NOT NULL ,
  `idRatings` INT NOT NULL ,
  `InstructorTitle` VARCHAR(64) NOT NULL ,
  `Year` INT NOT NULL ,
  `NumEnrolled` INT NULL ,
  `MaxEnrollment` INT NULL ,
  `ClassWebsite` VARCHAR(128) NULL ,
  `SLN` INT NULL ,
  PRIMARY KEY (`id`) ,
  INDEX `fk_Instances_Instructor` (`idInstructor` ASC) ,
  INDEX `fk_Instances_Courses1` (`idCourses` ASC) ,
  INDEX `fk_Instances_Ratings1` (`idRatings` ASC) ,
  INDEX `InstanceQuarter` (`Quarter` ASC) ,
  INDEX `InstanceInstTitle` (`InstructorTitle` ASC) ,
  CONSTRAINT `fk_Instances_Instructor`
    FOREIGN KEY (`idInstructor` )
    REFERENCES `scheduler`.`Instructor` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Instances_Courses1`
    FOREIGN KEY (`idCourses` )
    REFERENCES `scheduler`.`Course` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Instances_Ratings1`
    FOREIGN KEY (`idRatings` )
    REFERENCES `scheduler`.`Rating` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `scheduler`.`Building`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `scheduler`.`Building` ;

CREATE  TABLE IF NOT EXISTS `scheduler`.`Building` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `Abbreviation` VARCHAR(12) NOT NULL ,
  `Name` VARCHAR(128) NULL ,
  `Latitude` DECIMAL(16,8) NULL ,
  `Longitude` DECIMAL(16,8) NULL ,
  PRIMARY KEY (`id`) ,
  INDEX `abbrev` (`Abbreviation` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `scheduler`.`Meeting`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `scheduler`.`Meeting` ;

CREATE  TABLE IF NOT EXISTS `scheduler`.`Meeting` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `Day` INT NULL ,
  `StartTime` INT NULL ,
  `EndTime` INT NULL ,
  `Type` INT NULL ,
  `idSection` INT NOT NULL ,
  `idBuilding` INT NOT NULL ,
  PRIMARY KEY (`id`) ,
  INDEX `fk_Meetings_Instances1` (`idSection` ASC) ,
  INDEX `fk_Meetings_Building1` (`idBuilding` ASC) ,
  CONSTRAINT `fk_Meetings_Instances1`
    FOREIGN KEY (`idSection` )
    REFERENCES `scheduler`.`Section` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Meetings_Building1`
    FOREIGN KEY (`idBuilding` )
    REFERENCES `scheduler`.`Building` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `scheduler`.`SectionRelation`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `scheduler`.`SectionRelation` ;

CREATE  TABLE IF NOT EXISTS `scheduler`.`SectionRelation` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `idSection` INT NOT NULL ,
  `idParent` INT NOT NULL ,
  PRIMARY KEY (`id`) ,
  INDEX `fk_SectionRelations_Instances1` (`idSection` ASC) ,
  INDEX `fk_SectionRelations_Instances2` (`idParent` ASC) ,
  CONSTRAINT `fk_SectionRelations_Instances1`
    FOREIGN KEY (`idSection` )
    REFERENCES `scheduler`.`Section` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_SectionRelations_Instances2`
    FOREIGN KEY (`idParent` )
    REFERENCES `scheduler`.`Section` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;



SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
