import requests
import pytest
from requests.auth import HTTPBasicAuth
import urllib3

class Apitest():
    '''
    使用resful get,put,delete,post取得資料
    jdata為json格式資料
    key為keyname=value 
    '''
    def initUrl(self,base_url):
        self.base_url = base_url
        self.list = []
        self.rsp_pass = {'status':str}
        self.rsp_fail = {'status':str,
                         'err':{
                             'code':str,
                             'msg' :str
                         }}
        
    def get(self, key:str):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = requests.get(f'{self.base_url}?{key}',verify=False, auth = HTTPBasicAuth('igwwebapi', 'insynerger@tw')).json()
        return response
    
    def put(self, jsondata:dict):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = requests.put(f'{self.base_url}',json = jsondata,verify=False, auth = HTTPBasicAuth('igwwebapi', 'insynerger@tw')).json()
        return response
    
    def delete(self, jsondata:dict):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = requests.delete(f'{self.base_url}',json= jsondata,verify=False, auth = HTTPBasicAuth('igwwebapi', 'insynerger@tw')).json()
        return response

    def post(self, jsondata:dict):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = requests.post(f'{self.base_url}',json=jsondata,verify=False, auth = HTTPBasicAuth('igwwebapi', 'insynerger@tw')).json()
        return response
    
    def post1(self, jsondata:dict):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        response = requests.post(f'{self.base_url}',data=jsondata,verify=False, auth = HTTPBasicAuth('igwwebapi', 'insynerger@tw')).json()
        return response
    '''
    方法data_format 
    chNode為要比對的資料
    BcdNode為要被比對的資料
    '''
    def data_format(self, chNode , BcdNode):
        if(type(chNode) != type(BcdNode) and chNode != type(BcdNode)):return False
        if(type(chNode) == type({})):
            #這邊是OBJ
            for i in chNode.keys():
                if(BcdNode.get(i , None) == None):return False
                if(not self.data_format(chNode[i] , BcdNode[i])):return False
        elif(type(chNode) == type([])):
            #這邊是array
            tmp = chNode[0]
            for i,j in enumerate(BcdNode):
                if not self.data_format(tmp , BcdNode[i]):return False
        return True
    '''
    方法ALLCH
    chNode為要比對的資料
    BcdNode為要被比對的資料
    檢查資料是否完全一樣
    '''
    def ALLCH(chData , bchData):
        for i in chData:
            flag = False
            for j in bchData:
                if(i == j):
                    flag = True
                    break
            if(not flag):return False
    
    '''
    方法ALLCH
    chNode為要比對的資料
    BcdNode為要被比對的資料
    檢查BcdNode中有沒有chNode
    '''
    def check(self,chData , bchData):
        if(chData == bchData):return True
        if(type(chData) != type(bchData)):return False
        if(type(chData) == type({})):
            for i in chData.keys():
                if(bchData.get(i , None) == None): return False
                if(not self.check(chData[i] , bchData[i])):return False
            return True
        elif(type(chData) == type([])):
            for i in chData:
                flag = False
                for j in bchData:
                    if(self.check(i , j)):
                        flag = True
                        break
                if(not flag):return False
            return True
        return False
    '''
    方法api_get
    key為要帶入的鍵值
    data_format要比對get的出來的格式
    '''
    def api_get(self, key,data_format):
        self.reslut ='pass'
        try:
            rsp_get = self.get(key)
            if rsp_get['status'] =="ok": 
                assert self.data_format(data_format,rsp_get) == True
            elif rsp_get['status'] =="fail": 
                assert self.data_format(self.rsp_fail,rsp_get) == True
            else:
                assert False
        except AssertionError :
            self.reslut = 'fail'
            assert False
        finally:
            return self.reslut,rsp_get
        
    '''
    方法api_put
    key為要帶入的jsondata
    進行比對格式，並檢查respones資料是否有新增、修改jsondata
    ''' 
    def api_put(self, key):
        self.reslut ='pass'
        try:
            rsp_get = self.get('')
            rsp_put = self.put(key)
            if rsp_put['status'] =="ok":
                assert self.data_format(self.rsp_pass,rsp_put) == True
                rsp_putget = self.get('') 
                for i in rsp_putget.keys():
                    if rsp_putget[i] == type([]):
                        r  = rsp_putget[i] 
                target = []
                target_data = {}
                for i in key:
                    solution = i["solution"]
                    dev_info = {
                        "dev_id": i["dev_id"],
                        "target": i["target"]
                    }
                if solution not in target_data:
                    target_data[solution] = {
                        "solution": solution,
                        "dev_list": []
                    }
                target_data[solution]["dev_list"].append(dev_info)
                target = list(target_data.values())
                assert self.check(target,r) ==True
            elif rsp_put['status'] =="fail":
                assert self.data_format(self.rsp_fail,rsp_put) == True
                rsp_putget = self.get('') 
                assert rsp_putget == rsp_get
            else:
                rsp_putget = self.get('')
                assert False
        except AssertionError:
            self.reslut = 'fail'
            assert False
        finally:
            if rsp_put['status'] == 'fail': return self.reslut,rsp_put
            else: return self.reslut,rsp_putget
    '''
    方法api_del
    key為要帶入的jsondata
    進行比對格式，並檢查respones資料是否有刪除jsondata
    '''   
    def api_del(self,key):
        self.reslut = 'pass'
        try:
            rsp_get = self.get('')
            rsp_delete = self.delete(key)
            if rsp_delete['status'] == 'ok':
                assert self.data_format(self.rsp_pass,rsp_delete) == True
                rsp_deleteget = self.get('')
                for i in rsp_deleteget.keys():
                    if rsp_deleteget[i] == type([]):
                        r  = rsp_deleteget[i] 
                list = []
                if type(key) == type({}):
                    for j in key.keys():
                        if  "_list" in j:
                            for k in key[i]:
                                e = {}
                                e[j.replace('list','')] =k
                                list.append(e)
                if type(key) == type([]):
                    for j in key:
                        e={}
                        for k in j:
                            if type(i[j]) == type([]):
                                e[k.replace("_id","_list")]  =[]
                                for c in j[k]:
                                    e[k.replace("_id","_list")].append({k:c})
                                list.append(e)
                            else:
                                e[k] = j[k]
                elif list != []:
                    key = list
                assert self.check(key,r) == False
            elif rsp_delete['status'] == 'fail':
                assert self.data_format(self.rsp_fail,rsp_delete) == True
                rsp_deleteget = self.get('') 
                assert rsp_deleteget == rsp_get
            else:
                rsp_deleteget = self.get('') 
                assert False
        except AssertionError:
            self.reslut = 'fail'
            assert False
        finally:
            if rsp_delete['status'] == 'fail': return self.reslut,rsp_delete
            else: return self.reslut,rsp_deleteget
    '''
    方法api_post
    key為要帶入的jsondata
    進行比對格式，並檢查respones資料是否有刪除jsondata
    '''
    def api_post(self, key):
        self.reslut ='pass'
        try:
            rsp_get = self.get('')
            rsp_post = self.post(key)
            if rsp_post['status'] =="ok":
                assert self.data_format(self.rsp_pass,rsp_post) == True
                rsp_postget = self.get('') 
                for i in rsp_postget.keys():
                    if rsp_postget[i] == type([]):
                        r  = rsp_postget[i] 
                assert self.check(key,rsp_postget) ==True
            elif rsp_post['status'] =="fail":
                assert self.data_format(self.rsp_fail,rsp_post) == True
                rsp_postget = self.get('') 
                assert rsp_postget == rsp_get
            else:
                rsp_postget = self.get('')
                assert False
        except AssertionError:
            self.reslut = 'fail'
            assert False
        finally:
            if rsp_post['status'] == 'fail': return self.reslut,rsp_post
            else: return self.reslut,rsp_postget

    def api_post1(self, key):
        self.reslut ='pass'
        try:
            rsp_get = self.post1('')
            rsp_post = self.post1(key)
            if rsp_post['status'] =="ok":
                assert self.data_format(self.rsp_pass,rsp_post)== True
                rsp_postget = self.post1('')
                assert self.check(key,rsp_postget) == True
            elif rsp_post['status'] =="fail":
                assert self.data_format(self.rsp_fail,rsp_post) == True
                rsp_postget = self.post1('')
                assert rsp_postget==rsp_get
            else: 
                rsp_postget = self.post1('')
                assert False         

        except AssertionError:
            self.reslut = 'fail'
            assert False
        finally:
            if rsp_post['status'] == 'fail': return self.reslut,rsp_post
            else: return self.reslut,rsp_postget

