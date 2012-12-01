from django.core.management.base import BaseCommand, NoArgsCommand, CommandError
import django.db
import csv
from main.models import Curriculum, Course, Section, Rating, Instructor, Meeting, Building, SectionRelation

class Command(NoArgsCommand):
	help = 'Wipes the entire database'

	def handle_noargs(self, **options):
		self.stdout.write("SectionRelations...\r\n")
		SectionRelation.objects.all().delete()

		self.stdout.write("Meeting...\r\n")
		Meeting.objects.all().delete()

		self.stdout.write("Building...\r\n")
		Building.objects.all().delete()

		self.stdout.write("Sections...\r\n")
		Section.objects.all().delete()

		self.stdout.write("Ratings...\r\n")
		Rating.objects.all().delete()

		self.stdout.write("Instructors...\r\n")
		Instructor.objects.all().delete()

		self.stdout.write("Course...\r\n")
		Course.objects.all().delete()

		self.stdout.write("Curriculum...\r\n")
		Curriculum.objects.all().delete()


