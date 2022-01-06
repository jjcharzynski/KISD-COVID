# -*- coding: utf-8 -*-
"""
Created on Sun Sep  5 16:12:13 2021
@author: jjcharzynski
"""

from datetime import  datetime

print('Started at ', datetime.now())

#geckodriver must be installed
geckopath = "geckodriver/geckodriver.exe" #geckodriver must be installed
#allschools.txt mush be created

url = 'https://katyisd.maps.arcgis.com/apps/dashboards/cb86720693b84f048bc389e1c74483f5'
url2 = 'https://gis.katyisd.org/covid/'
cumulativeerrorvalue = 3000

#Create List of Schools
b_file = open("allschools.txt", "r")
# b_file = open("tempschools.txt", "r") #use this when re-pulling schools that didnt work the first time
schools = []
schoolcount = 0
for line in b_file:
  schools.append(line)
  schoolcount += 1
b_file.close()

#Pull All Data from Dashboard
def getandsavealldata():
    '''
    Get data from the All Facilities, Elementary, Junior High, and High School Tabs
    Returns
    -------
    None.

    '''
    from selenium import webdriver # module containing implementations of browser drivers
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager # Chrome driver 
    import time
    import pyperclip
    import datetime
    import shutil
    
    # Initialize Chrome browser and launch the dashboard in Chrome
    chrome_options = Options()  
    chrome_options.add_argument("--headless")  
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
    driver.set_window_size(1050, 10000)
    driver.get(url)
    size = driver.get_window_size()
    print("Window size is ", size)
    delay = 10
    time.sleep(delay)
    alldata = driver.find_element_by_css_selector('body').text
    print("alldata scraped")
    driver.refresh()
    time.sleep(delay)
    bodyelement = driver.find_element_by_css_selector('body')
    bodyelement.send_keys(Keys.TAB, Keys.TAB, Keys.TAB, Keys.ENTER)
    time.sleep(1)
    elementarydata = driver.find_element_by_css_selector('body').text
    print("elementarydata scraped")
    driver.refresh()
    time.sleep(delay)
    bodyelement = driver.find_element_by_css_selector('body')
    bodyelement.send_keys(Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.ENTER)
    time.sleep(1)
    jrhighdata = driver.find_element_by_css_selector('body').text
    print("jrhighdata scraped")
    driver.refresh()
    time.sleep(delay)
    bodyelement = driver.find_element_by_css_selector('body')
    bodyelement.send_keys(Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.ENTER)
    time.sleep(1)
    highdata = driver.find_element_by_css_selector('body').text
    print("highdata scraped")
    driver.close()
    
    lines = alldata.split("\n")
    non_empty_lines = [line for line in lines if line.strip() != ""]
    string_without_empty_lines = ""
    for line in non_empty_lines:
          string_without_empty_lines += line
          string_without_empty_lines += "\n"
    with open('new.txt','w') as file:
        file.write(string_without_empty_lines)
    
    elines = elementarydata.split("\n")
    enon_empty_lines = [line for line in elines if line.strip() != ""]
    string_without_empty_lines = ""
    for line in enon_empty_lines:
          string_without_empty_lines += line
          string_without_empty_lines += "\n"
    with open('elementary.txt','w') as file:
        file.write(string_without_empty_lines)  
    
    jrlines = jrhighdata.split("\n")
    jrnon_empty_lines = [line for line in jrlines if line.strip() != ""]
    string_without_empty_lines = ""
    for line in jrnon_empty_lines:
          string_without_empty_lines += line
          string_without_empty_lines += "\n"
    with open('juniorhigh.txt','w') as file:
        file.write(string_without_empty_lines)
    
    highlines = highdata.split("\n")
    highnon_empty_lines = [line for line in highlines if line.strip() != ""]
    string_without_empty_lines = ""
    for line in highnon_empty_lines:
          string_without_empty_lines += line
          string_without_empty_lines += "\n"
    with open('high.txt','w') as file:
        file.write(string_without_empty_lines)         
    
    #save the data pull everytime I run the script
    now = datetime.datetime.now()
    current_time = now.strftime("%y%d%m%H%M%S")
    shutil.copy('new.txt', 'katyisdcoviddatapulls/all' + current_time + '.txt')
    shutil.copy('elementary.txt', 'katyisdcoviddatapulls/elem' + current_time + '.txt')
    shutil.copy('juniorhigh.txt', 'katyisdcoviddatapulls/jrhi' + current_time + '.txt')
    shutil.copy('high.txt', 'katyisdcoviddatapulls/high' + current_time + '.txt')
    
    print('All data scraped and saved.')

