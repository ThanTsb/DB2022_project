--QUERY 1)
--IMPLEMENTATION

--Get available programms..
SELECT programs.pr_id, programs.prog_name, programs.prog_address
FROM projects
RIGHT JOIN programs ON projects.pr_id = programs.pr_id 
WHERE p_id IS NULL;
--Get registered projects based on ...
SELECT * 
FROM projects 
WHERE FLOOR(DATEDIFF(End_date,Start_date)/365) = {}  AND e_id = {} AND End_date = {}
--Where clause is adjusted in our application depending on which criteria the user chooses.
-- Brackets({}) are user-defined fields in our application.

--2)CREATE 2 VIEWS 
--1. CONTAINS PROJECTS FOR EACH RESEARCHER
--2. CUSTOM view 
--IMPLEMENTATION
--DDL scripts for views contained in ddl.sql file.

--Get project_per_researchers
SELECT * FROM projects_per_researcher

--Get Project_duration
SELECT * FROM Project_duration

--QUERY 3)
--IMPLEMENTATION

SELECT p.Title, r.res_name , r.res_surname 
FROM 
scientific_fields sf 
INNER JOIN project_fields pf ON sf.field_name = pf.field_name 
INNER JOIN projects p ON pf.p_id = p.p_id 
INNER JOIN works_on wo  ON p.p_id = wo.p_id 
INNER JOIN researchers r ON r.r_id = wo.r_id
WHERE (sf.field_name = 'USER_DEFINED_FIELD' AND p.End_date > current_date() )
--USER_DEFINED_FIELD is defined by the user in our app.

--QUERY 4)
--IMPLEMENTATION 

SELECT b.o_id, b.org_name, b.sums,a.years,b.years
FROM
	(
	SELECT  organisations.o_id, organisations.org_name, YEAR(projects.Start_date) AS years, COUNT(*) AS sums
	FROM organisations
	INNER JOIN projects ON organisations.o_id = projects.o_id 
	GROUP BY organisations.o_id, YEAR(projects.Start_date)
	HAVING COUNT(*) >= 10
	)as a,
	(
	SELECT  organisations.o_id, organisations.org_name, YEAR(projects.Start_date) AS years, COUNT(*) AS sums
	FROM organisations
	INNER JOIN projects ON organisations.o_id = projects.o_id 
	GROUP BY organisations.o_id, YEAR(projects.Start_date)
	HAVING COUNT(*) >= 10
	)as b
WHERE  ((a.years - b.years = 1 ) AND (a.sums=b.sums) AND (a.o_id = b.o_id));

--QUERY 5)
--IMPLEMENTATION

SELECT pf_1.field_name, pf_2.field_name, COUNT(*) AS sums
FROM 
project_fields AS pf_1 
INNER JOIN project_fields AS pf_2 ON pf_1.p_id = pf_2.p_id AND pf_1.field_name < pf_2.field_name 
GROUP BY pf_1.field_name, pf_2.field_name
ORDER BY sums DESC
LIMIT 3;

--QUERY 6)
--IMPLEMENTATION 

SELECT res_name, res_surname, maximum
FROM
(
SELECT MAX(fin.sums) as maximum
FROM
(
SELECT r.r_id, r.res_name, r.res_surname, r.Age, count(*) as sums 
FROM
(
SELECT *
FROM
researcher_age
WHERE (researcher_age.Age < 40 )
) r
INNER JOIN works_on wo ON r.r_id = wo.r_id 
GROUP BY wo.r_id 
)fin
)res
,
(
SELECT r.r_id, r.res_name, r.res_surname, r.Age, count(*) as sums 
FROM
(
SELECT *
FROM
researcher_age
WHERE (researcher_age.Age < 40 )
) r
INNER JOIN works_on wo ON r.r_id = wo.r_id 
GROUP BY wo.r_id 
)fin2
WHERE fin2.sums = res.maximum

--QUERY 7)
--IMPLEMENTATION

SELECT exec_name, exec_surname, org_name, SUM(Amount) as Amount
FROM
(
SELECT p.o_id, p.e_id, p.Amount, org.org_name 
FROM
organisations org
INNER JOIN projects p ON org.o_id = p.o_id 
WHERE org_type = "Company"
)comp
INNER JOIN executives e ON comp.e_id = e.e_id
GROUP BY e.e_id,comp.o_id
ORDER BY SUM(Amount) DESC
LIMIT 5;

--QUERY 8)
--IMPLEMENTATION
SELECT researchers.res_name, researchers.res_surname, fin.proj_numb
FROM
(
SELECT works_on.r_id, COUNT(*) as proj_numb
FROM
(
SELECT p.p_id
FROM
projects p
LEFT JOIN assignments a ON p.p_id = a.p_id
WHERE (a.assign_title is NULL)
)res 
INNER JOIN works_on ON res.p_id = works_on.p_id 
GROUP BY works_on.r_id
HAVING COUNT(r_id) >= 5
)fin 
INNER JOIN researchers ON fin.r_id = researchers.r_id 
