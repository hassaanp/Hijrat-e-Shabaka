from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
driver = webdriver.Firefox()
driver.get("http://localhost:3000")
assert "Nova-Neutron Migration" in driver.title
elem = driver.find_element_by_id("user")
elem.send_keys("admin")
elem = driver.find_element_by_id("tenant")
elem.send_keys("admin")
elem = driver.find_element_by_id("pswd")
elem.send_keys("nomoresecrete")
elem = driver.find_element_by_id("ip")
elem.send_keys("172.19.25.33")
elem.send_keys(Keys.RETURN)
driver.find_element_by_css_selector('li').click()
driver.find_element_by_css_selector('li').click()
driver.find_element_by_css_selector('li').click()
driver.find_element_by_id("button").click()
try:
    WebDriverWait(driver, 60).until(EC.alert_is_present(),
                                   'Timed out waiting for PA creation ' +
                                   'confirmation popup to appear.')

    alert = driver.switch_to_alert()
    alert.accept()
    print "alert accepted"
except TimeoutException:
    print "no alert"
