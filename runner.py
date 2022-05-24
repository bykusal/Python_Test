from main import jmeter_log_files, update_csv, remove_attribute
update_csv(21,23)
remove_attribute('outParams')
jmeter_log_files("resources/jmeter_log_files/Jmeter_log1.jtl")