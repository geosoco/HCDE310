from HCDE310.settings import BASE_URL
from django import template
from main.models import Curriculum, Course, Section, Rating, Instructor

register = template.Library()

@register.simple_tag
def instructor(value, text = None):
	if value is not None:
		return '<i class="icon-user"></i><a href="%sinstructor/%d">%s</a>'%(BASE_URL, value.id, (value.name if text is None else text) )

@register.simple_tag
def curriculum(value, text = None):
	if value is not None:
		return '<i class="icon-home"></i><a href="%scurriculum/%d">%s</a>'%(BASE_URL, value.id, (value.name if text is None else text) )

@register.simple_tag
def course(value, text = None):
	if value is not None:
		return '<i class="icon-book"></i><a href="%scourse/%d">%s</a>'%(BASE_URL, value.id, (text if text is not None else (value.idcurriculum.abbreviation + ' ' + str(value.number)) ))

@register.simple_tag        
def section(value, text = None):
    if value is not None:
		return '<i class="icon-book"></i><a href="%scourse/%d">%s</a>'%(BASE_URL, value.idcourse.id, (text if text is not None else (value.idcourse.idcurriculum.abbreviation + ' ' + str(value.idcourse.number)) ))
