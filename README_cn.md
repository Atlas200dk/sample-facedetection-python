中文|[英文](README.md)

开发者可以将本application部署至Atlas 200DK上实现对摄像头数据的实时采集、并对视频中的人脸信息进行预测的功能。

## 前提条件

部署此Sample前，需要准备好以下环境：

-   保证开发版的系统版本为887及其以上，连接好相机，并连接在Channel1上。
-   开发板完成相关Python环境和系统必要配置。

## 环境配置
-   步骤 1 UIHost端配置相关环境。

    在UIHost端root用户下，进入sample-facedetection-python目录下的script目录执行bash install_uihost.sh即可完成所有配置。
-   步骤 2 获取源码包。

    将https://github.com/Ascend/sample-facedetection-python仓中的代码下载至所在Ubuntu服务器的任意目录，例如代码存放路径为：$HOME/ascend/sample-facedetection-python。


## 部署<a name="zh-cn_topic_0167071573_section7994174585917"></a>
	部署操作全部在UIHost端操作
-   步骤 1 以root用户在终端切换到sample-facedetection-python的script目录，然后执行下列指令。

	在终端键入bash deploy.sh按照提示输入两次密码即可完成deploy操作
	
	在终端键入bash install_host.sh自动完成环境依赖安装
	
	在终端键入bash network_uihost.sh USB网卡名称 外网地址 自动完成UIHost联网操作
	
	例如：如下图，
	![](doc/source/img/ifconfig.png "网口配置图")
	则应该写成bash network_uihost.sh ens33 ens35u1

	在终端键入./network_host.sh进行Host更新与安装依赖
	
-   步骤 2 启动Presenter Server。

	以root用户在终端切换到sample-facedetection-python目录下script目录执行Face Detection应用的Presenter Server主程序。
	
	bash run_presenterserv.sh

	**图 1**  Presenter Server进程启动  
	使用上图提示的URL登录Presenter Server，仅支持Chrome浏览器。IP地址为图中输入的IP地址，端口号默为7007，如下图所示，表示Presenter Server启动成功。


## 运行
-   步骤 1 运行sample-facedetection-python程序。
	以root用户在UIHost端的终端切换到sample-facedetection-python/script运行应用程序。
	bash run.sh
-   步骤 2 在UIHost端使用启动Presenter Server服务时提示的URL登录 Presenter Server 网站，详细可参考部署的步骤2。
	等待Presenter Agent传输数据给服务端，单击“Refresh”刷新，当有数据时相应的Channel 的Status变成绿色，如图3.2所示。

	**图 3**  Presenter Sever界面


	Face Detection的Presenter Server最多支持10路Channel同时显示，每个 presenter_view_app_name 对应一路Channel。
	由于硬件的限制，每一路支持的最大帧率是20fps，受限于网络带宽的影响，帧率会自动适配为较低的帧率进行展示。
-   步骤 3单击右侧对应的View Name链接，比如上图的“video”，查看结果，对于检测到的人脸，会给出置信度的标注。

## 后续处理

-   **停止Face Detection应用**

    Face Detection应用执行后会处于持续运行状态，若要停止sample-facedetection-python应用程序，在到UIHost端以root用户切换单sample-facedetection-python/script目录下执行终端命令
    
	bash stop.sh

-   **停止Presenter Server服务**

    Face Detection的Presenter Server执行后会处于持续运行状态，若要停止Presenter Server应用程序，在到UIHost端以root用户切换单sample-facedetection-python/script目录下执行终端命令
    
	bash stop_presenterserver.sh
