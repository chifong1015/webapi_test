from filefc import Test
from doc import Doc
import pytest

test = Test()
doc = Doc()
#測試報告檔案名稱
file_name = 'Web-GUI統計資料API調整報告'
#測試報告裝置名稱
dev_name = 'web-GUI 統計資料API調整'
#測試報告的陣列
report_array = []
#測試的Url
base_url = "https://192.168.10.135/api/data/stats/get"
#需要比對的資料格式
format = {
            "status": str,
            "attr_list": str,
            "type": str,
            "st": str,
            "et": str,
            "data_list": [
                {
                    "dev_id": str,
                    "count_total": str,
                    "data": [
                        {
                            "time": str,
                            "attrId": str,
                            "sum": str,
                            "acc": str,
                            "table_type": str
                        }
                    ]
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
gdata = [['取得區間段統計資料','可以取得正確的區間統計資料','dev_id=IN27-1FFDD1-C043-036|01&attr=50090001200&st=2024-06-01T00:00:00&et=2024-06-01T10:00:00&type=3'],
         ['取得區間段統計資料給予錯誤','回覆錯誤代碼','dev_i=IN27-1FFDD1-C043-036|01&attr=50090001200&st=2024-06-01T00:00:00&et=2024-06-01T10:00:00&type=3']]

#呼叫測試方法
test.init(base_url,format)
@pytest.mark.parametrize('data',gdata)
def test_get(data):
    rs,rq = test.get_test(data[2])
    report_array.append((data[0],data[1],rs,step,'get',base_url,data[2],rq,rq))

# def test_report():
#     assert doc.report_word(file_name,dev_name,report_array) == True 