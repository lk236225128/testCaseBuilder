import pytest
from appium import webdriver


APPIUM_LOCAL_HOST_URL = 'http://localhost:4723/wd/hub'
PLATFORM_VERSION = '9'

@pytest.fixture(scope="function")
def getDriver(request):
    desired_caps = {
        'appPackage': 'im.xinda.youdu',
        'appActivity': 'im.xinda.youdu.ui.activities.DefaultActivity',
        'platformName': 'android',
        'platformVersion': PLATFORM_VERSION,
        'deviceName': '4d9b81a6',
        "noReset": True,
        'autoGrantPermissions': True,
        'automationName': "uiautomator2"
    }
    driver = webdriver.Remote(APPIUM_LOCAL_HOST_URL, desired_caps)
    driver.implicitly_wait(5000)

    return driver
