from Tools import tools_v000 as tools
from Jira import jira as j
from MyHours import myhours as m
import os
from os.path import dirname
import time
from datetime import datetime

# -11 for the name of this project LogWorkJira
save_path = os.path.dirname(os.path.abspath("__file__"))
propertiesFolder_path = save_path + "/"+ "Properties"

# Example of used
# user_text = tools.readProperty(propertiesFolder_path, 'LogWorkJira', 'user_text=')
j.jira = tools.readProperty(propertiesFolder_path, 'LogWorkJira', 'jira=')

# Open Browser
tools.openBrowserChrome()

# # Go to the jira to know when the jira was created
j.connectToJira(j.jira)
j.recoverJiraInformation()

# # Open MyHours
m.connectToMyHours()
m.enterCredentials()

# Need to go to the date of the Jira was created
# Select the date in the select button
tools.waitLoadingPageByXPATH2(20, '//*[@id="selectDayTrackButton"]')     
selectDayTrackButton = tools.driver.find_element_by_xpath('//*[@id="selectDayTrackButton"]')
selectDayTrackButton.click()    

# Translate the date (Creation of this JIRA) retrieved in the Jira
j.created_val = j.created_val.replace('+0200', '')
datetime_object = datetime.strptime(j.created_val, '%Y-%m-%dT%H:%M:%S')
print(j.created_val)

# sub 1921 because 2022 = 101 2023 = 102
year_to_search = str(datetime_object.year- 1921) 
print('year_to_search = ' + year_to_search)
# Select the year
# //*[@id="AppWrapper"]/div[3]/div[2]/div[1]/table/thead/tr[1]/th[2]/select[2]
# //*[@id="AppWrapper"]/div[3]/div[2]/div[1]/table/thead/tr[1]/th[2]/select[2]/option[101] 2022
# //*[@id="AppWrapper"]/div[3]/div[2]/div[1]/table/thead/tr[1]/th[2]/select[2]/option[102] 2023
tools.waitLoadingPageByXPATH2(10, '//*[@id="AppWrapper"]/div[3]/div[2]/div[1]/table/thead/tr[1]/th[2]/select[2]')     
AppWrapper_year = tools.driver.find_element_by_xpath('//*[@id="AppWrapper"]/div[3]/div[2]/div[1]/table/thead/tr[1]/th[2]/select[2]/option['+year_to_search+']')
AppWrapper_year.click()   
time.sleep(1)  

# Select the month
# //*[@id="AppWrapper"]/div[3]/div[2]/div[1]/table/thead/tr[1]/th[2]/select[1]
# //*[@id="AppWrapper"]/div[3]/div[2]/div[1]/table/thead/tr[1]/th[2]/select[1]/option[1] Jan
# //*[@id="AppWrapper"]/div[3]/div[2]/div[1]/table/thead/tr[1]/th[2]/select[1]/option[2] Feb
month_to_search = str(datetime_object.month)
print('month_to_search = ' + month_to_search)
tools.waitLoadingPageByXPATH2(10, '//*[@id="AppWrapper"]/div[3]/div[2]/div[1]/table/thead/tr[1]/th[2]/select[1]')     
AppWrapper_month = tools.driver.find_element_by_xpath('//*[@id="AppWrapper"]/div[3]/div[2]/div[1]/table/thead/tr[1]/th[2]/select[1]/option['+month_to_search+']')
AppWrapper_month.click() 
time.sleep(1)  

# Selecet the day
# //*[@id="AppWrapper"]/div[3]/div[2]/div[1]/table/tbody/tr[4]/td[2]
day_to_search = str(datetime_object.day)
print('day_to_search = ' + day_to_search)


for tr_n in range(1, 7):

    for td_n in range(1, 8):
        # print (str(tools.driver.find_element_by_xpath('//*[@id="AppWrapper"]/div[3]/div[2]/div[1]/table/tbody/tr[' + str(tr_n) + ']/td[' + str(td_n) + ']').text.encode('utf-8')))
        if (day_to_search == str(tools.driver.find_element_by_xpath('//*[@id="AppWrapper"]/div[3]/div[2]/div[1]/table/tbody/tr[' + str(tr_n) + ']/td[' + str(td_n) + ']').text.encode('utf-8'))) :
            AppWrapper_day = tools.driver.find_element_by_xpath('//*[@id="AppWrapper"]/div[3]/div[2]/div[1]/table/tbody/tr[' + str(tr_n) + ']/td[' + str(td_n) + ']')
            AppWrapper_day.click()  
            break    


