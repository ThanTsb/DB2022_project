from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, DateField
from wtforms.validators import DataRequired

## when passed as a parameter to a template, an object of this class will be rendered as a regular HTML form
## with the additional restrictions specified for each field
class ProjectForm(FlaskForm):
    Title = StringField(label = "Title", validators = [DataRequired(message = "Title is a required field.")])

    Summary = TextAreaField(label = "Summary", validators = [DataRequired(message = "Summary is a required field.")])

    Start_date = DateField(label = "Start Date", validators = [DataRequired(message = "Start Date is a required field.")])

    End_date = DateField(label = "End Date", validators = [DataRequired(message = "End Date is a required field.")])
    
    Amount = StringField(label = "Amount", validators = [DataRequired(message = "Amount is a required field.")])
    
    pr_id = StringField(label = "Program ID", validators = [DataRequired(message = "Program ID is a required field.")])

    e_id = StringField(label = "Executive ID", validators = [DataRequired(message = "Executive ID is a required field.")])

    r_id_supervisor = StringField(label = "Supervisor's ID", validators = [DataRequired(message = "Supervisor's ID is a required field.")])

    o_id = StringField(label = "Organisation ID", validators = [DataRequired(message = "Organisation ID is a required field.")])

    r_id_rater = StringField(label = "Rater's ID", validators = [DataRequired(message = "Rater's ID is a required field.")])
    
    submit = SubmitField("Create")

class ResearchersForm(FlaskForm):
    res_name = StringField(label = "Researcher Name", validators = [DataRequired(message = "Researcher Name is a required field.")])
    res_surname = StringField(label = "Researcher Surname", validators = [DataRequired(message = "Researcher Surname is a required field.")])
    gender = StringField(label = "Gender", validators = [DataRequired(message = "Gender is a required field.")])
    date_of_birth = DateField(label = "Date Of Birth", validators = [DataRequired(message = "Date Of Birth is a required field.")])
    o_id = StringField(label = "Organisation ID", validators = [DataRequired(message = "Organisation ID a required field.")])
    start_date = DateField(label = "Start Date", validators = [DataRequired(message = "Start Date is a required field.")])
    submit = SubmitField("Create")

class OrganisationsForm(FlaskForm):
    org_name = StringField(label = "Organisation Name", validators = [DataRequired(message = "Organisation Name is a required field.")])
    acronym = StringField(label = "Acronym", validators = [DataRequired(message = "Acronym is a required field.")])
    postal_code = StringField(label = "Postal Code", validators = [DataRequired(message = "Postal Code is a required field.")])
    city = StringField(label = "City", validators = [DataRequired(message = "City is a required field.")])
    street = StringField(label = "Street", validators = [DataRequired(message = "Street a required field.")])
    org_type = StringField(label = "Organisation Type", validators = [DataRequired(message = "Organisation Type is a required field.")])
    minedu_funding = StringField(label = "Minedu Funding")
    priv_funding = StringField(label = "Private Funding")
    submit = SubmitField("Create")

class AssignmentsForm(FlaskForm):

    assign_title = StringField(label = "Assignment Title", validators = [DataRequired(message = "Assignment Title is a required field.")])
    assign_summary = StringField(label = "Assignment Summary", validators = [DataRequired(message = "Assignment Summary is a required field.")])

    p_id = StringField(label = "Project ID", validators = [DataRequired(message = "Project ID is a required field.")])
    
    due_to = DateField(label = "Due Date", validators = [DataRequired(message = "Due Date is a required field.")])
    
    submit = SubmitField("Create")

class AssignmentsFormUpdate(FlaskForm):
    assign_summary = TextAreaField(label = "Assignment Summary", validators = [DataRequired(message = "Assignment Summary is a required field.")])

    p_id = StringField(label = "Project ID", validators = [DataRequired(message = "Project ID is a required field.")])
    
    due_to = DateField(label = "Due Date", validators = [DataRequired(message = "Due Date is a required field.")])
    
    submit = SubmitField("Create")    

class ProgramsForm(FlaskForm):
    prog_name = StringField(label = "Program Name", validators = [DataRequired(message = "Program Name is a required field.")])
    
    prog_address = StringField(label = "Program Address(ΕΛ.ΙΔ.Ε.Κ)", validators = [DataRequired(message = "Program Address(ΕΛ.ΙΔ.Ε.Κ) is a required field.")])
    
    submit = SubmitField("Create")

class ExecutivesForm(FlaskForm):
    exec_name = StringField(label = "Executive Name", validators = [DataRequired(message = "Executive Name is a required field.")])
    
    exec_surname= StringField(label = "Executive Surname", validators = [DataRequired(message = "Executive Surname is a required field.")])
    
    submit = SubmitField("Create")

class Works_OnForm(FlaskForm):
    p_id = StringField(label = "Project ID", validators = [DataRequired(message = "Project ID is a required field.")])
    r_id = StringField(label = "Researcher ID")
    
    submit = SubmitField("Create")

class Project_FieldsForm(FlaskForm):
    field_name = StringField(label = "Name of Scientific Field", validators = [DataRequired(message = "Name of Scientific Field is a required field.")])
    p_id = StringField(label = "Project ID")
    
    submit = SubmitField("Create")

class Scientific_FieldsForm(FlaskForm):
    field_name = StringField(label = "Name of Scientific Field", validators = [DataRequired(message = "Name of Scientific Field is a required field.")])
    
    submit = SubmitField("Create")

class PhonesForm(FlaskForm):
    o_id = StringField(label = "Organisation ID", validators = [DataRequired(message = "Organisation ID is a required field.")])
    phone_number= StringField(label = "Phone Number", validators = [DataRequired(message = "Phone Number is a required field.")])
    
    submit = SubmitField("Create")

