from selenium import webdriver
def write_to_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
options = webdriver.ChromeOptions()
options.add_argument("--auto-open-devtools-for-tabs")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
options.add_argument("--start-maximized")
options.add_argument("--incognito")
options.add_argument("--enable-javascript")
options.add_argument('--no-sandbox')
options.add_argument('--disable-setuid-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--headless=new")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")

if __name__=="__main__":
    #Passed in by manager
    input={'URL': 'https://modesens.com/product/givenchy-women-straw-medium-voyou-basket-shopping-bag-brown-107056049/?srsltid=AfmBOopaeFWB1EfjVueUNeuLWF9SBGWBGEYC4EF-Wcb8IehkINLozNHl', 'Variations': ['BB50V9B1UC-105'], 'Level': 'modesens', 'Currency': 'Wrong Currency'}
    driver = webdriver.Chrome(options=options)
    URL = input.get("URL","")
    driver.get(URL)
    page_source = driver.execute_script("return document.documentElement.outerHTML;")
    print(page_source)
    file_name="output.html"
    write_to_file(file_name,page_source)
    #Save page source to s3 url and add to output
    s3_url=""
    input["html_url"]=s3_url
    output=input
    #return output to GetProductData