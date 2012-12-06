#

from tastypie import fields, utils
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from main.models import *


class CurriculumResource(ModelResource):
	class Meta:
		queryset = Curriculum.objects.all()
		resource_name = 'curriculum'

class CourseResource(ModelResource):
	sections = fields.ToManyField("main.api.SectionResource", 'section_set', full=True)
	curriculum = fields.ToOneField(CurriculumResource, 'idcurriculum', full=True)

	class Meta:
		queryset = Course.objects.all()
		resource_name = 'course'
		filtering = {
			'name': ALL,
			'genedreqs': ALL,
			'description': ALL,
			'comment': ALL,

		}

class InstructorResource(ModelResource):
	class Meta:
		queryset = Instructor.objects.all()
		resource_name = 'instructor'


class RatingResource(ModelResource):
	class Meta:
		queryset = Rating.objects.all()
		resource_name = 'rating'

class BuildingResource(ModelResource):
	class Meta:
		queryset = Building.objects.all()
		resource_name = 'building'

class RoomResource(ModelResource):
	building = fields.ToOneField(BuildingResource, 'idbuilding', full = True)
	class Meta:
		queryset = Room.objects.all()
		resource_name = 'room'



class MeetingTypeResource(ModelResource):
	#meetings = fields.ToManyField()
	#meetings = fields.ToManyField("main.api.MeetingResource", 'idmeetingtype', full=True)
	class Meta:
		queryset = MeetingType.objects.all()
		resource_name = 'meetingtype'

class MeetingResource(ModelResource):
	meetingtype = fields.ToOneField(MeetingTypeResource, 'idmeetingtype', full=True)
	room = fields.ToOneField(RoomResource, 'idroom', full=True)
	#section = fields.ToOneField("main.api.SectionResource", 'idSection', full=True)

	class Meta:
		queryset = Meeting.objects.all()
		resource_name = 'meeting'

class SectionResource(ModelResource):
	meetings = fields.ToManyField(MeetingResource, 'meeting_set', full=True)
	instructor = fields.ToOneField(InstructorResource, 'idinstructor', full=True, null=True)
	ratings = fields.ToOneField(RatingResource, 'idrating', full=True, null=True)
	#course = fields.ToOneField(CourseResource, 'idCourse', full=True)

	class Meta:
		queryset = Section.objects.all()
		resource_name = 'section'
		filtering = {
			'meetings': ALL_WITH_RELATIONS,
		}

