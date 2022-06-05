from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_mysqldb import MySQL
from db_proj_2022 import app, db ## initially created by __init__.py, need to be used here
from db_proj_2022.forms import OrganisationsForm, PhonesForm, RatesForm, ProjectForm, ResearchersForm, Scientific_FieldsForm, ProgramsForm, AssignmentsForm, AssignmentsFormUpdate, ExecutivesForm, Project_FieldsForm, Works_OnForm, View1Form, View2Form, query1Form, query12Form, query3Form, query4Form, query5Form, query6Form, query7Form, query8Form

@app.route("/")
def index():
    try:
        return render_template("home_page.html",
                               pageTitle = "Home Page"
                               )
    except Exception as e:
        print(e)
        return render_template("home_page.html", pageTitle = "Home Page")

@app.route("/queries")
def index_queries():
    try:
        return render_template("queries_page.html",
                               pageTitle = "Queries Page"
                               )
    except Exception as e:
        print(e)
        return render_template("queries_page.html", pageTitle = "Queries Page")

@app.route("/project_page")
def index_projects():
    try:
        return render_template("project_page.html",
                               pageTitle = "Projects Page"
                               )
    except Exception as e:
        print(e)
        return render_template("project_page.html", pageTitle = "Projects Page")

@app.route("/researcher_page")
def index_researchers():
    try:
        return render_template("researcher_page.html",
                               pageTitle = "Researchers Page"
                               )
    except Exception as e:
        print(e)
        return render_template("researcher_page.html", pageTitle = "Researchers Page")

@app.route("/organisation_page")
def index_organisations():
    try:
        return render_template("organisation_page.html",
                               pageTitle = "Organisations Page"
                               )
    except Exception as e:
        print(e)
        return render_template("organisation_page.html", pageTitle = "Organisations Page")

@app.route("/executive_page")
def index_executives():
    try:
        return render_template("executive_page.html",
                               pageTitle = "Executives Page"
                               )
    except Exception as e:
        print(e)
        return render_template("executive_page.html", pageTitle = "Executives Page")

@app.route("/program_page")
def index_programs():
    try:
        return render_template("program_page.html",
                               pageTitle = "Programs Page"
                               )
    except Exception as e:
        print(e)
        return render_template("program_page.html", pageTitle = "Programs Page")

@app.route("/query_1", methods = ["GET", "POST"]) ## "GET" by default
def createQuery_1():
    """
    Get field from user
    """
    form = query1Form()
    ## when the form is submitted
    if(request.method == "POST" and form.validate_on_submit()):
        criteria = form.__dict__
        selected = 0
        query1 = "SELECT * FROM projects WHERE"
        #e_id = '{}' AND floor(DATEDIFF(End_date,Start_date)) = '{}' AND End_date = '{}'".format(criteria['executive'].data, criteria['duration'],criteria['date'].data)
        if(criteria['duration'].data != "-"):
            query1 += " FLOOR(DATEDIFF(End_date,Start_date)/365) = {}".format(criteria['duration'].data)
            selected += 1
        if(criteria['executive'].data != "-"):
            if(selected == 0):
                query1 += " e_id = '{}'".format(criteria['executive'].data)
                selected += 1
            else:
                query1 += " AND e_id = {}".format(criteria['executive'].data)
                selected += 1
        if(criteria['date'].data != "-"):
            if(selected == 0):
                query1 += " End_date = '{}'".format(criteria['date'].data)
            else:
                query1 += " AND End_date = '{}'".format(criteria['date'].data)
        try:
            cur = db.connection.cursor()
            cur.execute(query1)
            column_names = [i[0] for i in cur.description]
            results = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
            db.connection.commit()
            cur.close()
            flash("Search was successfull", "success")
            return render_template("query_1_show.html", results = results, pageTitle = "Query 1 Results", form = form)
        except Exception as e: ## OperationalError
            flash(str(e), "danger")

    ## else, response for GET request
    return render_template("query_1.html", pageTitle = "Search for projects", form = form)


@app.route("/query_1/<int:projectID>", methods = ["POST"])
def getQuery1(projectID):
    """
    Retrieve assigned researchers to a project from database
    """
    query = '''
            SELECT researchers.*
            FROM
            researchers
            INNER JOIN works_on ON researchers.r_id = works_on.r_id
            WHERE works_on.p_id = '{}'
    
    '''.format(projectID)
    try:
        form = ResearchersForm()
        cur = db.connection.cursor()
        cur.execute(query)
        column_names = [i[0] for i in cur.description]
        researchers = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("query_1_res.html", researchers = researchers, pageTitle = "Query 1 Page", form = form)
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)


