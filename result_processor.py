import sys
import re
import dateutil.parser
from datetime import timedelta

CHROME_PATTERN = re.compile('VM\d+:\d+ (.*)')

def preprocess_browser_output(output_as_text):
	lines = output_as_text.split('\n')
	for i in range(0, len(lines)):
		try:
			lines[i] = re.match(CHROME_PATTERN, lines[i]).groups()[0]
		except AttributeError:
			pass
		lines[i] = lines[i].split(': ')
		lines[i][1] = dateutil.parser.parse(lines[i][1])
	return lines

def gather_entries(processed_list):
	result = dict()
	for entry in processed_list:
		if entry[0] in result.keys():
			result[entry[0]].append([entry[1], entry[2]])
		else:
			result[entry[0]] = [[entry[1], entry[2]]]
	return result

def get_durations(entries):
	online_periods = []
	last_time = None
	last_status = None
	for entry in entries:
		if entry[1] == 'true':
			last_time = entry[0]
		elif entry[1] == 'false' and last_status == 'true':
			online_periods.append((entry[0] - last_time).seconds)
		last_status = entry[1]
	return online_periods

def get_average_duration(entries):
	return sum(entries) / len(entries)

def main(file_name):
	with open(file_name) as output_file:
		output_as_text = output_file.read()
		processed_list = preprocess_browser_output(output_as_text)
		processed_list = gather_entries(processed_list)
		for user in processed_list.keys():
			durations = get_durations(processed_list[user])
			durations_str = [":".join(map(str, divmod(x, 60))) for x in durations]
			average = get_average_duration(durations)
			average_str = ":".join(map(str, divmod(average, 60)))
			print user, 'timespans:', durations_str
			print user, 'average:', average_str

if __name__ == '__main__':
	if len(sys.argv) > 1:
		main(sys.argv[1])
	else:
		raise ValueError("Filename missing")