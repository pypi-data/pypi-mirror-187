"""
Author      : Lorenzo Feng (正崽不emo)
Date        : 2023/1/20
Description : Help with your tasks of Hangzhou Safety Education Question
"""
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time

login_url = r'https://hangzhou.xueanquan.com/login.html'
driver_path = r'.\chromedriver.exe'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')  # 无头模式
chrome_options.add_argument('--disable-gpu')

browser = webdriver.Chrome(options=chrome_options, executable_path=driver_path)


def ge(xpath):
    return browser.find_element(By.XPATH, xpath)


def ges(xpath):
    return browser.find_elements(By.XPATH, xpath)


def login(_account, pwd):
    browser.implicitly_wait(30)
    browser.maximize_window()
    browser.get(url=login_url)

    browser.switch_to.frame("wx-login")
    browser.execute_script('document.getElementsByTagName("span")[0].click()')

    ge("//*[@id=\"app\"]/div/div[1]/div[2]/form/div[1]/div/div/input").send_keys(_account)
    ge("//*[@id=\"app\"]/div/div[1]/div[2]/form/div[2]/div/div/input").send_keys(pwd)
    ge("//*[@id=\"app\"]/div/div[1]/div[2]/form/button").click()

    try:
        en = ge('/html/body/div/div/div/button')
        if en:
            en.click()
    except NoSuchElementException:
        pass

    i = 0
    print("[*] %s logging... " % _account)
    timeout = 5
    while '欢迎你' not in browser.find_elements(By.TAG_NAME, "span")[0].text:
        time.sleep(2)
        i += 1
        if i == timeout:
            print("[-] Failed to login.")
            return False
    else:
        print("[+] Login succeeded.")
        return True


def get_tasks():
    ge('/html/body/div[3]/div/div[2]/div/a[4]').click()
    btns = browser.find_elements_by_xpath('//a[@class=\'learn-btn\']')
    tags = browser.find_elements_by_xpath('//a[@class=\'learn-btn\']/preceding-sibling::p[2]')

    _tasks = []
    for i in range(len(btns)):
        flag = '安全学习' == tags[i].text
        _tasks.append([btns[i], flag, False])

    return _tasks


def safe_study_solution(_task):
    _task[0].click()

    print('[*] solving...')
    browser.switch_to.window(browser.window_handles[-1])

    script = '''
        var WcContent = "";
        testinfo = "已掌握技能";
        var testanswer = "0|0|0";
        var testMark = 20 * rightnum;
        var CourseID = $("#CourseID").val();
        if (userInfo.regionalAuthority != 0) {
            $("#buzhou2").hide();
            $("#buzhou2s").show();
            $("#buzhou2ss").hide();
            $(".bto_testbox").hide();
            $("#yes").show();
            location.href = "#top";
        } else {
            insertCourseStatus_New(userInfo.prvId, 20 * rightnum, function (res) {
                if (res && res.result) {
                    $("#buzhou2").hide();
                    $("#buzhou2s").show();
                    $("#buzhou2ss").hide();
                    $(".bto_testbox").hide();
                    $("#yes").show();
                    location.href = "#top";
                }
                else {
                    $("#input_button").click(function () {
                        clickkThree();
                    });
                    layer.msg(res.message);
                }
            })
        }
    '''
    browser.execute_script(script)
    browser.close()
    print('[+] Done')
    browser.switch_to.window(browser.window_handles[0])


def video_solution(_task):
    _task[0].click()
    print('[*] solving...')
    browser.switch_to.window(browser.window_handles[-1])

    for li in browser.find_elements_by_class_name('noact'):
        browser.implicitly_wait(3)
        li.click()
        ge('/html/body/div[1]/div[2]/div[2]/div[1]/div/div/a').click()
    browser.close()
    print('[+] Done')
    browser.switch_to.window(browser.window_handles[0])


def help_me(_account, _pwd):
    try:
        if not login(_account, _pwd):
            return
        print('[*] Getting Tasks...')
        tasks = get_tasks()
        print('[+] Done.')
        task_number0 = 0  # video solution number
        for task in tasks:
            if not task[1]:
                task_number0 += 1

        print('[+] Question Tasks:%d\tVideo Tasks:%d' % (len(tasks) - task_number0, task_number0))

        for task in tasks:
            if task[1]:
                safe_study_solution(task)
            else:
                video_solution(task)

    finally:
        browser.quit()


if __name__ == '__main__':
    help_me('fengtangzheng', 'jDT3TBALkZ8rJ78')