'''
Test為繼承Apitest
get_test為測試resful get api 給予key，如果不是pass會回覆哪個key錯誤
put_test為測試resful put api 給予json data，如果不是pass會回覆哪個key錯誤
del_test為測試resful delete api 給予json data，如果不是pass會回覆哪個key錯誤
post_test為測試resful post api 給予json data，如果不是pass會回覆哪個key錯誤
'''            
class Test(Apitest):
    def init(self,base_url,format):
        self.initUrl(base_url)
        self.format = format

    def get_test(self,key=""):
        rs,rg=self.api_get(key,self.format)
        if key == '':key='全部'
        pytest.assume(rs=='pass',"GET data:"+key+"錯誤")
        return rs,rg
    
    def put_test(self,key):
        rs,rg = self.api_put(key)
        pytest.assume(key != '', 'jsondata不可為空的')
        pytest.assume(rs == 'pass',('PUT data:',key,'錯誤'))
        return rs,rg

    def del_test(self, key):
        rs,rg = self.api_del(key)
        pytest.assume(rs == 'pass',('Del data:',key,'錯誤'))
        pytest.assume(key != '', 'jsondata不可為空的')
        return rs,rg
    
    def post_test(self,key):
        rs,rg = self.api_post(key)
        pytest.assume(key != '', 'jsondata不可為空的')
        pytest.assume(rs == 'pass',('post data:',key,'錯誤'))
        return rs,rg
    
    def post1_test(self,key):
        rs,rg = self.api_post1(key)
        pytest.assume(key != '', 'jsondata不可為空的')
        pytest.assume(rs == 'pass',('post data:',key,'錯誤'))
        return rs,rg
