SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";

CREATE TABLE Nicknames (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  nick VARCHAR(255) UNIQUE NOT NULL,
  PRIMARY KEY(id)
)
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Users (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR(50) UNIQUE NOT NULL,
  email VARCHAR(150) UNIQUE NULL,
  user_password VARCHAR(150) NOT NULL,
  trust_level SMALLINT UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY(id)
)
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Authors (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  first_name VARCHAR(50) NOT NULL,
  middle_name VARCHAR(50) NULL,
  last_name VARCHAR(50) NOT NULL,
  PRIMARY KEY(id)
)
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE Quotes (
  id INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
  author_id INTEGER UNSIGNED,
  content TEXT NOT NULL,
  date DATETIME NOT NULL,
  context TEXT NULL,
  PRIMARY KEY(id),
  INDEX Quotes_FKIndex1(author_id),
  FOREIGN KEY(author_id)
    REFERENCES Authors(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
)
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE LikedQuotes (
  Quotes_id INTEGER UNSIGNED NOT NULL,
  Users_id INTEGER UNSIGNED NOT NULL,
  PRIMARY KEY(Quotes_id, Users_id),
  INDEX Quotes_has_Users_FKIndex1(Quotes_id),
  INDEX Quotes_has_Users_FKIndex2(Users_id),
  FOREIGN KEY(Quotes_id)
    REFERENCES Quotes(id)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION,
  FOREIGN KEY(Users_id)
    REFERENCES Users(id)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION
)
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE AuthorsNicknames (
  Authors_id INTEGER UNSIGNED NOT NULL,
  Nicknames_id INTEGER UNSIGNED NOT NULL,
  PRIMARY KEY(Authors_id, Nicknames_id),
  INDEX Authors_has_Nicknames_FKIndex1(Authors_id),
  INDEX Authors_has_Nicknames_FKIndex2(Nicknames_id),
  FOREIGN KEY(Authors_id)
    REFERENCES Authors(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(Nicknames_id)
    REFERENCES Nicknames(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
)
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE UserNicknamesPreferences (
  user_id INTEGER UNSIGNED NULL,
  author_id INTEGER UNSIGNED NULL,
  nickname_id INTEGER UNSIGNED NULL,
  INDEX UserNicknamesPreferences_FKIndex1(nickname_id),
  INDEX UserNicknamesPreferences_FKIndex2(author_id),
  INDEX UserNicknamesPreferences_FKIndex3(user_id),
  FOREIGN KEY(nickname_id)
    REFERENCES Nicknames(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(author_id)
    REFERENCES Authors(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE,
  FOREIGN KEY(user_id)
    REFERENCES Users(id)
      ON DELETE CASCADE
      ON UPDATE CASCADE
)
ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


