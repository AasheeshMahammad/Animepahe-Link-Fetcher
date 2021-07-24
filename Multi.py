from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as Ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from msedge.selenium_tools import EdgeOptions
from msedge.selenium_tools import Edge
from multiprocessing.pool import ThreadPool
import os, time, sys, pyttsx3, psutil, random
from termcolor import colored
from Skip import Decrypt

global links
links=[]

global invalid
invalid=[]

global t_color
t_color="green"

global print_hold
print_hold=0
if "npr" in sys.argv:
    print_hold=1

global set_hdl
set_hdl=[1,1,0,2]

if "break" in sys.argv:
    set_hdl[2]=1

global set_img
set_img=[0,0,0,0]

global jnp_eng
jnp_eng=1
if "eng" in sys.argv:
    jnp_eng=0

global max_threads
max_threads=9


for i in sys.argv:
    if "max_threads" in i:
        try:
            i=int(i.split("=")[-1])
        except:
            break
        if 1 <= i <= 24:
            max_threads=int(i)+1
        break


def set_driver(**kwargs):
    hdl=kwargs.get("hdl",0)
    img=kwargs.get("img",0)
    ch=kwargs.get("ch",0)
    a=1
    chrome_driver='chromedriver.exe'
    if check_argv(["-e","-E","edge","Edge"])==1:
        a=2
    if a==1:
        options = ChromeOptions()
        if hdl==1:
            options.add_argument("--headless")
        if img==1:
            options.add_experimental_option("prefs",{'profile.managed_default_content_settings.images':2})  # don't load images
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation","enable-logging"])
        options.add_argument('--log-level=3')
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--window-size=1920x1080")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        options.add_argument("test-type")
        #options.add_experimental_option("prefs",{"profile.default_content_setting_values.notifications" : 2})
        if set_img[3]==1 and ch==1:
            load = DesiredCapabilities().CHROME
            #load["pageLoadStrategy"] = "normal"  #  complete
            load["pageLoadStrategy"] = "eager"    #  interactive
            #load["pageLoadStrategy"] = "none"    #  undefined
            #print("pref",flush=True)
            driver = webdriver.Chrome(desired_capabilities=load,executable_path=chrome_driver, options=options)
            return driver
        driver = webdriver.Chrome(chrome_driver, options=options)
        return driver
    elif a==2:
        edge_options = EdgeOptions()
        edge_options.use_chromium = True
        if hdl==1:
            edge_options.add_argument('headless')
        edge_options.add_argument('disable-gpu')
        driver = Edge(executable_path="msedgedriver.exe",options=edge_options)
        return driver


def check_argv(a):
    for i in a:
        if i in sys.argv:
            return 1
    return 0

def get_arg(arg):
    for i in sys.argv:
        if arg in i:
            return i.split('=')[-1]
    return 0

def set_ar():
    if check_argv(["do"])==1:
        sys.argv.append("dec")
        sys.argv.append("no_et")
    if check_argv(["-h","-H","head","Head"])==1:
        set_hdl[0]=set_hdl[1]=0
    if "dec" in sys.argv:
        set_img[3]=1
    if check_argv(["img","-i","-I"])==1:
        set_img[0]=set_img[1]=1
    if check_argv(["-s","-S","speak","Speak"])==1:
        set_img[2]=1
    colors=["grey","red","green","yellow","blue","magenta","cyan","white"]
    if get_arg('color') in colors:
        t_color=get_arg('color')
    if "colors" in sys.argv:
        print(colors)
        quit()
    if check_argv(["kill","clean"])==1:
        if check_argv(["chrome","edge"])==1:
            clean(1)
            quit()
        clean()
        quit()
    if check_argv(["help","Help","--help","--Help"])==1:
        print("\nclean :To clean Left out Drivers","Speak :To Notify With Voice","img :To Stop Loading Of Images",sep="\n")
        print("Edge :To Use Edge Instead Of Chrome",sep="\n")
        quit()


def check(a):
    if "http" in a:
        return 1
    else:
        return 0


def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.runAndWait()
    pyttsx3.speak(text)

