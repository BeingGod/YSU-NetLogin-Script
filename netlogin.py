# coding:utf-8
import re
import json
import sys


VERSION  = 0 # Python版本


# 封装post请求
def post(url,headers={},data={}):
    if VERSION == 3:
        data = bytes(urllib.parse.urlencode(data),encoding='utf-8')
        request = urllib.request.Request(url,headers=headers,data=data)
        response = urllib.request.urlopen(request)
    else:
        data = bytes(urllib.urlencode(data))
        request = urllib2.Request(url,headers=headers,data=data)
        response = urllib2.urlopen(request)

    return response


# 封装get请求
def get(url,headers={}):
    if VERSION == 3:
        request = urllib.request.Request(url,headers=headers)
        response = urllib.request.urlopen(request)
    else:
        request = urllib2.Request(url,headers=headers)
        response = urllib2.urlopen(request)

    return response


class Netlogin():
    def __init__(self):
        '''
        登陆服务
        0：校园网
        1：中国移动
        2：中国联通
        3：中国电信
        '''
        self.services = {
            '0': '%e6%a0%a1%e5%9b%ad%e7%bd%91', 
            '1': '%E4%B8%AD%E5%9B%BD%E7%A7%BB%E5%8A%A8',
            '2': '%e4%b8%ad%e5%9b%bd%e8%81%94%e9%80%9a',
            '3': '%e4%b8%ad%e5%9b%bd%e7%94%b5%e4%bf%a1',
        }
        self.url = 'http://auth.ysu.edu.cn/eportal/InterFace.do?method='
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134',
            'Accept-Encoding':'identify'
        }
        self.isLogined = None
        self.alldata = None


    def tst_net(self):
        '''
        测试网络是否认证
        :return: 是否已经认证
        '''
        res = get('http://auth.ysu.edu.cn',headers = self.header)
        if res.geturl().find('success.jsp')>0:
            self.isLogined = True
        else:
            self.isLogined = False
        return self.isLogined


    def isCode(self):
        '''
        检测是否需要输入验证码
        未开放
        :return:是否需要验证码
        '''
        pass

        return False


    def login(self,user,pwd,type,code=''):
        '''
        输入参数登入校园网，自动检测当前网络是否认证。
        :param user:登入id
        :param pwd:登入密码
        :param type:认证服务
        :param code:验证码
        :return:元祖第一项：是否认证状态；第二项：详细信息
        '''
        if self.isLogined == None:
            self.tst_net()
        if self.isLogined == False:
            if user == '' or pwd == '':
                return (False,'用户名或密码为空')
            self.data = {
                'userId': user,
                'password': pwd,
                'service': self.services[type],
                'operatorPwd': '',
                'operatorUserId': '',
                'validcode': code,
                'passwordEncrypt':'False'
            }
            res = get('http://auth.ysu.edu.cn',headers = self.header)
            queryString = re.findall(r"href='.*?\?(.*?)'", res.read().decode('utf-8'), re.S)
            self.data['queryString'] = queryString[0]
	    
            res = post(self.url+'login',headers = self.header,data = self.data)
            login_json = json.loads(res.read().decode('utf-8'))
            self.userindex = login_json['userIndex']
            #self.info = login_json
            self.info = login_json['message']
            if login_json['result'] == 'success':
                return (True,'认证成功')
            else:
                return (False,self.info)

        return (True,'已经在线')
    def get_alldata(self):
        '''
        获取当前认证账号全部信息
        #！！！注意！！！#此操作会获得账号alldata['userId']姓名alldata['userName']以及密码alldata['password']
        :return:全部数据的字典格式
        '''
        res = get('http://auth.ysu.edu.cn/eportal/InterFace.do?method=getOnlineUserInfo',headers = self.header)
        try:
            self.alldata = json.loads(res.read().decode('utf-8'))
        except json.decoder.JSONDecodeError as e:
            print('数据解析失败，请稍后重试。')

        return self.alldata


    def logout(self):
        '''
        登出，操作内会自动获取特征码
        :return:元祖第一项：是否操作成功；第二项：详细信息
        '''
        if self.alldata==None:
            self.get_alldata()

        res = get(self.url+'logout',headers = self.header)
        logout_json = json.loads(res.read().decode('utf-8'))
        #self.info = logout_json
        self.info = logout_json['message']

        if logout_json['result'] == 'success':
            return (True,'下线成功')
        else:
            return (False,self.info)

if __name__ == '__main__':
    # 判断Python版本
    if sys.version_info < (3, 0):
        VERSION = 2
    else:
        VERSION = 3

    # 根据不同版本导入不同的urllib库
    if VERSION == 3:
        import urllib.request
        import urllib.parse
    else:
        import urllib2
        import urllib

    loger = Netlogin()
    l = len(sys.argv)
    name = sys.argv[0]
    if l==2 and sys.argv[1]=='logout':
        state,info = loger.logout()
        if state:
            print(info)
        else:
            print('出现错误!')
            print(info)
        sys.exit(0)
    elif l==3:
        state, info = loger.login(user=sys.argv[1], pwd=sys.argv[2], type='0')
    elif l==4:
        state, info = loger.login(user=sys.argv[1], pwd=sys.argv[2], type=sys.argv[3])
    else:
        print('登陆服务： 0.校园网 1.中国移动 2.中国联通 3.中国电信')
        print('格式：')
        print('登入：%s userid password [service_type=校园网] ' % name)
        print('注销：%s logout ' % name)
        sys.exit(0)
    if state:
        print(info)
    else:
        print('出现错误!')
        print(info)

