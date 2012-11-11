# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class Courses(models.Model):
    id = models.IntegerField(primary_key=True)
    abbreviation = models.CharField(max_length=30, db_column='Abbreviation') # Field name made lowercase.
    number = models.IntegerField(db_column='Number') # Field name made lowercase.
    name = models.CharField(max_length=384, db_column='Name') # Field name made lowercase.
    comment = models.CharField(max_length=768, db_column='Comment', blank=True) # Field name made lowercase.
    description = models.CharField(max_length=6144, db_column='Description', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'Courses'

class Instructor(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=192, db_column='Name') # Field name made lowercase.
    title = models.CharField(max_length=192, db_column='Title', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'Instructor'

class Instances(models.Model):
    id = models.IntegerField(primary_key=True)
    idcourse = models.IntegerField(db_column='idCourse') # Field name made lowercase.
    idinstructor = models.IntegerField(db_column='idInstructor') # Field name made lowercase.
    section = models.CharField(max_length=12, db_column='Section', blank=True) # Field name made lowercase.
    instructor = models.ForeignKey(Instructor, db_column='Instructor_id') # Field name made lowercase.
    courses = models.ForeignKey(Courses, db_column='Courses_id') # Field name made lowercase.
    courserating = models.DecimalField(decimal_places=0, null=True, max_digits=9, db_column='CourseRating', blank=True) # Field name made lowercase.
    textbookrating = models.DecimalField(decimal_places=0, null=True, max_digits=9, db_column='TextbookRating', blank=True) # Field name made lowercase.
    instructorrating = models.DecimalField(decimal_places=0, null=True, max_digits=9, db_column='InstructorRating', blank=True) # Field name made lowercase.
    instructorcontributionrating = models.DecimalField(decimal_places=0, null=True, max_digits=9, db_column='InstructorContributionRating', blank=True) # Field name made lowercase.
    instructorinterestrating = models.DecimalField(decimal_places=0, null=True, max_digits=9, db_column='InstructorInterestRating', blank=True) # Field name made lowercase.
    amountlearnedrating = models.DecimalField(decimal_places=0, null=True, max_digits=9, db_column='AmountLearnedRating', blank=True) # Field name made lowercase.
    homeworkusefulnessrating = models.DecimalField(decimal_places=0, null=True, max_digits=9, db_column='HomeworkUsefulnessRating', blank=True) # Field name made lowercase.
    ratingsurveyed = models.IntegerField(null=True, db_column='RatingSurveyed', blank=True) # Field name made lowercase.
    ratingenrolled = models.IntegerField(null=True, db_column='RatingEnrolled', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'Instances'