def download_check():
    dl_wait = True
    path_=""
    while dl_wait:
        time.sleep(1)
        dl_wait = False
        for fname in os.listdir(path_):
            if fname.endswith('.crdownload'):
                dl_wait = True

def get_screenshot(driver):
    fn=''
    for i in range(10):
        fn+=str(random.randint(10,99))
    driver.get_screenshot_as_file(f"{fn}.png")

def download_files():
    temp=[]
    for i in links:
        temp.append(i.split("-")[-1].strip())
    driver=set_driver(hdl=0,img=set_img[1])
    for i in range(len(temp)):
        driver.get(temp[i])
        if i==0:
            input("Waiting...")
        down=WebDriverWait(driver,20).until(Ec.presence_of_element_located((By.TAG_NAME, 'button')))
        down.click()
        try:
            driver.switch_to.window(driver.window_handles[1])
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        except:
            #time.sleep(1)
            pass
    download_check()
    driver.quit()

def selectskip(driver,ch=1):
    if 0 < set_hdl[2] < set_hdl[3]:
        cur="None"
        if(print_hold==1):
            print(colored(". ",t_color),end="",flush=True)
        else:
            print(colored(f"{len(links)} Out of {ep_max_count} Done...",t_color),end='\r',flush=True)
        return cur
    time.sleep(5)
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(5)
    cur=""
    rt=0
    try:
        driver.implicitly_wait(4)
        time.sleep(2)
        driver.implicitly_wait(2)
        while True:
            #driver.implicitly_wait(2)
            add_skip = WebDriverWait(driver,20).until(Ec.presence_of_element_located((By.ID, 'skip_bu2tton')))
            #driver.implicitly_wait(1)
            #time.sleep(1.5)
            cur = add_skip.get_attribute('href')
            rt=rt+1
            if rt==750:
                if check(str(cur))==0:
                    cur="None"
                    driver.quit()
                else:
                    driver.quit()
                break
            if check(cur)==1:
                driver.quit()
                #time.sleep(.5)
                break
            else:
                continue
    except:
        cur="None"
        driver.quit()
    #time.sleep(.2)
    #driver.quit()
    if ch==1:
        if(print_hold==1):
            print(colored(". ",t_color),end="",flush=True)
        else:
            print(colored(f"{len(links)} Out of {ep_max_count} Done...",t_color),end='\r',flush=True)
    #time.sleep(.5)

    return str(cur)


def get_index(sel,stop=0):
    index = 0
    if len(sel) > 1:
        dict_in={};sel1=[];indices=[];jpc=1;count=0
        if jnp_eng==1:
            count=1
        elif jnp_eng==0:
            count=2
        for i in range(0,len(sel)):
            dict_in[i]=sel[i].text
            sel1.append(sel[i].text)
        rm_key=[]
        for key in dict_in:
            if "p eng (" in dict_in[key] or "eng" in dict_in[key]:
                rm_key.append(key)
        rm_key.sort(reverse=True)
        tmp=sel1.copy();eng=[]
        if len(rm_key)!=len(tmp):
            for i in rm_key:
                eng.append(dict_in[i])
                tmp.remove(dict_in[i])
        #print(dict_in)
        if len(eng)==0:
            count=1
        for cn in range(0,count):
            for i in range(0,len(tmp)):
                hld=tmp[i].split("-")
                for y in hld:
                    if "(" in y and ")" in y:
                        tmp[i]=y
                    if "eng" in tmp[i]:
                        tmp[i]=tmp[i].replace("eng","")
                try:
                    tmp[i]=int(tmp[i].split("p")[0].strip())
                except:
                    pass
            tmp.sort(reverse=True)
            index=-1
            for i in sel1:
                if (str(tmp[0]) in i and jpc==1) or ((str(tmp[0]) in i) and (str("p eng") in i) and(jnp_eng==0 and jpc==0)):
                   for key, value in dict_in.items():
                       if i==value:
                           index=key
                           indices.append(key)
                           if jnp_eng==0:
                                if len(eng) > 0:
                                    tmp=eng.copy()
                                    jpc=0
                                else:
                                    tmp=[]
                           break
                if index!=-1:
                    break
        if jnp_eng==0 and len(eng) > 0:
            index=indices[1]
        else:
            index=indices[0]
    elif len(sel)==1:
        index=0
    if (0> index  or index> len(sel)):
        if(stop < 900):
            temp=get_index(sel,stop+1)
            if(temp[0]!=None):
                index=temp[0]
            else:
                index=-1
        else:
            return None,None
    if index!=None:
        try:
            size=int(sel[index].text.split("-")[-1].split("(")[-1].split(")")[0].replace("MB",""))
        except:
            size=0
        #print(size)
        return index,size


