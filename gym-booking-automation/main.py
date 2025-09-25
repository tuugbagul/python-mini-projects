from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import os
import time

ACCOUNT_EMAIL = "tugba@test.com"
ACCOUNT_PASSWORD = "tugbagul"
GYM_URL = "https://appbrewery.github.io/gym/"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach",True)

user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
driver = webdriver.Chrome(options=chrome_options)

driver.get(GYM_URL)
wait = WebDriverWait(driver,10)
login_button = wait.until(ec.element_to_be_clickable((By.ID,"login-button")))
login_button.click()

email_input = wait.until(ec.presence_of_element_located((By.ID, "email-input")))
email_input.clear()
email_input.send_keys(ACCOUNT_EMAIL)

password_input = wait.until(ec.presence_of_element_located((By.ID,"password-input")))
password_input.clear()
password_input.send_keys(ACCOUNT_PASSWORD)

submit_button = driver.find_element(By.ID, "submit-button")
submit_button.click()

wait.until(ec.presence_of_element_located((By.ID,"schedule-page")))
class_cards = driver.find_elements(By.CSS_SELECTOR, "div[id^='class-card-']")

booked_count = 0
waitlist_count = 0
already_booked_count = 0

processed_classes = []

for card in class_cards:
    day_group = card.find_element(By.XPATH, "./ancestor::div[contains(@id,'day-group')]")
    day_title = day_group.find_element(By.TAG_NAME,"h2").text
    time = card.find_element(By.CSS_SELECTOR, "p[id^='class-time-']").text

    if ("Tue" in day_title) or ("Thu" in day_title and "6:00 PM" in time):
        class_name = card.find_element(By.CSS_SELECTOR,"h3[id^='class-name-']").text
        button = (card.find_element(By.CSS_SELECTOR,"button[id^='book-button-']"))

        class_info = f"{class_name} on {day_title}"

        if button.text == "Booked":
            already_booked_count += 1
            print(f"✓ Already booked: {class_info}")
        elif button.text == "Waitlisted":
            already_booked_count += 1
            print(f"✓ Already on waitlist: {class_info} ")
        elif button.text == "Book Class":
            booked_count += 1
            button.click()
            processed_classes.append(f"• [New Booking] {class_info}")
            print(f"✓ Successfully Booked: {class_info}")
        elif button.text == "Join Waitlist":
            waitlist_count += 1
            button.click()
            processed_classes.append((f"• [New Waitlist] {class_info}"))
            print(f"✓ Joined waitlist for: {class_info}")


print("\n------BOOKING SUMMARY-----")
print(f"New bookings: {booked_count}")
print(f"New waitlist entries: {waitlist_count}")
print(f"Already booked/waitlisted: {already_booked_count}")
print(f"Total Tuesday & Thursday 6pm classes processed: {booked_count + waitlist_count + already_booked_count}")

print("\n--- DETAILED CLASS LIST ---")
for class_detail in processed_classes:
    print(f"\n {class_detail}")