@app.route("/query_1_2")
def getQuery_1_2():
    """
    Query 1_2
    """
    try:
        form = query12Form()
        cur = db.connection.cursor()
        query_1_2 = '''   
                SELECT programs.pr_id, programs.prog_name, programs.prog_address
                FROM projects
                RIGHT JOIN programs ON projects.pr_id = programs.pr_id 
                WHERE p_id IS NULL;
        '''
        cur.execute(query_1_2)
        column_names = [i[0] for i in cur.description]
        results = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("query_1_2.html", results = results, pageTitle = "Query 1_1 Results", form = form)
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)

@app.route("/view_1")
def getView_1():
    """
    Retrieve projects from database
    """
    try:
        form = View1Form()
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM projects_per_researcher")
        column_names = [i[0] for i in cur.description]
        projects_researchers = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("view_1.html", projects_researchers = projects_researchers, pageTitle = "View 1 Page", form = form)
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)

@app.route("/view_2")
def getView_2():
    """
    Retrieve duration of projects
    """
    try:
        form = View2Form()
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM Project_duration")
        column_names = [i[0] for i in cur.description]
        projects_durations = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("view_2.html", projects_durations = projects_durations, pageTitle = "View 2 Page", form = form)
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)

@app.route("/query_3", methods = ["GET", "POST"]) ## "GET" by default
def createQuery_3():
    """
    Get field from user
    """
    form = query3Form()
    ## when the form is submitted
    if(request.method == "POST" and form.validate_on_submit()):
        newQuery3 = form.__dict__
        query3 = '''
                    SELECT p.Title, r.res_name , r.res_surname 
                    FROM 
                    scientific_fields sf 
                    INNER JOIN project_fields pf ON sf.field_name = pf.field_name 
                    INNER JOIN projects p ON pf.p_id = p.p_id 
                    INNER JOIN works_on wo  ON p.p_id = wo.p_id 
                    INNER JOIN researchers r ON r.r_id = wo.r_id
                    WHERE (sf.field_name = '{}' AND p.End_date > current_date() )
        '''.format(newQuery3['field_name'].data)
        try:
            cur = db.connection.cursor()
            cur.execute(query3)
            column_names = [i[0] for i in cur.description]
            results = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
            db.connection.commit()
            cur.close()
            flash("Search was successfull", "success")
            return render_template("query_3_show.html", results = results, pageTitle = "Query 3 Results", form = form)
        except Exception as e: ## OperationalError
            flash(str(e), "danger")

    ## else, response for GET request
    return render_template("query_3.html", pageTitle = "Search by project", form = form)

@app.route("/query_4")
def getQuery_4():
    """
    Query 4 
    """
    try:
        form = query4Form()
        cur = db.connection.cursor()
        query_4 = '''   
                    SELECT b.o_id, b.org_name, b.sums,a.years as year_a, b.years as year_b
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
        '''
        cur.execute(query_4)
        column_names = [i[0] for i in cur.description]
        results = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("query_4.html", results = results, pageTitle = "Query 4 Results", form = form)
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)

@app.route("/query_5")
def getQuery_5():
    """
    Query 5
    """
    try:
        form = query5Form()
        cur = db.connection.cursor()
        query_5 = '''   
                    SELECT pf_1.field_name as field_1, pf_2.field_name as field_2, COUNT(*) AS sums
                    FROM 
                    project_fields AS pf_1 
                    INNER JOIN project_fields AS pf_2 ON pf_1.p_id = pf_2.p_id AND pf_1.field_name < pf_2.field_name 
                    GROUP BY pf_1.field_name, pf_2.field_name
                    ORDER BY sums DESC
                    LIMIT 3;
        '''
        cur.execute(query_5)
        column_names = [i[0] for i in cur.description]
        results = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("query_5.html", results = results, pageTitle = "Query 5 Results", form = form)
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)

@app.route("/query_6")
def getQuery_6():
    """
    Query 6
    """
    try:
        form = query6Form()
        cur = db.connection.cursor()
        query_6 = '''   
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
        '''
        cur.execute(query_6)
        column_names = [i[0] for i in cur.description]
        results = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("query_6.html", results = results, pageTitle = "Query 6 Results", form = form)
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)

