-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema plant_quiz
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `plant_quiz` ;

-- -----------------------------------------------------
-- Schema plant_quiz
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `plant_quiz` DEFAULT CHARACTER SET utf8 ;
USE `plant_quiz` ;

-- -----------------------------------------------------
-- Table `plant_quiz`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `plant_quiz`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NULL,
  `last_name` VARCHAR(45) NULL,
  `email` VARCHAR(45) NULL,
  `password` VARCHAR(300) NULL,
  `bio` VARCHAR(200) NULL,
  `general_score` INT(10) NULL,
  `pnw_score` INT(10) NULL,
  `herb_score` INT(10) NULL,
  `flower_score` INT(10) NULL,
  `date` DATE NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `plant_quiz`.`plants`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `plant_quiz`.`plants` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `common_name` VARCHAR(100) NULL,
  `latin_name` VARCHAR(100) NULL,
  `pic_A` BLOB NULL,
  `pic_B` BLOB NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `plant_quiz`.`posts`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `plant_quiz`.`posts` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(45) NULL,
  `content` VARCHAR(1000) NULL,
  `date` DATE NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_posts_users1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_posts_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `plant_quiz`.`users` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `plant_quiz`.`comments`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `plant_quiz`.`comments` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `content` VARCHAR(255) NULL,
  `date` DATE NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  `user_id` INT NOT NULL,
  `post_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_comments_users_idx` (`user_id` ASC) VISIBLE,
  INDEX `fk_comments_posts1_idx` (`post_id` ASC) VISIBLE,
  CONSTRAINT `fk_comments_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `plant_quiz`.`users` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_comments_posts1`
    FOREIGN KEY (`post_id`)
    REFERENCES `plant_quiz`.`posts` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `plant_quiz`.`likes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `plant_quiz`.`likes` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `like` INT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  `user_id` INT NOT NULL,
  `post_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_likes_users1_idx` (`user_id` ASC) VISIBLE,
  INDEX `fk_likes_posts1_idx` (`post_id` ASC) VISIBLE,
  CONSTRAINT `fk_likes_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `plant_quiz`.`users` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_likes_posts1`
    FOREIGN KEY (`post_id`)
    REFERENCES `plant_quiz`.`posts` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
