from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from have_class import have_class_today
import time

#检测是否存在子行
def isNormalrow(str):
    if '正常' in str:
        return True
    else:
        return False

#今天有没有 名为Classname的课程
def HaveClassToday(classnumber):
    localtime=time.localtime()



# 当测试好能够顺利爬取后，为加快爬取速度可设置无头模式，即不弹出浏览器
# 添加无头headlesss 使用chrome headless
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
kebiao_browser = webdriver.Chrome(chrome_options=chrome_options)
# kebiao_browser=webdriver.Chrome()

#----请自定义你的用户密码-------------------------------

username=''
passwd=''


#读取本地数据
try:
    with open("kb.txt","r") as kb_file:
        kb_lists=eval(kb_file.read())
except FileNotFoundError:
    #不存在则
    #爬取每周课表 并存到一个list里
    kebiao_browser.get('http://jwc.cqupt.edu.cn/kebiao/kb_stu.php?xh='+username)
    open_list=kebiao_browser.find_element_by_partial_link_text("列表查询")
    open_list.click()
    #定位课表表格所在元素
    kb_table=kebiao_browser.find_element_by_id('kbStuTabs-list')
    #定位每一行所在元素
    kb_content_tr=kb_table.find_elements_by_tag_name('tr')
    #将课标处理储存到list里
    kb_lists=[]
    temp_list=[]

    for a_content_tr in kb_content_tr[1:]:
        kb_content_td=a_content_tr.find_elements_by_tag_name('td')
        for a_content_td in kb_content_td:
            temp_list.append(a_content_td.text)
        kb_lists.append(temp_list[:])
        temp_list.clear()


    #fix-up 由于存在rowspan 所以需要对 kb_list 进行fix-up
    i=0
    while i < len(kb_lists):
        if(len(kb_lists[i])!=3):
            kb_lists[i][1]=kb_lists[i][1].split('-')[0]
        if(len(kb_lists[i])==3):
            j=0
            while j <= i:
                if kb_lists[i][0]==kb_lists[j][5]:
                    kb_lists[i]=kb_lists[j][:5]+kb_lists[i]
                j+=1
        i+=1
    print(kb_lists)

    local_kb=open("kb.txt","w")
    local_kb.write(str(kb_lists))
    local_kb.close()


#打开重邮教务在线主页
qiandao_denglu_brower=webdriver.Chrome()
qiandao_denglu_brower.get('http:/jwc.cqupt.edu.cn')
#打开主页右上角登录button
login_button=qiandao_denglu_brower.find_element_by_class_name('loginButton')
login_button.click()
#点击页中登录tab
login_tabs=qiandao_denglu_brower.find_element_by_id('loginTabs')
login_tabs.click()

#输入用户名 密码登录
input_username=qiandao_denglu_brower.find_element_by_id('username')
input_username.send_keys(username)

input_passwd=qiandao_denglu_brower.find_element_by_id('password')
input_passwd.send_keys(passwd)

submit_button=qiandao_denglu_brower.find_element_by_class_name('img1')
submit_button.click()
#保存当前页面句柄
main_window=qiandao_denglu_brower.current_window_handle

#根据存储的课表和当天日期进行签到
qiandao_button=qiandao_denglu_brower.find_element_by_partial_link_text('学生学习问卷')
qiandao_button.click()


to_window=qiandao_denglu_brower.window_handles

for handle in to_window:
    if handle == main_window:
        continue
qiandao_denglu_brower.switch_to.window(handle)

for list in kb_lists:
    if have_class_today(list):
        buttons=qiandao_denglu_brower.find_elements_by_class_name('kchChoose')
        for button in buttons:
            button_calss_name=button.find_element_by_xpath('..')
            if list[1] in button_calss_name.text:
                button.click()
                qiandao_denglu_brower.maximize_window()
                js="var q=document.documentElement.scrollTop=10000"
                qiandao_denglu_brower.execute_script(js)
                radio=qiandao_denglu_brower.find_elements_by_name('xxfs')[1]




exit()