@app.route("/query_7")
def getQuery_7():
    """
    Query 7
    """
    try:
        form = query7Form()
        cur = db.connection.cursor()
        query_7 = '''   
                    SELECT exec_name, exec_surname, org_name, SUM(Amount)as Amount 
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
        '''
        cur.execute(query_7)
        column_names = [i[0] for i in cur.description]
        results = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("query_7.html", results = results, pageTitle = "Query 7 Results", form = form)
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)

@app.route("/query_8")
def getQuery_8():
    """
    Query 8
    """
    try:
        form = query8Form()
        cur = db.connection.cursor()
        query_8 = '''   
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
        '''
        cur.execute(query_8)
        column_names = [i[0] for i in cur.description]
        results = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("query_8.html", results = results, pageTitle = "Query 8 Results", form = form)
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)


@app.route("/projects")
def getProjects():
    """
    Retrieve projects from database
    """
    try:
        form = ProjectForm()
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM projects")
        column_names = [i[0] for i in cur.description]
        projects = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("projects.html", projects = projects, pageTitle = "Projects Page", form = form)
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)

@app.route("/projects/create", methods = ["GET", "POST"]) ## "GET" by default
def createProject():
    """
    Create new project in the database
    """
    form = ProjectForm()
    ## when the form is submitted
    if(request.method == "POST" and form.validate_on_submit()):
        newProject = form.__dict__
        query = "INSERT INTO projects(Title, Summary, Start_date, End_date, Amount, pr_id, e_id, r_id_supervisor, o_id, r_id_rater) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}' );".format(newProject['Title'].data, newProject['Summary'].data, newProject['Start_date'].data, newProject['End_date'].data, newProject['Amount'].data, newProject['pr_id'].data, newProject['e_id'].data, newProject['r_id_supervisor'].data, newProject['o_id'].data, newProject['r_id_rater'].data)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Project inserted successfully", "success")
            return redirect(url_for("index"))
        except Exception as e: ## OperationalError
            flash(str(e), "danger")

    ## else, re sponse for GET request
    return render_template("create_project.html", pageTitle = "Create Project", form = form)

@app.route("/projects/update/<int:projectID>", methods = ["POST"])
def updateProject(projectID):
    """
    Update a project in the database, by id
    """
    form = ProjectForm()
    updateData = form.__dict__
    if(form.validate_on_submit()):
        query = "UPDATE projects SET Title = '{}', Summary = '{}', Start_date = '{}', End_date = '{}', Amount = '{}', pr_id = '{}', e_id = '{}', r_id_supervisor = '{}', o_id = '{}', r_id_rater = '{}' WHERE p_id = {};".format(updateData['Title'].data, updateData['Summary'].data, updateData['Start_date'].data, updateData['End_date'].data, updateData['Amount'].data, updateData['pr_id'].data, updateData['e_id'].data, updateData['r_id_supervisor'].data, updateData['o_id'].data, updateData['r_id_rater'].data, projectID)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Project updated successfully", "success")
        except Exception as e:
            flash(str(e), "danger")
    else:
        for category in form.errors.values():
            for error in category:
                flash(error, "danger")
    return redirect(url_for("getProjects"))

@app.route("/projects/delete/<int:projectID>", methods = ["POST"])
def deleteProject(projectID):
    """
    Delete project by id from database
    """
    query = f"DELETE FROM projects WHERE p_id = {projectID};"
    try:
        cur = db.connection.cursor()
        cur.execute(query)
        db.connection.commit()
        cur.close()
        flash("Project deleted successfully", "primary")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for("getProjects"))

@app.route("/researchers")
def getResearcher():
    """
    Retrieve researchers from database
    """
    try:
        form = ResearchersForm()
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM researchers")
        column_names = [i[0] for i in cur.description]
        researchers = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("researchers.html", researchers = researchers, pageTitle = "researchers Page", form = form)
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)

@app.route("/researchers/create", methods = ["GET", "POST"]) ## "GET" by default
def createResearcher():
    """
    Create new researchers in the database
    """
    form = ResearchersForm()
    ## when the form is submitted
    if(request.method == "POST" and form.validate_on_submit()):
        newResearcher = form.__dict__
        query = "INSERT INTO researchers(res_name, res_surname, gender, date_of_birth, o_id, start_date) VALUES ('{}', '{}', '{}', '{}', '{}', '{}' );".format(newResearcher['res_name'].data, newResearcher['res_surname'].data, newResearcher['gender'].data, newResearcher['date_of_birth'].data, newResearcher['o_id'].data, newResearcher['start_date'].data)

        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Researcher inserted successfully", "success")
            return redirect(url_for("index"))
        except Exception as e: ## OperationalError
            flash(str(e), "danger")

    ## else, response for GET request
    return render_template("create_researcher.html", pageTitle = "Create researchers", form = form)

