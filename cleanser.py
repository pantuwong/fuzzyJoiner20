from sys import argv
from string import maketrans   # Required to call maketrans function.
#first use a set of things we don't want in the final output
name_reject_set = frozenset(["father of", "(", "author of"])
company_reject_set = frozenset(["("])
nametester = 0
maxlen = 0
def test_100_names(data):
	global nametester
	nametester += 1
	if nametester > 100:
		return False
	else:
		return good_name_data(data)
#test whether or not a company name should be used
def good_company_data(data):
	if data.startswith("<http://dbpedia.org/resource"):
		return False
	#used https://www.tutorialspoint.com/python/string_translate.htm
	#change if we want to preserve any of these things
	intab = "\n"
	outtab = " "
	trantab = maketrans(intab, outtab)
	data.translate(trantab)
	try:
		data.encode('utf-8')
	except UnicodeDecodeError:
		return False
	data = data.lower()
	for item in company_reject_set:
		if item in data:
			return False
	return True
def good_name_data(data):
	#used https://www.tutorialspoint.com/python/string_translate.htm
	#change if we want to preserve any of these things
	intab = "\n"
	outtab = " "
	trantab = maketrans(intab, outtab)
	data.translate(trantab)
	try:
		data.encode('utf-8')
	except UnicodeDecodeError:
		return False
	data = data.lower()
	for item in name_reject_set:
		if item in data:
			return False
	return True
#cleanses the data and returns only good data
#if we cannot get 2 peices of good data returns the empty string
def cleanseData(dataToCleanse, cleansing_function):
	ret = []
	global maxlen
	name_array = dataToCleanse.split("|")
	for part in name_array:
		if len(ret) >= 2:
			break
		if cleansing_function(part):
			if part[-1:] == "\n":
				part = part[:-1]
			if len(part) > maxlen:
				maxlen = len(part)
			ret.append(part)
	if len(ret) == 2:
		return "|".join(ret)
	return ""
#parses input file and writes an output
def parse_file(input_file, output_file, parsing_function):
	lines = input_file.readlines()
	for line in lines:
		newline = cleanseData(line, parsing_function)
		if newline != "":
			output_file.write(newline)
			output_file.write('\n')

if len(argv) >= 3:
	nametester = 0
	parsing_function = good_name_data
	function_dictionary = {"name":good_name_data, "company":good_company_data, "test100":test_100_names}
	if len(argv) == 4:
		parsing_function = function_dictionary[argv[3]]
	input_file = open(argv[1])
	output_file = open(argv[2], "w")
	parse_file(input_file, output_file,parsing_function)
	input_file.close()
	output_file.close()
	print maxlen

