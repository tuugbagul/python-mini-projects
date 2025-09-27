from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, NoSuchElementException
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

def retry(func,retries=7, description=None):
    for i in range(retries):
        print(f"Trying {description}. Attempt: {i + 1}")
        try:
            return func()
        except TimeoutException:
            if i == retries - 1:
                raise
            time.sleep(1)

def login():
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

    wait.until(ec.presence_of_element_located((By.ID, "schedule-page")))

def book_class(booking_button):
    booking_button.click()
    wait.until(lambda d: booking_button.text == "Booked")

retry(login, description="login")

booked_count = 0
waitlist_count = 0
already_booked_count = 0
processed_classes = []

class_cards = driver.find_elements(By.CSS_SELECTOR, "div[id^='class-card-']")

for card in class_cards:
    day_group = card.find_element(By.XPATH, "./ancestor::div[contains(@id,'day-group')]")
    day_title = day_group.find_element(By.TAG_NAME,"h2").text
    time_text = card.find_element(By.CSS_SELECTOR, "p[id^='class-time-']").text

    if ("Tue" in day_title or "Thu" in day_title) and "6:00 PM" in time_text:
        class_name = card.find_element(By.CSS_SELECTOR,"h3[id^='class-name-']").text
        button = (card.find_element(By.CSS_SELECTOR,"button[id^='book-button-']"))

        class_info = f"{class_name} on {day_title}"

        if button.text == "Booked":
            print(f"✓ Already booked: {class_info}")
            already_booked_count += 1

        elif button.text == "Waitlisted":
            print(f"✓ Already on waitlist: {class_info} ")
            already_booked_count += 1

        elif button.text == "Book Class":
            retry(lambda: book_class(button), description="booking")
            print(f"✓ Successfully Booked: {class_info}")
            booked_count += 1
            processed_classes.append(f"• [New Booking] {class_info}")
            time.sleep(0.5)
        elif button.text == "Join Waitlist":
            retry(lambda: book_class(button),description="waitlisting")
            print(f"✓ Joined waitlist for: {class_info}")
            waitlist_count += 1
            processed_classes.append((f"• [New Waitlist] {class_info}"))
            time.sleep(0.5)

total_booked = booked_count + waitlist_count + already_booked_count
print(f"\nTotal Tuesday & Thursday 6pm classes processed: {total_booked}")
print("\n--- VERIFYING ON MY BOOKINGS PAGE ---")

def get_my_bookings():
    my_bookings_button = driver.find_element(By.ID,"my-bookings-link")
    my_bookings_button.click()

    wait.until(ec.presence_of_element_located((By.ID, "my-bookings-page")))

    cards = driver.find_elements(By.CSS_SELECTOR,"div[id*='card-']")

    if not cards:
        raise TimeoutException("No booking cards found - page may not have loaded")
    return cards

all_cards = retry(get_my_bookings,description="get my bookings")

verified_count = 0

for card in all_cards:
    try:
        when_paragraph = card.find_element(By.XPATH,".//p[strong[text()='When:']]")
        when_text = when_paragraph.text

        if ("Tue" in when_text or "Thu" in when_text) and "6:00 PM" in when_text:
            class_name = card.find_element(By.TAG_NAME,"h3").text
            print(f"✓ Verified: {class_name}")
            verified_count += 1
    except NoSuchElementException:
        pass

print("\n--- VERIFICATION RESULT ---")
print(f"Expected: {total_booked} bookings")
print(f"Found: {verified_count} bookings")

if total_booked == verified_count:
    print("✅ SUCCESS: All bookings verified!")
else:
    print(f"❌ MISMATCH: Missing {total_booked - verified_count} bookings")










