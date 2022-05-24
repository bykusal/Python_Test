import csv
import datetime
import json
import pytz
import xml.etree.ElementTree as ET


#************* START OF UPDATE XML DATES *****************
def increase_date_by(days):
	return datetime.datetime.now() + datetime.timedelta(days = days)

def update_csv_values(root, x, y):
	for element in root:
		if(element.tag == 'DEPART'):
			element.text = increase_date_by(x).strftime('%Y%m%d')
		elif(element.tag == 'RETURN'):
			element.text = increase_date_by(y).strftime('%Y%m%d')
		update_csv_values(element,x,y)

#main function
def update_csv(x,y):
	tree = ET.parse('resources/test_payload1.xml')
	root = tree.getroot()
	update_csv_values(root, x, y)
	output = ET.tostring(root)
	with open("output/test_payload1_output.xml", "wb") as f:
    		f.write(output)

#************* END OF UPDATE XML DATES *****************



#************* START OF DELETE JSON KEYS *****************
#recursive function
def find_keys_and_delete(json_data, x):
	if x in json_data:
		del json_data[x]
	for json_field in json_data:
		if isinstance(json_data[json_field], dict):
			find_keys_and_delete(json_data[json_field], x)

#main function
def remove_attribute(*del_data):
	f = open('resources/test_payload.json')
	data = json.load(f)
	for x in del_data:
		find_keys_and_delete(data, x)
	with open("output/test_payload_output.json", "w") as outfile:
    		json.dump(data, outfile, indent=4)
	f.close()
#************* END OF DELETE JSON KEYS *****************




#************* START OF CHECK JMETER LOGS *****************
def convert_to_utc(date_time):
	utc_datetime = datetime.datetime.utcfromtimestamp(float(date_time) / 1000.)
	utc_datetime.replace(tzinfo = pytz.timezone('UTC')).astimezone(pytz.timezone('America/Los_Angeles')).strftime('%Y-%m-%d %H:%M:%S %Z')
	return utc_datetime

def jmeter_log_files(file_path):
	log_file = open(file_path)
	csvreader = csv.reader(log_file)
	header = next(csvreader)
	index = ["timeStamp", "label", "responseCode", "responseMessage", "failureMessage"]
	for row in csvreader:
		if(not row[header.index("responseCode")] == '200'):
			row[header.index("timeStamp")] = convert_to_utc(row[header.index("timeStamp")])
			for i in index:
				print(row[header.index(i)], end = "\t ")
			print()

	log_file.close()
#************* START OF CHECK JMETER LOGS *****************