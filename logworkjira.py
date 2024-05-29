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

# Example of used
# user_text = tools.readProperty(propertiesFolder_path, 'LogWorkJira', 'user_text=')
j.jira = tools.readProperty(propertiesFolder_path, 'LogWorkJira', 'jira=')
j.userInsim = tools.readProperty(propertiesFolder_path, 'LogWorkJira', 'userInsim=')

delay_properties = 10

# Open Browser
tools.openBrowserChrome()

# # Go to the jira to know when the jira was created
j.connectToJiraInsim(j.jira, j.userInsim)
j.recoverJiraInformation()

# # Open MyHours
m.connectToMyHours()
# Enter credentilas into the loading screen
m.enterCredentials()

# Need to go to the date of the Jira was created

# Select the date in the select button

# tools.waitLoadingPageByXPATH2(20, '//*[@id="selectDayTrackButton"]')     
# selectDayTrackButton = tools.driver.find_element(By.XPATH, '//*[@id="selectDayTrackButton"]')
tools.waitLoadingPageByXPATH2(20, '/html/body/mh-root/div/div/mh-large-layout/div/ng-component/mh-track-navigation-bar/div/div[1]/div[1]/mh-track-date-picker/div/sds-date-picker/div[1]/button[2]/div/div[2]/span')
selectDayTrackButton = tools.driver.find_element(By.XPATH, '/html/body/mh-root/div/div/mh-large-layout/div/ng-component/mh-track-navigation-bar/div/div[1]/div[1]/mh-track-date-picker/div/sds-date-picker/div[1]/button[2]/div/div[2]/span')
selectDayTrackButton.click()   
time.sleep(1) 

# # Translate the date (Creation of this JIRA) retrieved in the Jira
j.created_val = j.created_val.replace('+0200', '')
j.created_val = j.created_val.replace('+0100', '')
datetime_object = datetime.strptime(j.created_val, '%Y-%m-%dT%H:%M:%S')
print(j.created_val)

# sub 1923 because 2024 = 103
# sub 1922 because 2023 = 102
# sub 1921 because 2022 = 101
year_to_search = str(datetime_object.year) 
print('year_to_search = ' + year_to_search)
# # Select the year
# tools.waitLoadingPageByXPATH2(10, '//*[@id="AppWrapper"]/div[3]/div[2]/div[1]/table/thead/tr[1]/th[2]/select[2]')     
# AppWrapper_year = tools.driver.find_element(By.XPATH, '//*[@id="AppWrapper"]/div[3]/div[2]/div[1]/table/thead/tr[1]/th[2]/select[2]/option['+year_to_search+']')
# AppWrapper_year.click()   
# time.sleep(1)  

# Select the month
month_to_search = str(datetime_object.month)
print('month_to_search = ' + month_to_search)
# tools.waitLoadingPageByXPATH2(10, '//*[@id="AppWrapper"]/div[3]/div[2]/div[1]/table/thead/tr[1]/th[2]/select[1]')     
# AppWrapper_month = tools.driver.find_element(By.XPATH, '//*[@id="AppWrapper"]/div[3]/div[2]/div[1]/table/thead/tr[1]/th[2]/select[1]/option['+month_to_search+']')
# AppWrapper_month.click() 
# time.sleep(1)  

# Select the day
day_to_search = str(datetime_object.day)
print('day_to_search = ' + day_to_search)


print(j.created_val)
tools.waitLoadingPageByXPATH2(10, '//*[@id="date-inputs"]/div/dx-date-box/div/div/div[1]/input') 
time.sleep(1)  
date_input = tools.driver.find_element(By.XPATH, '//*[@id="date-inputs"]/div/dx-date-box/div/div/div[1]/input')
time.sleep(1)  
date_input.send_keys(day_to_search)
# time.sleep(1)  
date_input.send_keys(month_to_search)
# time.sleep(1)
date_input.send_keys(year_to_search)
# time.sleep(1)
date_input.send_keys(Keys.RETURN)

# Send the key ESC
date_input.send_keys(Keys.ESCAPE)

# for tr_n in range(1, 7):

#     for td_n in range(1, 8):
#         # print (str(tools.driver.find_element(By.XPATH, '//*[@id="AppWrapper"]/div[3]/div[2]/div[1]/table/tbody/tr[' + str(tr_n) + ']/td[' + str(td_n) + ']').text.encode('utf-8').decode()))
#         if (day_to_search == str(tools.driver.find_element(By.XPATH, '//*[@id="AppWrapper"]/div[3]/div[2]/div[1]/table/tbody/tr[' + str(tr_n) + ']/td[' + str(td_n) + ']').text.encode('utf-8').decode())) :
#             AppWrapper_day = tools.driver.find_element(By.XPATH, '//*[@id="AppWrapper"]/div[3]/div[2]/div[1]/table/tbody/tr[' + str(tr_n) + ']/td[' + str(td_n) + ']')
#             AppWrapper_day.click()  
#             break    


