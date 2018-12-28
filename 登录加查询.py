import tkinter as tk
from tkinter import messagebox,ttk
import requests,json,random



class Search(object):
    def __init__(self):
        self.windows = tk.Tk()
        self.windows.title('12306余票查询')
        self.windows.geometry('750x600')
        self.header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
        }
        self.mian_ui()

    def get_code(self):
        all_code={}
        url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js'
        res = requests.get(url,headers = self.header).content.decode('utf-8')
        code = res.split('@')[1:]
        for i in code:
            self.fin = i.split('|')
            all_code[self.fin[1]]=self.fin[2]
        return all_code


    def get_ticket_url(self):
        code = self.get_code()
        if self.start_input.get():
            start = code[self.start_input.get()]
            if self.end_input.get():
                end = code[self.end_input.get()]
                if self.date_input.get():
                    date = self.date_input.get()
                    url = 'https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date=' + date + '&leftTicketDTO.from_station=' + start + '&leftTicketDTO.to_station=' + end + '&purpose_codes=ADULT'
                    return url
                else:
                    messagebox.showinfo(message='请输入日期')
            else:
                messagebox.showinfo(message='请输入终点')
        else:

            messagebox.showinfo(message='请输入出发地')

    def parser(self):
        x=self.tree.get_children()
        for i in x:
            self.tree.delete(i)
        url = self.get_ticket_url()
        info = requests.get(url,headers = self.header).content.decode('utf-8')
        print(info)
        info_name = json.loads(info)['data']['map']
        info_js = json.loads(info)['data']['result']
        for each in range(0,len(info_js)):
            all_info = info_js[each].split('|')
            cc = all_info[3]
            start_time = all_info[8]
            arr_time = all_info[9]
            star_sta = info_name[all_info[6]]
            get_sta = info_name[all_info[7]]
            yz = all_info[31] if str(all_info[31]) != '' else "-"
            # [29]---二等座
            wz = all_info[30] if str(all_info[30]) != '' else "-"
            # [30]---硬座
            ze = all_info[29] if str(all_info[29]) != '' else "-"
            # [31]---无座
            zy = all_info[26] if str(all_info[26]) != '' else "-"
            # 硬卧
            xx = all_info[28] if str(all_info[28]) != '' else "-"
            # 软卧
            yy = all_info[23] if str(all_info[23]) != '' else "-"
            self.tree.insert('',each, values=(
                cc, star_sta, get_sta, start_time, arr_time, str(yz), str(wz), str(xx), str(yy), str(ze), str(zy)))





    def mian_ui(self):
        self.start = tk.Label(self.windows, text='出发站:', font=('黑体'))
        self.start.place(y=20)
        self.start_input = tk.Entry(self.windows)
        self.start_input.place(x=80, y=22, width=100)
        self.end = tk.Label(self.windows, text='终点站:', font=('黑体'))
        self.end.place(x=190, y=20)
        self.end_input = tk.Entry(self.windows)
        self.end_input.place(x=280, y=20,width = 100)
        self.ser_but = tk.Button(self.windows, text='查询',command = self.parser)
        self.ser_but.place(x=690, y=20,width = 50)
        self.date = tk.Label(self.windows, text='日期(xxxx-xx-xx):', font=('黑体'))
        self.date.place(x=380, y=20)
        self.date_input = tk.Entry(self.windows)
        self.date_input.place(x=560, y=20, width=100)
        self.tree = ttk.Treeview(self.windows,columns=("车次", "出发站名", "到达站名", "出发时间", "到达时间", "一等座", "二等座", "硬卧", "软卧", "硬座", "无座"),show="headings")
        self.tree.column('车次', width=50, anchor='center')
        self.tree.column('出发站名', width=80, anchor='center')
        self.tree.column('到达站名', width=80, anchor='center')
        self.tree.column('出发时间', width=80, anchor='center')
        self.tree.column('到达时间', width=80, anchor='center')
        self.tree.column('一等座', width=60, anchor='center')
        self.tree.column('二等座', width=60, anchor='center')
        self.tree.column('硬卧', width=60, anchor='center')
        self.tree.column('软卧', width=60, anchor='center')
        self.tree.column('硬座', width=60, anchor='center')
        self.tree.column('无座', width=60, anchor='center')
        self.tree.heading('车次', text='车次')
        self.tree.heading('出发站名', text='出发站名')
        self.tree.heading('到达站名', text='到达站名')
        self.tree.heading('出发时间', text='出发时间')
        self.tree.heading('到达时间', text='到达时间')
        self.tree.heading('一等座', text='一等座')
        self.tree.heading('二等座', text='二等座')
        self.tree.heading('硬卧', text='硬卧')
        self.tree.heading('软卧', text='软卧')
        self.tree.heading('硬座', text='硬座')
        self.tree.heading('无座', text='无座')
        self.tree.place(x=10, y=80, width=730, height=500)




