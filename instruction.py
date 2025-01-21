import subprocess 

class instruction():
    def Tojunit(self,name):  
        Tj = subprocess.run("pytest "+name+" --junitxml junit-report.xml",shell=True, text=True, capture_output=True) 
        return Tj.stdout ,Tj.stderr
    
    def trcli(self,username,passsword, testrailURL, project,file, title, log = False): 
        if log:
            tr = subprocess.run("trcli -u "+username+" -p "+passsword+" -h "+testrailURL+" --project "+project+" -v  parse_junit -f "+file+" --title "+title,shell=True, text=True, capture_output=True) 
        else:
            tr = subprocess.run("trcli -u "+username+" -p "+passsword+" -h "+testrailURL+" --project "+project+" parse_junit -f "+file+" --title "+title,shell=True, text=True, capture_output=True) 
        return tr.stdout ,tr.stderr

