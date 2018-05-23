# -*- coding: utf-8 -*-
import scrapy
import urllib.request
from PIL import Image


class DoubanSpiderSpider(scrapy.Spider):
    name = 'douban_spider'
    allowed_domains = ['douban.com']
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'}

    def start_requests(self):
        return [scrapy.FormRequest("https://accounts.douban.com/login", headers=self.headers, meta={"cookiejar": 1}, callback=self.parse_before_login)]

    def parse_before_login(self, response):
        print("登录前表单填充")
        captcha_id = response.xpath('//input[@name="captcha-id"]/@value').extract()[0]
        print(captcha_id)
        captcha_image_url = response.xpath('//img[@id="captcha_image"]/@src').extract()[0]
        print(captcha_image_url)
        if captcha_image_url is None:
            print("登录时无验证码")
            formdata = {
                "source": "index_nav",
                "form_email": "luojintaodota@gmail.com",
                # 请填写你的密码
                "form_password": "Brave2018",
            }
        else:
            print("登录时有验证码")
            save_image_path = "/home/luojintao/tutorial/captcha.jpeg"
            urllib.request.urlretrieve(captcha_image_url, save_image_path)
            try:
                im = Image.open('captcha.jpeg')
                im.show()
            except:
                pass

        captcha_solution = input("根据打开的图片输入验证码:")
        formdata = {
            "source": "None",
            "redir": "https://www.douban.com",
            "form_email": "luojintaodota@gmail.com",
            # 此处请填写密码
            "form_password": "Brave2018",
            "captcha-solution": captcha_solution,
            "captcha-id": captcha_id,
            "login": "登录",
        }
        print("登录中")
        # 提交表单
        return scrapy.FormRequest.from_response(response, meta={"cookiejar": response.meta["cookiejar"]},
                                                headers=self.headers, formdata=formdata,
                                                callback=self.parse_after_login, dont_filter=True)

    def parse_after_login(self, response):
        '''
        验证登录是否成功
        '''
        account = response.xpath('//a[@class="bn-more"]/span/text()').extract()
        if account is None:
            print("登录失败")
        else:
            print(u"登录成功,当前账户为 %s" % account)