# # Need to wait the load of the Total of the day
# tools.waitLoadingPageByXPATH2(5, '//*[@id="trackPage"]/div[5]/div/div[10]/span')


# Need to store data 
array = [ ]



# Click on the button Next until we arrived of Today
while True :
    # Click on the button Next 
    # print("date selected = " + tools.driver.find_elements(By.XPATH, '//*[@id="datePickerText"]/span[1]')[0].text.encode('utf-8').decode())
    
    print("date selected = " + tools.driver.find_elements(By.XPATH, '/html/body/mh-root/div/div/mh-large-layout/div/ng-component/mh-track-navigation-bar/div/div[1]/div[1]/mh-track-date-picker/div/sds-date-picker/div[1]/button[2]/div/div[2]/span')[0].text.encode('utf-8').decode())
    

    # try to find if the date selected is today
    # eg : Wed, 22 May (Today) 
    # Try to find if in this date there is the word (Today)
    if "(Today)" in tools.driver.find_elements(By.XPATH, '/html/body/mh-root/div/div/mh-large-layout/div/ng-component/mh-track-navigation-bar/div/div[1]/div[1]/mh-track-date-picker/div/sds-date-picker/div[1]/button[2]/div/div[2]/span')[0].text.encode('utf-8').decode(): 
        time.sleep(1) 
        break

    # if (tools.driver.find_elements(By.XPATH, '/html/body/mh-root/div/div/mh-large-layout/div/ng-component/mh-track-navigation-bar/div/div[1]/div[1]/mh-track-date-picker/div/sds-date-picker/div[1]/button[2]/div/div[2]/span')[0].text.encode('utf-8').decode() == '(Today)') :
    #     time.sleep(1)
    #     break
    
    time.sleep(2)
    
    # Try to find if the JIRA is present or not
    # Need to know how much row there is in this day
    # The row is difened like this : <mh-log-item _ngcontent-qjd-c211="" _nghost-qjd-c210="">
    # how I can find the count of this row on this ellement /html/body/mh-root/div/div/mh-large-layout/div/ng-component/mh-log-list/div?
    count_of_divs = len(tools.driver.find_elements(By.XPATH, '/html/body/mh-root/div/div/mh-large-layout/div/ng-component/mh-log-list/div/mh-log-item'))
    print ("count_of_divs : " + str(count_of_divs))

    # count_of_divs = len(tools.driver.find_elements(By.XPATH, '/html/body/mh-root/div/div/mh-large-layout/div/ng-component/mh-log-list/div/div'))
    # print ("count_of_divs : " + str(count_of_divs))
    
    # Need to wait the load of the Total of the day except when they are no logs for this day => count_of_divs = 1
    # if (count_of_divs != 1) :
    #     tools.waitLoadingPageByXPATH2(5, '//*[@id="trackPage"]/div[5]/div/div['+str(count_of_divs)+']/span')
    
    for x in range(count_of_divs):

        # I have this element, how I can find the text of this element /html/body/mh-root/div/div/mh-large-layout/div/ng-component/mh-log-list/div/mh-log-item[3]/div/div/div/div[1]/div/div[1]/mh-log-item-details/div/div[1]/div[2]/span
        text = tools.driver.find_elements(By.XPATH, '/html/body/mh-root/div/div/mh-large-layout/div/ng-component/mh-log-list/div/mh-log-item['+ str(x + 1) + ']/div/div/div/div[1]/div/div[1]/mh-log-item-details/div/div[1]/div[2]/span')
        # if len(text) > 0:
        #     print(text[0].text.encode('utf-8').decode())
        #     print(len(text))

        if (len(text) > 0 ) :
            # print(text[0].text.encode('utf-8').decode())
            if (text[0].text.encode('utf-8').decode() == j.jira) :
                print ('Find the JIRA = ' + text[0].text.encode('utf-8').decode() )
                text2 = tools.driver.find_elements(By.XPATH, '/html/body/mh-root/div/div/mh-large-layout/div/ng-component/mh-log-list/div/mh-log-item['+ str(x + 1) + ']/div/div/div/div[2]/div/div/mh-time-display/span')
                print ('Time for this task = ' + str(text2[0].text.encode('utf-8').decode()))
                array.append([tools.driver.find_elements(By.XPATH, '/html/body/mh-root/div/div/mh-large-layout/div/ng-component/mh-track-navigation-bar/div/div[1]/div[1]/mh-track-date-picker/div/sds-date-picker/div[1]/button[2]/div/div[2]/span')[0].text.encode('utf-8').decode(), str(text2[0].text.encode('utf-8').decode())])
                
    # Click on the button Next
    tools.waitLoadingPageByXPATH2(10, '//*[@id="datePickerText"]/div[1]/button[3]')    
    next_button = tools.driver.find_element(By.XPATH, '//*[@id="datePickerText"]/div[1]/button[3]')
    next_button.click()
    
    time.sleep(1)
    
