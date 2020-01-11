#!/usr/bin/python3
# coding=utf-8

import requests
import json
import pysnooper
from T_Mylog import mylogger

# @pysnooper.snoop()
class Public_Params:
    def __init__(self,Login_Token=None,Product=None):
        '''
        公共参数
        self.product_keyword  这个对应为你的产品代号也是从外部传入的产品号 也对应这产品解析记录的字典类型
        解析主机和解析值自己可以定义
        self.product_keyword = {'@':'your record',
                                'www':'your record',
                                'your hosts headers':'your record'}
        :param Login_Token:
        :param Product:
        '''
        self.Login_Token = Login_Token
        self.Product = Product
        self.Format = 'json'
        self.DnsApi_host = 'https://dnsapi.cn'
        self.Record_Line = '默认'
        self.Domain_Status = 'enable'
        self.offset = '0'
        self.length = '200'

        self.product_keyword = {'@':'your record',
                        'www':'your record',}

# @pysnooper.snoop()
class Dnsapi_requests(Public_Params):
    '''
    发送API请求,返回字典数据格式
    '''
    def add_domain(self,domain=None):
        return_data = {}
        Add_domain_url = self.DnsApi_host + '/Domain.Create'
        self.data['domain'] = domain
        try:
           r = requests.post(url=Add_domain_url,data=self.data)
        except Exception as e:
            return_data['status'] = 'error'
            return_data['message'] = f"异常信息为:{e.__str__()}"
            return return_data
        else:
           return r.json()

    def delete_domain(self,domain=None):
        return_data = {}
        Delete_domain_url = self.DnsApi_host + '/Domain.Remove'
        self.data['domain'] = domain
        try:
           r = requests.post(url=Delete_domain_url,data=self.data)
        except Exception as e:
            return_data['status'] = 'error'
            return_data['message'] = f"异常信息为:{e.__str__()}"
            return return_data
        else:
            return r.json()

    def list_domain(self):
        return_data = {}
        List_domain_url = self.DnsApi_host + '/Domain.List'
        try:
           r = requests.post(url=List_domain_url,data=self.data)
        except Exception as e:
            return_data['status'] = 'error'
            return_data['message'] = f'异常信息为:{e.__str__()}'
            return return_data
        else:
            return r.json()

    def add_domain_record(self,Domain=None,Sub_domain=None,Record_Type=None,Value=None):
        return_data = {}
        Add_domain_record_url = self.DnsApi_host + '/Record.Create'
        try:
           self.data['domain'] = Domain
           self.data['sub_domain'] = Sub_domain
           self.data['record_type'] = Record_Type
           self.data['record_line'] = self.Record_Line
           self.data['status'] = self.Domain_Status
           self.data['value'] = Value
           r = requests.post(url=Add_domain_record_url,data=self.data)
        except Exception as e:
            return_data['status'] = 'error'
            return_data['message'] = f"异常信息为:{e.__str__()}"
            return return_data
        else:
            data = {}
            data['code'] = r.json()['status']['code']
            data['record_id'] = r.json()['record']['id']
            data['sub_domain'] = r.json()['record']['name']
            data['record_line'] = self.Record_Line
            data['record_type'] = Record_Type
            data['value'] = Value
            data['status'] = r.json()['record']['status']
            data['belong_domain'] = Domain
            data['message'] = r.json()['status']['message']
            return_data['data'] = data

        return return_data

    def get_domain_log(self,Domain=None):
        return_data = {}
        Get_domain_record_log_url = self.DnsApi_host + '/Domain.Log'
        try:
            self.data['domain'] = Domain
            self.data['offset'] = self.offset
            self.data['length'] = self.length
            r = requests.post(url=Get_domain_record_log_url,data=self.data)
        except Exception as e:
            return_data['status'] = 'error'
            return_data['message'] = f"异常信息为:{e.__str__()}"
            return return_data
        else:
            return r.json()

    def get_domain_record_list(self,Domain=None):
        return_data = {}
        Get_domain_record_list_url = self.DnsApi_host + '/Record.List'
        try:
            self.data['domain'] = Domain
            r = requests.post(url=Get_domain_record_list_url,data=self.data)
        except Exception as e:
            return_data['status'] = 'error'
            return_data['message'] = f"异常信息为:{e.__str__()}"
            return return_data
        else:
            return r.json()
    def batch_and_domain_record(self,Domain=None):
        Record_Type = 'CNAME'
        Domain_Status = 'enable'
        return_data = {}
        Batch_domainRocord_url = self.DnsApi_host + '/Record.Create'
        try:
            if not self.Product:
               mylogger.error('传入产品号为空,请检查')
            elif self.Product:
                for Sub_Domain in eval('self.{}'.format(self.Product)):
                    Value = eval("self.{}['{}']".format(self.Product, Sub_Domain))
                    self.data['domain'] = Domain
                    self.data['sub_domain'] = Sub_Domain
                    self.data['record_type'] = Record_Type
                    self.data['record_line'] = self.Record_Line
                    self.data['value'] = Value
                    self.data['status'] = Domain_Status
                    r = requests.post(url=Batch_domainRocord_url,data=self.data)
            else:
                mylogger.error('传入产品错误,请检查')
        except Exception as e:
            return_data['status'] = 'error'
            return_data['message'] = f"异常信息为:{e.__str__()}"
            return return_data
        else:
            return r.json()

    def alter_domain_record(self,Domain=None):
        pass

