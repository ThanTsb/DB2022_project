CREATE DATABASE elidek;
USE elidek;

-- DB2022.organisation definition

CREATE TABLE `organisations` (
  `o_id` int unsigned auto_increment,
  `org_name` varchar(100)  UNIQUE NOT NULL,
  `acronym` varchar(20) NOT NULL,
  `postal_code` varchar(10) NOT NULL,
  `city` varchar(45) NOT NULL,
  `street` varchar(45) NOT NULL,
  `org_type` varchar(45) NOT NULL CHECK (org_type = 'University' OR org_type = 'Company' OR org_type = 'Scientific Center'),
  `minedu_funding` int(11) DEFAULT NULL, 
  `priv_funding` int(11) DEFAULT NULL,
  CHECK ((org_type = 'University' AND priv_funding IS NULL) OR (org_type <> 'University')),
  CHECK ((org_type = 'Company' AND minedu_funding IS NULL) OR (org_type <> 'Company')),
  PRIMARY KEY (`o_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- DB2022.projects definition

CREATE TABLE `projects` (
  `p_id` int unsigned auto_increment,
  `Title` varchar(250) NOT NULL,
  `Summary` text NOT NULL,
  `Start_date` date NOT NULL ,
  `End_date` date NOT NULL ,
  `Amount` int(11) NOT NULL CHECK(`Amount` >= 100000 and `Amount` <= 1000000),
  KEY (`Amount`),
  PRIMARY KEY (`p_id`),
  CONSTRAINT proj_duration CHECK (datediff(`End_date`,`Start_date`) >= 365 and datediff(`End_date`,`Start_date`) <= 1460)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- DB2022.researchers definition

CREATE TABLE `researchers` (
  `r_id` int unsigned auto_increment,
  `res_name` varchar(45) NOT NULL,
  `res_surname` varchar(45) NOT NULL,
  `gender` varchar(20) NOT NULL,
  `date_of_birth` date NOT NULL,
  PRIMARY KEY (`r_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- DB2022.assignments definition

CREATE TABLE `assignments` (
  `assign_title` varchar(100) NOT NULL,
  `assign_summary` TEXT NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- DB2022.programs definition

CREATE TABLE `programs` (
  `pr_id` int unsigned auto_increment,
  `prog_name` varchar(45) UNIQUE NOT NULL,
  `prog_address` varchar(45) NOT NULL,
  PRIMARY KEY(`pr_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- DB2022.scientific_fields definition

CREATE TABLE `scientific_fields` (
  `field_name` varchar(45) NOT NULL,
  PRIMARY KEY(`field_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- DB2022.executives definition

CREATE TABLE `executives` (
  	`exec_name` varchar(45) NOT NULL,
  	`exec_surname` varchar(45) NOT NULL,
  	`e_id` int unsigned auto_increment,
  	PRIMARY KEY(e_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- DB2022.project_fields definition

CREATE TABLE `project_fields` (
	`field_name` varchar(45) NOT NULL,
	`p_id` int unsigned NOT NULL,
	CONSTRAINT `pk_projects_fields` PRIMARY KEY (field_name, p_id)
)
COLLATE=utf8mb4_general_ci;

-- DB2022.rates definition

CREATE TABLE `rates` (
	`rating` int unsigned NOT NULL CHECK (`rating` >= 0 AND `rating` <= 10),
	`rating_date` varchar(100) NOT NULL,
	`p_id` int unsigned NOT NULL,
	`r_id` int unsigned NOT NULL,
	FOREIGN KEY (`p_id`) REFERENCES `projects` (`p_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
	FOREIGN KEY (`r_id`) REFERENCES `researchers` (`r_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
	PRIMARY KEY (`p_id`)
)COLLATE=utf8mb4_general_ci;

-- DB2022.works_on definition

CREATE TABLE `works_on` (
	`p_id` int unsigned NOT NULL,
	`r_id` int unsigned NOT NULL,
	CONSTRAINT `pk_works_on` PRIMARY KEY (p_id,r_id)
	
)
COLLATE=utf8mb4_general_ci;

-- DB2022.organisations_phones definition

CREATE TABLE `organisations_phones` (
	`o_id`  int unsigned NOT NULL,
	`phone_number` varchar(20) UNIQUE,
	PRIMARY KEY (`o_id`, `phone_number`),
	FOREIGN KEY (`o_id`) REFERENCES `organisations` (`o_id`) ON DELETE RESTRICT ON UPDATE CASCADE
)COLLATE=utf8mb4_general_ci;

-- DB2022.assignments (definition of foreign keys)

ALTER TABLE `assignments` ADD `p_id` int unsigned NOT NULL;

ALTER TABLE `assignments` ADD `due_to` date NOT NULL;

ALTER TABLE `assignments` ADD FOREIGN KEY (`p_id`) REFERENCES `projects` (`p_id`)  ON DELETE RESTRICT ON UPDATE CASCADE;

ALTER TABLE `assignments` ADD PRIMARY KEY (`assign_title`);

-- DB2022.projects (definition of foreign keys and constraints)

ALTER TABLE `projects` ADD `pr_id` int unsigned NOT NULL;

ALTER TABLE `projects` ADD `e_id` int unsigned NOT NULL;

ALTER TABLE `projects` ADD `r_id_supervisor` int unsigned NOT NULL;

ALTER TABLE `projects` ADD `o_id` int unsigned NOT NULL;

ALTER TABLE `projects` ADD `r_id_rater` int unsigned NOT NULL;

ALTER TABLE `projects` ADD FOREIGN KEY (`o_id`) REFERENCES `organisations`(`o_id`) ON DELETE RESTRICT ON UPDATE CASCADE;

ALTER TABLE `projects` ADD FOREIGN KEY (`r_id_supervisor`) REFERENCES `researchers`(`r_id`) ON DELETE RESTRICT ON UPDATE CASCADE;

ALTER TABLE `projects` ADD FOREIGN KEY (`e_id`) REFERENCES `executives`(`e_id`) ON DELETE RESTRICT ON UPDATE CASCADE;

ALTER TABLE `projects` ADD FOREIGN KEY (`pr_id`) REFERENCES `programs` (`pr_id`) ON DELETE RESTRICT ON UPDATE CASCADE;

ALTER TABLE `projects` ADD FOREIGN KEY (`r_id_rater`) REFERENCES `researchers` (`r_id`) ON DELETE RESTRICT ON UPDATE CASCADE; 

ALTER TABLE `projects` ADD CONSTRAINT fk_res_not_same CHECK (`r_id_supervisor` <> `r_id_rater`);  

-- DB2022.researchers (definition of foreign keys)

ALTER TABLE `researchers` ADD `o_id` int unsigned NOT NULL;

ALTER TABLE `researchers` ADD `start_date` date NOT NULL;

ALTER TABLE `researchers` ADD FOREIGN KEY(`o_id`) REFERENCES `organisations`(`o_id`)  ON DELETE RESTRICT ON UPDATE CASCADE;

-- DB2022.works_on (definition of foreign keys)

ALTER TABLE `works_on` ADD FOREIGN KEY(`p_id`) REFERENCES `projects`(`p_id`) ON DELETE RESTRICT ON UPDATE CASCADE;

ALTER TABLE `works_on` ADD FOREIGN KEY(`r_id`) REFERENCES `researchers`(`r_id`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- DB2022.project_fields (definition of foreign keys)

ALTER TABLE `project_fields` ADD FOREIGN KEY(`p_id`) REFERENCES `projects`(`p_id`) ON DELETE RESTRICT ON UPDATE CASCADE;

ALTER TABLE `project_fields` ADD FOREIGN KEY(`field_name`) REFERENCES `scientific_fields`(`field_name`) ON DELETE RESTRICT ON UPDATE CASCADE;

-- DB2022.Researcher_age view definition

CREATE VIEW Researcher_age AS 
SELECT res.r_id, res.res_name, res.res_surname ,FLOOR(DATEDIFF(current_date(),res.date_of_birth)/365) as Age 
FROM researchers as res;

-- DB2022.Project_duration view definition

CREATE VIEW Project_duration AS
SELECT *, FLOOR(DATEDIFF(projects.End_date ,projects.Start_date)/365) as Duration
FROM projects;

-- DB2022.project_per_researcher view definition

CREATE VIEW projects_per_researcher AS 
SELECT works_on.p_id, Title, works_on.r_id, res_name, res_surname
FROM projects
INNER JOIN works_on ON works_on.p_id = projects.p_id 
INNER JOIN researchers ON works_on.r_id = researchers.r_id 
ORDER BY r_id;

-- Triggers for date validation

DELIMITER $$
CREATE TRIGGER valid_start_proj BEFORE INSERT ON projects
FOR EACH ROW
BEGIN 
IF new.Start_date > CURRENT_DATE() THEN
SIGNAL sqlstate '45000'
SET MESSAGE_TEXT = "Start date cant be a future date.";
END IF;
END;$$ 

DELIMITER $$
CREATE TRIGGER valid_start_res BEFORE INSERT ON researchers
FOR EACH ROW
BEGIN 
IF new.start_date > CURRENT_DATE() THEN
SIGNAL sqlstate '45000'
SET MESSAGE_TEXT = "Start date cant be a future date.";
END IF;
END;$$ 

DELIMITER $$
CREATE TRIGGER valid_birth_date_res BEFORE INSERT ON researchers
FOR EACH ROW
BEGIN 
IF new.date_of_birth > CURRENT_DATE() THEN
SIGNAL sqlstate '45000'
SET MESSAGE_TEXT = "Date of birth cant be a future date.";
END IF;
END;$$ 

DELIMITER $$
CREATE TRIGGER due_to BEFORE INSERT ON assignments
FOR EACH ROW
BEGIN 
IF new.due_to <= CURRENT_DATE() THEN
SIGNAL sqlstate '45000'
SET MESSAGE_TEXT = "Assignment cant be due to a past date.";
END IF;
END;$$ 

DELIMITER $$
CREATE TRIGGER rating_date BEFORE INSERT ON rates
FOR EACH ROW
BEGIN 
IF new.rating_date > CURRENT_DATE() THEN
SIGNAL sqlstate '45000'
SET MESSAGE_TEXT = "Rating date cant be a future date.";
END IF;
END;$$ 