def link_fetch(a,ch=1):
    driver=set_driver(hdl=set_hdl[1],img=set_img[1],ch=ch)
    driver.get(a)
    #driver.find_element_by_tag_name("html").send_keys(Keys.END) --scroll down--
    if ch==1:
        if(print_hold==1):
            print(colored(". ",t_color),end="",flush=True)
    #time.sleep(.15)
    #down = driver.find_element_by_id('downloadMenu')
    #driver.execute_script(f'window.open("{a}","_blank");')
    #driver.close()
    #driver.switch_to.window(driver.window_handles[1])
    #driver.execute_script("scroll(0, 250);")
    down=driver.find_elements_by_xpath("//div[@class='col-12 col-sm-3']")
    down[-1].click()
    while False:
        try:
            driver.execute_script("arguments[0].click();",down[-1])
            break;
        except:
            pass
    time.sleep(1)
    try:
        driver.switch_to.window(driver.window_handles[1])
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    except:
        #time.sleep(1)
        pass
    epm=driver.find_element_by_tag_name('h1')
    #print("clicked")
    epm=str(epm.text)
    epm=epm.split("-")[-1].replace("Online" ,"").strip()
    epm=int(epm)
    #print(".",end=" ",flush=True)
    sel=[]
    i=0
    while(True):
        i=i+1
        sel = driver.find_element_by_xpath('//div[@id="pickDownload"]')
        sel = sel.find_elements_by_tag_name('a')# //div[@id="pickDownload"]#//a[@class="dropdown-item"]
        if(len(sel)!=0 or i==500):
            break
        try:
            down[-1].click()
            driver.switch_to.window(driver.window_handles[1])
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        except:
            #time.sleep(1)
            pass
    #print(len(sel),flush=True)
    index,size=get_index(sel)
    if index==None:
        invalid.append(int(epm)-1)
        driver.quit()
        return
    val=0;cur="";d_cur=""
    if set_img[3]==1:
        if 0 < set_hdl[2] < set_hdl[3]:
            sel=None
        try:
            #time.sleep(.4)
            d_cur=str(Decrypt(str(sel[index].get_attribute('href'))))
        except:
            #print(epm-1,len(sel),index,flush=True)
            driver.quit()
            invalid.append(int(epm)-1)
            return
        d_cur=str(epm)+"-"+d_cur
    try:
        #time.sleep(.4)
        if ch==1:
            if set_img[3]==1:
                 if check(d_cur)==1:
                    links.append(d_cur)
                 else:
                    invalid.append(int(epm)-1)
                 if(print_hold==1):
                    print(colored(". ",t_color),end="",flush=True)
                 else:
                    print(colored(f"{len(links)} Out of {ep_max_count} Done...",t_color),end='\r',flush=True)
                 #time.sleep(.6)
                 driver.close()
                 driver.quit()
                 return
        #sel[index].click()
        driver.execute_script("arguments[0].click();", sel[index])
    except:
        val=1
        driver.quit()
    #time.sleep(.2)
    driver.close()
    if val==0:
        if ch==1:
            cur=selectskip(driver)
        if ch==0:
            cur=selectskip(driver,0)
    if val==1:
        invalid.append(int(epm)-1)
    else:
        if check(cur)==0:
            invalid.append(int(epm)-1)
        else:
            li=str(epm)+"-"+cur
            links.append(li)
            if ch==0 and set_img[3]==1:
                if li==d_cur:
                    set_img[3]=1
                else:
                    set_img[3]=0


def check_diff(l1, l2):
    l_diff = [i for i in l1 + l2 if i not in l1 or i not in l2]
    return l_diff