#Extract and compile alldata
def extractandcompilealldata():
    '''
    Extract data from text files and save to data frames

    Returns
    -------
    None.

    '''
    import pandas as pd
    import datetime
    import csv
    import os
    # import shutil
    
    global update_date
    global ldf
    global tldf
    global df
    global numbers
    
    now = datetime.datetime.now()
    # current_time = now.strftime("%y%d%m%H%M%S")
    
    L = ['Last Updated\n', 'Cumulative Cases\n', 'Active Cases\n', 'Active Student Cases\n', 'Active Staff Cases\n']
    today = {}
    numbers = {}  
    a_file = open("new.txt","r")   
    for number, line in enumerate(a_file):
        if "Stage" in line:
            size = len(line)
            line = line[:size - 12]
            line = line + '\n'
            # print(line)
        today[number] = line
    # key_list = list(today.keys())
    val_list1 = list(today.values())
    lastupdatedline = val_list1.index('Last Updated\n')
    lastupdateddateline = lastupdatedline + 1
    lastupdated = today[lastupdateddateline] #datepull
    for string in L:
        label = string.rstrip("\n")
        try:
            position = val_list1.index(string)
            position2 = position + 1
            numbers[label] = today[position2].rstrip("\n")
        except ValueError:
            numbers[label] = None
    a_file.close()
    
    nolongertracked = ['KVA Elementary\n', 'KVA Junior High\n']
    for string in schools:
        if string in nolongertracked:
            print(string, ' is no longer tracked.')
        else:
            schoolstring = string.strip("\n")
            position3 = val_list1.index(string)
            position4 = position3 + 1
            position5 = position3 + 2
            position6 = position3 + 3
            position7 = position3 + 4
            activecases = today[position4]
            activecasesname, activecasesnumber = activecases.rstrip("\n").split(":")
            activecasesdict = schoolstring + ' ' + activecasesname
            numbers[activecasesdict] = activecasesnumber
            activestaff = today[position5]
            activestaffname, activestaffnumber = activestaff.rstrip("\n").split(":")
            activestaffdict = schoolstring + ' ' + activestaffname
            numbers[activestaffdict] = activestaffnumber
            activestudents = today[position6]
            activestudentsname, activestudentsnumber = activestudents.rstrip("\n").split(":")
            activestudentsdict = schoolstring + ' ' + activestudentsname
            numbers[activestudentsdict] = activestudentsnumber
            activeauxiliary = today[position7]
            activeauxiliaryname, activeauxiliarynumber = activeauxiliary.rstrip("\n").split(":")
            activeauxiliarydict = schoolstring + ' ' + activeauxiliaryname
            numbers[activeauxiliarydict] = activeauxiliarynumber
    
    M = ['Cumulative Cases\n']
    etoday = {} 
    b_file = open("elementary.txt","r")    
    for number, line in enumerate(b_file):
        etoday[number] = line
    val_list = list(etoday.values())
    for string in M:
        label = 'Elementary ' + string.rstrip("\n")
        label2 = 'Percent of Elementary Staff'
        label3 = 'Percent of Elementary Students'
        try:
            position = val_list.index(string)
            position2 = position + 1
            position3 = position - 1
            position4 = position - 4
            numbers[label] = etoday[position2].rstrip("\n")
            numbers[label2] = etoday[position3].rstrip("% of staff\n")
            numbers[label3] = etoday[position4].rstrip("% of students\n")
        except ValueError:
            numbers[label] = None
    b_file.close()
    
    jrtoday = {} 
    c_file = open("juniorhigh.txt","r")    
    for number, line in enumerate(c_file):
        jrtoday[number] = line
    val_list = list(jrtoday.values())
    for string in M:
        label = 'Junior High ' + string.rstrip("\n")
        label2 = 'Percent of Junior High Staff'
        label3 = 'Percent of Junior High Students'
        try:
            position = val_list.index(string)
            position2 = position + 1
            position3 = position - 1
            position4 = position - 4
            numbers[label] = jrtoday[position2].rstrip("\n")
            numbers[label2] = jrtoday[position3].rstrip("% of staff\n")
            numbers[label3] = jrtoday[position4].rstrip("% of students\n")
        except ValueError:
            numbers[label] = None
    c_file.close()
    
    hightoday = {} 
    d_file = open("high.txt","r")    
    for number, line in enumerate(d_file):
        hightoday[number] = line
    val_list = list(hightoday.values())
    for string in M:
        label = 'High ' + string.rstrip("\n")
        label2 = 'Percent of High Staff'
        label3 = 'Percent of High Students'
        try:
            position = val_list.index(string)
            position2 = position + 1
            position3 = position - 1
            position4 = position - 4
            numbers[label] = hightoday[position2].rstrip("\n")
            numbers[label2] = hightoday[position3].rstrip("% of staff\n")
            numbers[label3] = hightoday[position4].rstrip("% of students\n")
            position = val_list.index(string)
            position2 = position + 1
            numbers[label] = hightoday[position2].rstrip("\n")
        except ValueError:
            numbers[label] = None
    d_file.close()
    
    e_file = open("new.txt","r")   
    for string in M:
        label = string.rstrip("\n")
        label2 = 'Percent of Active Staff'
        label3 = 'Percent of Active Students'
        try:
            position = val_list1.index(string)
            position3 = position - 1
            position4 = position - 4
            numbers[label2] = today[position3].rstrip("% of staff\n")
            numbers[label3] = today[position4].rstrip("% of students\n")        
        except ValueError:
            numbers[label] = None
    e_file.close()
    
    #create daily csv file
    date1 = lastupdated.rstrip("\n")
    date2 = date1.replace(",","")
    update_date1 = datetime.datetime.strptime(date2,'%B %d %Y')
    update_date = datetime.datetime.date(update_date1)
    csvfilename1 = "%s.csv" % update_date
    dailyfolder = 'C:\\Users\\homer\\katyisdcoviddailydata\\'
    csvfilename = dailyfolder + csvfilename1
    
    with open(csvfilename, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        for key, value in numbers.items():
           writer.writerow([key, value])
    
    #starting file (before 8/26/2021)
    ldf = pd.read_csv('Previous Data - 2020-2021.csv')
    ldf.set_index('Identifier',inplace=True)
    ldf.to_csv('previousdata20-21.csv')
    tldf = ldf.transpose()
    df = pd.read_csv('Previous Data - 2021-2022.csv')
        
    #compile data from all the days 
    directory = r'C:\\Users\\homer\\katyisdcoviddailydata\\'
    for filename in os.listdir(directory):
        columnname = os.path.splitext(filename)[0]
        absolutepath = dailyfolder + filename
        if filename.endswith(".csv"):   
            df[columnname] = pd.read_csv(absolutepath, usecols=[1])
    df.set_index('Identifier',inplace=True)
    df = df.replace(',','', regex=True)
    df = df.apply(pd.to_numeric)
    # print(df)
    df.to_csv('latestdata.csv')
    
    print('All data extracted and compiled.')
    
#Pull School Data from Dashboard
def getcampusdata():
    '''
    Pulls the daily campus numbers

    Returns
    -------
    None.

    '''
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.firefox.options import Options
    import time
    import pyperclip
    import os
    import shutil
    
    delay = 10
    # delay2 = 6
    wait = 2
    # wait2 = 2
    count = 1
    errorcampuses = () 
    
    tempschools = []
    now = time.time()

    # code to move old files
    path1 = 'katyisdcovidschooldata/'
    dest = 'katyisdcovidschooldataold/'
    for f in os.listdir(path1):
        f = os.path.join(path1, f)
        if os.stat(f).st_mtime < now - 0.25 * 86400:
            if os.path.isfile(f):
                shutil.copy(f, dest) #move files   

    firefox_options = Options()
    # firefox_options.headless = True #Runs in headless... but does not work

    for string in schools:
        attempts = 1
        while attempts < 4:
            try:
                print('Attempt ', attempts, 'for ', string.strip("\n"))
                bodyelement = None
                while bodyelement == None:
                    pyperclip.copy('')
                    driver = webdriver.Firefox(options=firefox_options, executable_path=geckopath)
                    driver.set_window_size(600,800)
                    driver.get(url2)
                    time.sleep(delay)
                    bodyelement = driver.find_element_by_css_selector('body')
                    if bodyelement == None:
                        driver.close()
                        print('Retrying...')
                
                #old - worked before 12/8
                # bodyelement.send_keys(Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.ENTER)
                # bodyelement.send_keys(Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.ENTER)
                # bodyelement.send_keys(Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.ENTER) #text box
                #end of old
                
                #new - worked on 12/9
                bodyelement.send_keys(Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.TAB, Keys.ENTER)
                bodyelement.send_keys(Keys.SHIFT, Keys.TAB)
                bodyelement.send_keys(Keys.SHIFT, Keys.TAB)
                bodyelement.send_keys(Keys.SHIFT, Keys.TAB)
                bodyelement.send_keys(Keys.ENTER)
                #end of new
                
                if string == 'Davidson Elementary\n':
                    schoolstring = 'Davidson  Elementary'
                    savestring = 'Davidson Elementary'
                else:    
                    schoolstring = string.strip("\n")
                    savestring = schoolstring
                bodyelement.send_keys(schoolstring)              
                bodyelement.send_keys(Keys.TAB, Keys.TAB, Keys.SPACE)
                time.sleep(wait)
                bodyelement.send_keys(Keys.CONTROL+'a')
                bodyelement.send_keys(Keys.CONTROL+'c')
                campusdata = pyperclip.paste()
                lines = campusdata.split("\n")
                non_empty_lines = [line for line in lines if line.strip() != ""]
                string_without_empty_lines = ""
                for line in non_empty_lines:
                    string_without_empty_lines += line
                    strings = ("Loading...")
                    if strings in line:
                        errorcampuses += str(string + ' ' + line)
                        tempschools.append(schoolstring)
                        raise ValueError('Did not load campus data.', 'custom 1')
                with open('katyisdcovidschooldata/' + savestring + '.txt','w') as file:
                    file.write(string_without_empty_lines)
                with open('katyisdcovidschooldata/' + savestring + '.txt','r') as file2:
                    if string not in file2.read():
                        tempschools.append(schoolstring)
                        print('Error scraping ', schoolstring)
                        raise ValueError('Did not pull campus data.', 'custom 2')
                with open('katyisdcovidschooldata/' + savestring + '.txt','r') as file3:
                    linestocheck = file3.readlines()
                # print(linestocheck)
                print('Cumulative check: ', linestocheck[18].rstrip("\n"))
                if int((linestocheck[18].rstrip("\n")).replace(',', '')) > cumulativeerrorvalue:
                    print('Error scraping ', schoolstring.split("\n"))
                    raise ValueError('Did not pull cumulative campus data.', 'custom 3')
                print(schoolstring + ' data scraped successfuly. ' + str(count) + ' of ' + str(schoolcount) + '.' + "\n")
                driver.close()
                count += 1
                break
            except TypeError:
                print("TypeError on Attempt ", attempts, " for ", string.rstrip("\n"))
                attempts += 1
                driver.close()
            except ValueError as err:
                print("ValueError on Attempt ", attempts, " for ", string.rstrip("\n"))
                print(err.args)
                attempts += 1
                driver.close()
    # with open('tempschools.txt','w') as file:
    #     for string in tempschools:
    #         file.write(string,'\n')
    print(tempschools)
    print(errorcampuses)
    print('All the Campus data has been scraped.')
    
    
#Save Campus Data
def savecampusdata():
    '''
    Saves the daily campus numbers

    Returns
    -------
    None.

    '''        
    import datetime
    import os
    import pandas as pd
    
    global schooldf
    
    #Save Campus Data
    path, dirs, files = next(os.walk('katyisdcovidschooldata/'))
    file_count = len(files)
    if file_count != 72:
        raise KeyError()
    now = datetime.datetime.now()
    current_time = now.strftime("%y%d%m%H%M%S")
    school = {}
    folder = r'katyisdcovidschooldata/'
    S = 'Cumulative Cases\n'
    for file in os.listdir(folder):
        campus = file.rstrip(".txt")
        schooltoday = {} 
        s_file = open(folder + file,"r")    
        for number, line in enumerate(s_file):
            schooltoday[number] = line
        val_list = list(schooltoday.values())
        label =  campus + ' ' + S.rstrip("\n")
        label2 = campus + ' ' + 'Percent of Staff with Active Case'
        label3 = campus + ' ' + 'Percent of Students with Active Case'
        label4 = campus + ' ' + 'Active Student Cases'
        label5 = campus + ' ' + 'Active Cases'
        label6 = campus + ' ' + 'Active Staff Cases'
        try:
            position = val_list.index(S)
            position2 = position + 1 #cumulative cases data
            position3 = position - 1 #percent of staff
            position4 = position - 4 #percent of students
            position5 = position - 5 #active student cases
            position6 = position - 7 #active cases
            position7 = position - 2 #active staff cases
            school[label] = schooltoday[position2].rstrip("\n")
            school[label5] = schooltoday[position6].rstrip("\n")
            school[label4] = schooltoday[position5].rstrip("\n")
            school[label6] = schooltoday[position7].rstrip("\n")
            school[label2] = schooltoday[position3].rstrip("% of staff\n")
            school[label3] = schooltoday[position4].rstrip("% of students\n")
        except ValueError:
            school[label] = None
            school[label5] = None
            school[label4] = None
            school[label6] = None
            school[label2] = None
            school[label3] = None
        s_file.close()  
    schooldf = pd.Series(school, name=update_date)
    schooldf.index.name = 'Campus'
    schooldf.reset_index()
    schooldf.to_csv('katyisdcoviddatapulls/' + current_time + 'AllCampuses.csv')
    schooldf.to_csv('katyisdcoviddailyschooldata/' + str(update_date) + 'AllCampuses.csv')
    print('Campus Data saved.')

#Compile data
def compilecampusdata():
    '''
    Compiles and massages data
    Returns
    -------
    None.

    '''
    import os
    import pandas as pd
    import numpy as np
    import shutil
    import datetime
    
    global campusdf
    global tdf
    global activedf
    global activecolumns
    global staffcolumns
    global studentcolumns
    global auxiliarycolumns
    global elementarycolumns
    global jrhighcolumns
    global highcolumns
    global centercolumns
    global campusnewcasescolumns
    global columndict
    global campusnewcasesdf
    global alldf
    global campusstudentpercentcolumns
    global campusstaffpercentcolumns
    global campusstudentpercentdf
    global campusstaffpercentdf
    global campuspercentcolor
    global campuspercentcolorreal
        
    now = datetime.datetime.now()
    current_time = now.strftime("%y%d%m%H%M%S")
    
    #Compile Campus Data
    campusdf = pd.read_csv('AllCampusesBlank.csv')
    directory = r'C:\\Users\\homer\\katyisdcoviddailyschooldata\\'
    for filename in os.listdir(directory):
        # print(filename)
        campusdaily = pd.read_csv('katyisdcoviddailyschooldata/'+ filename)
        campusdf = pd.merge(campusdf, campusdaily, on ='Campus', how ='inner')
    campusdf.set_index('Campus', inplace=True)
    campusdf.to_csv('allcampusdata.csv')
    
    #Merge campusdf with tdf, and remove overlap
    alldf = pd.merge(df, campusdf, left_index=True, right_index=True, how ='outer')
    # print(alldf)
    alldf.to_csv('alldata1.csv')
    duplicatecol = {}
    for col in alldf.columns:
        if '_x' in col:
            col2 = col.rstrip(col[-1]) + 'y'
            duplicatecol[col] = col2
            col4 = col.rstrip(col[-1])
            col3 = col4.rstrip(col4[-1])
            alldf[col3] = np.where(np.isnan(alldf[col]) == True, alldf[col2], alldf[col])
            del alldf[col]
            del alldf[col2]  
    alldf = alldf.reindex(sorted(alldf.columns), axis=1)
    alldf.to_csv('alldata.csv')
    
    #Transpose
    trdf = alldf.transpose()
    #need to sorf trdf by date
    # print(trdf.index)
    # trdf.index = pd.to_datetime(trdf.index)
    # trdf.sort_index(ascending=False)
    # print(trdf.index)
    
        
    trdf.to_csv('latestdatatransposedraw.csv')
    tdf = trdf.iloc[1: , :]
    
    #add total daily new cases
    tdf = tdf.replace(',','', regex=True)
    tdf = tdf.apply(pd.to_numeric)
    tdf['Active Cases Interpolate'] = tdf['Active Cases'].interpolate()
    tdf['Active Student Cases Interpolate'] = tdf['Active Student Cases'].interpolate()
    tdf['Active Staff Cases Interpolate'] = tdf['Active Staff Cases'].interpolate()
    tdf['Cumulative Cases Interpolate'] = tdf['Cumulative Cases'].interpolate()
    tdf['Yesterdays Cumulative Cases'] = tdf['Cumulative Cases Interpolate'].shift(1)
    tdf['New Cases'] = tdf['Cumulative Cases Interpolate'] - tdf['Yesterdays Cumulative Cases']
    tdf['Interpolated Data'] = np.where(tdf['Cumulative Cases'].isnull(), 1, 0)
    
    
    #add daily new cases by campus
    campuscumulativescolumns = {}
    campuscumulativescolumnslist = []
    campusnewcasescolumns = []
    campusstudentpercentcolumnsdict = {}
    campusstudentpercentcolumns = []
    campusstaffpercentcolumnsdict = {}
    campusstaffpercentcolumns = []
    campuspercentcolor = []
    for string in schools:
        campus = string.strip("\n")
        cumcol = campus + ' Cumulative Cases'
        campuscumulativescolumns[campus] = cumcol
        campuscumulativescolumnslist.append(cumcol)
        studentpercentcol = campus + ' Percent of Students with Active Case'
        campusstudentpercentcolumnsdict[campus] = studentpercentcol
        staffpercentcol = campus + ' Percent of Staff with Active Case'
        campusstaffpercentcolumnsdict[campus] = staffpercentcol
        if 'Elementary' in campus:
            campuspercentcolor.append('limegreen')
        else:
            if 'Junior high' in campus:
                campuspercentcolor.append('orange')
            else:
                if 'Center' in campus:
                    campuspercentcolor.append('cornflowerblue')
                else:
                    if 'Academy' in campus:
                            campuspercentcolor.append('cornflowerblue')
                    else:
                        if 'High' in campus:
                            if 'Junior' in campus:
                                campuspercentcolor.append('orange')
                            else:
                                campuspercentcolor.append('cornflowerblue')
                        else:
                            campuspercentcolor.append('purple')
    # print(campuspercentcolor)
    for key, value in campuscumulativescolumns.items():
        yesterday = key + ' Yesterdays Cumulative Cases'
        tdf[yesterday] = tdf[value].shift(1)
        newcases = key + ' New Cases'
        tdf[newcases] = tdf[value] - tdf[yesterday]
        campusnewcasescolumns.append(newcases)
    for key, value in campusstudentpercentcolumnsdict.items():
        campusstudentpercentcolumns.append(value)
    for key, value in campusstaffpercentcolumnsdict.items():
        campusstaffpercentcolumns.append(value)
    
    # print(campuscumulativescolumns)
    # print(campusstudentpercentcolumns)
    
    #create column dictionary and active, staff, student, auxillary, elementry, junior high, high lists
    columnstoignore = ['Cumulative Cases','Cumulative Cases Interpolate', 'Active Cases', 'Active Student Cases', 'Active Staff Cases', 'Active Cases Interpolate', 'Active Student Cases Interpolate', 'Active Staff Cases Interpolate', 'Active Auxiliary Cases', 'Yesterdays Cumulative Cases', 'New Cases', 'Active Auxiliary Cases - calculated', 'Elementary Cumulative', 'Junior High Cumulative', 'High School Cumulative', 'Percent of Elementary Staff with Active Case', 'Percent of Elementary Students with Active Case', 'Percent of Junior High Staff with Active Case', 'Percent of Junior High Students with Active Case', 'Percent of High School Staff with Active Case', 'Percent of High School Students with Active Case', 'Percent of Total Staff with Active Case', 'Percent of Total Students with Active Case']
    activecolumns = []
    staffcolumns = []
    studentcolumns = []
    auxiliarycolumns = []
    elementarycolumns = []
    jrhighcolumns = []
    highcolumns = []
    centercolumns = []
    key = 1
    columndict = {}
    for col in tdf.columns:
        columndict[key] = col
        key += 1
        if col not in columnstoignore:
            if 'Active Cases' in col:
                activecolumns += [col]
            if 'Staff Cases' in col:
                staffcolumns += [col]
            if 'Student Cases' in col:
                studentcolumns += [col]
            if 'Auxiliary Cases' in col:
                auxiliarycolumns += [col]
            if 'Elementary' in col:
                if 'Active Cases' not in col:
                    if 'Cumulative' not in col:
                        if 'Percent' not in col:
                            elementarycolumns += [col]
            if 'Junior high' in col:
                if 'Active Cases' not in col:
                    if 'Cumulative' not in col:
                        if 'Percent' not in col:
                            jrhighcolumns += [col]
            if 'High' in col:
                if 'Active Cases' not in col:
                    if 'Junior' in col:
                        if 'Cumulative' not in col:
                            if 'Percent' not in col:
                                jrhighcolumns += [col]
                    else:
                        if 'Cumulative' not in col:
                            if 'Percent' not in col:
                                highcolumns += [col]
            if 'Center' in col:
                if 'Active Cases' not in col:
                    centercolumns += [col]
            
    auxsum = tdf[auxiliarycolumns]
    tdf['Active Auxiliary Cases - calculated'] = auxsum.sum(axis=1)
    activesum = tdf[activecolumns]
    tdf['Active Cases - calculated'] = activesum.sum(axis=1)       
    staffsum = tdf[staffcolumns]
    tdf['Active Staff Cases - calculated'] = staffsum.sum(axis=1)
    studentsum = tdf[studentcolumns]
    tdf['Active Student Cases - calculated'] = studentsum.sum(axis=1)
    elementarysum = tdf[elementarycolumns]
    tdf['Active Elementary Cases - calculated'] = elementarysum.sum(axis=1)
    jrhighsum = tdf[jrhighcolumns]
    tdf['Active Junior High Cases - calculated'] = jrhighsum .sum(axis=1)
    highsum = tdf[highcolumns]
    tdf['Active High School Cases - calculated'] = highsum .sum(axis=1)
    centersum = tdf[centercolumns]
    tdf['Active Center Cases - calculated'] = centersum.sum(axis=1)
    
    allactivebycasetype = tdf[['Active Staff Cases - calculated', 'Active Student Cases - calculated', 'Active Auxiliary Cases - calculated']]
    tdf['All Active from calculated case type'] = allactivebycasetype.sum(axis=1)
    allactivebyschooltype = tdf[['Active Elementary Cases - calculated', 'Active Junior High Cases - calculated', 'Active High School Cases - calculated', 'Active Center Cases - calculated']]
    tdf['All Active from calculated school type'] = allactivebyschooltype.sum(axis=1)
    
    tdf['New Cases 7 Day Average'] = tdf['New Cases'].rolling(7).mean().shift(0)
    
    tdf.to_csv('latestdatatransposed.csv')
    shutil.copy('latestdatatransposed.csv', 'katyisdcoviddatapulls/alldata' + current_time + '.csv')
    
    #barchart data
    active1df = pd.DataFrame()
    active1df['Identifier'] = activecolumns
    activedf = pd.merge(df, active1df, on ='Identifier', how ='inner')
    activedf = activedf.replace(' Active Cases','', regex=True)
    activedf.set_index('Identifier',inplace=True)
    activedf = activedf.apply(pd.to_numeric)
    
    #new cases barchart data
    campusnewcasesdf1 = pd.DataFrame()
    campusnewcasesdf1['Campus'] = campusnewcasescolumns
    campusnewcasesdf1.set_index('Campus',inplace=True)
    # print(campusnewcasesdf1)
    trantdf = tdf.transpose()
    # print(trantdf)
    campusnewcasesdf = pd.merge(trantdf, campusnewcasesdf1, right_index = True, left_index = True, how ='inner')
    campusnewcasesdf = campusnewcasesdf.apply(pd.to_numeric)
    campusnewcasesdf = campusnewcasesdf.reset_index()
    campusnewcasesdf = campusnewcasesdf.replace(' New Cases','', regex=True)
    campusnewcasesdf.set_index('index',inplace=True)
    # print(campusnewcasesdf)
    
    #student percent barchart data
    campusstudentpercentdf1 = pd.DataFrame()
    campusstudentpercentdf1['Campus'] = campusstudentpercentcolumns
    campusstudentpercentdf1.set_index('Campus', inplace=True)
    # print(campusstudentpercentdf1)
    campusstudentpercentdf = pd.merge(trantdf, campusstudentpercentdf1, right_index = True, left_index = True, how ='inner')
    campusstudentpercentdf = campusstudentpercentdf.apply(pd.to_numeric)
    campusstudentpercentdf = campusstudentpercentdf.reset_index()
    campusstudentpercentdf = campusstudentpercentdf.replace(' Percent of Students with Active Case','', regex=True)
    campusstudentpercentdf.set_index('index',inplace=True)
    # print(campusstudentpercentdf)
    campuspercentcolorreal = []
    for row in campusstudentpercentdf.index:
        # print(row)
        if 'Elementary' in row:
            campuspercentcolorreal.append('limegreen')
        else:
            if 'Junior high' in row:
                campuspercentcolorreal.append('orange')
            else:
                if 'Center' in row:
                    campuspercentcolorreal.append('cornflowerblue')
                else:
                    if 'Academy' in row:
                            campuspercentcolorreal.append('cornflowerblue')
                    else:
                        if 'High' in row:
                            if 'Junior' in row:
                                campuspercentcolorreal.append('orange')
                            else:
                                campuspercentcolorreal.append('cornflowerblue')
                        else:
                            campuspercentcolorreal.append('purple')
    # print(campuspercentcolorreal)                        
    
    #staff percent barchart data
    campusstaffpercentdf1 = pd.DataFrame()
    campusstaffpercentdf1['Campus'] = campusstaffpercentcolumns
    campusstaffpercentdf1.set_index('Campus', inplace=True)
    # print(campusstaffpercentdf1)
    campusstaffpercentdf = pd.merge(trantdf, campusstaffpercentdf1, right_index = True, left_index = True, how ='inner')
    campusstaffpercentdf = campusstaffpercentdf.apply(pd.to_numeric)
    campusstaffpercentdf = campusstaffpercentdf.reset_index()
    campusstaffpercentdf = campusstaffpercentdf.replace(' Percent of Staff with Active Case','', regex=True)
    campusstaffpercentdf.set_index('index',inplace=True)
    # print(campusstaffpercentdf)
    # campuspercentcolorreal = []
    # for row in campusstaffpercentdf.index:
    #     # print(row)
    #     if 'Elementary' in row:
    #         campuspercentcolorreal.append('limegreen')
    #     else:
    #         if 'Junior high' in row:
    #             campuspercentcolorreal.append('orange')
    #         else:
    #             if 'Center' in row:
    #                 campuspercentcolorreal.append('cornflowerblue')
    #             else:
    #                 if 'Academy' in row:
    #                         campuspercentcolorreal.append('cornflowerblue')
    #                 else:
    #                     if 'High' in row:
    #                         if 'Junior' in row:
    #                             campuspercentcolorreal.append('orange')
    #                         else:
    #                             campuspercentcolorreal.append('cornflowerblue')
    #                     else:
    #                         campuspercentcolorreal.append('purple')    
    
    
    
    
    
    print('Campus Data Compiled.')
        
#Make Plots
def visualizedata():
    '''
    makes plots
    Returns
    -------
    None.

    '''
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    import datetime
    import pandas as pd
    
    xmax = update_date
    tdf.index = pd.to_datetime(tdf.index)
    tldf.index = pd.to_datetime(tldf.index)
    ymax = 10
    for col in tdf.columns:
        if col in activecolumns:
            column = tdf[col]
            max_value = column.max()
            print(max_value)
            if max_value > ymax:
                ymax = 5 * round(max_value/5)
                if max_value > ymax:
                    ymax += 5
    ymax = ymax + 5
    print('Ymax = ', ymax)
    #visualization

    
    # New Cases Plot
    fig = plt.figure(figsize=(20,10))
    colors = {1: 'orange', 0: 'lightpink'}
    barchart1 = plt.bar(tdf.index, tdf['New Cases'].rolling(window=1).mean(), color=[colors[i] for i in tdf['Interpolated Data']])
    line1, = plt.plot(tdf.index, tdf['New Cases 7 Day Average'], color='darkred', linewidth=5)
    plt.xlabel('Date', fontsize=16)
    plt.xticks(rotation = 90)
    # plt.yscale('log')
    plt.ylabel('Cases', fontsize=16)
    plt.title('Katy ISD New Cases Per Day - 2021-2022', fontsize=20)
    for x,y in zip(tdf.index,tdf['New Cases']):
        label = "{:.0f}".format(y)
        plt.annotate(label, # this is the text
                     (x,y), # these are the coordinates to position the label
                     textcoords="offset points", # how to position the text
                     xytext=(0,10), # distance from text to points (x,y)
                     ha='center')
    first_day_of_school = datetime.date(2021,8,18)
    plt.axvline(first_day_of_school, linewidth=2.5, linestyle='--', color='tab:gray', alpha=0.5)
    plt.text(first_day_of_school, 100,'First Day of School', rotation=90, ha='center')
    # plt.annotate('charzynski.com/katycovidcharts', xy=(0.01, .97), xycoords='axes fraction', style='italic', fontsize=12)
    # plt.legend([barchart1[20:21], barchart1[0:1], line1], ['New Cases', 'Interpolated','7 Day Average'], loc=2, prop={'size': 14}, title = 'charzynski.com/katycovidcharts')
    plt.legend([barchart1[20:21], line1], ['New Cases','7 Day Average'], loc=2, prop={'size': 14}, title = 'charzynski.com/katycovidcharts')
    plt.savefig('katyisdcovidnewestplots/01newcases.png')
    plt.show()
    plt.close()
    
    # Plot total active, student, and staff cases
    fig2 = plt.figure(figsize=(20,10))
    line1, = plt.plot(tdf.index, tdf['Active Cases Interpolate'], color='tab:red', linewidth=5)
    line2, = plt.plot(tdf.index, tdf['Active Student Cases Interpolate'], color='limegreen', linewidth=3.5)
    line3, = plt.plot(tdf.index, tdf['Active Staff Cases Interpolate'], color='cornflowerblue', linewidth=3.5)
    plt.xlabel('Date', fontsize=16)
    plt.xticks(rotation = 90)
    plt.ylabel('Cases', fontsize=16)
    plt.title('Katy ISD Active Cases - 2021-2022', fontsize=20)
    first_day_of_school = datetime.date(2021,8,18)
    plt.axvline(first_day_of_school, linewidth=2.5, linestyle='--', color='tab:gray', alpha=0.5)
    plt.text(first_day_of_school, 300,'First Day of School', rotation=90, ha='center')
    plt.legend([line1, line2, line3], ['Total Cases','Student Cases','Staff Cases'], loc=2, prop={'size': 14}, title = 'charzynski.com/katycovidcharts')
    plt.savefig('katyisdcovidnewestplots/02activecases.png')
    plt.show()
    plt.close()
    
    # Plot total active, student, and staff cases and compare to last year
    x_values1 = tdf.index
    y_values1 = tdf['Active Cases Interpolate']
    y_values12 = tdf['Active Student Cases Interpolate']
    y_values13 = tdf['Active Staff Cases Interpolate']
    x_values2 = tldf.index
    y_values2 = tldf['Active Cases']
    y_values22 = tldf['Active Student Cases']
    y_values23 = tldf['Active Staff Cases']
    fig=plt.figure(figsize=(20,10))
    ax=fig.add_subplot(111, label="1")
    ax2=fig.add_subplot(111, label="2", frame_on=False)
    line1, = ax.plot(x_values1, y_values1, color="red", linewidth=3)
    line2, = ax.plot(x_values1, y_values12, color="limegreen", linewidth=3)
    line3, = ax.plot(x_values1, y_values13, color="cornflowerblue", linewidth=3)
    ax.set_xlabel('Date')
    ax.set_xticklabels(ax.get_xticks(), rotation = 90)
    ax.set_ylabel('Cases')
    ax.set_ylim(0,1500)
    ax.set_xlim([datetime.date(2021,7,24), datetime.date(2022,6,7)])
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b-%d'))
    # ax.axvline(datetime.date(2021,8,18), linewidth=2.5, linestyle='--', color='tab:gray', alpha=0.5)
    line4, = ax2.plot(x_values2, y_values2, color="red", linestyle='dashed')
    line5, = ax2.plot(x_values2, y_values22, color="limegreen", linestyle='dashed')
    line6, = ax2.plot(x_values2, y_values23, color="cornflowerblue", linestyle='dashed')
    ax2.set_ylim(0,1500)  
    ax2.set_xlim([datetime.date(2020,7,24), datetime.date(2021,6,7)])
    ax2.axes.xaxis.set_visible(False)
    ax2.axes.yaxis.set_visible(False)
    # ax2.axvline(datetime.date(2020,8,18), linewidth=2.5, linestyle='--', color='tab:gray', alpha=0.5)
    plt.title('Katy ISD Active Cases Compared to Last School Year')
    plt.legend([line1, line2, line3, line4, line5, line6], 
               ["21-22 Total","21-22 Student","21-22 Staff", "20-21 Total","20-21 Student","20-21 Staff"], 
               loc=1, 
               title = 'charzynski.com/katycovidcharts')
    plt.savefig('katyisdcovidnewestplots/09activecasescomparedtolastyear.png', dpi=fig.dpi, bbox_inches='tight')
    plt.show()
    plt.close()
    
    # Plot CALCULATED total active, student, and staff cases
    # fig2 = plt.figure(figsize=(12,10))
    # line1, = plt.plot(tdf.index, tdf['All Active from calculated case type'], color='tab:red', linewidth=7)
    # line2, = plt.plot(tdf.index, tdf['Active Student Cases - calculated'], color='limegreen', linewidth=3.5, linestyle='dashed')
    # line3, = plt.plot(tdf.index, tdf['Active Staff Cases - calculated'], color='cornflowerblue', linewidth=3.5, linestyle='dashed')
    # line4, = plt.plot(tdf.index, tdf['Active Auxiliary Cases - calculated'], color='tab:orange', linewidth=3.5, linestyle='dashed')
    # plt.xlim(['2021-08-25', xmax])
    # plt.xlabel('Date', fontsize=16)
    # plt.xticks(rotation = 90)
    # plt.ylabel('Cases', fontsize=16)
    # plt.title('Katy ISD Active Cases - 2021-2022', fontsize=20)
    # first_day_of_school = '2021-08-18'
    # plt.axvline(first_day_of_school, linewidth=2.5, linestyle='--', color='tab:gray', alpha=0.5)
    # plt.text(first_day_of_school, 300,'First Day of School', rotation=90, ha='center')
    # plt.legend([line1, line2, line3, line4], ['Total Cases','Student Cases','Staff Cases', 'Auxiliary Cases'], loc=2, prop={'size': 14}, title = 'charzynski.com/katycovidcharts')
    # plt.savefig('katyisdcovidnewestplots/02activecasescalculated.png')
    # plt.show()
    # plt.close()
    
    #plot CALCUATED total, elementary, junior high, high, center
    # tdf['All Active from calculated school type']
    # fig2 = plt.figure(figsize=(12,10))
    # line1, = plt.plot(tdf.index, tdf['All Active from calculated school type'], color='tab:red', linewidth=7)
    # line2, = plt.plot(tdf.index, tdf['Active Elementary Cases - calculated'], color='limegreen', linewidth=3.5, linestyle='dashed')
    # line3, = plt.plot(tdf.index, tdf['Active Junior High Cases - calculated'], color='tab:orange', linewidth=3.5, linestyle='dashed')
    # line4, = plt.plot(tdf.index, tdf['Active High School Cases - calculated'], color='cornflowerblue', linewidth=3.5, linestyle='dashed')
    # line5, = plt.plot(tdf.index, tdf['Active Center Cases - calculated'], color='tab:purple', linewidth=3.5, linestyle='dashed')
    # plt.xlim(['2021-08-25', xmax])
    # plt.xlabel('Date', fontsize=16)
    # plt.xticks(rotation = 90)
    # plt.ylabel('Cases', fontsize=16)
    # plt.title('Katy ISD Active Cases - 2021-2022', fontsize=20)
    # first_day_of_school = '2021-08-18'
    # plt.axvline(first_day_of_school, linewidth=2.5, linestyle='--', color='tab:gray', alpha=0.5)
    # plt.text(first_day_of_school, 300,'First Day of School', rotation=90, ha='center')
    # plt.legend([line1, line2, line3, line4, line5], ['Total Cases','Elementary Cases','Junior High Cases', 'High Cases', 'Center Cases'], loc=2, prop={'size': 14}, title = 'charzynski.com/katycovidcharts')
    # plt.savefig('katyisdcovidnewestplots/03activecasesbyschooltypecalculated.png')
    # plt.show()
    # plt.close()
    
    #Cumulative Cases Plot
    fig3 = plt.figure(figsize=(12,10))
    linechart1 = plt.plot(tdf.index, tdf['Cumulative Cases Interpolate'], color='tab:red', linewidth=3.5)
    # linechart2 = plt.plot(tdf.index, tdf['Elementary Cumulative'], color='limegreen', linewidth=3.5)
    # linechart3 = plt.plot(tdf.index, tdf['Junior High Cumulative'], color='tab:orange', linewidth=3.5)
    # linechart4 = plt.plot(tdf.index, tdf['High School Cumulative'], color='cornflowerblue', linewidth=3.5)
    plt.xlabel('Date', fontsize=16)
    plt.xticks(rotation = 90)
    # plt.yscale('log')
    plt.ylabel('Cases', fontsize=16)
    plt.title('Katy ISD Cumulative Cases Since June 1, 2021', fontsize=20)
    first_day_of_school = datetime.date(2021,8,18)
    plt.axvline(first_day_of_school, linewidth=2.5, linestyle='--', color='tab:gray', alpha=0.5)
    plt.text(first_day_of_school, 600,'First Day of School', rotation=90, ha='center')
    plt.annotate('charzynski.com/katycovidcharts', xy=(0.01, .97), xycoords='axes fraction', style='italic', fontsize=12)
    plt.savefig('katyisdcovidnewestplots/03cumulativecases.png')
    plt.show()
    plt.close()
    
    #plot 
    

    
    # #Spaghetti Plot - Molly
    # fig, ax = plt.subplots(figsize=(12,10))
    # for col in tdf.columns:
    #     if col in activecolumns:
    #         if 'Elementary' in col:
    #             line1,  = plt.plot(tdf.index, tdf[col], color='limegreen')
    #         if 'High' in col:
    #             if 'Junior' in col:
    #                 line2,  = plt.plot(tdf.index, tdf[col], color='tab:orange')
    #             else:
    #                 line3,  = plt.plot(tdf.index, tdf[col], color='cornflowerblue')
    #         if 'high' in col:
    #             plt.plot(tdf.index, tdf[col], color='cornflowerblue')
    
    # plt.xlim(datetime.date(2021,8,17), xmax)
    # plt.xlabel('Date', fontsize=16)
    # plt.xticks(rotation = 90)
    # plt.ylim([0,ymax])
    # plt.ylabel('Cases', fontsize=16)
    # title = 'All Schools'
    # plt.title(title, fontsize=20)
    # first_day_of_school = datetime.date(2021,8,18)
    # plt.axvline(first_day_of_school, linewidth=2.5, linestyle='--', color='tab:gray', alpha=0.5)
    # firstdayposition = ymax / 2
    # plt.text(first_day_of_school, firstdayposition,'First Day of School', rotation=90, ha='center')
    # plt.legend([line1, line2, line3], ['Elementary', 'Junior High', 'High'], title = 'charzynski.com/katycovidcharts', loc=2, prop={'size': 14})      
    # #figure out a way to post under the chart the top X schools
    # plt.savefig('katyisdcovidnewestplots/09allschoolspaghettiplot.png')
    # plt.show()
    # plt.close()
    
    #Bar Plot - John
    fig3 = plt.figure(figsize=(20,10))
    barchart1 = plt.bar(activedf.index, activedf[str(update_date)], color=campuspercentcolor)
    plt.ylim([0,ymax])
    plt.xticks(rotation = 90)
    # plt.axhline(20, linewidth=2.5, linestyle='--', color='tab:gray', alpha=0.5)
    for x,y in zip(activedf.index, activedf[str(update_date)]):
        label = "{:.0f}".format(y)
        plt.annotate(label, # this is the text
                     (x,y), # these are the coordinates to position the label
                     textcoords="offset points", # how to position the text
                     xytext=(0,10), # distance from text to points (x,y)
                     ha='center')
    plt.title('Active Cases on ' + str(update_date.strftime("%m/%d/%Y")), fontsize=20)
    plt.ylabel('Active Cases', fontsize=16)
    plt.xlabel('School', fontsize=16)
    plt.legend(barchart1[52:55], 
               ['Elementary', 'Junior High', 'High'], 
               loc=2, title = 'charzynski.com/katycovidcharts') #loc=2
    plt.savefig('katyisdcovidnewestplots/05allschoolbarplot.png', dpi=fig3.dpi, bbox_inches='tight')
    plt.show()
    plt.close()
    
    #Bar Plot - New Cases
    fig3 = plt.figure(figsize=(20,10))
    barchart1 = plt.bar(campusnewcasesdf.index, campusnewcasesdf[str(update_date)], 
                        color=campuspercentcolor)
    plt.xticks(rotation = 90)
    # plt.axhline(20, linewidth=2.5, linestyle='--', color='tab:gray', alpha=0.5)
    for x,y in zip(campusnewcasesdf.index, campusnewcasesdf[str(update_date)]):
        label = "{:.0f}".format(y)
        plt.annotate(label, # this is the text
                     (x,y), # these are the coordinates to position the label
                     textcoords="offset points", # how to position the text
                     xytext=(0,10), # distance from text to points (x,y)
                     ha='center')
    plt.title('New Cases on ' + str(update_date.strftime("%m/%d/%Y")), fontsize=20)
    plt.ylabel('New Cases', fontsize=16)
    plt.xlabel('School', fontsize=16)
    plt.legend(barchart1[52:55], 
           ['Elementary', 'Junior High', 'High'], 
           title = 'charzynski.com/katycovidcharts') #loc=2
    plt.savefig('katyisdcovidnewestplots/06allschoolnewcasesbarplot.png', dpi=fig3.dpi, 
                bbox_inches='tight')
    plt.show()
    plt.close()
    
    #Bar Chart of Percent of Students with Active Case
    fig3 = plt.figure(figsize=(20,10))
    barchart1 = plt.bar(campusstudentpercentdf.index, 
                        campusstudentpercentdf[str(update_date)], 
                        color=campuspercentcolorreal)
    plt.xticks(rotation = 90)
    # plt.axhline(20, linewidth=2.5, linestyle='--', color='tab:gray', alpha=0.5)
    for x,y in zip(campusstudentpercentdf.index, campusstudentpercentdf[str(update_date)]):
        label = "{:.1f}".format(y)
        plt.annotate(label, # this is the text
                     (x,y), # these are the coordinates to position the label
                     textcoords="offset points", # how to position the text
                     xytext=(0,10), # distance from text to points (x,y)
                     ha='center')
    plt.title('Percent of Students with Active Case on ' + str(update_date.strftime("%m/%d/%Y")), fontsize=20)
    plt.ylabel('Percent', fontsize=16)
    plt.xlabel('School', fontsize=16)
    plt.legend(barchart1[38:51], 
           ['Elementary', 'Junior High', 'High'], 
           title = 'charzynski.com/katycovidcharts') #loc=2,
    plt.savefig('katyisdcovidnewestplots/07allschoolpercentstudentbarplot.png', dpi=fig3.dpi, bbox_inches='tight')
    plt.show()
    plt.close()
    
    #Bar Chart of Percent of Staff with Active Case
    fig3 = plt.figure(figsize=(20,10))
    barchart1 = plt.bar(campusstaffpercentdf.index, 
                        campusstaffpercentdf[str(update_date)], 
                        color=campuspercentcolorreal)
    plt.xticks(rotation = 90)
    # plt.axhline(20, linewidth=2.5, linestyle='--', color='tab:gray', alpha=0.5)
    for x,y in zip(campusstaffpercentdf.index, campusstaffpercentdf[str(update_date)]):
        label = "{:.1f}".format(y)
        plt.annotate(label, # this is the text
                     (x,y), # these are the coordinates to position the label
                     textcoords="offset points", # how to position the text
                     xytext=(0,10), # distance from text to points (x,y)
                     ha='center')
    plt.title('Percent of Staff with Active Case on ' + str(update_date.strftime("%m/%d/%Y")), fontsize=20)
    plt.ylabel('Percent', fontsize=16)
    plt.xlabel('School', fontsize=16)
    plt.legend(barchart1[38:51], 
           ['Elementary', 'Junior High', 'High'], 
           title = 'charzynski.com/katycovidcharts') #loc=2,
    plt.savefig('katyisdcovidnewestplots/08allschoolpercentstaffbarplot.png', dpi=fig3.dpi, bbox_inches='tight')
    plt.show()
    plt.close()
    
    # plt.xlim(738019.5, xmax)
    # plt.xlabel('Date', fontsize=16)
    # plt.xticks(rotation = 90)
    # plt.ylim([0,ymax])
    # plt.ylabel('Cases', fontsize=16)
    # title = 'All Schools'
    # plt.title(title, fontsize=20)
    # first_day_of_school = datetime.date(2021,8,18)
    # plt.axvline(first_day_of_school, linewidth=2.5, linestyle='--', color='tab:gray', alpha=0.5)
    # firstdayposition = ymax / 2
    # plt.text(first_day_of_school, firstdayposition,'First Day of School', rotation=90, ha='center')
    # plt.legend([line1, line2, line3], ['Elementary', 'Junior High', 'High'], title = 'charzynski.com/katycovidcharts')      
    # plt.savefig('katyisdcovidnewestplots/09allschoolspaghettiplot.png')
    # plt.show()
    # plt.close()
    
    
    #plots of percent of school type infected
    tdf.index = pd.to_datetime(tdf.index, format='%Y%m%d', unit='D') #might need to use this other places now that I know how to do it
    xvalues = tdf.index
    TotalPercent = tdf['Percent of Total Students with Active Case']
    ElementaryPercent = tdf['Percent of Elementary Students with Active Case']
    JuniorPercent = tdf['Percent of Junior High Students with Active Case']
    HighPercent = tdf['Percent of High School Students with Active Case']
    TotalStaffPercent = tdf['Percent of Total Staff with Active Case']
    ElementaryStaffPercent = tdf['Percent of Elementary Staff with Active Case']
    JuniorStaffPercent = tdf['Percent of Junior High Staff with Active Case']
    HighStaffPercent = tdf['Percent of High School Staff with Active Case']
    width = datetime.timedelta(days=0.15)        # the width of the bars
    
    #student percent
    fig, ax = plt.subplots(figsize=(20,10))
    rects1 = ax.bar(xvalues, TotalPercent, width, color='r')
    rects2 = ax.bar(xvalues + width, ElementaryPercent, width, color='limegreen')
    rects3 = ax.bar(xvalues + width + width, JuniorPercent, width, color='orange')
    rects4 = ax.bar(xvalues+ width + width + width, HighPercent, width, color='cornflowerblue')
    ax.set_ylabel('Percent with Active Cases', fontsize=16)
    ax.set_xlabel('Date', fontsize=16)
    # print(ax.get_xlim()) #useful for determininf lims
    ax.set_xticks(tdf.index + width + width/2)
    plt.xticks(rotation = 90)
    # ax.set_xlim(738030.75,)
    # print(update_date)
    xmax1 = datetime.datetime.strptime(str(update_date), '%Y-%m-%d') + datetime.timedelta(days=1)  
    xmin1 = xmax1 - datetime.timedelta(days=32.25)  
    ax.set_xlim(xmin1, xmax1)
    # print(ax.get_xlim())
    # ax.set_xlim(datetime.date(2021,12,3), datetime.datetime.strptime(str(update_date), '%Y-%m-%d'))
    ax.set_ylim(0,6)
    ax.set_title('Percent of Student Population with Active Cases over Last Month', fontsize=20)
    ax.legend((rects1[0], rects2[0], rects3[0], rects4[0]), ('All','Elementary','Junior High', 'High'), loc=2, title = 'charzynski.com/katycovidcharts')
    plt.savefig('katyisdcovidnewestplots/04aPercentofStudentsWithActiveCases.png', dpi=fig3.dpi, bbox_inches='tight')
    plt.show()
    plt.close()
    
    #staff percent
    fig, ax = plt.subplots(figsize=(20,10))
    rects1 = ax.bar(xvalues, TotalStaffPercent, width, color='r')
    rects2 = ax.bar(xvalues + width, ElementaryStaffPercent, width, color='limegreen')
    rects3 = ax.bar(xvalues + width + width, JuniorStaffPercent, width, color='orange')
    rects4 = ax.bar(xvalues+ width + width + width, HighStaffPercent, width, color='cornflowerblue')
    ax.set_ylabel('Percent with Active Cases', fontsize=16)
    ax.set_xlabel('Date', fontsize=16)
    # print(ax.get_xlim()) #useful for determininf lims
    ax.set_xticks(tdf.index + width + width/2)
    plt.xticks(rotation = 90)
    # ax.set_xlim(738030.75,)
    # print(update_date)
    xmax1 = datetime.datetime.strptime(str(update_date), '%Y-%m-%d') + datetime.timedelta(days=1)  
    xmin1 = xmax1 - datetime.timedelta(days=32.25)  
    ax.set_xlim(xmin1, xmax1)
    # print(ax.get_xlim())
    # ax.set_xlim(datetime.date(2021,12,3), datetime.datetime.strptime(str(update_date), '%Y-%m-%d'))
    ax.set_ylim(0,6)
    ax.set_title('Percent of Staff Population with Active Cases over Last Month', fontsize=20)
    ax.legend((rects1[0], rects2[0], rects3[0], rects4[0]), ('All','Elementary','Junior High', 'High'), loc=2, title = 'charzynski.com/katycovidcharts')
    plt.savefig('katyisdcovidnewestplots/04bPercentofStaffWithActiveCases.png', dpi=fig3.dpi, bbox_inches='tight')
    plt.show()
    plt.close()

    print('Plots completed.')

def visualizebyschool():
    '''
    

    Returns
    -------
    None.

    '''
    import matplotlib.pyplot as plt
    import datetime
    import pandas as pd
    
    #Iterate over data for each school and make plots
    xmax = update_date + datetime.timedelta(days=1)
    tdf.index = pd.to_datetime(tdf.index)
    ymax = 10
    for col in tdf.columns:
        if col in activecolumns:
            column = tdf[col]
            max_value = column.max()
            # print(max_value)
            if max_value > ymax:
                ymax = 5 * round(max_value/5)
                if max_value > ymax:
                    ymax += 5
                    print('Max_value is ', max_value, '.')
    print('y-axis maximum is ', ymax)
    imagecounter = 10
    
    for col in tdf.columns:
        if col in activecolumns:
            campus = col.rstrip(' Active Cases')
            fig3 = plt.figure(figsize=(12,10))
            line1, = plt.plot(tdf.index, tdf[col], color='tab:red', linewidth=8)
            line2, = plt.plot(tdf.index, tdf[campus + ' Active Staff Cases'], color='cornflowerblue', linewidth=4, linestyle='dashed')                
            line3, = plt.plot(tdf.index, tdf[campus + ' Active Student Cases'], color='limegreen', linewidth=4, linestyle='dashed')
            try:
                line4, = plt.plot(tdf.index, tdf[campus + ' Active Auxiliary Cases'], color='tab:orange', linewidth=4, linestyle='dotted')
            except KeyError:
                line4, = plt.plot(tdf.index, tdf[campus + ' Active AuxiliaryCases'], color='tab:orange', linewidth=4, linestyle='dotted')
            
                
            barchart1 = plt.bar(tdf.index, tdf[campus + ' New Cases'], color='lightcoral')
            plt.xlim(datetime.date(2021,8,17), xmax)
            plt.xlabel('Date', fontsize=16)
            plt.xticks(rotation = 90)
            plt.ylim([0,ymax])
            plt.ylabel('Cases', fontsize=16)
            title = col
            plt.title(title, fontsize=20)
            first_day_of_school = datetime.date(2021,8,18)
            plt.axvline(first_day_of_school, linewidth=2.5, linestyle='--', color='tab:gray', alpha=0.5)
            plt.axhline(30, linewidth=2.5, linestyle='--', color='tab:gray', alpha=0.5)
            firstdayposition = ymax / 2
            plt.text(first_day_of_school, firstdayposition,'First Day of School', rotation=90, ha='center')
            # plt.legend([line1, line2, line3, line4], ['Total Cases','Staff','Student', 'Auxiliary (not in Total)'], loc=2, prop={'size': 14}, title = 'charzynski.com/katycovidcharts')
            if campus == 'Davidson Elementary':
                plt.legend([line1, line2, line3, line4, barchart1], ['Total Cases','Staff','Student', 'Auxiliary (not in Total)', 'New Cases (starting 10/9)'], loc=2, prop={'size': 14}, title = 'charzynski.com/katycovidcharts')
            else:
                plt.legend([line1, line2, line3, line4, barchart1], ['Total Cases','Staff','Student', 'Auxiliary (not in Total)', 'New Cases (starting 9/6)'], loc=2, prop={'size': 14}, title = 'charzynski.com/katycovidcharts')
            imagenumber = str(imagecounter)
            schoolfilename = 'katyisdcovidnewestplots/' + imagenumber + col + '.png'
            imagecounter += 1
            plt.savefig(schoolfilename)
            plt.show()
            plt.close()


#TO-DO LIST
#limit/fix campus pull errors
#make campus loading faster
#calculate ratios (1 in XXX)
#write what gets posted
#make a gif of schools above 30
#TypeError: can only concatenate tuple (not "str") to tuple
#new cases different color where interpolating

# getandsavealldata()
# getcampusdata()

extractandcompilealldata()
savecampusdata()
compilecampusdata()

visualizedata()
visualizebyschool()

print('Completed at ', datetime.now())