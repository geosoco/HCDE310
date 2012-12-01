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
    firstyear = models.IntegerField(db_column='FirstYear') # Field name made lowercase.
    lastyear = models.IntegerField(db_column='LastYear') # Field name made lowercase.
    url = models.CharField(max_length=384, db_column='Url', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'Departments'

    def __str__(self):
        return "%s (%s)"%(self.name,self.abbreviation)


class Courses(models.Model):
    NW = 1
    VLPA = 2
    IS = 4
    W = 8
    EC = 16
    QSR = 32

    #NW = 'N'
    #VLPA = 'V'
    #IS = 'I'
    #W = 'W'
    #EC = 'E'
    #QSR = 'Q'
    #GEN_ED_REQ_CHOICES = (
    #    (NW, 'NW'),
    #    (VLPA, 'VLPA'),
    #   (IS, 'I&S'),
    #    (W, 'W'),
    #    (QSR, 'QSR'),
    #    (EC, 'EC')
    #)

    id = models.AutoField(primary_key=True)
    number = models.IntegerField(db_column='Number') # Field name made lowercase.
    name = models.CharField(max_length=384, db_column='Name', blank=True) # Field name made lowercase.
    comment = models.CharField(max_length=768, db_column='Comment', blank=True) # Field name made lowercase.
    description = models.CharField(max_length=6144, db_column='Description', blank=True) # Field name made lowercase.
    iddepartment = models.ForeignKey(Departments, db_column='idDepartment') # Field name made lowercase.
    genedreqs = models.IntegerField(db_column='GenEdReqs', blank=True)
    firstyear = models.IntegerField(null=True, db_column='FirstYear', blank=True) # Field name made lowercase.
    firstquarter = models.CharField(max_length=6, db_column='FirstQuarter', blank=True) # Field name made lowercase.
    lastyear = models.IntegerField(null=True, db_column='LastYear', blank=True) # Field name made lowercase.
    lastquarter = models.CharField(max_length=6, db_column='LastQuarter', blank=True) # Field name made lowercase.
    mincredits = models.IntegerField(null=True, db_column='MinCredits', blank=True) # Field name made lowercase.
    maxcredits = models.IntegerField(null=True, db_column='MaxCredits', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'Courses'

    def convertGenEdReqsToInt(self, nw, vlpa, iands, w, ec, qsr):
        val = 0
        val |= self.NW if nw.lower() == 'true' else 0
        val |= self.VLPA if vlpa.lower() == 'true' else 0
        val |= self.IS if iands.lower() == 'true' else 0
        val |= self.W if w.lower() == 'true' else 0
        val |= self.EC if ec.lower() == 'true' else 0
        val |= self.QSR if qsr.lower() == 'true' else 0
        return val

    def __str__(self):
        return "%s %d (%s)"%(self.name,self.abbreviation)        

class Instructors(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=192, db_column='Name') # Field name made lowercase.
    class Meta:
        db_table = u'Instructors'        

    def __str__(self):
        return self.name


class Ratings(models.Model):
    id = models.AutoField(primary_key=True)
    coursewhole = models.DecimalField(decimal_places=4, null=True, max_digits=10, db_column='CourseWhole', blank=True) # Field name made lowercase.
    coursecontent = models.DecimalField(decimal_places=4, null=True, max_digits=10, db_column='CourseContent', blank=True) # Field name made lowercase.
    instructorcontribution = models.DecimalField(decimal_places=4, null=True, max_digits=10, db_column='InstructorContribution', blank=True) # Field name made lowercase.
    instructorinterest = models.DecimalField(decimal_places=4, null=True, max_digits=10, db_column='InstructorInterest', blank=True) # Field name made lowercase.
    instructoreffectiveness = models.DecimalField(decimal_places=4, null=True, max_digits=10, db_column='InstructorEffectiveness', blank=True) # Field name made lowercase.
    amountlearned = models.DecimalField(decimal_places=4, null=True, max_digits=10, db_column='AmountLearned', blank=True) # Field name made lowercase.
    grading = models.DecimalField(decimal_places=4, null=True, max_digits=10, db_column='Grading', blank=True) # Field name made lowercase.
    numsurveyed = models.IntegerField(db_column='NumSurveyed') # Field name made lowercase.
    numenrolled = models.IntegerField(db_column='NumEnrolled') # Field name made lowercase.
    class Meta:
        db_table = u'Ratings'


class Instances(models.Model):
    id = models.AutoField(primary_key=True)
    quarter = models.CharField(max_length=6, db_column='Quarter') # Field name made lowercase.
    section = models.CharField(max_length=12, db_column='Section', blank=True) # Field name made lowercase.
    idinstructor = models.ForeignKey(Instructors, db_column='idInstructor') # Field name made lowercase.
    idcourses = models.ForeignKey(Courses, db_column='idCourses') # Field name made lowercase.
    idratings = models.ForeignKey(Ratings, db_column='idRatings') # Field name made lowercase.
    instructortitle = models.CharField(max_length=192, db_column='InstructorTitle') # Field name made lowercase.
    year = models.IntegerField(db_column='Year') # Field name made lowercase.
    numenrolled = models.IntegerField(null=True, db_column='NumEnrolled', blank=True) # Field name made lowercase.
    maxenrollment = models.IntegerField(null=True, db_column='MaxEnrollment', blank=True) # Field name made lowercase.
    classwebsite = models.CharField(max_length=384, db_column='ClassWebsite', blank=True) # Field name made lowercase.
    sln = models.IntegerField(null=True, db_column='SLN', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'Instances'

class Meetings(models.Model):
    id = models.AutoField(primary_key=True)
    day = models.IntegerField(null=True, db_column='Day', blank=True) # Field name made lowercase.
    starttime = models.IntegerField(null=True, db_column='StartTime', blank=True) # Field name made lowercase.
    endtime = models.IntegerField(null=True, db_column='EndTime', blank=True) # Field name made lowercase.
    meetingtype = models.IntegerField(null=True, db_column='Type', blank=True) # Field name made lowercase.
    idinstance = models.ForeignKey(Instances, db_column='idInstance') # Field name made lowercase.
    building = models.CharField(max_length=24, db_column='Building', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'Meetings'


class SectionRelations(models.Model):
    id = models.AutoField(primary_key=True)
    idinstance = models.ForeignKey(Instances, db_column='idInstance', related_name='sectionrelation_instance') # Field name made lowercase.
    idparent = models.ForeignKey(Instances, db_column='idParent', related_name='sectionrelation_parent') # Field name made lowercase.
    class Meta:
        db_table = u'SectionRelations'

