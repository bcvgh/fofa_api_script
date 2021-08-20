import os.path
import requests,base64,time,json
import argparse
import configparser
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import csv
requests.packages.urllib3.disable_warnings()
pwd_dir = os.path.dirname(os.path.abspath(__file__))
f_route = pwd_dir+'\\'+'data'+'\\'
conf = configparser.ConfigParser()
conf.read(pwd_dir+"\\config.ini")
email = conf.get("Data","email")
api_key = conf.get("Data","api_key")
num = conf.get("Data","number")
session=requests.session()
header = {
    'Use-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0Accept: application/json, text/javascript, */*; q=0.01',
    'Upgrade-Insecure-Request':'1',
}
par =['search','type','file','route']
def arg_s():
    parser = argparse.ArgumentParser(description="fofa!fofa!fofa!")
    parser.add_argument('-s','--search',help='查询内容')
    parser.add_argument('-t','--type',help='查询类型')
    parser.add_argument('-f','--file',help='导出文件名')
    parser.add_argument('-r','--route',help='导出文件路径')
    parser.add_argument('-n','--num',help='显示数量')
    args = parser.parse_args()
    if args.search is None:
        print(parser.print_help())
        exit()
    if args.type is None:
        args.type = "csv"
    if args.file is None:
        now = str(args.search)+'_'+str(time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time())))
        args.file=now
    if args.route is None:
        args.route=f_route
    if args.num is None:
        args.num = num
    return args

def main():
    args = arg_s()
    sea = args.search.encode()
    qbase64 = base64.b64encode(sea)
    qbase64 = str(qbase64,'utf-8')
    url = 'https://fofa.so/api/v1/search/all?email={0}&key={1}&qbase64={2}&size={3}'.format(email,api_key,qbase64,args.num)
    res = session.get(url=url,verify=False,headers=header)
    result=res.text
    result = json.loads(result)
    _file=args.route+args.file+'.'+args.type
    with open(_file,'w+',newline='') as csvs:
        csv_w = csv.writer(csvs)
        csv_w.writerow(["host","ip","port"])
        for i in result["results"]:
            csv_w.writerow([i[0],i[1],i[2]])
        csv_w.writerow(str(len(result["results"])))
    # with open(args.file+'_'+str(len(result["results"]))+'.'+args.type) as fi:
    #     for i in result["result"]:
    #         fi.write(i[0].encode('utf-8')+'\n')
    # print(len(result["result"]))

if __name__ == "__main__":
    main()
    print('success!')
