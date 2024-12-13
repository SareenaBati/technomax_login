import time
import re
import random
import string

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


# pytest fixture to set up and tear down the web driver
@pytest.fixture()
def driver():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


# Function to check if string is a valid email address
def is_valid_email(email):
    email_pattern = r"^[a-z]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
    return bool(re.search(email_pattern, email))


# Function to generate random data
def generate_random_email_address():
    domain = "test.com"
    email_length = 5
    random_string = ''.join(random.choice(string.ascii_lowercase) for _ in range(email_length))
    return random_string + "@" + domain


def generate_random_first_name():
    return ''.join(random.choices(string.ascii_letters, k=6))


def generate_random_last_name():
    return ''.join(random.choices(string.ascii_letters, k=6))


def generate_random_phone_number():
    return "98" + ''.join(random.choices(string.digits, k=8))


def generate_random_message():
    return ''.join(random.choices(string.ascii_letters, k=50))


# Generate random data for 5 test cases
random_data = [
    (
        generate_random_first_name(),
        generate_random_last_name(),
        generate_random_email_address(),
        generate_random_phone_number(),
        generate_random_message(),
    )
    for _ in range(5)
]


# Test the function to fill form with random data
@pytest.mark.parametrize("first_name,last_name,email_address,phone_number,message", random_data)
def test_form_filling(driver, first_name, last_name, email_address, phone_number, message):
    driver.get("https://technomax.com.np/")
    driver.maximize_window()

    # Scroll to the form
    target_y = 6000
    scroll_distance = 1000
    current_y = 0

    while current_y < target_y:
        driver.execute_script(f"window.scrollBy(0, {scroll_distance});")
        current_y += scroll_distance
        time.sleep(0.25)

    # Locate the fields and fill them with random data
    first_name_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@id='form_name']"))
    )
    last_name_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@id='form_lastname']"))
    )
    email_address_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@id='form_email']"))
    )
    phone_number_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@id='form_phone']"))
    )
    message_field = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//textarea[@id='form_message']"))
    )

    # Fill the form fields
    first_name_field.clear()
    first_name_field.send_keys(first_name)
    time.sleep(0.75)

    last_name_field.clear()
    last_name_field.send_keys(last_name)
    time.sleep(0.75)

    if is_valid_email(email_address):
        email_address_field.clear()
        email_address_field.send_keys(email_address)
    else:
        print("Invalid email address")
    time.sleep(0.75)

    phone_number_field.clear()
    phone_number_field.send_keys(phone_number)
    time.sleep(0.75)

    message_field.clear()
    message_field.send_keys(message)
    time.sleep(0.75)

    # Print the values for verification
    print(f"First Name: {first_name}")
    print(f"Last Name: {last_name}")
    print(f"Phone Number: {phone_number}")
    print(f"Email Address: {email_address}")
    print(f"Message: {message}")