# Try to find if the JIRA is present or not for Today
# Need to know how much row there is in this day
# Need to wait the load of the Total of the day except when they are no logs for this day => count_of_divs = 1
count_of_divs = len(tools.driver.find_elements(By.XPATH, '/html/body/mh-root/div/div/mh-large-layout/div/ng-component/mh-log-list/div/mh-log-item'))
print ("count_of_divs : " + str(count_of_divs))

# if (count_of_divs != 1) :
#     tools.waitLoadingPageByXPATH2(5, '//*[@id="trackPage"]/div[5]/div/div['+str(count_of_divs)+']/span')

time.sleep(2)

# for x in range(count_of_divs):
#     text = tools.driver.find_elements(By.XPATH, '//*[@id="trackPage"]/div[5]/div/div['+ str(x + 1) + ']/div/log-display/div/div[1]/div/div[1]/log-details-display/div/div[2]/span')
#     if (len(text) > 0 ) :
#         # print(text[0].text.encode('utf-8').decode())
#         if (text[0].text.encode('utf-8').decode() == j.jira) :
#             # print ('Find the JIRA = ' + text[0].text.encode('utf-8').decode() )
#             text2 = tools.driver.find_elements(By.XPATH, '//*[@id="trackPage"]/div[5]/div/div['+ str(x + 1) + ']/div/log-display/div/div[2]/div/div[1]/span/time-display/span')
#             # print ('Time for this task = ' + str(text2[0].text.encode('utf-8').decode()))
#             array.append([tools.driver.find_elements(By.XPATH, '//*[@id="datePickerText"]/span[1]')[0].text.encode('utf-8').decode(), str(text2[0].text.encode('utf-8').decode())])
for x in range(count_of_divs):
    # I have this element, how I can find the text of this element /html/body/mh-root/div/div/mh-large-layout/div/ng-component/mh-log-list/div/mh-log-item[3]/div/div/div/div[1]/div/div[1]/mh-log-item-details/div/div[1]/div[2]/span
    text = tools.driver.find_elements(By.XPATH, '/html/body/mh-root/div/div/mh-large-layout/div/ng-component/mh-log-list/div/mh-log-item['+ str(x + 1) + ']/div/div/div/div[1]/div/div[1]/mh-log-item-details/div/div[1]/div[2]/span')
    # if len(text) > 0:
    #     print(text[0].text.encode('utf-8').decode())
    #     print(len(text))

    if (len(text) > 0 ) :
        print(text[0].text.encode('utf-8').decode())
        print(j.jira)

        if (text[0].text.encode('utf-8').decode() == j.jira) :
            print ('Find the JIRA = ' + text[0].text.encode('utf-8').decode() )
            text2 = tools.driver.find_elements(By.XPATH, '/html/body/mh-root/div/div/mh-large-layout/div/ng-component/mh-log-list/div/mh-log-item['+ str(x + 1) + ']/div/div/div/div[2]/div/div/mh-time-display/span')
            print ('Time for this task = ' + str(text2[0].text.encode('utf-8').decode()))
            # Create an array with the date and the time for this JIRA
            # date : /html/body/mh-root/div/div/mh-large-layout/div/ng-component/mh-track-navigation-bar/div/div[1]/div[1]/mh-track-date-picker/div/sds-date-picker/div[1]/button[2]/div/div[2]/span
            # time : /html/body/mh-root/div/div/mh-large-layout/div/ng-component/mh-log-list/div/mh-log-item[3]/div/div/div/div[2]/div/div/mh-time-display/span
            
            array.append([tools.driver.find_elements(By.XPATH, '/html/body/mh-root/div/div/mh-large-layout/div/ng-component/mh-track-navigation-bar/div/div[1]/div[1]/mh-track-date-picker/div/sds-date-picker/div[1]/button[2]/div/div[2]/span')[0].text.encode('utf-8').decode(), str(text2[0].text.encode('utf-8').decode())])
                

