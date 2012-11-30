import csv
import student


years = range(1980,2014)
quarters = ["autumn", "winter", "spring", "summer"]
#quarters = ["autumn"]

curriculums = {}


for y in years:
    for q in quarters:
        c_data = student.get_curriculum_data(y,q)
        for c in c_data['Curricula']:
        	abbr = c['CurriculumAbbreviation']
        	if abbr not in curriculums:
        		c['LastYear'] = 9999
        		curriculums[abbr] = c
        	else:
        		curriculums[abbr]['LastYear'] = y
        # check for missing data and that should signify the last year 
        abbreviations = set([c['CurriculumAbbreviation'] for c in c_data['Curricula']])
        for abbr in curriculums:
        	if abbr not in abbreviations:
        		if curriculums[abbr]['LastYear'] == 9999:
        			curriculums[abbr]['LastYear'] = y
        	#else:
        		#if curriculums[abbr]['LastYear'] != 9999:
        		#	print 'wtf %s %d-%d'%(abbr,curriculums[abbr]['LastYear'],y)


print curriculums.keys()[0]
fieldnames = curriculums[curriculums.keys()[0]]
print fieldnames

data_file = open("curriculums.csv", "wt")
csvwriter = csv.DictWriter(data_file, delimiter=",", fieldnames=fieldnames)
csvwriter.writerow(dict((fn,fn) for fn in fieldnames))
for abbr,row in curriculums.items():
	csvwriter.writerow(row)
