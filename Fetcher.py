from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as Ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from msedge.selenium_tools import EdgeOptions
from msedge.selenium_tools import Edge
from multiprocessing.pool import ThreadPool
import os, time, sys, pyttsx3, psutil, random
from termcolor import colored
from pahe import decode
import re

global episode_links
episode_links={}

global invalid
invalid=[]

global set_attr
set_attr={"title_page_image_disable":True,"fetch_page_image_disable":True,"speak":False,"title_headless":True,
          "fetch_headless":True,"term_color":"green","max_threads":9,"english":False, "debug": False}


def set_driver(**kwargs):
    headless=kwargs.get("headless",False)
    image_disable=kwargs.get("image_disable",False)
    use_chrome=True
    chrome_driver='../drivers/chromedriver.exe'
    if check_argv(["-e","edge"]):
        use_chrome=False
    if use_chrome:
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless")
        if image_disable:
            options.add_experimental_option("prefs",{'profile.managed_default_content_settings.images':2})  # don't load images
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation","enable-logging"])
        options.add_argument('--log-level=3')
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--window-size=1920x1080")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-gpu") #--test this--------------------------------------------------
        options.add_argument("test-type")
        #options.add_argument("user-data-dir=D:/New Folder/Data/Chrome_Test_Profile")
        #options.add_experimental_option("prefs",{"profile.default_content_setting_values.notifications" : 2})
        load = DesiredCapabilities().CHROME
        #load["pageLoadStrategy"] = "normal"  #  complete
        load["pageLoadStrategy"] = "eager"    #  interactive
        #load["pageLoadStrategy"] = "none"    #  undefined
        #print("pref",flush=True)
        driver = webdriver.Chrome(desired_capabilities=load,executable_path=chrome_driver, options=options)
        return driver
    else:
        edge_options = EdgeOptions()
        edge_options.use_chromium = True
        if headless:
            edge_options.add_argument('headless')
        edge_options.add_argument('disable-gpu')
        driver = Edge(executable_path="../drivers/msedgedriver.exe",options=edge_options)
        return driver


def check_argv(a):
    for i in a:
        if i in set(sys.argv):
            return True
    return False

def get_arg(arg):
    for i in sys.argv:
        if arg in i:
            return i.split('=')[-1]
    return -1

def set_ar():
    for i in range(1,len(sys.argv)):
        sys.argv[i]=sys.argv[i].lower()
    for i in sys.argv:
        if "max_threads" in i:
            try:
                val=int(i.split("=")[-1])
            except:
                if i=='max_threads':
                    val=24
                else:
                    continue
            if 1 <= val <= 24:
                set_attr["max_threads"]=int(val)+1
        if "set_threads" in i:
            try:
                val=int(i.split("=")[-1])
            except ValueError:
                continue
            if 0 < val < 25:
                set_attr['set_threads']=val
    if check_argv(["eng"]):
        set_attr["english"]=True
    if check_argv(["-h","head"]):
        set_attr["title_headless"]=set_attr["fetch_headless"]=False
    if check_argv(["img","-i"]):
        set_attr["title_page_image_disable"]=set_attr["fetch_page_image_disable"]=True
    if check_argv(["-s","speak"]):
        set_attr["speak"]=True
    colors=["grey","red","green","yellow","blue","magenta","cyan","white"]
    if get_arg('color') in colors:
        set_attr["term_color"]=get_arg('color')
    if check_argv(["colors"]):
        print(colors)
        os._exit(1)
    if check_argv(["kill","clean"]):
        brow_kill=False
        if check_argv(["chrome","edge"]):
            brow_kill=True
        clean(brow_kill)
        os._exit(1)
    if check_argv(["debug"]):
        set_attr["debug"] = True
    if check_argv(["help","--help"]):
        print("\nclean :To clean Left out Drivers","Speak :To Notify With Voice","img :To Stop Loading Of Images",sep="\n")
        print("Edge :To Use Edge Instead Of Chrome",sep="\n")
        os._exit(1)


