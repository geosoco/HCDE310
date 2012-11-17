# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models


class Departments(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=384, db_column='Name') # Field name made lowercase.
    abbreviation = models.CharField(max_length=24, db_column='Abbreviation') # Field name made lowercase.
    class Meta:
        db_table = u'Departments'

class Courses(models.Model):
    NW = 'N'
    VLPA = 'V'
    IS = 'I'
    W = 'W'
    EC = 'E'
    QSR = 'Q'
    GEN_ED_REQ_CHOICES = (
        (NW, 'NW'),
        (VLPA, 'VLPA'),
        (IS, 'I&S'),
        (W, 'W'),
        (QSR, 'QSR'),
        (EC, 'EC')
    )


    id = models.IntegerField(primary_key=True)
    number = models.IntegerField(db_column='Number') # Field name made lowercase.
    name = models.CharField(max_length=384, db_column='Name', blank=True) # Field name made lowercase.
    comment = models.CharField(max_length=768, db_column='Comment', blank=True) # Field name made lowercase.
    description = models.CharField(max_length=6144, db_column='Description', blank=True) # Field name made lowercase.
    iddepartment = models.ForeignKey(Departments, db_column='idDepartment') # Field name made lowercase.
    genedreqs = models.CharField(max_length=33, db_column='GenEdReqs', blank=True, choices=GEN_ED_REQ_CHOICES) # Field name made lowercase.
    class Meta:
        db_table = u'Courses'



class Instructors(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=192, db_column='Name') # Field name made lowercase.
    class Meta:
        db_table = u'Instructors'

class Ratings(models.Model):
    id = models.AutoField(primary_key=True, db_column='id') # Field name made lowercase.
    coursewhole = models.DecimalField(decimal_places=0, null=True, max_digits=9, db_column='CourseWhole') # Field name made lowercase.
    coursecontent = models.DecimalField(decimal_places=0, null=True, max_digits=9, db_column='CourseContent', blank=True) # Field name made lowercase.
    instructoreffectiveness = models.DecimalField(decimal_places=0, null=True, max_digits=9, db_column='InstructorEffectiveness', blank=True) # Field name made lowercase.
    instructorcontribution = models.DecimalField(decimal_places=0, null=True, max_digits=9, db_column='InstructorContribution', blank=True) # Field name made lowercase.
    instructorinterest = models.DecimalField(decimal_places=0, null=True, max_digits=9, db_column='InstructorInterest', blank=True) # Field name made lowercase.
    amountlearned = models.DecimalField(decimal_places=0, null=True, max_digits=9, db_column='AmountLearned', blank=True) # Field name made lowercase.
    grading = models.DecimalField(decimal_places=0, null=True, max_digits=9, db_column='Grading', blank=True) # Field name made lowercase.
    numsurveyed = models.IntegerField(db_column='NumSurveyed') # Field name made lowercase.
    numenrolled = models.IntegerField(db_column='NumEnrolled') # Field name made lowercase.
    class Meta:
        db_table = u'Ratings'


class Instances(models.Model):
    id = models.IntegerField(primary_key=True)
    year = models.IntegerField(db_column='Year') # Field name made lowercase.
    quarter = models.CharField(max_length=6, db_column='Quarter') # Field name made lowercase.
    section = models.CharField(max_length=12, db_column='Section', blank=True) # Field name made lowercase.
    idinstructor = models.ForeignKey(Instructors, db_column='idInstructor') # Field name made lowercase.
    idcourses = models.ForeignKey(Courses, db_column='idCourses') # Field name made lowercase.
    idratings = models.ForeignKey(Ratings, db_column='idRatings') # Field name made lowercase.
    instructortitle = models.CharField(max_length=192, db_column='InstructorTitle') # Field name made lowercase.
    class Meta:
        db_table = u'Instances'

