from django.core.management.base import BaseCommand, CommandError
import csv
import main.models


class Command(BaseCommand):
	args = '<filename>'
	help = 'Closes the specified poll for voting.\nUsage: import_evals %s'

	courses = {}
	instructors = {}
	coursetypes = {}

	def handle(self, *args, **options):
		if args is None or len(args) == 0:
			raise CommandError('csv  "%s" does not exist' % poll_id)
		#print "opening %s"%args[0]
		self.stdout.write('opening: %s\n'%args[0])
		csvreader = csv.reader(args[0], delimeter=',', quotechar='"')
		for row in csvreader:



