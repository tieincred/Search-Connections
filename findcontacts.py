from selenium import webdriver
import time
# import keyboard
import pandas as pd
from selenium.webdriver.common.keys import Keys


from flask import send_file
import os


class extract:
    def __init__(self, username, password, multiple = False, filename = None):
        self.username = username
        self.password = password
        self.multiple = multiple
        self.filename = filename


    def extract_contacts(self, company=None, position=None):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("window-size=1920x1080")
        chrome_options.add_argument("--enable-javascript")
#         wd = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)

        wd = webdriver.Chrome('chromedriver',options=chrome_options)
        login_link = 'https://www.linkedin.com/uas/login'
        wd.get(login_link)
        time.sleep(10)

        elementID = wd.find_element_by_id('username')
        elementID.send_keys(self.username)
        elementID = wd.find_element_by_id('password')
        elementID.send_keys(self.password)
        elementID.submit()

        time.sleep(10)
        search_var = company + ' ' + position
        global_search = '//*[@id="global-nav-typeahead"]/input'
        global_element = wd.find_elements_by_xpath(global_search)
        print(global_element)
        print(global_element[0].text)
        global_element[0].send_keys(search_var)
        time.sleep(2)
        global_element[0].send_keys(Keys.RETURN)
        # time.sleep(2)
        # global_element[0].sendKeys(Keys.RETURN)
        time.sleep(5)
        fullel = wd.find_elements_by_xpath('/html/body')
        fullel[0].send_keys(Keys.RETURN)
        time.sleep(2)
        result_item = 'entity-result__item'
        search_res = wd.find_elements_by_class_name(result_item)
        search_res[0].click()
        time.sleep(3)
        print(wd.current_url)

        infourl = wd.current_url+'detail/contact-info/'
        wd.get(infourl)
        time.sleep(10)
        contact_card = 'ember-view'
        cont_card = wd.find_elements_by_class_name(contact_card)
        det = (cont_card[0].text).split("\n")
        cont_dict = {}
        cont_dict['Name'] = det[1]
        usages = ['Profile', 'Phone', 'Email']
        for i in range(3,len(det)):
            if i%2==0:
                cont_dict[det[i-1]] = det[i]
        update = {}
        update['Name'] = det[1]
        for k,v in cont_dict.items():
            for i in usages:
                if i in k:
                    update[k] = v
        wd.quit()
        return update

    def contacts_extraction(self, company=None, position=None):
        if self.multiple == False:
            dict_val = self.extract_contacts(company,position)
            print(dict_val)
            return dict_val

        if self.multiple == True:
            x = pd.read_csv(self.filename, header=None)
            print(x)
            profile = []
            email = []
            phone = []
            name = []
            for i, j in zip(x[0], x[1]):
                emails = False
                phones = False
                try:
                    di = (self.extract_contacts(i,j))
                    for k,v in di.items():
                        if k=='Name':
                            name.append(v)
                        elif 'Profile' in k:
                            profile.append(v)
                        elif 'Phone' in k:
                            phone.append(v)
                            phones = True
                        else:
                            email.append(v)
                            emails = True
                    if not phones:
                        phone.append('Not found')
                    if not emails:
                        email.append('Not found')
                except:
                    name.append('No profile found')
                    profile.append('No profile found')
                    email.append('No profile found')
                    phone.append('No profile found')
                    pass
            x['Names'] = name
            x['Profile'] = profile
            x['Email'] = email
            x['Phone'] = phone
            x.to_csv('Contact_Results.csv')
            time.sleep(3)
            # send_file('Contact_Results.csv',as_attachment=True)

if __name__ == '__main__':
    # new = extract('tausifiqbal10@gmail.com','mechanical.18',multiple=True,filename='static/files/testfile.txt')
    # new.contacts_extraction()
    new1 = extract('tausiffreelance10@gmail.com','tausiffreelance')
    new1.contacts_extraction('genesisAI', 'CEO')

# [<selenium.webdriver.remote.webelement.WebElement (session="69f6e6b71d61e4826887483134c92428", element="c7dca282-4a5f-4246-a946-ca38ff2f1154")>]