@app.route("/researchers/update/<int:researcherID>", methods = ["POST"])
def updateResearcher(researcherID):
    """
    Update a researchers in the database, by id
    """
    form = ResearchersForm()
    updateData = form.__dict__
    if(form.validate_on_submit()):
        query = "UPDATE researchers SET res_name = '{}', res_surname = '{}', gender = '{}', date_of_birth = '{}', o_id = '{}', start_date = '{}' WHERE r_id = {};".format(updateData['res_name'].data, updateData['res_surname'].data, updateData['gender'].data, updateData['date_of_birth'].data, updateData['o_id'].data, updateData['start_date'].data, researcherID)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Researcher updated successfully", "success")
        except Exception as e:
            flash(str(e), "danger")
    else:
        for category in form.errors.values():
            for error in category:
                flash(error, "danger")
    return redirect(url_for("getResearcher"))

@app.route("/researchers/delete/<int:researcherID>", methods = ["POST"])
def deleteResearcher(researcherID):
    """
    Delete researchers by id from database
    """
    query = f"DELETE FROM researchers WHERE r_id = {researcherID};"
    try:
        cur = db.connection.cursor()
        cur.execute(query)
        db.connection.commit()
        cur.close()
        flash("researchers deleted successfully", "primary")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for("getResearcher"))

@app.route("/organisations")
def getOrganisation():
    """
    Retrieve organisations from database
    """
    try:
        form = OrganisationsForm()
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM organisations")
        column_names = [i[0] for i in cur.description]
        organisations = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template(
            "organisations.html",
            organisations=organisations,
            pageTitle="organisations Page",
            form=form,
        )
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)


@app.route("/organisations/create", methods=["GET", "POST"])  ## "GET" by default
def createOrganisation():
    """
    Create new organisations in the database
    """
    form = OrganisationsForm()
    ## when the form is submitted
    if request.method == "POST" and form.validate_on_submit():
        newOrganisation = form.__dict__
        query = "INSERT INTO organisations(org_name, acronym, postal_code, city, street, org_type, minedu_funding, priv_funding) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}' );".format(
            newOrganisation["org_name"].data,
            newOrganisation["acronym"].data,
            newOrganisation["postal_code"].data,
            newOrganisation["city"].data,
            newOrganisation["street"].data,
            newOrganisation["org_type"].data,
            newOrganisation["minedu_funding"].data,
            newOrganisation["priv_funding"].data,
        )

        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Organisation inserted successfully", "success")
            return redirect(url_for("index"))
        except Exception as e:  ## OperationalError
            flash(str(e), "danger")

    ## else, re sponse for GET request
    return render_template(
        "create_organisation.html", pageTitle="Create Organisation", form=form
    )


@app.route("/organisations/update/<int:organisationID>", methods=["POST"])
def updateOrganisation(organisationID):
    """
    Update a organisations in the database, by id
    """
    form = OrganisationsForm()
    updateData = form.__dict__
    if form.validate_on_submit():
        query = "UPDATE organisations SET org_name = '{}', acronym = '{}', postal_code = '{}', city = '{}', street = '{}', org_type = '{}', minedu_funding = '{}', priv_funding = '{}' WHERE o_id = {};".format(
            updateData["org_name"].data,
            updateData["acronym"].data,
            updateData["postal_code"].data,
            updateData["city"].data,
            updateData["street"].data,
            updateData["org_type"].data,
            updateData["minedu_funding"].data,
            updateData["priv_funding"].data,
            organisationID,
        )
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Organisation updated successfully", "success")
        except Exception as e:
            flash(str(e), "danger")
    else:
        for category in form.errors.values():
            for error in category:
                flash(error, "danger")
    return redirect(url_for("getOrganisation"))


@app.route("/organisations/delete/<int:organisationID>", methods=["POST"])
def deleteOrganisation(organisationID):
    """
    Delete organisations by id from database
    """
    query = f"DELETE FROM organisations WHERE o_id = {organisationID};"
    try:
        cur = db.connection.cursor()
        cur.execute(query)
        db.connection.commit()
        cur.close()
        flash("Organisation deleted successfully", "primary")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for("getOrganisations"))

@app.route("/programs")
def getProgram():
    """
    Retrieve programs from database
    """
    try:
        form = ProgramsForm()
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM programs")
        column_names = [i[0] for i in cur.description]
        programs = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("programs.html", programs = programs, pageTitle = "Programs Page", form = form)
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)

