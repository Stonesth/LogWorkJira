from Tools import tools_v000 as tools
from Jira import jira as j
from MyHours import myhours as m
import os
from os.path import dirname
import time
from datetime import datetime, timedelta
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# -11 for the name of this project LogWorkJira
save_path = os.path.dirname(os.path.abspath("__file__"))
propertiesFolder_path = save_path + "/"+ "Properties"

j.jira = tools.readProperty(propertiesFolder_path, 'LogWorkJira', 'jira=')

delay_properties = 10

# Open Browser
tools.openBrowserChrome()

# MyHours part
m.connectToMyTimeTrack()

print ("Test if we need to wait the page of the user / password")
if tools.waitLoadingPageByID2(5, 'email-label') :
    # show_popup()
    # print ("Need to wait the page of the password")
    # tools.waitLoadingPageByID2(10, 'email-label')
    # time.sleep(30)
    m.enterCredentials2()

time.sleep(1)

# Force refresh the page
tools.driver.refresh()

# Need to start the task Admin
tools.waitLoadingPageByXPATH2(delay_properties, '//*[@id="add-task-button"]')
add_task_button = tools.driver.find_element(By.XPATH, '//*[@id="add-task-button"]')
add_task_button.click()
time.sleep(1)

# Need to update the task with information from Admin
# Click on the edit button
tools.waitLoadingPageByXPATH2(delay_properties, '//*[@id="group-no-project-no-task-bulk-edit"]')
add_task_button = tools.driver.find_element(By.XPATH, '//*[@id="group-no-project-no-task-bulk-edit"]')
add_task_button.click()

# Fill in the Projet
tools.waitLoadingPageByXPATH2(delay_properties, '//*[@id="bulk-project-autocomplete"]')
switchToWeekTrackBtn = tools.driver.find_element(By.XPATH, '//*[@id="bulk-project-autocomplete"]')
switchToWeekTrackBtn.send_keys("Business operations (non project / service related tasks)")
switchToWeekTrackBtn.send_keys(Keys.DOWN)
switchToWeekTrackBtn.send_keys(Keys.ENTER)


tools.waitLoadingPageByXPATH2(delay_properties, '//*[@id="bulk-task-name"]')
switchToWeekTrackBtn = tools.driver.find_element(By.XPATH, '//*[@id="bulk-task-name"]')
switchToWeekTrackBtn.click()
switchToWeekTrackBtn.send_keys("Mail + administration")
switchToWeekTrackBtn.send_keys(Keys.ENTER)

tools.waitLoadingPageByXPATH2(delay_properties, '//*[@id="bulk-notes"]')
switchToWeekTrackBtn = tools.driver.find_element(By.XPATH, '//*[@id="bulk-notes"]')
switchToWeekTrackBtn.click()
switchToWeekTrackBtn.send_keys("Mail + administration")
switchToWeekTrackBtn.send_keys(Keys.ENTER)

tools.waitLoadingPageByXPATH2(delay_properties, '//*[@id="bulk-tags"]')
switchToWeekTrackBtn = tools.driver.find_element(By.XPATH, '//*[@id="bulk-tags"]')
switchToWeekTrackBtn.click()
switchToWeekTrackBtn.send_keys("Mail + administration")
switchToWeekTrackBtn.send_keys(Keys.ENTER)

time.sleep(1)

# go to the research page
# https://timetrackingwindsurf.web.app/task-search
tools.driver.get('https://timetrackingwindsurf.web.app/task-search')

# Search the input task where we can enter the jira ticket (j.jira)
# //*[@id="task-search-input"]
tools.waitLoadingPageByXPATH2(delay_properties, '//*[@id="task-search-input"]')
task_search_input = tools.driver.find_element(By.XPATH, '//*[@id="task-search-input"]')
# Need to select all the current text in the input
task_search_input.send_keys(Keys.CONTROL + "a")
task_search_input.send_keys(j.jira)
task_search_input.send_keys(Keys.RETURN)

# Localiser le tableau
tools.waitLoadingPageByXPATH2(delay_properties, '//*[@id="search-results-table"]')
table = tools.driver.find_element(By.XPATH, '//*[@id="search-results-table"]')

# Parcourir les lignes du tableau
rows = table.find_elements(By.XPATH, './/tbody/tr')


# Need to store data 
array = [ ]

# Extraire les informations de chaque ligne
for row in rows:
    date = row.find_element(By.XPATH, './/td[contains(@id, "date-cell")]').text
    duration = row.find_element(By.XPATH, './/td[contains(@id, "duration-cell")]').text
    print(f"Date: {date}, Duration: {duration}")

    # I would like to save all those information in arrays
    array.append([date, duration])

print(array)

# Need to go to the Jira
j.connectToJira(j.jira)

# Need to add all the time for this JIRA
time_all = timedelta(hours=0, minutes=0, seconds=0)

# Print the array with all the info for this JIRA
print("----------------- Infos -----------------  ")