def clean(cr=0):
    n=0
    for proc in psutil.process_iter():
        try:
            if "chromedriver" in proc.name() or "msedgedriver" in proc.name() or (cr==1 and "chrome" in proc.name()) or (cr==1 and "msedge" in proc.name()):
                proc.kill()
                n=n+1
        except:
            pass
    print(str(n)+" "+"Processess have been cleaned")




def click_ep(driver):
    ep=[]
    try:
        pg_len=driver.find_element_by_xpath('//a[@title="Go to the Last Page"]')
        pg_count=int(pg_len.get_attribute('data-page'))
        asc=driver.find_elements_by_tag_name('label')
        if "asc" in asc[0].find_element_by_tag_name('input').get_attribute("id"):
            asc[0].click()
        else:
            asc[1].click()
        time.sleep(1)
        for i in range(1,pg_count):
            hold=1
            while True:
                try:
                    tmp=driver.find_elements_by_xpath('//a[@class="play"]')
                    time.sleep(.3)
                    for y in tmp:
                        ep.append(y.get_attribute('href'))
                    if(hold==1):
                        driver.find_element_by_xpath('//a[@class="page-link next-page"]').click()
                        hold=0
                    if i==pg_count-1:
                        time.sleep(1)
                        #driver.find_element_by_xpath('//a[@title="Go to the Last Page"]').click()
                        tmp=driver.find_elements_by_xpath('//a[@class="play"]')
                        for y in tmp:
                            ep.append(y.get_attribute('href'))
                    time.sleep(1)
                    break
                except:
                    pass
        return list(set(ep))
    except:
        ep = driver.find_elements_by_class_name('play')
        for i in range(0,len(ep)):
            tmp=ep[i].get_attribute('href')
            ep[i]=tmp
        return list(set(ep))


def find_count(driver):
    driver.implicitly_wait(3)
    time.sleep(2)
    count = driver.find_element_by_class_name('episode-count')
    temp = count.text.split('(')[1]
    count_val = temp.split(')')[0]
    name = driver.find_element_by_xpath('//h1')
    return int(count_val), name.text


def find_title(title,driver):
    driver.execute_script("document.body.style.zoom = '150%';")
    driver.get('https://animepahe.com/')
    #driver.implicitly_wait(2)
    query=f"document.getElementsByName('q')[0].value='{title}'"
    search = driver.find_element_by_xpath("//input[@class='input-search']")
    search.clear()
    driver.execute_script(query)
    search.send_keys(" ")
    # get_screenshot(driver)
    # time.sleep(2)
    #get_screenshot(driver)
    try:
        temp = WebDriverWait(driver, 10).until(Ec.presence_of_element_located((By.CLASS_NAME, "result-status")))
        return 1
    except:
        driver.quit()
        return 0


def cal(a,n):
    tmp=a
    b=0
    while tmp >= n:
        tmp=tmp-n
        b=b+1
    if tmp>0:
        b=b+1
    return b


def sor(val):
    return int(val.split("-")[0])
    
def fix_name(name):
    inval = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for i in inval:
        if i=='"':
            name = name.replace(i, '')
        else:
            name = name.replace(i, ' ')
    return name


def check_count(a=0):
    file = open("D:/New folder/Links/Links/" + "Temp" + '.txt', 'r',encoding="utf-8")
    Content = file.read()
    lin = Content.split("\n")
    file.close()
    tmp_list=[]
    if a==1:
        for i in lin:
            if "-" in i:
                tmp_list.append(i)
        tmp_list.sort(key=sor)
        return tmp_list
    for i in lin:
        if "-" in i:
            tmp_list.append(int(i.split("-")[0])-1)
    tmp_list.sort()
    return tmp_list


