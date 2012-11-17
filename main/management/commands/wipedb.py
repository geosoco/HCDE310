from django.core.management.base import BaseCommand, NoArgsCommand, CommandError
import django.db
import csv
from main.models import Departments, Courses, Instances, Ratings, Instructors

class Command(NoArgsCommand):
	help = 'Wipes the entire database'

	def handle_noargs(self, **options):
		self.stdout.write("Instances...\r\n")
		Instances.objects.all().delete()

		self.stdout.write("Ratings...\r\n")
		Ratings.objects.all().delete()

		self.stdout.write("Instructors...\r\n")
		Instructors.objects.all().delete()

		self.stdout.write("Courses...\r\n")
		Courses.objects.all().delete()

		self.stdout.write("Departments...\r\n")
		Departments.objects.all().delete()