for r in array:
    print( ' '.join([str(x) for x in r] ) )

    # Convertir la chaîne de temps en objet timedelta
    duration_str = r[1]
    time_parts = duration_str.split()
    time_kwargs = {}
    for part in time_parts:
        if 'h' in part:
            time_kwargs['hours'] = int(part.replace('h', ''))
        elif 'm' in part:
            time_kwargs['minutes'] = int(part.replace('m', ''))
        elif 's' in part:
            time_kwargs['seconds'] = int(part.replace('s', ''))

    time_object = timedelta(**time_kwargs)

    # Extraire les heures, minutes et secondes de l'objet timedelta
    total_seconds = int(time_object.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    print(f"{hours}h {minutes}m {seconds}s")

    # Need to add the time past to this JIRA
    time_all += time_object

    # Click on the more button to add the hours 
    tools.waitLoadingPageByXPATH2(10, '//*[@id="opsbar-operations_more"]')
    more_button = tools.driver.find_element(By.XPATH, '//*[@id="opsbar-operations_more"]')
    more_button.click()

    # Click on the log swork button to add the hours 
    tools.waitLoadingPageByXPATH2(10, '//*[@id="log-work"]/a/span')
    log_work_button = tools.driver.find_element(By.XPATH, '//*[@id="log-work"]/a/span')
    log_work_button.click()

    # Introduce into the input of Time Spent the time for this day
    tools.waitLoadingPageByXPATH2(10, '//*[@id="log-work-time-logged"]')
    log_work_time_logged = tools.driver.find_element(By.XPATH, '//*[@id="log-work-time-logged"]')
    if (hours > 0) :
        log_work_time_logged.send_keys(str(hours) + 'h ')
    if (seconds > 29) :
        log_work_time_logged.send_keys(str(minutes + 1) + 'm ')
    else :
        if (minutes > 0) :
            log_work_time_logged.send_keys(str(minutes) + 'm ')
        else :
            log_work_time_logged.send_keys(str(minutes + 1) + 'm ')

    # Introduce into the input the date
    tools.waitLoadingPageByXPATH2(10, '//*[@id="log-work-date-logged-date-picker"]')
    log_work_date_logged_date_picker = tools.driver.find_element(By.XPATH, '//*[@id="log-work-date-logged-date-picker"]')
    log_work_date_logged_date_picker.send_keys(Keys.CONTROL, 'a')

    date_object = datetime.strptime(r[0], '%d/%m/%Y')

    # Month
    month_number = str(date_object.month)
    datetime_object_month = datetime.strptime(month_number, "%m")
    month_name = datetime_object_month.strftime("%b")
    
    # Year
    year_2_digit = date_object.year % 100
    print(year_2_digit)

    log_work_date_logged_date_picker.send_keys(str(date_object.day) + '/' +month_name+ '/'+str(year_2_digit)+' 10:00 PM')

    tools.waitLoadingPageByXPATH2(10, '//*[@id="log-work-submit"]')
    log_button = tools.driver.find_element(By.XPATH, '//*[@id="log-work-submit"]')
    log_button.click()

    
    
print(f"Total time: {time_all}")

print(str(time_all))
timedelta_8 = timedelta(hours=8, minutes=0, seconds=0)

time_all_sec = time_all.total_seconds()
timedelta_8_sec = timedelta_8.total_seconds()
total_sec = time_all_sec / timedelta_8_sec
print(str(round(total_sec, 3)))

# Need to update the JIRA for the Story Points only if this one is not filled
if tools.waitLoadingPageByXPATH2(delay_properties, '//*[@id="customfield_10004-val"]') :
    print ("There is already a Story Point => don't update the Story Point ")
else : 
    # click on the edit button
    tools.waitLoadingPageByXPATH2(delay_properties, '//*[@id="opsbar-edit-issue_container"]')
    edit_button = tools.driver.find_element(By.XPATH, '//*[@id="opsbar-edit-issue_container"]')
    edit_button.click()

    # click in the input field Story Points
    tools.waitLoadingPageByXPATH2(delay_properties, '//*[@id="customfield_10004"]')
    inputStoryPoint = tools.driver.find_element(By.XPATH, '//*[@id="customfield_10004"]')
    time.sleep(1)
    inputStoryPoint.click()
    time.sleep(1)
    inputStoryPoint.send_keys(str(round(total_sec, 3)))

    # cllick in the update button
    tools.waitLoadingPageByXPATH2(delay_properties, '//*[@id="edit-issue-submit"]')
    update_button = tools.driver.find_element(By.XPATH, '//*[@id="edit-issue-submit"]')
    update_button.click()
    
    time.sleep(delay_properties)

# Need to place the JIRA in DONE
tools.waitLoadingPageByXPATH2(delay_properties, '//*[@id="opsbar-transitions_more"]')
log_button = tools.driver.find_element(By.XPATH, '//*[@id="opsbar-transitions_more"]')
log_button.click()

time.sleep(2)
tools.waitLoadingPageByXPATH2(delay_properties, '//*[@id="action_id_31"]/a/div/div[1]')
log_button = tools.driver.find_element(By.XPATH, '//*[@id="action_id_31"]/a/div/div[1]')
time.sleep(1)
log_button.click()

# Actual Story Points
time.sleep(1)
tools.waitLoadingPageByXPATH2(delay_properties, '//*[@id="customfield_13603"]')
customfield_13603 = tools.driver.find_element(By.XPATH, '//*[@id="customfield_13603"]')
customfield_13603.click()
customfield_13603.send_keys(str(round(total_sec, 3)))

# Click on the done button
tools.waitLoadingPageByXPATH2(delay_properties, '//*[@id="issue-workflow-transition-submit"]')
Done_button = tools.driver.find_element(By.XPATH, '//*[@id="issue-workflow-transition-submit"]')
Done_button.click()

# Close Browser
tools.closeBrowserChrome()