# Need to wait the load of the Total of the day
tools.waitLoadingPageByXPATH2(5, '//*[@id="trackPage"]/div[5]/div/div[10]/span')


# Need to store data 
array = [ ]



# Click on the button Next until we arrived of Today
while True :
    # Click on the button Next 
    print("date selected = " + tools.driver.find_elements_by_xpath('//*[@id="datePickerText"]/span[1]')[0].text.encode('utf-8'))
    
    time.sleep(2)
    
    # Try to find if the JIRA is present or not
    # Need to know how much row there is in this day
    count_of_divs = len(tools.driver.find_elements_by_xpath('//*[@id="trackPage"]/div[5]/div/div'))
    print ("count_of_divs : " + str(count_of_divs))
    
    # Need to wait the load of the Total of the day except when they are no logs for this day => count_of_divs = 1
    if (count_of_divs != 1) :
        tools.waitLoadingPageByXPATH2(5, '//*[@id="trackPage"]/div[5]/div/div['+str(count_of_divs)+']/span')
    
    for x in range(count_of_divs):
        text = tools.driver.find_elements_by_xpath('//*[@id="trackPage"]/div[5]/div/div['+ str(x + 1) + ']/div/log-display/div/div[1]/div/div[1]/log-details-display/div/div[2]/span')
        if (len(text) > 0 ) :
            # print(text[0].text.encode('utf-8'))
            if (text[0].text.encode('utf-8') == j.jira) :
                print ('Find the JIRA = ' + text[0].text.encode('utf-8') )
                text2 = tools.driver.find_elements_by_xpath('//*[@id="trackPage"]/div[5]/div/div['+ str(x + 1) + ']/div/log-display/div/div[2]/div/div[1]/span/time-display/span')
                print ('Time for this task = ' + str(text2[0].text.encode('utf-8')))
                array.append([tools.driver.find_elements_by_xpath('//*[@id="datePickerText"]/span[1]')[0].text.encode('utf-8'), str(text2[0].text.encode('utf-8'))])
                
    # Click on the button Next
    tools.waitLoadingPageByXPATH2(10, '//*[@id="nextDayTrackButton"]')    
    next_button = tools.driver.find_element_by_xpath('//*[@id="nextDayTrackButton"]')
    next_button.click()
    # Recovered the date selected
    if (tools.driver.find_elements_by_xpath('//*[@id="datePickerText"]/span[1]')[0].text.encode('utf-8') == 'Today,') :
        break
    time.sleep(1)
    


# Try to find if the JIRA is present or not for Today
# Need to know how much row there is in this day
count_of_divs = len(tools.driver.find_elements_by_xpath('//*[@id="trackPage"]/div[5]/div/div'))
# print ("count_of_divs : " + str(count_of_divs))

for x in range(count_of_divs):
    text = tools.driver.find_elements_by_xpath('//*[@id="trackPage"]/div[5]/div/div['+ str(x + 1) + ']/div/log-display/div/div[1]/div/div[1]/log-details-display/div/div[2]/span')
    if (len(text) > 0 ) :
        print(text[0].text.encode('utf-8'))
        if (text[0].text.encode('utf-8') == j.jira) :
            # print ('Find the JIRA = ' + text[0].text.encode('utf-8') )
            text2 = tools.driver.find_elements_by_xpath('//*[@id="trackPage"]/div[5]/div/div['+ str(x + 1) + ']/div/log-display/div/div[2]/div/div[1]/span/time-display/span')
            # print ('Time for this task = ' + str(text2[0].text.encode('utf-8')))
            array.append([tools.driver.find_elements_by_xpath('//*[@id="datePickerText"]/span[1]')[0].text.encode('utf-8'), str(text2[0].text.encode('utf-8'))])


# Print the array with all the info for this JIRA
print("----------------- Infos -----------------  ")
for r in array:
    print( ' '.join([str(x) for x in r] ) )
    
    # Need to go to the Jira
    j.connectToJira(j.jira)
    




# Close Browser
tools.closeBrowserChrome()