def is_valid_url(a):
    if "http" in a and "#pleasewait" not in a:
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
    path_="C:\\Users\\Aasheesh\\Downloads\\"
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
    for i in episode_links:
        temp.append(i.split("-")[-1].strip())
    driver=set_driver(headless=0,image_disable=set_attr["fetch_page_image_disable"])
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

def selectskip(driver):
    time.sleep(5)
    driver.switch_to.window(driver.window_handles[0])
    #time.sleep(5)
    cur=""
    rt=0
    try:
        #driver.implicitly_wait(4)
        #time.sleep(2)
        #driver.implicitly_wait(2)
        while True:
            #driver.implicitly_wait(2)
            add_skip = WebDriverWait(driver,20).until(Ec.presence_of_element_located((By.XPATH, "//a[@class = 'btn btn-secondary btn-block redirect']")))
            #driver.implicitly_wait(1)
            #time.sleep(1.5)
            cur = add_skip.get_attribute('href')
            rt=rt+1
            if rt==750:
                if is_valid_url(str(cur))==0:
                    cur="None"
                    driver.quit()
                else:
                    driver.quit()
                break
            if is_valid_url(cur)==1:
                driver.quit()
                #time.sleep(.5)
                break
            else:
                continue
    except Exception as e:
        print(e)
        cur="None"
        driver.quit()
    #time.sleep(.2)
    #driver.quit()
    print(colored(f"{len(episode_links)} Out of {ep_max_count} Done...",set_attr["term_color"]),end='\r',flush=True)
    #time.sleep(.5)

    return str(cur)

def get_index(sel):
    options = [(i, val.text.lower()) for i,val in enumerate(sel)]
    japanese = [op for op in options if 'eng' not in op[1]]
    english = [op for op in options if 'eng' in op[1]]
    quality = lambda x: int(re.findall(r'(\d+)p', x[1])[0])
    get_size = lambda x: int(re.findall(r'(\d+)mb', x[1])[0])
    japanese.sort(key=quality, reverse=True)
    english.sort(key=quality, reverse=True)
    option = None
    if len(japanese) > 0 or (len(english) == 0 and set_attr['english']):
        option = japanese[0]
    else:
        option = english[0]
    index = option[0]
    size = get_size(option)
    return index, size

def link_fetch(link):
    driver=set_driver(headless=set_attr["fetch_headless"],image_disable=set_attr["fetch_page_image_disable"])
    #driver.minimize_window()
    driver.set_page_load_timeout(15)
    driver.get(link)
    episode_num=driver.find_element(By.XPATH,"//button[@id='episodeMenu']")
    #print("clicked")
    episode_num=str(episode_num.text)
    #driver.find_element_by_tag_name("html").send_keys(Keys.END) --scroll down--
    #time.sleep(.15)
    #driver.execute_script(f'window.open("{a}","_blank");')
    down = driver.find_element(By.ID,'downloadMenu')
    actions= ActionChains(driver)
    actions.click(on_element=down)
    actions.perform()
    #time.sleep(1)
    try:
        driver.switch_to.window(driver.window_handles[1])
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        actions.perform()
    except :
        #time.sleep(1)
        pass
    #print(".",end=" ",flush=True)
    sel=[]
    i=0
    while True:
        try:
            actions.perform()
            driver.switch_to.window(driver.window_handles[1])
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        except IndexError:
            #time.sleep(1)
            pass
        i=i+1
        sel = driver.find_element(By.XPATH,'//div[@id="pickDownload"]')
        sel = sel.find_elements(By.TAG_NAME,'a')# //div[@id="pickDownload"]#//a[@class="dropdown-item"]
        try:
            if ((len(sel)!=0 and sel[0].text!='') or i>=500):
                break
        except Exception as e:
            pass
    index,size=get_index(sel)
    if set_attr['debug']:
        temp=[i.text for i in sel]
        print(temp,index,sel)
    if index==None:
        invalid.append(link)
        driver.quit()
        return
    d_cur=""
    try:
        #time.sleep(.4)
        temp = str(sel[index].get_attribute('href'))
        driver.close()
        driver.quit()
        d_cur=str(decode(temp))
    except (IndexError,TypeError) as e:
        #print(episode_num-1,len(sel),index,flush=True)
        driver.quit()
        invalid.append(link)
        #print(e)
        return
    if is_valid_url(d_cur)==1:
        episode_links[episode_num]=d_cur
        print(colored(f"{len(episode_links)} Out of {ep_max_count} Done...",set_attr["term_color"]),end='\r',flush=True)
    else:
        invalid.append(link)
        return
    #time.sleep(.6)


