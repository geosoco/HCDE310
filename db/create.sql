SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL';

DROP SCHEMA IF EXISTS `scheduler` ;
CREATE SCHEMA IF NOT EXISTS `scheduler` DEFAULT CHARACTER SET utf8 ;
USE `scheduler` ;

-- -----------------------------------------------------
-- Table `scheduler`.`Departments`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `scheduler`.`Departments` ;

CREATE  TABLE IF NOT EXISTS `scheduler`.`Departments` (
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
-- Table `scheduler`.`Courses`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `scheduler`.`Courses` ;

CREATE  TABLE IF NOT EXISTS `scheduler`.`Courses` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `Number` INT NOT NULL ,
  `Name` VARCHAR(128) NULL ,
  `Comment` VARCHAR(256) NULL ,
  `Description` VARCHAR(2048) NULL ,
  `idDepartment` INT NOT NULL ,
  `GenEdReqs` INT NULL ,
  `FirstYear` INT NULL ,
  `FirstQuarter` CHAR(2) NULL ,
  `LastYear` INT NULL ,
  `LastQuarter` CHAR(2) NULL ,
  `MinCredits` INT NULL ,
  `MaxCredits` INT NULL ,
  PRIMARY KEY (`id`) ,
  INDEX `fk_Courses_Departments1` (`idDepartment` ASC) ,
  INDEX `CourseNumber` (`Number` ASC) ,
  INDEX `CourseName` (`Name` ASC) ,
  INDEX `GenEdReqs` (`GenEdReqs` ASC) ,
  CONSTRAINT `fk_Courses_Departments1`
    FOREIGN KEY (`idDepartment` )
    REFERENCES `scheduler`.`Departments` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `scheduler`.`Instructors`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `scheduler`.`Instructors` ;

CREATE  TABLE IF NOT EXISTS `scheduler`.`Instructors` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `Name` VARCHAR(64) NOT NULL ,
  PRIMARY KEY (`id`) ,
  INDEX `InstructorName` (`Name` ASC) )
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `scheduler`.`Ratings`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `scheduler`.`Ratings` ;

CREATE  TABLE IF NOT EXISTS `scheduler`.`Ratings` (
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
-- Table `scheduler`.`Instances`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `scheduler`.`Instances` ;

CREATE  TABLE IF NOT EXISTS `scheduler`.`Instances` (
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
    REFERENCES `scheduler`.`Instructors` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Instances_Courses1`
    FOREIGN KEY (`idCourses` )
    REFERENCES `scheduler`.`Courses` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Instances_Ratings1`
    FOREIGN KEY (`idRatings` )
    REFERENCES `scheduler`.`Ratings` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `scheduler`.`Meetings`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `scheduler`.`Meetings` ;

CREATE  TABLE IF NOT EXISTS `scheduler`.`Meetings` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `Day` INT NULL ,
  `StartTime` INT NULL ,
  `EndTime` INT NULL ,
  `Type` INT NULL ,
  `idInstance` INT NOT NULL ,
  `Building` VARCHAR(8) NULL ,
  PRIMARY KEY (`id`) ,
  INDEX `fk_Meetings_Instances1` (`idInstance` ASC) ,
  CONSTRAINT `fk_Meetings_Instances1`
    FOREIGN KEY (`idInstance` )
    REFERENCES `scheduler`.`Instances` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `scheduler`.`SectionRelations`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `scheduler`.`SectionRelations` ;

CREATE  TABLE IF NOT EXISTS `scheduler`.`SectionRelations` (
  `id` INT NOT NULL AUTO_INCREMENT ,
  `idInstance` INT NOT NULL ,
  `idParent` INT NOT NULL ,
  PRIMARY KEY (`id`) ,
  INDEX `fk_SectionRelations_Instances1` (`idInstance` ASC) ,
  INDEX `fk_SectionRelations_Instances2` (`idParent` ASC) ,
  CONSTRAINT `fk_SectionRelations_Instances1`
    FOREIGN KEY (`idInstance` )
    REFERENCES `scheduler`.`Instances` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_SectionRelations_Instances2`
    FOREIGN KEY (`idParent` )
    REFERENCES `scheduler`.`Instances` (`id` )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;



SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