@app.route("/programs/create", methods = ["GET", "POST"]) ## "GET" by default
def createProgram():
    """
    Create new programs in the database
    """
    form = ProgramsForm()
    ## when the form is submitted
    if(request.method == "POST" and form.validate_on_submit()):
        newProgram = form.__dict__
        query = "INSERT INTO programs(prog_name, prog_address) VALUES ('{}', '{}');".format(newProgram['prog_name'].data, newProgram['prog_address'].data )


        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Program inserted successfully", "success")
            return redirect(url_for("index"))
        except Exception as e: ## OperationalError
            flash(str(e), "danger")

    ## else, re sponse for GET request
    return render_template("create_program.html", pageTitle = "Create program", form = form)

@app.route("/programs/update/<int:programID>", methods = ["POST"])
def updateProgram(programID):
    """
    Update a program in the database, by id
    """
    form = ProgramsForm()
    updateData = form.__dict__
    if(form.validate_on_submit()):
        query = "UPDATE programs SET prog_name= '{}', prog_address = '{}' WHERE pr_id = {};".format(updateData['prog_name'].data, updateData['prog_address'].data, programID)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Program updated successfully", "success")
        except Exception as e:
            flash(str(e), "danger")
    else:
        for category in form.errors.values():
            for error in category:
                flash(error, "danger")
    return redirect(url_for("getProgram"))

@app.route("/programs/delete/<int:programID>", methods = ["POST"])
def deleteProgram(programID):
    """
    Delete programs by id from database
    """
    query = f"DELETE FROM programs WHERE pr_id = {programID};"
    try:
        cur = db.connection.cursor()
        cur.execute(query)
        db.connection.commit()
        cur.close()
        flash("Program deleted successfully", "primary")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for("getProgram"))


@app.route("/executives")
def getExecutives():
    """
    Retrieve executives from database
    """
    try:
        form = ExecutivesForm()
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM executives")
        column_names = [i[0] for i in cur.description]
        executives = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template(
            "executives.html",
            executives=executives,
            pageTitle="Executives Page",
            form=form,
        )
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)


@app.route("/executives/create", methods=["GET", "POST"])  ## "GET" by default
def createExecutive():
    """
    Create new executive in the database
    """
    form = ExecutivesForm()
    ## when the form is submitted
    if request.method == "POST" and form.validate_on_submit():
        newExecutive = form.__dict__
        query = "INSERT INTO executives(exec_name, exec_surname) VALUES ('{}', '{}');".format(
            newExecutive["exec_name"].data,
            newExecutive["exec_surname"].data,
        )
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Executive inserted successfully", "success")
            return redirect(url_for("index"))
        except Exception as e:  ## OperationalError
            flash(str(e), "danger")

    ## else, re sponse for GET request
    return render_template(
        "create_executive.html", pageTitle="Create Executive", form=form
    )


@app.route("/executives/update/<int:executiveID>", methods=["POST"])
def updateExecutive(executiveID):
    """
    Update a executive in the database, by id
    """
    form = ExecutivesForm()
    updateData = form.__dict__
    if form.validate_on_submit():
        query = "UPDATE executives SET exec_name = '{}', exec_surname = '{}' WHERE e_id = {};".format(
            updateData["exec_name"].data,
            updateData["exec_surname"].data,
            executiveID,
        )
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Executive updated successfully", "success")
        except Exception as e:
            flash(str(e), "danger")
    else:
        for category in form.errors.values():
            for error in category:
                flash(error, "danger")
    return redirect(url_for("getExecutives"))


@app.route("/executives/delete/<int:executiveID>", methods=["POST"])
def deleteExecutive(executiveID):
    """
    Delete executive by id from database
    """
    query = f"DELETE FROM executives WHERE e_id = {executiveID};"
    try:
        cur = db.connection.cursor()
        cur.execute(query)
        db.connection.commit()
        cur.close()
        flash("Executive deleted successfully", "primary")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for("getExecutives"))

@app.route("/project_fields")
def getProject_field():
    """
    Retrieve project_fields from database
    """
    try:
        form = Project_FieldsForm()
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM project_fields ORDER BY p_id")
        column_names = [i[0] for i in cur.description]
        project_fields = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("project_fields.html", project_fields = project_fields, pageTitle = "Project_fields Page", form = form)
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)

