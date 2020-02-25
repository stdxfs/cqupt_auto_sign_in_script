import time,re
with open("kb.txt", "r") as kb_file:
    kb_lists = eval(kb_file.read())
def have_class_today(classlist):
    localtime=time.localtime()
    xingqi=localtime.tm_wday+1
    kaixue_day=55
    today=localtime.tm_yday
    #格式化处理
    tokens=re.split("星期|第|节|周| ",classlist[6])

    while tokens.count(""):
        tokens.remove("")

    #只支持 n-m周：3   (n-p周 o-n周）:4 n-m周单双周：4
    if int(tokens[0])==localtime.tm_wday+1:
        if len(tokens)== 3: #n-m 周
            start_week=int(tokens[2].split("-")[0])-1
            end_week=int(tokens[2].split("-")[1])-1
            if today-(kaixue_day+7*start_week)>=0 and today-(kaixue_day+7*end_week)<=0:
                return True
        elif len(tokens)==4:
            if tokens.count("单") or tokens.count("双"):
                start_week = tokens[2].split("-")[0] - 1
                end_week = tokens[2].split("_")[1] - 1
                if today-(kaixue_day+7*start_week)>=0 and today-(kaixue_day+7*end_week)<=0:
                    if tokens.count("单") and ((today-kaixue_day)/7)%2==1:
                        return True
                    elif tokens.count("双")  and ((today-kaixue_day)/7)%2==0:
                        return True
            else:
                start_week_0=int(tokens[2].split('-')[0])-1
                end_week_0=int(tokens[2].split('-')[1])-1
                start_week_1=int(tokens[3].split('-')[0])-1
                end_week_1=int(tokens[3].split('-')[1])-1
                if (today-(kaixue_day+7*start_week_0))>=0 and (today-(kaixue_day+7*end_week_0)<=0):
                    return True
                elif (today-(kaixue_day+7*start_week_1))>=0 and (today-(kaixue_day+7*end_week_1)<=0):
                    return True
                else:
                    return False
    else:
        return False


for list in kb_lists:
    if have_class_today(list):
        print(list)
