from filefc import Test
from doc import Doc
import pytest

test = Test()
doc = Doc()
#測試報告檔案名稱
file_name = 'Web API取得模組的啟用狀態、回報、輪詢時間'
#測試報告裝置名稱
dev_name = 'Setting 取得模組的啟用'
#測試報告的陣列
report_array = []
#測試的Url
base_url = "https://192.168.10.135/api/setting/config/module/enabled"
#需要比對的資料格式
format = {
            "status": str,
            "data": [
                { 
                    "module" : str,
                    "type" : str,
                    "main_module": str, 
                    "main_type": str,  
                    "enable" : int,
                    "reporting_period" : int,    
                    "polling_period" : int      
                }
            ]
        }

#測試步驟
step = [
    "1.輸入"+base_url,
    "2.給予data",
    "3.取得Rsp"
    ]

#gdata為測試api get所需的資料陣列 [[測試名稱,測試目的,key],[測試名稱,測試目的,key]...]
gdata = [['取得全部模組的啟用狀態','可以取得全部模組的啟用狀態',''],
         ['取得全部有啟用的模組','可以取得全部有啟用的模組','enable=1'],
         ['取得全部沒有啟用的模組','可以取得全部沒有啟用的模組','enable=0'],
         ['取得指定的模組類型','可以取得指定的模組類型','mode=modbus'],
         ['取得特殊模組主體','可以取得特殊模組主體','ex_need=main'],
         ['取得特殊模組子體','可以取得特殊模組子體','ex_need=sub'],
         ['取得沒有啟用類型為modbus','可以取得沒有啟用類型為modbus','enable=0&mode=modbus']]

#pdata為測試api post所需的資料陣列 [[測試名稱,測試目的,json_data],[測試名稱,測試目的,json_data]...]
pdata = [['修改單筆模組啟用狀態、回報、輪詢時間','可以單筆修改模組啟用狀態、回報、輪詢時間',[
    {
        "module" : "EBI21R",
        "enable" : 1,
        "reporting_period" : 60,        
        "polling_period" : 0            
    }
 
]],['修改多筆模組啟用狀態、回報、輪詢時間','可以多筆修改模組啟用狀態、回報、輪詢時間',[
    {
        "module" : "EBI21R",
        "enable" : 0,
        "reporting_period" : 60,        
        "polling_period" : 0            
    },
    {
        "module": "EM1100P",
        "enable": 1,
        "reporting_period": 120,
        "polling_period": 120            
    }
    ]],['修改模組啟用狀態、回報、輪詢時間給予錯誤的key','回報錯誤代碼',[
        {
        "mole" : "EBI21R",
        "enable" : 1,
        "reporting_period" : 60,        
        "poing_period" : 0            
        },

    ]]]

#呼叫測試方法
test.init(base_url,format)
@pytest.mark.parametrize('data',gdata)
def test_get(data):
    rs,rq = test.get_test(data[2])
    report_array.append((data[0],data[1],rs,step,'get',base_url,data[2],rq,rq))

@pytest.mark.parametrize('post_data',pdata)
def test_post(post_data):
    rs,rq = test.post_test(post_data[2])
    report_array.append((post_data[0],post_data[1],rs,step,'put',base_url,post_data[2],rq,rq))

def test_report():
    assert doc.report_word(file_name,dev_name,report_array) == True 