def clean(browser_kill=False):
    n=0
    for proc in psutil.process_iter():
        try:
            if "chromedriver" in proc.name() or "msedgedriver" in proc.name() or (browser_kill and "chrome" in proc.name()) or (browser_kill and "msedge" in proc.name()):
                proc.kill()
                n=n+1
        except:
            pass
    print(str(n)+" "+"Processess have been cleaned")


def click_ep(driver):
    ep=[]
    try:
        pg_len=driver.find_element(By.XPATH,'//a[@title="Go to the Last Page"]')
        pg_count=int(pg_len.get_attribute('data-page'))
        asc=driver.find_elements(By.TAG_NAME,'label')
        if "asc" in asc[0].find_element(By.TAG_NAME,'input').get_attribute("id"):
            asc[0].click()
        else:
            asc[1].click()
        time.sleep(1)
        for i in range(1,pg_count):
            hold=1
            while True:
                try:
                    tmp=driver.find_elements(By.XPATH,'//a[@class="play"]')
                    time.sleep(.3)
                    for y in tmp:
                        ep.append(y.get_attribute('href'))
                    print(colored(f"Page {i} of {pg_count}",set_attr["term_color"]),end='\r')
                    if(hold==1):
                        driver.find_element(By.XPATH,'//a[@class="page-link next-page"]').click()
                        hold=0
                    if i==pg_count-1:
                        time.sleep(1)
                        #driver.find_element(By.XPATH,'//a[@title="Go to the Last Page"]').click()
                        tmp=driver.find_elements(By.XPATH,'//a[@class="play"]')
                        for y in tmp:
                            ep.append(y.get_attribute('href'))
                    time.sleep(1)
                    break
                except:
                    pass
        print(colored(f"Page {pg_count} of {pg_count}",set_attr["term_color"]))
        return list(set(ep))
    except:
        ep = driver.find_elements(By.CLASS_NAME,'play')
        print(colored("Page 1 of 1",set_attr["term_color"]))
        for i in range(0,len(ep)):
            tmp=ep[i].get_attribute('href')
            ep[i]=tmp
        return list(set(ep))


def find_count(driver):
    driver.implicitly_wait(3)
    time.sleep(2)
    count = driver.find_element(By.CLASS_NAME,'episode-count')
    temp = count.text.split('(')[1]
    count_val = temp.split(')')[0]
    name = driver.find_element(By.XPATH,'//h1')
    name = name.text.split('\n')[0]
    return int(count_val), name


def find_title(title,driver):
    driver.execute_script("window.open('','_blank');")
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    driver.get('https://animepahe.com/')
    #driver.implicitly_wait(2)
    query=f"document.getElementsByName('q')[0].value='{title}';"
    search = driver.find_element(By.XPATH,"//input[@class='input-search']")
    search.clear()
    #driver.execute_script(query)
    search.send_keys(title)
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


    
def fix_name(name):
    inval = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for i in inval:
        if i=='"':
            name = name.replace(i, '')
        else:
            name = name.replace(i, ' ')
    return name


def fix(ep_links):
    if len(invalid)==1:
        print(colored(f"A link is Broken, Trying To Fix...",'red'),end='\n')
    else:
        print(colored(f"{len(invalid)} Links are Broken, Trying To Fix...",'red'),end='\n')
    dict_threads={}
    tmp_links=[]
    if set_attr["max_threads"] > len(invalid)+1:
        if len(invalid)==1:
            set_attr["max_threads"]=2
        else:
            set_attr["max_threads"]=len(invalid)+1
    for i in invalid:
        tmp_links.append(i)
    for i in range(1,set_attr["max_threads"]):
        dict_threads[i]=cal(len(invalid),i)
    dict_threads=sorted(dict_threads.items(), key =lambda x:(x[1], x[0]))
    invalid.clear()
    #print(dict_threads)
    #input("Wait...")
    if True:
        ThreadPool(dict_threads[0][0]).map(link_fetch,tmp_links)
    print(colored(f"{len(episode_links)} Out of {ep_max_count} Done...",set_attr["term_color"]),flush=True)