class train_login(object):
    def __init__(self):
        self.s = requests.session()
        self.url = 'https://kyfw.12306.cn/passport/web/login'
        self.ver_url = 'https://kyfw.12306.cn/passport/captcha/captcha-image'
        self.check_captcha_url = 'https://kyfw.12306.cn/passport/captcha/captcha-check'
        self.uamtk_url = 'https://kyfw.12306.cn/passport/web/auth/uamtk'
        self.auth_url = 'https://kyfw.12306.cn/otn/uamauthclient'

        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
            'Host': 'kyfw.12306.cn',
            'Origin': 'https://kyfw.12306.cn',
            'Referer': 'https://kyfw.12306.cn/otn/resources/login.html'
        }

        self.windows = tk.Tk()
        self.windows.title('12306登录')
        self.windows.geometry('350x180')
        self.acocunt = tk.Label(self.windows,text = '用户名/邮箱/手机号:',font = '黑体')
        self.acocunt.place(y = 20)
        self.acocunt_box = tk.Entry(self.windows)
        self.acocunt_box.place(x = 170,y=20)
        self.passwd = tk.Label(self.windows, text='密码:', font='黑体')
        self.passwd.place(x =120 ,y=50)
        self.passwd_box = tk.Entry(self.windows,show = '*')
        self.passwd_box.place(x=170, y=50)
        self.yzm = tk.Label(self.windows, text='验证码\n(输入1-8,以空格分隔):', font='黑体')
        self.yzm.place(x =0 ,y=80)
        self.yzm_box = tk.Entry(self.windows)
        self.yzm_box.place(x=175, y=90)
        self.login = tk.Button(self.windows, text='刷新验证码', command=self.get_captcha)
        self.login.place(x=200, y=130)
        self.login = tk.Button(self.windows,text = '登录',command = self.user_login)
        self.login.place(x=150, y=130)
        self.get_captcha()


    def get_captcha(self):
        data = {
            'login_site': 'E',
            'module': 'login',
            'rand': 'sjrand',
            str(random.random()): ''
        }
        response = self.s.get(self.ver_url, params=data,headers = self.header)
        with open('yzm.jpg', 'wb') as f:
            f.write(response.content)

    def get_tk(self):
        uamtk_data = {
            'appid': 'otn'
        }
        response = self.s.post(self.uamtk_url, data=uamtk_data)
        return response.json()['newapptk']

    # 获取权限
    def get_auth(self, tk):
        auth_data = {
            'tk': tk
        }
        response = self.s.post(self.auth_url, data=auth_data)
        if response.json()['result_code'] == 0:
            name = json.loads(response.text)['username']
            self.windows.destroy()
            new = Search()
            new.windows.title('当前用户：%s'%name)
            new.windows.mainloop()
            return True
        return False





    def get_code1(self):
        verify = {
            '1': '42,45,',
            '2': '117,48,',
            '3': '185,45,',
            '4': '257,49,',
            '5': '34,115,',
            '6': '120,119,',
            '7': '190,117,',
            '8': '262,116,'
        }
        text = ''
        iput = self.yzm_box.get()
        num = iput.split(' ')
        for i in range(len(num)):
            text = text + str(verify[num[i]])
        return text[:-1]

    def check_captcha(self):
        yzm = self.get_code1()
        data = {
            'answer':yzm,
            'login_site': 'E',
            'rand': 'sjrand'
        }
        response = self.s.post(self.check_captcha_url, data=data,headers = self.header)
        if response.json()['result_code'] == '4':
            messagebox.showinfo(message='登录成功')
            return True
            #self.windows.destroy()
            #new = Search()
            #new.windows.mainloop()
        else:
            print('验证码选择错误，请重新选择')
            return False
    def user_login(self):

        name = self.acocunt_box.get()
        ps = self.passwd_box.get()
        data1 = {
            "username": name,
            "password": ps,
            "appid": "otn"
        }
        if self.check_captcha():
            res = self.s.post(self.url,data=data1,headers = self.header)
            if res.json()['result_code'] == 0:
                tk = self.get_tk()
                auth_res = self.get_auth(tk)


if __name__ == '__main__':
    a = train_login()
    a.windows.mainloop()


