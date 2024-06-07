from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException

# Job application details
APPLICANT_NAME = "Miguel Rowe"
APPLICANT_EMAIL = "Miguelrowe428@gmail.com"
APPLICANT_PHONE = "914-830-0799"

# Job search URLs
JOB_SEARCH_URLS = [
    "https://fbijobs.gov/special-agents?gad_source=1&gclid=Cj0KCQjwqdqvBhCPARIsANrmZhPNErqoZdojlzaZ6EIuwkWduJnmgcMgItKDWbdogdG_TvFiUkNo3PAaAjNCEALw_wcB",
    "https://www.indeed.com/jobs?l=Hamilton%2C+NJ&radius=10&vjk=20206854565e05ea",
    "https://www.indeed.com/q-part-time-19-year-old-job-l-new-jersey-jobs.html?vjk=fc8c2526cd0aa6aa",
    "https://www.indeed.com/q-teen-l-township-of-hamilton,-nj-jobs.html?vjk=17e5f8e5a8774c07",
    "https://www.simplyhired.com/search?q=teen+jobs&l=township+of+hamilton%2C+nj",
    "https://www.hireteen.com/location/new-jersey/hamilton/",
    "https://www.hireteen.com/",
    "https://www.snagajob.com/search/w-hamilton+square,+nj/q-minimum+age+16+years+old",
    "https://www.monster.com/career-advice/article/teen-jobs-0617",
    "https://www.glassdoor.com/Job/jobs.htm?sc.keyword=teen",
    "https://www.linkedin.com/jobs/search?keywords=Teen%20Jobs&location=New%20Jersey&geoId=&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0",
    "https://www.careerbuilder.com/jobs-teen-in-nj",
    "https://www.ziprecruiter.com/candidate/search?search=teen&location=New%20Jersey"
]

def setup_driver():
    """Initializes and returns a Chrome WebDriver instance."""
    driver = webdriver.Chrome()
    return driver

def fill_application_form(driver, name, email, phone):
    """Fills out the job application form."""
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "name")))
        driver.find_element(By.NAME, "name").send_keys(name)
        driver.find_element(By.NAME, "email").send_keys(email)
        driver.find_element(By.NAME, "phone").send_keys(phone)
        driver.find_element(By.CSS_SELECTOR, ".css-hwq2i0").click()

        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, ".icl-u-xs-mt-2.css-1ge9ozh.e17bl7461"), "Thanks for your message")
        )
    except (TimeoutException, NoSuchElementException, ElementNotInteractableException) as e:
        print(f"Error filling application form: {e}")

def apply_to_jobs(driver, urls, name, email, phone):
    """Iterates through job search URLs and applies to jobs."""
    for url in urls:
        try:
            driver.get(url)
            WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".jobsearch-SerpJobCard")))
            
            job_cards = driver.find_elements(By.CSS_SELECTOR, ".jobsearch-SerpJobCard")
            for job_card in job_cards:
                try:
                    apply_button = job_card.find_element(By.CSS_SELECTOR, ".jobsearch-SerpJobCard .jobsearch-ReusableJobComponentButtonColorless .jobsearch-ReusableJobComponentButtonLink")
                    driver.execute_script("arguments[0].click();", apply_button)  # Use JavaScript to click the button
                    fill_application_form(driver, name, email, phone)
                except NoSuchElementException as e:
                    print(f"Error locating apply button or filling form: {e}")
        except TimeoutException as e:
            print(f"Error loading job listings: {e}")

def main():
    driver = setup_driver()
    try:
        apply_to_jobs(driver, JOB_SEARCH_URLS, APPLICANT_NAME, APPLICANT_EMAIL, APPLICANT_PHONE)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
