from selenium.webdriver.common.by import By

def get_text_by_selector(container, selector):
    if selector.startswith("//"):
        elem = container.find_elements_by_xpath(selector)
    else:
        elem = container.find_elements(By.CLASS_NAME, selector)

    if len(elem) > 0:
        return next(iter(elem)).text.replace('\n',' ').strip()
    else: 
        print(f'Missing value for selector {selector}')
        return ''
