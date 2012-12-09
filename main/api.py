#

from tastypie import fields, utils
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from main.models import *
from django.db.models import Q


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
			'query': ['icontains',],
			'days': ['eq',],
			'ger': ['eq',],
		}

	def build_filters(self, filters=None):
	    if filters is None:
	        filters = {}
	    orm_filters = super(CourseResource, self).build_filters(filters)

	    if('query' in filters):
	        query = filters['query']
	        qset = (
	                Q(name__icontains=query) |
	                Q(description__icontains=query) |
	                Q(idcurriculum__abbreviation__icontains=query)
	                )
	        orm_filters.update({'custom': qset})

	    if('ger' in filters):
	    	query = filters['ger']
	    	qset = (
	    		)

	    	orm_filters.extend({'custom': qset})

	    return orm_filters

	def apply_filters(self, request, applicable_filters):
	    if 'custom' in applicable_filters:
	        custom = applicable_filters.pop('custom')
	    else:
	        custom = None

	    semi_filtered = super(CourseResource, self).apply_filters(request, applicable_filters)

	    return semi_filtered.filter(custom) if custom else semi_filtered


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

