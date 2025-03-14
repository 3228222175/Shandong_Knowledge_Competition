import requests
from loguru import logger
import json
import random
import ddddocr
import execjs

session = requests.Session()

def jiami(fun,data):
    with open('demo.js', 'r', encoding='utf-8') as f:
        js_code=f.read()
    ctx=execjs.compile(js_code)
    return ctx.call(fun, data)


# 识别验证码
def get_code():
    ocr = ddddocr.DdddOcr(show_ad=False)  # 实例化
    with open('yzm.png', 'rb') as f:  # 打开图片
        img_bytes = f.read()  # 读取图片
    res = ocr.classification(img_bytes)
    logger.info('验证码识别成功--->'+res)
    return res
def get_headers():
    return {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Authorization': '',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            # 'Content-Length': '0',
            'Content-Type': 'application/json',
            'Origin': 'https://sdedu5.ngxy.xyz:58012',
            'Pragma': 'no-cache',
            'Referer': 'https://sdedu5.ngxy.xyz:58012/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'token': '',
        }
def get_school(name):
    try:
        with open('school.json','r',encoding='utf-8') as f:
            schools=json.load(f)
        for school in schools:
            if school['name'] == name:
                logger.info('获取学校id成功--->'+str(school['id']))
                return school['id']
        logger.info('学校不存在emmm')
        return None
    except Exception as e:
        logger.error('运行出错'+str(e))




# 登录逻辑
def login(userName,password,school):
    try:
        res = requests.post('https://sdedu3.ngxy.xyz:58012/api/common/organization/sessionApp', headers=get_headers())
        session=res.json()['response']
        params = {
            'random': str(random.random()),
            'session': session,
        }
        # 获取cookie信息
        res= requests.get('https://sdedu3.ngxy.xyz:58012/api/kaptcha/refresh', params=params, headers=get_headers())
        # 获取验证码
        img_data = requests.get('https://sdedu3.ngxy.xyz:58012/api/kaptcha/refresh', params=params,headers=get_headers())
        with open("yzm.png", "wb") as file:
            file.write(img_data.content)
        logger.info("图片保存成功")
        code=get_code()

        data={
            "userName": userName,
            "password": password,
            "organizationId": get_school(school),
            "code": code,
            "session": session
        }

        aes_data=jiami('encode', data)
        logger.info('加密后的数据--->'+aes_data)
        response = requests.post('https://sdedu3.ngxy.xyz:58012/api/user/login',  headers=get_headers(),data=aes_data)
        logger.info(response.json())
        return response.json()["response"]["token"]



    except Exception as e:
        logger.info('登录出错'+str(e))
        pass

# 主要运行逻辑
def run():
    userName=''
    password=''
    school=''
    token=login(userName,password,school)
    headers = get_headers()['Token']=token
    pass

if __name__ == '__main__':
    run()