@app.route("/project_fields/create", methods = ["GET", "POST"]) ## "GET" by default
def createProject_field():
    """
    Create new project_fields in the database
    """
    form = Project_FieldsForm()
    ## when the form is submitted
    if(request.method == "POST" and form.validate_on_submit()):
        newProject_fields = form.__dict__
        query = "INSERT INTO project_fields(field_name, p_id) VALUES ('{}', '{}');".format(newProject_fields['field_name'].data, newProject_fields['p_id'].data )


        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Field inserted into project successfully", "success")
            return redirect(url_for("index"))
        except Exception as e: ## OperationalError
            flash(str(e), "danger")

    ## else, re sponse for GET request
    return render_template("create_project_field.html", pageTitle = "Add field to a project", form = form)

@app.route("/project_fields/update/<int:p_ID><string:Field_Name>", methods = ["POST"])
def updateProject_field(Field_Name,p_ID):
    """
    Update a field of a project in the database, by p_id
    """
    form = Project_FieldsForm()
    updateData = form.__dict__
    if(form.validate_on_submit()):
        query = "UPDATE project_fields SET  field_name= '{}' WHERE  field_name = '{}' AND p_id = '{}';".format(updateData['field_name'].data, Field_Name, p_ID)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Field of project updated successfully", "success")
        except Exception as e:
            flash(str(e), "danger")
    else:
        for category in form.errors.values():
            for error in category:
                flash(error, "danger")
    return redirect(url_for("getProject_field"))

@app.route("/project_fields/delete/<int:p_ID><string:Field_Name>", methods = ["POST"])
def deleteProject_field(Field_Name,p_ID):
    """
    Delete project_fields by id from database
    """
    query = "DELETE FROM project_fields WHERE field_name = '{}' AND p_id = '{}';".format(Field_Name,p_ID)
    try:
        cur = db.connection.cursor()
        cur.execute(query)
        db.connection.commit()
        cur.close()
        flash("Field deleted from project successfully", "primary")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for("getProject_field"))

@app.route("/assignments")
def getAssignments():
    """
    Retrieve assignments from database
    """
    try:
        form = AssignmentsForm()
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM assignments ORDER BY p_id")
        column_names = [i[0] for i in cur.description]
        assignments = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template(
            "assignments.html",
            assignments=assignments,
            pageTitle="Assignments Page",
            form=form,
        )
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)


@app.route("/assignments/create", methods=["GET", "POST"])  ## "GET" by default
def createAssignment():
    """
    Create new assignment in the database
    """
    form = AssignmentsForm()
    ## when the form is submitted
    if request.method == "POST" and form.validate_on_submit():
        newAssignment = form.__dict__
        query = "INSERT INTO assignments(assign_title, assign_summary, p_id, due_to) VALUES ('{}', '{}', '{}', '{}');".format(
            newAssignment["assign_title"].data,
            newAssignment["assign_summary"].data,
            newAssignment["p_id"].data,
            newAssignment["due_to"].data,
        )
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Assignment inserted successfully", "success")
            return redirect(url_for("index"))
        except Exception as e:  ## OperationalError
            flash(str(e), "danger")

    ## else, re sponse for GET request
    return render_template(
        "create_assignment.html", pageTitle="Create Assignment", form=form
    )


@app.route("/assignments/update/<string:assignmentID>", methods=["POST"])
def updateAssignment(assignmentID):
    """
    Update an assignment in the database, by id(title)
    """
    form = AssignmentsFormUpdate()
    updateData = form.__dict__
    if form.validate_on_submit():
        query = "UPDATE assignments SET assign_summary = '{}', p_id = '{}' , due_to = '{}' WHERE assign_title = '{}';".format(
            updateData["assign_summary"].data,
            updateData["p_id"].data,
            updateData["due_to"].data,
            assignmentID
        )
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Assignment updated successfully", "success")
        except Exception as e:
            flash(str(e), "danger")
    else:
        for category in form.errors.values():
            for error in category:
                flash(error, "danger")
    return redirect(url_for("getAssignments"))


@app.route("/assignments/delete/<string:assignmentID>", methods=["POST"])
def deleteAssignment(assignmentID):
    """
    Delete assignment by id(title) from database
    """
    query = "DELETE FROM assignments WHERE assign_title = '{}';".format(assignmentID)
    try:
        cur = db.connection.cursor()
        cur.execute(query)
        db.connection.commit()
        cur.close()
        flash("Assignment deleted successfully", "primary")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for("getAssignments"))

@app.route("/works_on")
def getWorks_on():
    """
    Retrieve works_on from database
    """
    try:
        form = Works_OnForm()
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM works_on ORDER BY r_id")
        column_names = [i[0] for i in cur.description]
        works_on = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("works_on.html", works_on = works_on, pageTitle = "Works_on Page", form = form)
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)


