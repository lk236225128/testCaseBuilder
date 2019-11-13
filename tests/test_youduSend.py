from time import sleep


def swipe_down(driver, x_pecent):
    """
    向上滑动屏幕
    :param locator:
    :return:
    """
    # 打印屏幕高和宽
    print(driver._driver.get_window_size())
    # 获取屏幕的高
    x = driver._driver.get_window_size()['width']
    # 获取屏幕宽
    y = driver._driver.get_window_size()['height']

    # 滑屏，向下
    driver.swipe(x_pecent * x, 1 / 7 * y, x_pecent * x, 6 / 7 * y, 500)
    sleep(5)


def swipe_up(driver, x_pecent):
    """
    向上滑动屏幕
    :param locator:
    :return:
    """
    # 打印屏幕高和宽
    print(driver.get_window_size())
    # 获取屏幕的高
    x = driver.get_window_size()['width']
    # 获取屏幕宽
    y = driver.get_window_size()['height']

    # 向上滑动，第五个参数，时间设置大一点，否则容易看不到滑动效果
    driver.swipe(x_pecent * x, 6 / 7 * y, x_pecent * x, 1 / 7 * y, 500)
    sleep(5)

class TestYoudu(object):
    def test_getlist(self, getDriver):
        getDriver.find_element_by_xpath('//*[@text="8891福委會"]').click()
        getDriver.find_element_by_xpath('// android.support.v7.widget.LinearLayoutCompat').click()

        elements=getDriver.find_elements_by_id("im.xinda.youdu:id/people_name_textview")
        print(elements)
        for i in elements:
            print(i.text)
        elements2=getDriver.find_elements_by_id("im.xinda.youdu:id/people_job_textview")
        print(elements2)
        for i in elements2:
            print(i.text)
        sleep(5)

        swipe_up(getDriver,x_pecent=0.7)

        elements3 = getDriver.find_elements_by_id("im.xinda.youdu:id/people_name_textview")
        print(elements3)
        for i in elements3:
            print(i.text)

        assert False




