import json
import os
import sys

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from time import sleep

import JsonParser

collect_tags = ['button', 'input', 'label', 'h2', 'li']

options = Options()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument("--start-maximized")

print("testing started")
driver = webdriver.Chrome(options=options)
driver.get("https://tprdn.centennialcollege.ca:7443/applicationNavigator/seamless")

def recursive(root, widgets):
    elements = root.find_elements(By.XPATH, "*")
    for element in elements:
        # print(element.tag_name)
        if ((element.tag_name in collect_tags)
            and (element.location['x'] != 0 and element.location['y'] != 0)
            and (element.location['x'] != -1920)
            and (element.location['x'] != 3840)
        ) :
            unit = {}
            unit['type'] = element.tag_name
            unit['display'] = element.text
            unit['location'] = element.location
            unit['id'] = element.get_attribute('id')
            unit['xpath'] = get_xpath(element)
            junit = json.dumps(unit)
            print(junit)

            unit.pop('type')
            unit.pop('display')
            unit.pop('location')
            junit = json.dumps(unit)
            print(junit)

        subs = root.find_elements(By.XPATH, "*")
        if len(subs) > 0:
            recursive(element, widgets)

def get_xpath(element):
    xpath = driver.execute_script("""
                    function getElementXPath(element) {
                        var paths = [];
                        while (element.nodeType === Node.ELEMENT_NODE) {
                            var index = 0;
                            var siblings = element.parentNode.childNodes;
                            for (var i = 0; i < siblings.length; i++) {
                                var sibling = siblings[i];
                                if (sibling === element) {
                                    paths.unshift(element.nodeName.toLowerCase() + (index > 0 ? '[' + (index + 1) + ']' : ''));
                                    break;
                                }
                                if (sibling.nodeType === Node.ELEMENT_NODE && sibling.nodeName === element.nodeName) {
                                    index++;
                                }
                            }
                            element = element.parentNode;
                        }
                        return paths.length ? '/' + paths.join('/') : null;
                    }
                    return getElementXPath(arguments[0]);
                """, element)

    return xpath

def output_elements_id(root):
    inputs = root.find_elements(By.TAG_NAME, 'input')

    for input in inputs:
        print(input.location)
        if input.location['x'] != 0 and input.location['y'] != 0:
            xpath = driver.execute_script("""
                function getElementXPath(element) {
                    var paths = [];
                    while (element.nodeType === Node.ELEMENT_NODE) {
                        var index = 0;
                        var siblings = element.parentNode.childNodes;
                        for (var i = 0; i < siblings.length; i++) {
                            var sibling = siblings[i];
                            if (sibling === element) {
                                paths.unshift(element.nodeName.toLowerCase() + (index > 0 ? '[' + (index + 1) + ']' : ''));
                                break;
                            }
                            if (sibling.nodeType === Node.ELEMENT_NODE && sibling.nodeName === element.nodeName) {
                                index++;
                            }
                        }
                        element = element.parentNode;
                    }
                    return paths.length ? '/' + paths.join('/') : null;
                }
                return getElementXPath(arguments[0]);
            """, input)

            print("XPath of the element: ", xpath)

            print(input.get_attribute('id'))


print()

account = JsonParser.loadJsonFromFile('account.json')
login_ID = driver.find_element(By.ID, 'usernameUserInput')
login_pwd = driver.find_element(By.ID, 'password')

user = driver.find_element(By.XPATH, '/html/body/div/div/div/div/form/div/div/input')
user.send_keys(account['ID'])

user = driver.find_element(By.XPATH, '/html/body/div/div/div/div/form/div/div[2]/input')
user.send_keys(account['Password'])

while True:
    try:
        title = driver.find_element(By.XPATH, '/html/body/nav[5]/div/div[1]/ul/li[3]/h2')
        if title is not None:
            print('================  ' + title.text + '  ===============')
    except:
        pass

    root = driver.find_element(By.XPATH, '/html')
    try:
        widgets = {}
        recursive(root, widgets)
        print(widgets)
    except:
        pass
    sleep(10)

'''output_elements_id(root)

user = driver.find_element(By.XPATH, '/html/body/div/div/div/div/form/div/div/input')
user.send_keys('Username found')

user = driver.find_element(By.XPATH, '/html/body/div/div/div/div/form/div/div[2]/input')
user.send_keys('Passssssssssssssssssssssssss found')
'''
# sleep(10)