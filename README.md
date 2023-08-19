
# oracle服务器保活程序

超级简单的保活程序，纯python代码，只有一个文件。  

usage: oralive.py [-h] [-c OCCU_RATE] [-p PERTIME] [-i INTERVAL] [-m--memory MEM] [-n NETINTERVAL]

oracle服务器保活程序

optional arguments:  

  -h, --help            show this help message and exit  
  
  -c , --occupancy                     cpu占用率  
                        
  -p , --persistent                        占用时长(秒)  
                        
  -i , --interval                         间隔调用(分)  
                       
  -m , --memory         占用内存(MB)
  
  -n , --netinterval                网络占用的时间间隔(分钟)
                        
                        
## 安装

`git clone https://github.com/frankiejun/oralive.git`

### 依赖
`sudo apt install speedtest-cli`  

·sudo apt install pip·

`sudo apt install python3`  

`sudo pip install argparse`  

·sudo pip install cgroups·

`sudo pip install psutil`  


## 运行


cpu占用20%，每次占用10秒，每1分钟占用一次，长期占用内存100M，每2分钟跑一次speedtest：  

`nohup oralive.py -c 20 -p 10 -i 1 -m 100 -n 2 &`

也可以使用默认值(全为0使用的是默认值)：  

`nohup oralive.py -c 0 -p 0 -i 0 -m 0 -n 0 > /dev/null 2>&1 &`  

