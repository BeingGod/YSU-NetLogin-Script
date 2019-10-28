from netlogin import Netlogin
import sys

if __name__ == '__main__':
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
        print (info)
    else:
        print ('出现错误!')
        print (info)
    sys.exit(0)
