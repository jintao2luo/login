# -*- coding: utf-8 -*-
import scrapy
import urllib.request

class GithubSpiderSpider(scrapy.Spider):
    name = 'github_spider'
    allowed_domains = ['github.com']
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'}

    def start_requests(self):
        return [scrapy.FormRequest("https://github.com/login", headers=self.headers, meta={"cookiejar": 1},
                                   callback=self.parse_before_login)]

    def parse_before_login(self, response):
        print("登录前表单填充")
        authenticity_token = response.xpath('//input[@name="authenticity_token"]/@value').extract()[0]
        print(authenticity_token)
        formdata = {
            "utf8": "✓",
            "authenticity_token": authenticity_token,
            "login": "luojintaodota@gmail.com",
            "password": "Brave2017",
        }
        return scrapy.FormRequest.from_response(response, meta={"cookiejar": response.meta["cookiejar"]},
                                                headers=self.headers, formdata=formdata,
                                                callback=self.parse_after_login)

    def parse_after_login(self, response):
        '''
        验证登录是否成功
        '''
        account = response.xpath('//summary[@class="HeaderNavlink name mt-1"]/img/@alt').extract()
        if account is None:
            print("登录失败")
        else:
            print(u"登录成功,当前账户为 %s" % account)