def fix(ep_links,max_threads):
    invalid.sort()
    '''if len(ep_links)!=len(check_count()):
            tmp_links=check_count()
            tmp_num=[ i for i in range(0,len(ep_links))]
            tmp_invalid=check_diff(tmp_num,tmp_links)
            for i in tmp_invalid:
                if i not in invalid:
                    invalid.append(i)'''
    if len(invalid)==1:
        print(colored(f"{invalid} Link Is Broken, Trying To Fix...",'red'),end='\n')
    else:
        print(colored(f"{invalid} Links are Broken, Trying To Fix...",'red'),end='\n')
    dict_threads={}
    tmp_links=[]
    if max_threads > len(invalid)+1:
        if len(invalid)==1:
            max_threads=2
        else:
            max_threads=len(invalid)+1
    for i in invalid:
        tmp_links.append(ep_links[i])
    for i in range(1,max_threads):
        dict_threads[i]=cal(len(invalid),i)
    dict_threads=sorted(dict_threads.items(), key =lambda x:(x[1], x[0]))
    if print_hold==1:
        for i in range(0,2*len(invalid)+1):
            if i==2*len(invalid):
                print(colored(".",t_color),flush=True)
            else:
                print(colored(".",t_color),end=" ",flush=True)
    invalid.clear()
    #print(dict_threads)
    #input("Wait...")
    if __name__ == '__main__':
        ThreadPool(dict_threads[0][0]).map(link_fetch,tmp_links)
    if print_hold==1:
        print(colored(".",t_color),flush=True)
    else:
        print(colored(f"{len(links)} Out of {ep_max_count} Done...",t_color),flush=True)
    if 0 < set_hdl[2] < set_hdl[3]:
        set_hdl[2]=set_hdl[2]+1


def get(driver,max_threads):
    ep_count, find = find_count(driver)
    find=fix_name(find)
    ep_li = click_ep(driver)
    ep_count=len(ep_li)
    ep_links=ep_li.copy()
    driver.quit()
    print("Title :", find,flush=True)
    print("No. of Episodes :", ep_count,flush=True)
    #sys.stdout.flush()
    val=0
    if check_argv(["test","Test","multi"])==1:
        val=1
    else:
        val = input("Continue :")
        try:
            val = int(val)
        except:
            #print("Error")
            quit()
    if (val == 1):
        dict_threads = {};inc=-1
        if check_argv(["no_et"])==1:
            inc=0
        for i in range(1,max_threads):
            dict_threads[i]=cal(ep_count+inc,i)
        dict_threads=sorted(dict_threads.items(), key =lambda x:(x[1], x[0]))
        #print("Number Of Threads :",dict_threads[0][0])
        #print("Estimated Time :",round((dict_threads[0][1]+1)*(26.4839688142+2),10),"Seconds")
        start = time.time()
        #selectp_1(ep_links[0],0)
        # file = open("D:/New folder/Links/Links/" + "Temp" + '.txt', 'w+',encoding="utf-8")
        # file.close()
        thread_count=dict_threads[0][0]
        global ep_max_count
        ep_max_count=len(ep_links)
        for i in sys.argv:
            if "set_threads" in i:
                try:
                    i=int(i.split("=")[-1])
                except:
                    break
                if 0 < i < 25:
                    thread_count=i
                break
        if check_argv(["no_et"])!=1 or ep_count==1:
            link_fetch(ep_links[0],0)
            time_taken=time.time()-start
        if ep_count > 1:
            dec=2
            ep_links1=ep_links.copy()
            if check_argv(["no_et"])!=1:
                if set_img[3]==0:
                    print("Estimated Time :", round((dict_threads[0][1] + 1) * (time_taken + 2.8), 10)+15, "Seconds",flush=True)
                else:
                    print("Estimated Time :", round((dict_threads[0][1] + 1) * (time_taken-4.5), 10)+15, "Seconds",flush=True)
                ep_links1.pop(0)
            else:
                dec=0
            #os.system("")
            if print_hold==1:
                for i in range(0,2*ep_count-dec+1):
                    if i==2*ep_count-dec:
                        print(colored(".",t_color))
                    else:
                        print(colored(".",t_color),end=" ")
            else:
                print(colored("Fetching Links...","green"),flush=True)
            #time.sleep(.5)
            if __name__ == '__main__':
                ThreadPool(thread_count).map(link_fetch,ep_links1)
            if ep_max_count > 1:
                if print_hold==1:
                    print(colored(".",t_color),flush=True)
                else:
                    print(colored(f"{len(links)} Out of {ep_max_count} Done...",t_color),flush=True)
        '''else:
            dict_threads={}
            for i in range(1,9):
                dict_threads[i]=cal(ep_count+1,i)
            dict_threads=sorted(dict_threads.items(), key =lambda x:(x[1], x[0]))
            for i in range(0,2*ep_count+1):
                if i==2*ep_count:
                    print(colored(".",t_color))
                else:
                    print(colored(".",t_color),end=" ")
            if __name__ == '__main__':
                ThreadPool(dict_threads[0][0]).map(link_fetch,ep_links)
            print(colored(".",t_color),flush=True)'''
        '''if ep_count!=len(check_count()):
            tmp_links=check_count()
            tmp_num=[ i+1 for i in range(0,ep_count)]
            tmp_invalid=check_diff(tmp_num,tmp_links)
            for i in tmp_invalid:
                if i not in invalid:
                    invalid.append(i)'''
        while len(invalid) > 0:
            fix(ep_links,max_threads)
        links.sort(key=sor)
        path=""
        file = open(path + str(find) + ".txt", 'w+',encoding="utf-8")
        file.write(find + '\r\n')
        file.close()
        file_path=path + str(find) + '.txt\"'
        file = open(path + str(find) + '.txt', 'a+',encoding="utf-8")
        for i in links:
            file.write(i + '\r\n')
        file.close()
        if set_img[2]==1:
           speak("Done")
        #clean()
        print("All Saved")
        print("Total Time Taken :",round(time.time() - start,10), "Seconds")
        '''if "auto" in sys.argv
            download_files()
        '''
        invalid.clear()
        links.clear()
        if check_argv(["Download","download"])==1:
            #time.sleep(2)
            #os.system("cls")
            os.system(f"python DNC.py name=\"{str(find)}.txt\"")
        #print("Data Need to Download :",down_size)
    #driver.quit()