def get(driver):
    global episode_links
    ep_count, find = find_count(driver)
    find=fix_name(find)
    #print(find)
    ep_li = click_ep(driver)
    ep_count=len(ep_li)
    #print(ep_li)
    ep_links=ep_li.copy()
    driver.quit()
    print("Title :", find,flush=True)
    print("No. of Episodes :", ep_count,flush=True)
    #sys.stdout.flush()
    val=0
    if check_argv(["test","multi"]):
        val=1
    else:
        val = input("Continue :")
        try:
            val = int(val)
            if val != 1:
                return
        except ValueError:
            #print("Error")
            return
    dict_threads = {}
    for i in range(1,set_attr["max_threads"]):
        dict_threads[i]=cal(ep_count,i)
    dict_threads=sorted(dict_threads.items(), key =lambda x:(x[1], x[0]))
    #print("Number Of Threads :",dict_threads[0][0])
    start = time.time()
    thread_count=dict_threads[0][0]
    global ep_max_count
    ep_max_count=len(ep_links)
    if "set_threads" in set_attr:
        thread_count=set_attr["set_threads"]
    #os.system("")
    print(colored("Fetching Links...",set_attr["term_color"]),flush=True)
    #time.sleep(.5)

    if __name__ == '__main__':
        ThreadPool(thread_count).map(link_fetch,ep_links)

    print(colored(f"{len(episode_links)} Out of {ep_max_count} Done...",set_attr["term_color"]),flush=True)

    while len(invalid) > 0:
        fix(ep_links)
    episode_links = sorted(episode_links.items(),key=lambda x:float(re.findall(r'\d+',x[0])[0]))

    file_path=f"D:\\New folder\\Links\\Links\\{find}.txt"

    with open(f"D:/New Folder/Links/Links/{find}.txt", 'w+',encoding="utf-8") as file:
        file.write(find + '\r\n')
        for key,val in episode_links:
            file.write(str(key)+' - '+str(val) + '\r\n')
    os.system("copy /Y "+file_path+" \"E:\\New folder\\Links\\Links/\" >NUL")
    if set_attr["speak"]==1:
        speak("Done")
    #clean()
    print(colored('*'*28,'magenta'),flush=True,end=' ')
    print("Total Time Taken :",round(time.time() - start,10), "Seconds",end=' ')
    print(colored('*'*28,'magenta'),flush=True,end='\n\n')
    '''if "auto" in sys.argv
        download_files()
    '''
    invalid.clear()
    episode_links.clear()
    if check_argv(["download"]):
        #time.sleep(2)
        #os.system("cls")
        os.system(f"python DNC.py name=\"{str(find)}.txt\"")
    #print("Data Need to Download :",down_size)


def main_block(title="",cho=0):
    st = 1
    #os.environ["WDM_LOG_LEVEL"] = str(logging.WARNING)
    while st == 1:
        if(cho==0):
            os.system("cls")
            if get_arg("title")!=-1:
                find=get_arg('title')
            else:
                find = input('Enter Name :').strip()
        else:
            find=title
        if find=="":
            return None,None
        driver=set_driver(headless=set_attr["title_headless"],image_disable=set_attr["title_page_image_disable"])
        val = find_title(find,driver)
        if val == 1:
            result = driver.find_elements(By.XPATH,"//div[@class='result-title']")
            rep = driver.find_elements(By.XPATH,"//div[@class ='result-status']")
            dt = driver.find_elements(By.XPATH,"//div[@class ='result-season']")
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
                    print(colored('*'*90,'blue'),flush=True)
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
                except ValueError:
                    #print("Error")
                    driver.quit()
                    quit()
            if choose > 0:
                if choose > len(result):
                    driver.quit()
                    return choices,find
                choose = choose - 1
                driver.find_elements(By.CLASS_NAME,"result-title")[choose].click()
                get(driver)
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
        except ValueError:
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