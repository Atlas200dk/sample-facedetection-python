中文|[English](Readme.md)

# 人脸检测（python）<a name="ZH-CN_TOPIC_0232621882"></a>

开发者可以将本application部署至Atlas 200DK上实现对摄像头数据的实时采集、并对视频中的人脸信息进行预测的功能。

当前分支中的应用适配**1.3.0.0**与**1.32.0.0及以上**版本的[DDK&RunTime](https://ascend.huawei.com/resources)。

## 前提条件<a name="zh-cn_topic_0228757088_section1524472882216"></a>

部署此Sample前，需要准备好以下环境：

-   已完成Mind Studio的安装。

-   已完成Atlas 200 DK开发者板与Mind Studio的连接，SD卡的制作、编译环境的配置等。
-   由于需要配置开发板联网，默认设置为USB连接，开发板地址为192.168.1.2

## 环境部署<a name="zh-cn_topic_0228757088_section772075917223"></a>

可以选择如下快速部署或者常规方法部署，二选一即可：

1.  快速部署，请参考：  [https://github.com/Atlas200dk/faster-deploy](https://github.com/Atlas200dk/faster-deploy)  。

    >![](public_sys-resources/icon-note.gif) **说明：**   
    >-   该快速部署脚本可以快速部署多个案例，请选择sample-facedetection-python案例部署即可。  
    >-   该快速部署脚本自动完成了代码下载、模型转换、环境变量配置等流程，如果需要了解详细的部署过程请选择常规部署方式。转：**[2. 常规部署](#zh-cn_topic_0228752402_li3208251440)**  

2.  <a name="zh-cn_topic_0228752402_li3208251440"></a>常规部署，请参考：  [https://github.com/Atlas200dk/sample-README/tree/master/sample-facedetection-python](https://github.com/Atlas200dk/sample-README/tree/master/sample-facedetection-python)  。

    >![](public_sys-resources/icon-note.gif) **说明：**   
    >-   该部署方式，需要手动完成代码下载、模型转换、环境变量配置等过程。完成后，会对其中的过程更加了解。  


## 环境配置<a name="zh-cn_topic_0228757088_section1637464117139"></a>

**注：开发板上hiai库、opencv库、相关依赖已安装可跳过此步骤。**

1.  配置开发板联网。

    请参考[https://github.com/Atlas200dk/sample-README/tree/master/DK\_NetworkConnect](https://github.com/Atlas200dk/sample-README/tree/master/DK_NetworkConnect)  ，进行开发板网络连接配置。

2.  安装环境依赖（请安装python3相关依赖，当前此案例只适配python3）。

    请参考[https://github.com/Atlas200dk/sample-README/tree/master/DK\_Environment](https://github.com/Atlas200dk/sample-README/tree/master/DK_Environment)  ，进行环境依赖配置。


## 部署<a name="zh-cn_topic_0228757088_section7994174585917"></a>

1.  以Mind Studio安装用户进入facedetectionapp应用代码所在根目录，如：$HOME/sample-facedetection-python。
2.  修改face\_detection.conf中presenter\_server\_ip为当前ubuntu服务器上和atlas200dk开发板连接的网口ip，atlas200dk\_board\_ip为开发板上和ubuntu服务器连接的网口ip。

    如使用USB连接，开发板的USB网口ip为192.168.1.2，ubuntu服务器和开发板连接的虚拟网卡的网口ip为192.168.1.134，则配置文件内容如下所示：

    **presenter\_server\_ip=192.168.1.134**

    **presneter\_server\_port=7006**

    **atlas200dk\_board\_id=192.168.1.2**

    >![](public_sys-resources/icon-note.gif) **说明：**   
    >-   一般通过USB连接时，atlas200dk\_board\_ip为开发板的USB网口ip，默认为192.168.1.2。通过网口连接时，atlas200dk\_board\_ip为开发板的网络网口ip，默认为192.168.0.2。  

3.  应用代码拷贝到开发板。

    以Mind Studio安装用户进入语义分割网络应用\(python\)代码所在根目录，如：$HOME/sample-facedetection-python，执行以下命令将应用代码拷贝到开发板。

    **scp -r ../sample-facedetection-python/ HwHiAiUser@192.168.1.2:/home/HwHiAiUser/HIAI\_PROJECTS**

    提示password时输入开发板密码，开发板默认密码为**Mind@123**

4.  启动Presenter Server。

    执行如下命令在后台启动人脸检测python应用的Presenter Server主程序。

    **bash run\_presenter\_server.sh &**

    使用提示的URL登录Presenter Server。如下图所示，表示Presenter Server启动成功。

    **图 1**  主页显示<a name="zh-cn_topic_0228757088_fig64391558352"></a>  
    ![](figures/主页显示.png "主页显示")

    Presenter Server、Mind Studio与Atlas 200 DK之间通信使用的IP地址示例如下图所示：

    **图 2**  IP地址示例<a name="zh-cn_topic_0228757088_fig1881532172010"></a>  
    ![](figures/IP地址示例.png "IP地址示例")

    其中：

    -   Atlas 200 DK开发者板使用的IP地址为192.168.1.2（USB方式连接）。
    -   Presenter Server与Atlas 200 DK通信的IP地址为UI Host服务器中与Atlas 200 DK在同一网段的IP地址，例如：192.168.1.223。
    -   通过浏览器访问Presenter Server的IP地址本示例为：10.10.0.1，由于Presenter Server与Mind Studio部署在同一服务器，此IP地址也为通过浏览器访问Mind Studio的IP。


## 运行<a name="zh-cn_topic_0228757088_section551710297235"></a>

1.  在Mind Studio所在Ubuntu服务器中，以HwHiAiUser用户SSH登录到Host侧。

    **ssh HwHiAiUser@192.168.1.2**

    >![](public_sys-resources/icon-note.gif) **说明：**   
    >-   这里是以USB方式连接举例，此时ip为192.168.1.2。运行时请根据连接情况自行更换。  

2.  在HwHiAiUser用户下进入应用代码所在目录。

    **cd \~/HIAI\_PROJECTS/sample-facedetection-python**

3.  执行应用程序。

    **python3 main.py**

    >![](public_sys-resources/icon-note.gif) **说明：**   
    >- 可使用ctrl+c停止程序  
    >- 当前此案例只支持python3

4.  使用启动Presenter Server服务时提示的URL登录 Presenter Server 网站。

    等待Presenter Agent传输数据给服务端，单击“Refresh“刷新，当有数据时相应的Channel 的Status变成绿色，如[图 Presenter Server界面](#zh-cn_topic_0228757088_fig113691556202312)所示。

    **图 3**  Presenter Server界面<a name="zh-cn_topic_0228757088_fig113691556202312"></a>  
    ![](figures/Presenter-Server界面.png "Presenter-Server界面")

    >![](public_sys-resources/icon-note.gif) **说明：**   
    >-   Presenter Server最多支持10路Channel同时显示，每个  _presenter\_view\_app\_name_  对应一路Channel。  
    >-   由于硬件的限制，每一路支持的最大帧率是20fps，受限于网络带宽的影响，帧率会自动适配为较低的帧率进行展示。  

5.  单击右侧对应的View Name链接，比如上图的“video”，查看结果。

## 后续处理<a name="zh-cn_topic_0228757088_section1092612277429"></a>

-   **停止Presenter Server服务**

    Presenter Server服务启动后会一直处于运行状态，若想停止人脸检测应用对应的Presenter Server服务，可执行如下操作。

    以Mind Studio安装用户在Mind Studio所在服务器中的命令行中执行如下命令查看人脸检测应用对应的Presenter Server服务的进程。

    **ps -ef | grep presenter | grep face\_detection**

    ```
    ascend@ascend-HP-ProDesk-600-G4-PCI-MT:~/sample-facedetection-python$ ps -ef | grep presenter | grep face_detection
    ascend    7701  1615  0 14:21 pts/8    00:00:00 python3 presenterserver/presenter_server.py --app face_detection
    ```

    如上所示  _7701_  即为人脸检测应用对应的Presenter Server服务的进程ID。

    若想停止此服务，执行如下命令：

    **kill -9** _7701_


