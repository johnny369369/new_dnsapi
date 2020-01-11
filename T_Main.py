#!/usr/bin/python3
# coding=utf-8
import sys,os,json
from T_Dnsapi import *
from T_Params import *
from T_Mylog import mylogger
scpipts_path = os.getcwd()
import pysnooper

# @pysnooper.snoop()
class Dnspod_Operate:
    def __init__(self,Login_Token=None,Product=None):
        '''
         operate menuApi Dnspod api
        :param Login_Token:
        :param Product:
        :return:
        '''
        self.Login_Token = Login_Token
        self.Product = Product
        self.Operate_domain = Dnsapi_requests(self.Login_Token, self.Product)

        domain_first = input(All_params.display('\n=====>>请输入要操作的域名(已,为分隔符),留空则从文件读入域名:','yellow'))
        if os.path.exists(scpipts_path + '/domain_list'):
           print(All_params.display('=====>>domain_list文件存在无需创建','green'))
        else:
           os.mknod(scpipts_path + '/domain_list')
           print(All_params.display('=====>>domain_list文件不存在创建成功', 'green'))
        with open(f'{scpipts_path}/domain_list', 'r') as domain_file:
            self.domain_list = domain_first.split(',') if domain_first else domain_file.read().splitlines()
        while True:
            operate_choose = {'1':'添加域名','2':'删除域名','3':'域名列表','4':'添加域名记录','5':'查询域名日志',
                              '6':'查询域名解析记录','7':'批量添加域名和域名记录','8':'修改域名记录'}
            check_choose = All_params.check_menu_dict(operate_choose,'你的操作')
            if int(check_choose) == 1:
                self.A_add_domain()
            elif int(check_choose) == 2:
                self.A_delete_domain()
            elif int(check_choose) == 3:
                self.A_domain_list()
            elif int(check_choose) == 4:
                self.A_add_domain_record()
            elif int(check_choose) == 5:
                self.A_query_domain_log()
            elif int(check_choose) == 6:
                self.A_query_domain_record_list()
            elif int(check_choose) == 7:
                self.A_batch_addDomdin_record()
            elif int(check_choose) == 8:
                self.A_alter_domain_record()

    def A_add_domain(self):
       for Domain in self.domain_list:
           result_json = self.Operate_domain.add_domain(Domain)
           if result_json['status']['code'] == '1':
               mylogger.info('域名:{}添加成功,操作信息返回:{}'.format(Domain,result_json['status']['message']))
           else:
               mylogger.error('域名:{}添加失败,操作信息返回:{}'.format(Domain,result_json['status']['message']))
    def A_delete_domain(self):
        for Domain in self.domain_list:
            result_json = self.Operate_domain.delete_domain(Domain)
            if result_json['status']['code'] == '1':
                mylogger.info('域名:{}删除成功,操作信息返回:{}'.format(Domain,result_json['status']['message']))
            else:
                mylogger.error('域名:{}删除失败,操作信息返回:{}'.format(Domain,result_json['status']['message']))
    def A_domain_list(self):
        result_json = self.Operate_domain.list_domain()
        if result_json['status']['code'] == '1':
           mylogger.info('域名列表获取成功状态为:{},共有:{}个域名'.format(result_json['status']['code'],result_json['info']['domain_total']))
        else:
           mylogger.error('域名列表获取失败状态为:{},异常信息为:{}'.format(result_json['status']['code'],result_json['status']['message']))

    def A_add_domain_record(self):
        Sub_domian = All_params.check_input("需要添加的子域名，用逗号分隔:")
        Record_Type = All_params.check_input("选择记录类型,输入( A 或 CNAME ):")
        Value = All_params.check_input("要解析的记录值")
        for Domain in domain_list:
            result_json = self.Operate_domain.add_domain_record(Domain,Sub_domian,Record_Type,Value)
            if result_json['data']['code'] == '1':
               mylogger.info('域名{} 二级域名:{} 记录:{}成功,操作信息返回:{}'.format(Domain,Sub_domian,Value,result_json['data']['message']))
            else:
               mylogger.error('域名{} 二级域名:{} 记录:{}失败,操作信息返回:{}'.format(Domain,Sub_domian,Value,result_json['data']['message']))
    def A_query_domain_log(self):
        for Domain in self.domain_list:
            result_json = self.Operate_domain.get_domain_log(Domain)
            if result_json['status']['code'] == '1':
               for log_record in result_json['log']:
                   mylogger.info(log_record)
            else:
               mylogger.error('域名日志获取失败,异常信息为:{}'.format(result_json['message']))
    def A_query_domain_record_list(self):
        for Domain in self.domain_list:
            result_json = self.Operate_domain.get_domain_record_list(Domain)
            if result_json['status']['code'] == '1':
               mylogger.info('域名解析记录共有:{}条,如下是解析记录详情.'.format(result_json['info']['sub_domains']))
               for record_list in result_json['records']:
                   mylogger.info('主机头:{} 解析类型:{} 记录值:{} 解析状态:{} 解析时间:{}'.format(record_list['name'],record_list['type'],
                                record_list['value'],record_list['status'],record_list['updated_on']))
            else:
                mylogger.error('域名记录获取失败,异常信息为:{}'.format(result_json['status']['message']))
    def A_batch_addDomdin_record(self):
        self.A_add_domain()
        for Domain in self.domain_list:
            result_json = self.Operate_domain.batch_and_domain_record(Domain)
            if result_json['status']['code'] == '1':
               mylogger.info('域名:{}批量添加解析值成功,操作信息返回:{}'.format(Domain,result_json['status']['message']))
            else:
               mylogger.error('域名:{}批量添加二级域名失败,操作信息返回:{}'.format(Domain,result_json['message']))

    def A_alter_domain_record(self):
        for Domain in self.domain_list:
            result_json = self.Operate_domain.get_domain_record_list(Domain)
            if result_json['status']['code'] == '1':
               print(All_params.display('\n获取域名:{}记录列表成功,操作信息返回:{}','green'.format(Domain,result_json['status']['message'])))
               for record_list in result_json['records']:
                   print('域名ID:{} 域名记录值:{} 域名主机头:{} 解析类型:{} 解析线路:{}'.format(record_list['id'],record_list['value'],
                         record_list['name'],record_list['type'],record_list['line']))
        alter_type = All_params.check_input("需要修改的解析记录的ID，并且输入ID，用逗号分隔:")

if __name__ == '__main__':
    try:
        Login_Token = {'product_keyword':'your dnsapi Login_Token'}
        Product = sys.argv[1]
        if Product:
            Dnspod_Operate(Login_Token[Product],Product)
    except KeyError as e:
        print(f'''
        未找到:{e.__str__()}对应产品,请检查!
        product_list:your product
        用法: python T_Main.py product
        ''')
    except IndexError:
        print('''
        product_list:your product
        用法:python T_Main.py product
             ''')