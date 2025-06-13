import requests
import base64

class AutoAdd():
    def __init__(self):
        self.auth_header = base64.b64encode(f"{'john.jian@insynerger.com'}:{'I3JZQgjhRyZrQVMW21sT-u47Nw36YQNj0O0Od6gfR'}".encode()).decode()
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.auth_header}"
        }
        self.URL = "https://chifong0123456.testrail.io/index.php?/api/v2/"
    
    def GetPID(self, APIname,name):
        key = "projects"
        get = requests.get(self.URL+APIname,headers=self.headers).json()
        for i in get[key]:
            if i['name'] == name: return i['id']
        return False
    
    def Addsection(self,addinproject,data):
        id = self.GetPID("get_projects",addinproject)
        reponses = requests.post(self.URL+'add_section/'+str(id),json=data,headers=self.headers).json()
        return reponses,id
    
    def Addcase(self,Project,addinsection,data):
        id = self.GetPID("get_projects",Project)
        get = requests.get(self.URL+"get_sections/"+str(id),headers=self.headers).json()
        for i in get['sections']:
            if i['name'] == addinsection: sID = i['id']       
        reponses = requests.post(self.URL+'add_case/'+str(sID),json=data,headers=self.headers).json()
        return reponses
auth_header = base64.b64encode(f"{'john.jian@insynerger.com'}:{'I3JZQgjhRyZrQVMW21sT-u47Nw36YQNj0O0Od6gfR'}".encode()).decode()
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Basic {auth_header}"
}
get = requests.get("https://chifong0123456.testrail.io/index.php?/api/v2/get_cases/4",headers=headers).json()
# data = {
#     "name": "New Section Name",
#     "description": "Optional description for this section",    
# } 
# Pid = AutoAdd().Addsection('test1',data)
# print(Pid)
# data1= {
#     "title": "New Test Case Example",
#     "refs": "123",
#     "custom_automation_id" : "New Test Case Example",
#     "custom_preconds": "123",
#     "custom_steps": "My test steps",
#     "custom_expected": "My expected final results"
# }
# print(AutoAdd().Addcase('test1','New Section Name',data1))
