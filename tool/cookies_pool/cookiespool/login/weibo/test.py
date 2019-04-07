from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from urllib.request import urlretrieve
from bs4 import BeautifulSoup
from lxml.html import etree
import re,requests
from PIL import Image
from time import sleep

username = 13925848599
password = ",wwa0aaglei"


class Jiyan_test:
    def __init__(self):
        self.url='https://passport.bilibili.com/login'
        self.brower=webdriver.Chrome('chromedriver')
        self.wait=WebDriverWait(self.brower,20)#设置等待
 
    def login(self):
        self.brower.get(self.url)
        self.user=self.wait.until(EC.presence_of_element_located((By.ID,'login-username')))
        self.passwd=self.wait.until(EC.presence_of_element_located((By.ID,'login-passwd')))
        self.user.send_keys(username)
        self.passwd.send_keys(password)

    def get_images(self):#获取验证码图片
        # print(self.brower.page_source)
        full_position=[]#完整散图坐标
        bg_position=[]#缺口散图坐标
        html=etree.HTML(self.brower.page_source)
        gt_cut_fullbg_slices=html.xpath('//div[@class="gt_cut_fullbg_slice"]/@style')
        full_slice_url=re.findall('url\(\"(.*)\"\);',gt_cut_fullbg_slices[0])[0].replace('webp','jpg')
        gt_cut_bg_slices = html.xpath('//div[@class="gt_cut_bg_slice"]/@style')
        bg_slice_url = re.findall('url\(\"(.*)\"\);', gt_cut_bg_slices[0])[0].replace('webp', 'jpg')
        print(gt_cut_fullbg_slices)
        for i in gt_cut_fullbg_slices:
            position=re.findall('background-position: (.*);',i)[0].replace('px','').split(' ')
            position=[int(i) for i in position]
            full_position.append(position)
        for i in gt_cut_fullbg_slices:
            position = re.findall('background-position: (.*);', i)[0].replace('px','').split(' ')
            position=[int(i) for i in position]
            bg_position.append(position)
        print(full_position)
        print(bg_position)
        print(full_slice_url)
        print(bg_slice_url)
        full_pic_data=requests.get(full_slice_url).content
        bg_pic_data=requests.get(bg_slice_url).content
        with open('image/full_pic.jpg','wb') as f:
            f.write(full_pic_data)
        with open('image/bg_pic.jpg', 'wb') as f:
            f.write(bg_pic_data)
        full_image=Image.open('image/full_pic.jpg')
        bg_image=Image.open('image/bg_pic.jpg')
        return full_image,bg_image,full_position,bg_position


    def pic_cut(self,file,position):#分割图片
        first_line_pic=[]
        second_line_pic=[]
        # full_image, bg_image, full_position, bg_position=self.get_images()
        for p in position:
            if p[1]==-58:
                first_line_pic.append(file.crop((abs(p[0]),58,abs(p[0])+10,166)))
            if p[1]==0:
                second_line_pic.append(file.crop((abs(p[0]),0,abs(p[0])+10,58)))
        print(first_line_pic)
        print(second_line_pic)
        return first_line_pic,second_line_pic



    def merge_pics_new(self,first_line_pic,second_line_pic,file_name):
        #新建图片
        image=Image.new('RGB',(260,116))
        offset=0#设置偏移量
        #拼接第一行
        for i in first_line_pic:
            image.paste(i,(offset,0))
            offset+=i.size[0]
        offset_x=0
        #拼接第二行
        for j in second_line_pic:
            image.paste(j,(offset_x,58))
            offset_x+=j.size[0]
        image.save('image/'+file_name)#合成完整图片
 
    def merge_pics(self):#合并图片
        #先割切乱码图片
        full_image, bg_image, full_position, bg_position=self.get_images()
        first_line_pic, second_line_pic=self.pic_cut(full_image,full_position)
        self.merge_pics_new(first_line_pic, second_line_pic,'full_new_pic.jpg')
        first_line_pic, second_line_pic = self.pic_cut(bg_image, bg_position)
        self.merge_pics_new(first_line_pic, second_line_pic, 'bg_new_pic.jpg')



    def check_pics_is_same(self,bg_image,full_image,x,y):#判断图片是否一样
        bg_pixel=bg_image.getpixel((x,y))
        full_pixel=full_image.getpixel((x,y))
        for i in range(0,3):
            if abs(bg_pixel[i]-full_pixel[i])>=50:
                return False
            else:
                return True



    def reckon_distance2(self):#计算滑块
        try:
            full_image = Image.open('image/full_new_pic.jpg')
            bg_image = Image.open('image/bg_new_pic.jpg')
            for i in range(0,full_image.size[0]):
                for j in range(0,full_image.size[1]):
                    if not self.check_pics_is_same(bg_image,full_image,i,j):
                        return i
        except Exception:
            print('图片读取失败')



    def reckon_trail(self):#计算运动轨迹
        print('计算运动轨迹')
        track=[]
        distance=self.reckon_distance2()
        distance=int(distance)-7#矫正值
        print('缺口坐标',distance)
        fast_distance=distance*(4/5)
        start,v0,t=0,0,0.2
        while start<distance:
            if start<fast_distance:#加速状态
                a=1.5#加速
            else:
                a=-3#减速
            #数学公式 s=v0*t+1/2 v*t平方
            move=v0*t+1/2*a*t*t
            #当前速度
            v=v0+a*t
            #重置粗速度
            v0=v
            #重置起始位置
            start+=move
            track.append(round(move))
        return track


    def move_block(self):# 模拟拖动滑块
        print('开始模拟')
        track=self.reckon_trail()
        #找寻滑块标签
        slider=self.wait.until(EC.presence_of_element_located((By.CLASS_NAME,'gt_slider_knob')))
        ActionChains(self.brower).click_and_hold(slider).perform()#执行
        for x in track:
            ActionChains(self.brower).move_by_offset(xoffset=x,yoffset=0).perform()
        sleep(0.4)
        ActionChains(self.brower).release().perform()#释放滑块
 
if __name__ == '__main__':
    c=Jiyan_test()
    c.login()
    c.merge_pics()
    c.move_block()
