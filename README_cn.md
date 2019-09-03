中文|[英文](README.md)

开发者可以将本application部署至Atlas 200DK上实现对摄像头数据的实时采集、并对视频中的人脸信息进行预测的功能。

## 前提条件

部署此Sample前，需要准备好以下环境：

-   保证开发版的系统版本为887及其以上，连接好相机，并连接在Channel1上。
-   开发板完成相关Python环境和系统必要配置。

## 环境配置

    将https://github.com/Ascend/sample-facedetection-python  
	仓中的代码下载至所在Ubuntu服务器的任意目录，例如代码存放路径为：$HOME/ascend/sample-facedetection-python。


## 部署<a name="zh-cn_topic_0167071573_section7994174585917"></a>
	部署操作全部在UIHost端操作
-   步骤 1 进入sample-facedetection-python的script目录，切换到root用户:

        cd sample-facedetection-python/script/
        su root 
        
	然后执行命令：

	bash deploy.sh <用户名> <ip地址> <usb网卡名> <外网名> 
	
	即可完成样例的部署。命令执行过程中需要按照提示输入用户名密码等信息。
    
	示例：

	**图 1**  网口配置<a name="zh-cn_topic_0167071573_fig184321447181017"></a>  
	![](doc/source/img/ifconfig.png "网口配置图")
	
	例如：如[图1](#zh-cn_topic_0167071573_fig184321447181017)所示，假设自己的用户用户名为HwHiAiUser,开发板ip地址为192.168.1.2,则终端命令应该写成

        bash deploy.sh HwHiAiUser 192.168.1.2 ens33 ens35u1

	
-   步骤 2<a name="zh-cn_topic_0167071573_fig184321447181030"></a>启动Presenter Server

	在部署脚本执行成功后，继续输入命令
	
	bash run_presenterserv.sh

	**图 2**  Presenter Server进程启动<a name="zh-cn_topic_0167071573_fig184321447181018"></a>  
	![](doc/source/img/PresenterServerStartup.png "Presenter Server进程启动")  
	
	使用[图2](#zh-cn_topic_0167071573_fig184321447181018)提示的URL登录Presenter Server，仅支持Chrome浏览器。IP地址为图中输入的IP地址，端口号默为7007，如图3<a name="zh-cn_topic_0167071573_fig184321447181019"></a>  所示，表示Presenter Server启动成功。    
	
	**图 3**  Presenter Server页面<a name="zh-cn_topic_0167071573_fig184321447181019"></a>  
	![](doc/source/img/PresenterServerWeb.png "Presenter Server页面")  	


## 运行
-   步骤 1<a name="zh-cn_topic_0167071573_fig184321447181032"></a> 运行sample-facedetection-python程序。
	进入sample-facedetection-python的script目录，切换到root用户:

        cd sample-facedetection-python/script/
        su root 
	
	然后执行命令
	
	bash run_facedetectionapp.sh <用户名>@<ip>      
	
        其中：   
       （1）用户名参数为开发板的登录用户名，默认为HwHiAiUser   
       （2）ip参数为开发板网口地址。采用usb网口连接时，默认地址是192.168.1.2； 网线连接时，默认地址是192.168.0.2    
	如果不输入用户名和ip参数，脚本默认采用 HwHiAiUser@192.168.1.2    
        
-   步骤 2 登录 Presenter Server web页面。地址为启动Presenter Server服务时提示的URL，详细可参考部署的步骤[2](#zh-cn_topic_0167071573_fig184321447181030)。    
	等待Presenter Agent传输数据给服务端，单击“Refresh”刷新，当有数据时相应的Channel 的Status变成绿色，如图4所示。

	**图 4**  Presenter Sever运行<a name="zh-cn_topic_0167071573_fig184321447181020"></a>  
    ![](doc/source/img/PresenterServerRun.png "Presenter Server运行.png")  

	Face Detection的Presenter Server最多支持10路Channel同时显示，每个 presenter_view_app_name 对应一路Channel。
	由于硬件的限制，每一路支持的最大帧率是20fps，受限于网络带宽的影响，帧率会自动适配为较低的帧率进行展示。
-   步骤 3 单击右侧对应的View Name链接，比如上图的“video”，查看结果，对于检测到的人脸，会给出置信度的标注。

## 后续处理

-   **停止Face Detection应用**	
	
	执行Face Detection运行脚本后， 应用会处于持续运行状态。若要停止应用程序，可以在UIHost端进入ample-facedetection-python/script目录，切换到root用户
    
        cd sample-facedetection-python/script/
        su root
	
	执行命令
        
        bash stop_facedetectionapp.sh <用户名>@<ip> 
	
	用户名和ip参数参见运行节步骤[1](#zh-cn_topic_0167071573_fig184321447181032)，如果不输入参数 默认为HwHiAiUser@192.168.1.2

-   **停止Presenter Server服务**

       Face Detection的Presenter Server启动后会处于持续运行状态。若要停止Presenter Server应用程序，可以在UIHost端进入sample-facedetection-python/script目录下，切换到root用户
	  	  
         cd sample-facedetection-python/script/    
         su root
  
       执行终端命令
    
         bash stop_presenterserver.sh   