def main_block(title="",cho=0):
    st = 1
    #os.environ["WDM_LOG_LEVEL"] = str(logging.WARNING)
    while st == 1:
        if(cho==0):
            os.system("cls")
            if get_arg("title")!=0:
                find=get_arg('title')
            else:
                find = input('Enter Name :').strip()
        else:
            find=title
        if find=="":
            quit()
        driver=set_driver(hdl=set_hdl[0],img=set_img[0])
        val = find_title(find,driver)
        if val == 1:
            result = driver.find_elements_by_xpath("//div[@class='result-title']")
            rep = driver.find_elements_by_xpath("//div[@class ='result-status']")
            dt = driver.find_elements_by_xpath("//div[@class ='result-season']")
            #sys.stdout.flush()
            if cho==0:
                print("Search Results :")
                for i in range(0, len(result)):
                    print(str(i + 1) + "." + str(result[i].text) + ",", str(rep[i].text)+",",str(dt[i].text),flush=True)
                    #sys.stdout.flush()
            choose=1
            choices=[]
            if len(result)==1:
                choose=1
            else:
                if cho==0:
                    choose=input("Select :")
                    try:
                        choose=choose.split(",")
                        if(len(choose) > 1):
                            choices=choose.copy()
                            choices.pop(0)
                            if len(choices) > 0:
                                os.system("cls")
                            choose=choose[0]
                        elif(len(choose)==1):
                            choose=choose[0]
                    except:
                        pass
                elif cho!=0:
                    choose=cho
                try:
                    choose = int(choose)
                except:
                    #print("Error")
                    driver.quit()
                    quit()
            if choose > 0:
                if choose > len(result):
                    driver.quit()
                    return choices,find
                choose = choose - 1
                driver.find_elements_by_class_name("result-title")[choose].click()
                get(driver,max_threads)
                if len(choices) > 0:
                    return choices,find
            else:
                driver.quit()
            #start=time.time()
        elif val == 0:
            print("Title Not Found")
        #print("Total Time Taken :",time.time()-start, "Seconds")
        '''st = input("Retry :")
        try:
            st=int(st)
        except:
            pass'''
        st=0
        if st==0:
            break
    return None,None


def main():
    set_ar()
    arr,name=main_block()
    if(arr!=None):
        for i in arr:
            main_block(name,i)


if __name__=="__main__":
    main()