class query3Form(FlaskForm):
    field_name = StringField(label = "Field Name", validators = [DataRequired(message = "You must choose a field to perform the search.")])

    submit = SubmitField("Search")
class query4Form(FlaskForm):
    o_id = StringField(label = "Organisation ID", validators = [DataRequired(message = "Organisation ID is a required field.")])
    org_name = StringField(label = "Organisation Name", validators = [DataRequired(message = "Organisation Name is a required field.")])
    sums = StringField(label = "sums", validators = [DataRequired(message = "sums is a required field.")])
    year_a = StringField(label = "year_a", validators = [DataRequired(message = "year_a is a required field.")])
    year_b = StringField(label = "year_b", validators = [DataRequired(message = "year_b is a required field.")])
    submit = SubmitField("Create")

class query5Form(FlaskForm):
    field_1 = StringField(label = "field_1", validators = [DataRequired(message = "field_1 is a required field.")])
    field_2 = StringField(label = "field_2", validators = [DataRequired(message = "field_1 is a required field.")])
    sums = StringField(label = "sums", validators = [DataRequired(message = "sums is a required field.")])
    submit = SubmitField("Create")

class query6Form(FlaskForm):
    res_name = StringField(label = "Researcher Name", validators = [DataRequired(message = "Researcher Name is a required field.")])
    res_surname = StringField(label = "Researcher Surname", validators = [DataRequired(message = "Researcher Surname is a required field.")])
    maximum = StringField(label = "maximum", validators = [DataRequired(message = "maximum is a required field.")])
    submit = SubmitField("Create")

class query7Form(FlaskForm):
    exec_name = StringField(label = "Executive Name", validators = [DataRequired(message = "Executive Name is a required field.")])
    exec_surname = StringField(label = "Executive Surname", validators = [DataRequired(message = "Executive Surname is a required field.")])
    org_name = StringField(label = "Organisation Name", validators = [DataRequired(message = "Organisation Name is a required field.")])
    Amount = StringField(label = "Amount", validators = [DataRequired(message = "Amount is a required field.")])
    
    submit = SubmitField("Create")   

class query8Form(FlaskForm):
    res_name = StringField(label = "Researcher Name", validators = [DataRequired(message = "Researcher Name is a required field.")])
    res_surname = StringField(label = "Researcher Surname", validators = [DataRequired(message = "Researcher Surname is a required field.")])
    proj_numb = StringField(label = "proj_number", validators = [DataRequired(message = "proj_numb is a required field.")])
    
    submit = SubmitField("Create") 

durations = ['-', 1, 2, 3, 4]
class query1Form(FlaskForm):
    duration = SelectField(label = 'Duration(Years)', choices=[duration for duration in durations])
    executive = StringField(label = "Executive's id(Enter '-' to exclude as criterion)", validators = [DataRequired(message = "Executive's id is a required field.")])
    date = StringField(label = "Date (YYYY-MM-DD) (Enter '-' to exclude as criterion)", validators = [DataRequired(message = "Date is a required field.")])
    submit = SubmitField("Find") 

class query12Form(FlaskForm):
    res_name = StringField(label = "Researcher Name", validators = [DataRequired(message = "Researcher Name is a required field.")])
    res_surname = StringField(label = "Researcher Surname", validators = [DataRequired(message = "Researcher Surname is a required field.")])
    Title = StringField(label = "Title", validators = [DataRequired(message = "proj_numb is a required field.")])
    
    submit = SubmitField("Create") 

class View1Form(FlaskForm):
    res_name = StringField(label = "Researcher Name", validators = [DataRequired(message = "Researcher Name is a required field.")])
    res_surname = StringField(label = "Researcher Surname", validators = [DataRequired(message = "Researcher Surname is a required field.")])
    Title = StringField(label = "Title", validators = [DataRequired(message = "proj_numb is a required field.")])
    
    submit = SubmitField("Create") 

class View2Form(FlaskForm):
    p_id = StringField(label = "Project ID", validators = [DataRequired(message = "Project ID is a required field.")])
    Title = StringField(label = "Title", validators = [DataRequired(message = "Researcher Surname is a required field.")])
    Summary = StringField(label = "Summary", validators = [DataRequired(message = "proj_numb is a required field.")])
    Start_date = DateField(label = "Start Date", validators = [DataRequired(message = "proj_numb is a required field.")])
    End_date = DateField(label = "End Date", validators = [DataRequired(message = "proj_numb is a required field.")])   
    Amount = StringField(label = "Amount", validators = [DataRequired(message = "proj_numb is a required field.")])
    pr_id = StringField(label = "Program ID", validators = [DataRequired(message = "proj_numb is a required field.")])
    e_id = StringField(label = "Executive ID", validators = [DataRequired(message = "proj_numb is a required field.")])
    r_id_supervisor = StringField(label = "Supervisor's ID", validators = [DataRequired(message = "proj_numb is a required field.")])
    o_id = StringField(label = "Organisation ID", validators = [DataRequired(message = "proj_numb is a required field.")])
    r_id_rater = StringField(label = "Rater's ID", validators = [DataRequired(message = "proj_numb is a required field.")])
    Duration = StringField(label = "Duration", validators = [DataRequired(message = "proj_numb is a required field.")])
    submit = SubmitField("Create") 

class RatesForm(FlaskForm):
    p_id = StringField(label = "Project ID")
    rating = StringField(label = "Rating(0-10)", validators = [DataRequired(message = "Rating is a required field.")])
    rating_date = DateField(label = "Date of Rate", validators = [DataRequired(message = "Date of rate is a required field.")])
    r_id = StringField(label = "Rater ID", validators = [DataRequired(message = "Rater ID is a required field.")])
    
    submit = SubmitField("Create")


    