@app.route("/works_on/create", methods = ["GET", "POST"]) ## "GET" by default
def createWorks_on():
    """
    Create new works_on in the database
    """
    form = Works_OnForm()
    ## when the form is submitted
    if(request.method == "POST" and form.validate_on_submit()):
        newworks_on = form.__dict__
        query = "INSERT INTO works_on(p_id, r_id) VALUES ('{}','{}');".format(newworks_on['p_id'].data, newworks_on['r_id'].data )


        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Researcher assigned to project successfully", "success")
            return redirect(url_for("index"))
        except Exception as e: ## OperationalError
            flash(str(e), "danger")

    ## else, response for GET request
    return render_template("create_works_on.html", pageTitle = "Create works_on", form = form)

@app.route("/works_on/update/<int:p_ID>/<int:r_ID>", methods = ["POST"])
def updateWorks_on(p_ID, r_ID):
    """
    Update a field of a project in the database, by p_id
    """
    form = Works_OnForm()
    updateData = form.__dict__
    if(form.validate_on_submit()):
        query = "UPDATE works_on SET  p_id = '{}' WHERE  p_id = '{}' AND r_id = '{}';".format(updateData['p_id'].data, p_ID, r_ID)
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Researcher assigned to project successfully", "success")
        except Exception as e:
            flash(str(e), "danger")
    else:
        for category in form.errors.values():
            for error in category:
                flash(error, "danger")
    return redirect(url_for("getWorks_on"))

@app.route("/works_on/delete/<int:p_ID>/<int:r_ID>", methods = ["POST"])
def deleteWorks_on(p_ID,r_ID):
    """
    Delete works on by r_id,p_id from database
    """
    query = "DELETE FROM works_on WHERE r_id = {} AND p_id = {};".format(r_ID,p_ID)
    try:
        cur = db.connection.cursor()
        cur.execute(query)
        db.connection.commit()
        cur.close()
        flash("Researcher unassigned from project successfully", "primary")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for("getWorks_on"))


@app.route("/phones")
def getPhones():
    """
    Retrieve Organisation phones from database
    """
    try:
        form = PhonesForm()
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM organisations_phones ORDER BY o_id")
        column_names = [i[0] for i in cur.description]
        organisations_phones = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template(
            "phones.html",
            organisations_phones=organisations_phones,
            pageTitle="Phones Page",
            form=form,
        )
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)


@app.route("/phones/create", methods=["GET", "POST"])  ## "GET" by default
def createPhone():
    """
    Create new phone of organisation in the database
    """
    form = PhonesForm()
    ## when the form is submitted
    if request.method == "POST" and form.validate_on_submit():
        newPhone = form.__dict__
        query = "INSERT INTO organisations_phones(o_id, phone_number) VALUES ('{}','{}');".format(
            newPhone["o_id"].data,
            newPhone["phone_number"].data
        )
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Phone of organisation inserted successfully", "success")
            return redirect(url_for("index"))
        except Exception as e:  ## OperationalError
            flash(str(e), "danger")

    ## else, re sponse for GET request
    return render_template(
        "create_phone.html", pageTitle="Add Phone", form=form
    )

@app.route("/phones/update/<int:organisationID>", methods=["POST"])
def updatePhone(organisationID):
    """
    Update a phone number in the database, by org_id
    """
    form = PhonesForm()
    updateData = form.__dict__
    if form.validate_on_submit():
        query = "UPDATE organisations_phones SET phone_number = '{}' WHERE o_id = {};".format(
            updateData["phone_number"].data,
            organisationID
        )
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Phone of organisation updated successfully", "success")
        except Exception as e:
            flash(str(e), "danger")
    else:
        for category in form.errors.values():
            for error in category:
                flash(error, "danger")
    return redirect(url_for("getPhones"))


@app.route("/phones/delete/<int:organisationID><string:Phone>", methods=["POST"])
def deletePhone(organisationID,Phone):
    """
    Delete phone of organisation by id from database
    """
    query = f"DELETE FROM organisations_phones WHERE o_id = {organisationID} AND phone_number = {Phone};"
    try:
        cur = db.connection.cursor()
        cur.execute(query)
        db.connection.commit()
        cur.close()
        flash("Phone number of organisation deleted successfully", "primary")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for("getPhones"))

@app.route("/rates")
def getRates():
    """
    Retrieve rates from database
    """
    try:
        form = RatesForm()
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM rates ORDER BY p_id")
        column_names = [i[0] for i in cur.description]
        rates = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("rates.html", rates=rates, pageTitle="Ratings Page", form=form)
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)