# Need to go to the Jira
j.connectToJira(j.jira)

# Need to add all the time for this JIRA
time_all = timedelta(hours=0, minutes=0, seconds=0)

# Print the array with all the info for this JIRA
print("----------------- Infos -----------------  ")
for r in array:
    print( ' '.join([str(x) for x in r] ) )
    
    # Don't find for the moment how to translate the name of the day directly
    date_to_translate = r[0]
    date_to_translate = date_to_translate.replace('Mon, ', '')
    date_to_translate = date_to_translate.replace('Tue, ', '')
    date_to_translate = date_to_translate.replace('Wed, ', '')
    date_to_translate = date_to_translate.replace('Thu, ', '')
    date_to_translate = date_to_translate.replace('Fri, ', '')
    date_to_translate = date_to_translate.replace('Sat, ', '')
    date_to_translate = date_to_translate.replace('Sun, ', '')
    date_to_translate = date_to_translate.replace('(Today)', '')
    
    print(date_to_translate + ' ' + str(datetime_object.year))

    if r[0].find('(Today)') != -1:
        date_object = datetime.now()
    else:
        date_object = datetime.strptime(date_to_translate + ' ' + str(datetime_object.year), '%d %b %Y')
    
    # print(date_object.day)
    # print(date_object.month)
    
    time_object = datetime.strptime(r[1], '%H:%M:%S')
    
    
    # Click on the more button to add the hours 
    tools.waitLoadingPageByXPATH2(10, '//*[@id="opsbar-operations_more"]')
    more_button = tools.driver.find_element(By.XPATH, '//*[@id="opsbar-operations_more"]')
    more_button.click()
    
    # Click on the log work button to add the hours 
    tools.waitLoadingPageByXPATH2(10, '//*[@id="log-work"]/a/span')
    log_work_button = tools.driver.find_element(By.XPATH, '//*[@id="log-work"]/a/span')
    log_work_button.click()
    
    # Introduce into the input of Time Spent the time for this day
    tools.waitLoadingPageByXPATH2(10, '//*[@id="log-work-time-logged"]')
    log_work_time_logged = tools.driver.find_element(By.XPATH, '//*[@id="log-work-time-logged"]')
    if (time_object.hour > 0) :
        log_work_time_logged.send_keys(str(time_object.hour) + 'h ')
    if (time_object.second > 29) :
        log_work_time_logged.send_keys(str(time_object.minute + 1) + 'm ')
    else :
        if (time_object.minute > 0) :
            log_work_time_logged.send_keys(str(time_object.minute) + 'm ')
        else :
            log_work_time_logged.send_keys(str(time_object.minute + 1) + 'm ')
        
    # Introduce into the input the date
    tools.waitLoadingPageByXPATH2(10, '//*[@id="log-work-date-logged-date-picker"]')
    log_work_date_logged_date_picker = tools.driver.find_element(By.XPATH, '//*[@id="log-work-date-logged-date-picker"]')
    log_work_date_logged_date_picker.send_keys(Keys.CONTROL, 'a')
    
    # Month
    month_number = str(date_object.month)
    datetime_object_month = datetime.strptime(month_number, "%m")
    month_name = datetime_object_month.strftime("%b")
    # print(month_name)
    
    # Year (2 digit)
    # I have the day of the weak => can find the year 
    # given date
    x_date = datetime.strptime(str(datetime_object.year)+'-'+str(date_object.month)+'-'+str(date_object.day)+'', '%Y-%m-%d')   
    # print(x_date.strftime('%w'))
    # print(x_date.strftime('%A')[:3])
    
    # print (r[0].find(x_date.strftime('%A')[:3]))
    # print(str(datetime_object.year))
    if (r[0].find(x_date.strftime('%A')[:3]) == 0) :
        year_2_digit = str(datetime_object.year - 2000)  
    else :
        year_2_digit = str(datetime_object.year - 2001)

    # print(year_2_digit)
    log_work_date_logged_date_picker.send_keys(str(date_object.day) + '/' +month_name+ '/'+str(year_2_digit)+' 10:00 PM')

    tools.waitLoadingPageByXPATH2(10, '//*[@id="log-work-submit"]')
    log_button = tools.driver.find_element(By.XPATH, '//*[@id="log-work-submit"]')
    log_button.click()
    
    # Need to add the time past to this JIRA
    time_all = time_all + timedelta(hours=time_object.hour, minutes=time_object.minute, seconds=time_object.second)
    # print(str(time_all))
    
    time.sleep(5)

print(str(time_all))
timedelta_8 = timedelta(hours=8, minutes=0, seconds=0)
# print(str(timedelta_8))

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