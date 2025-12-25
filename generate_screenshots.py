import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options  

def capture_screenshots(url="http://localhost:8080"):  
    """Capture screenshots for hackathon submission""" 

    print("📸 Starting screenshot capture...")

    # Set up headless Chrome
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--window-size=1920,1080')    

    driver = webdriver.Chrome(options=options)

    try:
        # Screenshot 1: Upload page
        print("📸 Capturing screenshot 1: Upload interface...")
        driver.get(url)
        time.sleep(2)
        driver.save_screenshot('screenshot_1_upload.png')

        # Screenshot 2: Click sample data and wait for analysis
        print("📸 Capturing screenshot 2: Analysis results...")
        sample_btn = driver.find_element("xpath", "//button[contains(text(), 'Try Sample Data')]")
        sample_btn.click()
        time.sleep(3)  # Wait for analysis
        driver.save_screenshot('screenshot_2_analysis.png')

        # Screenshot 3: Scroll to recommendations      
        print("📸 Capturing screenshot 3: Recommendations...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        driver.save_screenshot('screenshot_3_recommendations.png')

        print("✅ All screenshots captured successfully!")
        print("📁 Files saved: screenshot_1_upload.png, screenshot_2_analysis.png, screenshot_3_recommendations.png")

    finally:
        driver.quit()

if __name__ == "__main__":
    # Install selenium first: pip install selenium     
    capture_screenshots()