@app.route("/rates/create", methods=["GET", "POST"])  ## "GET" by default
def createRate():
    """
    Create rate for project in the database
    """
    form = RatesForm()
    ## when the form is submitted
    if request.method == "POST" and form.validate_on_submit():
        newRate = form.__dict__
        query = "INSERT INTO rates(p_id, rating, rating_date, r_id) VALUES ('{}','{}','{}','{}');".format(
            newRate["p_id"].data,
            newRate["rating"].data,
            newRate["rating_date"].data,
            newRate["r_id"].data
        )
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Rating of project inserted successfully", "success")
            return redirect(url_for("index"))
        except Exception as e:  ## OperationalError
            flash(str(e), "danger")

    ## else, re sponse for GET request
    return render_template(
        "create_rate.html", pageTitle="Add Rate", form=form
    )


@app.route("/rates/update/<int:projectID>", methods=["POST"])
def updateRate(projectID):
    """
    Update a rate in the database, by p_id
    """
    form = RatesForm()
    updateData = form.__dict__
    if form.validate_on_submit():
        query = "UPDATE rates SET rating = '{}', rating_date = '{}', r_id = '{}' WHERE p_id = {};".format(
            updateData["rating"].data,
            updateData["rating_date"].data,
            updateData["r_id"].data,
            projectID
        )
        query_up_rater = "UPDATE projects SET r_id_rater = '{}' WHERE p_id = {}".format(
            updateData["r_id"].data,
            projectID 
        )
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            cur.execute(query_up_rater)
            db.connection.commit()
            cur.close()
            flash("Rating info of project updated successfully", "success")
        except Exception as e:
            flash(str(e), "danger")
    else:
        for category in form.errors.values():
            for error in category:
                flash(error, "danger")
    return redirect(url_for("getRates"))


@app.route("/rates/delete/<int:projectID>", methods=["POST"])
def deleteRate(projectID):
    """
    Delete rate of project by p_id from database
    """
    query = f"DELETE FROM rates WHERE p_id = {projectID};"
    try:
        cur = db.connection.cursor()
        cur.execute(query)
        db.connection.commit()
        cur.close()
        flash("Rating of project deleted successfully", "primary")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for("getRates"))

@app.route("/scientific_fields")
def getScientific_fields():
    """
    Retrieve scientific fields from database
    """
    try:
        form = Scientific_FieldsForm()
        cur = db.connection.cursor()
        cur.execute("SELECT * FROM scientific_fields")
        column_names = [i[0] for i in cur.description]
        scientific_fields = [dict(zip(column_names, entry)) for entry in cur.fetchall()]
        cur.close()
        return render_template("scientific_fields.html", scientific_fields = scientific_fields, pageTitle = "Scientific Fields Page", form = form)
    except Exception as e:
        ## if the connection to the database fails, return HTTP response 500
        flash(str(e), "danger")
        abort(500)

@app.route("/scientific_fields/create", methods = ["GET", "POST"]) ## "GET" by default
def createScientific_field():
    """
    Create new scientific_field in the database
    """
    form = Scientific_FieldsForm()
    ## when the form is submitted
    if(request.method == "POST" and form.validate_on_submit()):
        newScientific_field = form.__dict__
        query = "INSERT INTO scientific_fields(field_name) VALUES ('{}');".format(newScientific_field['field_name'].data )
        try:
            cur = db.connection.cursor()
            cur.execute(query)
            db.connection.commit()
            cur.close()
            flash("Scientific field inserted successfully", "success")
            return redirect(url_for("index"))
        except Exception as e: ## OperationalError
            flash(str(e), "danger")

    ## else, re sponse for GET request
    return render_template("create_scientific_field.html", pageTitle = "Create Scientific Field", form = form)

@app.route("/scientific_fields/delete/<string:fieldID>", methods = ["POST"])
def deleteScientific_field(fieldID):
    """
    Delete scientific field by field name from database
    """
    query = "DELETE FROM scientific_fields WHERE field_name = '{}';".format(fieldID)
    try:
        cur = db.connection.cursor()
        cur.execute(query)
        db.connection.commit()
        cur.close()
        flash("Field deleted successfully", "primary")
    except Exception as e:
        flash(str(e), "danger")
    return redirect(url_for("getScientific_fields"))

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template("errors/404.html", pageTitle = "Not Found"), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template("errors/500.html", pageTitle = "Internal Server Error"), 500
