from Tools import tools_v000 as tools
from Jira import jira as j
from MyHours import myhours as m
import os
from os.path import dirname


# -11 for the name of this project LogWorkJira
save_path = os.path.dirname(os.path.abspath("__file__"))
propertiesFolder_path = save_path + "/"+ "Properties"

# Example of used
# user_text = tools.readProperty(propertiesFolder_path, 'LogWorkJira', 'user_text=')
j.jira = tools.readProperty(propertiesFolder_path, 'LogWorkJira', 'jira=')

# Open Browser
tools.openBrowserChrome()

# Go to the jira to know when the jira was created
j.connectToJira(j.jira)
j.recoverJiraInformation()

# Open MyHours
m.connectToMyHours()
m.enterCredentials()


# Try to find if the JIRA is present or not
# Need to know how much row there is in this day
# //*[@id="trackPage"]/div[5]/div/div[4]/div/log-display/div/div[1]/div/div[1]/log-details-display/div/div[2]/span
# //*[@id="trackPage"]/div[5]/div/div[6]/div/log-display/div/div[1]/div/div[1]/log-details-display/div/div[2]/span
tools.waitLoadingPageByXPATH2(10, '//*[@id="trackPage"]/div[5]/div/div[10]/span')
count_of_divs = len(tools.driver.find_elements_by_xpath('//*[@id="trackPage"]/div[5]/div/div'))
print ("count_of_divs : " + str(count_of_divs))

for x in range(count_of_divs):
    text = tools.driver.find_elements_by_xpath('//*[@id="trackPage"]/div[5]/div/div['+ str(x + 1) + ']/div/log-display/div/div[1]/div/div[1]/log-details-display/div/div[2]/span')
    if (len(text) > 0 ) :
        print(text[0].text.encode('utf-8'))


# Close Browser
tools.closeBrowserChrome()