#

from tastypie import fields, utils
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from main.models import *
from django.db.models import Q


class CurriculumResource(ModelResource):
	#courses = fields.ToManyField("main.api.CourseResource", 'course_set', related_name='idcurriculum')
	class Meta:
		queryset = Curriculum.objects.all()
		resource_name = 'curriculum'

class CourseResource(ModelResource):
	sections = fields.ToManyField("main.api.SectionResource", 'section_set', full=True, related_name='idcourse')
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
			'section': ALL_WITH_RELATIONS,
			'days': ['eq',],
			'endtime': ALL,
			'open': ALL,
			'offered': ALL,
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

	    #if('ger' in filters):
	    # 	query = filters['ger']
	    #	qset = (
	    #		Q
	    #		)
		#
	    #	orm_filters.update({'custom': qset})

	    return orm_filters

	def apply_filters(self, request, applicable_filters):
	    if 'custom' in applicable_filters:
	        custom = applicable_filters.pop('custom')
	    else:
	        custom = None

	    semi_filtered = super(CourseResource, self).apply_filters(request, applicable_filters)

	    if "ger" in request.REQUEST:
	    	ger = int(request.REQUEST['ger'])
	    	semi_filtered = semi_filtered.extra(where=["GenEdReqs & %s = %s"], params=(ger, ger))

	    if "days" in request.REQUEST:
	    	d = (~int(request.REQUEST['days'])) & 255
	    	semi_filtered = semi_filtered.extra(where=["Meeting.Day & %s = 0"], params=(d), tables=['section', 'meeting'])

	    if "endtime" in request.REQUEST:
	    	endtime = int(request.REQUEST['endtime'])
	    	semi_filtered = semi_filtered.exclude(section__meeting__endtime__gt=endtime)

	    if "starttime" in request.REQUEST:
	    	starttime = int(request.REQUEST['starttime'])
	    	semi_filtered = semi_filtered.exclude(section__meeting__starttime__lt=starttime)

	    if "offered" in request.REQUEST:
	    	semi_filtered = semi_filtered.filter(section__quarter__exact ='WI', section__year='2013').exclude(section__isnull=True)

	    if "open" in request.REQUEST:
	    	semi_filtered = semi_filtered.filter(section__maxenrollment__gt=F('section__numenrolled'))



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
		filtering = {
			'building': ALL_WITH_RELATIONS,
			'name': ALL,
		}



class MeetingTypeResource(ModelResource):
	#meetings = fields.ToManyField()
	#meetings = fields.ToManyField("main.api.MeetingResource", 'idmeetingtype', full=True)
	class Meta:
		queryset = MeetingType.objects.all()
		resource_name = 'meetingtype'

class MeetingResource(ModelResource):
	meetingtype = fields.ToOneField(MeetingTypeResource, 'idmeetingtype', full=True)
	room = fields.ToOneField(RoomResource, 'idroom', full=True)
	section = fields.ToOneField("main.api.SectionResource", 'idsection')

	class Meta:
		queryset = Meeting.objects.all()
		resource_name = 'meeting'
		filtering = {
			'endtime': ALL,
			'starttime': ALL,
			'day': ALL,
			'room': ALL_WITH_RELATIONS,
		}

class SectionResource(ModelResource):
	meetings = fields.ToManyField(MeetingResource, 'meeting_set', full=True, related_name='section')
	instructor = fields.ToOneField(InstructorResource, 'idinstructor', full=True, null=True)
	ratings = fields.ToOneField(RatingResource, 'idrating', full=True, null=True)
	course = fields.ToOneField(CourseResource, 'idcourse')

	class Meta:
		queryset = Section.objects.all()
		resource_name = 'section'
		filtering = {
			'meeting': ALL_WITH_RELATIONS,
		}

