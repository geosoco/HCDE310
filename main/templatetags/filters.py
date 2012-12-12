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

@register.simple_tag
def day(value, text = None):
    if value.day == 255:
        return 'TBD'
    else: 
        day_chars = ['M', 'Tu', 'W', 'Th', 'F', 'Sa']
        str = ''
        for d in range(0, len(day_chars)):
           bit = 2**d
           if value.day & bit == bit:
               str += day_chars[d]
           else:
               str += ' '
        return str
    
@register.simple_tag
def credittype(value, text = None):
    if (value.genedreqs == 1):
        return '<span class="label label-info">NW</span>'
    elif (value.genedreqs == 2):
        return '<span class="label label-info">VLPA</span>'
    elif (value.genedreqs == 4):
        return '<span class="label label-info">I&amp;S</span>'
    elif (value.genedreqs == 8):
        return '<span class="label label-info">W</span>'
    elif (value.genedreqs == 16):
        return '<span class="label label-info">EC</span>'
    elif (value.genedreqs == 32):
        return '<span class="label label-info">QSR</span>'
    else:
        return ''

@register.simple_tag
def status(value, text = None):
    if (value.numenrolled < value.maxenrollment):
        return '<span class="label label-success">Open</span>'
    else:
        return '<span class="label label-important">Closed</span>'
        
@register.simple_tag
def buildingmap(value, text = None):
    buildings = {'ACC':'31', 'AER':'33', 'ALB':'34', 'AND':'35', 'ARC':'36', 'ART':'37', 'ATG':'38', 'BAG':'40', 'BGH':'45', 'BHQ':'', 'BIOE':'255', 'BLD':'44', 'BMM':'51', 'BNS':'43', 'BRY':'50', 'CDH':'64', 'CHB':'58', 'CHD':'', 'CHL':'59', 'CLK':'61', 'CMA':'57', 'CMU':'63', 'CNH':'53', 'CSE':'183', 'CSH':'65', 'DEM':'2269','DEN':'69', 'DRC':'272', 'DSC':'11', 'ECC':'76', 'EDP':'71', 'EEB':'72', 'EGA':'73', 'EGL':'70', 'ELB':'74', 'EXED':'41', 'FIS':'78', 'FLK':'81', 'FSH':'80', 'FTR':'79', 'GA1':'96', 'GA2':'97', 'GA3':'98', 'GDR':'89', 'GLD':'90', 'GNOM':'256', 'GRB':'88', 'GTH':'100', 'GUG':'95', 'GWN':'91', 'HAG':'107', 'HCK':'108', 'HGT':'102', 'HHL':'105', 'HLL':'103', 'HND':'101', 'HPT':'109', 'HSA':'140', 'HSB':'142', 'HSD':'145', 'HSE':'153', 'HSI':'150', 'HSJ':'151', 'HSK':'77', 'HSR':'', 'HST':'153', 'HUB':'231', 'HUT':'110', 'ICH':'68', 'ICT':'9', 'IMA':'113', 'JHA':'', 'JHN':'116', 'KIN':'118', 'KNE':'117', 'LA1':'135', 'LA2':'135', 'LA3':'135', 'LAW':'260', 'LEW':'136', 'LOW':'137', 'MAR':'155', 'MEB':'160', 'MGH':'156', 'MKZ':'139', 'MLR':'162', 'MNY':'159', 'MOR':'163', 'MSB':'154', 'MUE':'165', 'MUS':'166', 'NRB':'164', 'OBS':'233', 'OCE':'175', 'OCN':'174', 'OTB':'178', 'OUG':'179', 'PAA':'185', 'PAB':'186', 'PAT':'187', 'PAR':'182', 'PCAR':'180', 'PDL':'181', 'PHT':'199', 'PLT':'189', 'ATG':'38', 'RAI':'203', 'ROB':'205', 'RTB':'39', 'RVC':'206', 'SAV':'211', 'SGS':'12', 'SIG':'214', 'SMI':'215', 'SMZ':'212', 'SUZ':'232', 'SWS':'216', 'TER':'120', 'TGB':'93', 'THO':'234', 'UMC':'252', 'UME':'252', 'UMSP':'244', 'WCL':'262', 'WFS':'264', 'WIL':'259'}
    if value.upper() in buildings:
        return '<iframe width="450" height="375" src="http://uw.edu/maps/embed/?place=' + buildings[value.upper()] + '" frameborder="0"></iframe>'
    else:
        return ''

@register.simple_tag
def timecorrect(value):
    if value > 1300:
        result = timehelp(value - 1200)
        return result
    else:
        return timehelp(value)
        
@register.simple_tag
def calendarhelper(value, letter, time):
    dayconvert = dayhelper(value)
    if (value.starttime <= time <= value.endtime) and (letter in dayconvert):
#        if (value.day % 2 == 1) and (letter is 'M'):
        return '<td id="calendar"></td>'
        #else:
            #return '<td></td>'
    else:
        return '<td></td>'

def dayhelper(value, text = None):
    if value.day == 255:
        return 'TBD'
    else: 
        day_chars = ['M', 'Tu', 'W', 'Th', 'F', 'Sa']
        str = ''
        for d in range(0, len(day_chars)):
           bit = 2**d
           if value.day & bit == bit:
               str += day_chars[d]
           else:
               str += ' '
        return str
       
def timehelp(value, text = None):
    timestr = '' + str(value / 100) + ':' + str(value % 100)
    return timestr       