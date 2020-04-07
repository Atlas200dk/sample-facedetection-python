English|[中文](Readme_cn.md)

# Face Detection \(Python\)<a name="EN-US_TOPIC_0232617557"></a>

You can deploy this application on the Atlas 200 DK to collect camera data in real time and predict facial information in the video.

The current application adapts to  [DDK&RunTime](https://ascend.huawei.com/resources)  of 1.3.0.0 as well as 1.32.0.0 and later versions.

## Prerequisites<a name="section1524472882216"></a>

Before deploying this sample, ensure that:

-   Mind Studio  has been installed.

-   The Atlas 200 DK developer board has been connected to  Mind Studio, the SD card has been created, and the build environment has been configured.
-   The developer board is connected to the Internet over the USB port by default. The IP address of the developer board is  **192.168.1.2**.

## Software Preparation<a name="section772075917223"></a>

You can use either of the following methods:

1.  Quick deployment: visit  [https://github.com/Atlas200dk/faster-deploy](https://github.com/Atlas200dk/faster-deploy).

    >![](public_sys-resources/icon-note.gif) **NOTE:**   
    >-   The quick deployment script can be used to quickly deploy multiple cases. Select  **sample-facedetection-python**.  
    >-   The quick deployment script automatically completes code download, model conversion, and environment variable configuration. To learn about the detailed deployment process, select the common deployment mode. Go to  [2. Common deployment](#li3208251440).  

2.  <a name="li3208251440"></a>Common deployment: visit  [https://github.com/Atlas200dk/sample-README/tree/master/sample-facedetection-python](https://github.com/Atlas200dk/sample-README/tree/master/sample-facedetection-python).

    >![](public_sys-resources/icon-note.gif) **NOTE:**   
    >-   In this deployment mode, you need to manually download code, convert models, and configure environment variables. After that, you will have a better understanding of the process.  


## Environment Settings<a name="section1637464117139"></a>

Note: If the HiAI library, OpenCV library, and related dependencies have been installed on the developer board, skip this step.

1.  Configure the network connection of the developer board.

    Configure the network connection of the Atlas DK developer board by referring to  [https://github.com/Atlas200dk/sample-README/tree/master/DK\_NetworkConnect](https://github.com/Atlas200dk/sample-README/tree/master/DK_NetworkConnect).

2.  Install the environment dependencies（please deploy in python3）.

    Configure the environment dependency by referring to  [https://github.com/Atlas200dk/sample-README/tree/master/DK\_Environment](https://github.com/Atlas200dk/sample-README/tree/master/DK_Environment).


## Deployment<a name="section19787193103013"></a>

1.  Go to the root directory where the crowdcounting-python application code is located as the  Mind Studio  installation user, for example,  **$HOME/sample-facedetection-python**.
2.  In  **face\_detection.conf**, change  **presenter\_server\_ip **to the IP address of the ETH port on the Ubuntu server for connecting to the Atlas 200 DK developer board, and  **atlas200dk\_board\_ip **to the IP address of the ETH port on the developer board for connecting to the Ubuntu server.

    In USB connection mode, the IP address of the USB ETH port on the Atlas DK is 192.168.1.2, and the IP address of the virtual NIC ETH port on the Ubuntu server connected to the Atlas DK is 192.168.1.134. The configuration file content is as follows:

    **presenter\_server\_ip=192.168.1.134**

    **presneter\_server\_port=7006**

    **atlas200dk\_board\_id=192.168.1.2**

    >![](public_sys-resources/icon-note.gif) **NOTE:**   
    >-   Generally,  **atlas200dk\_board\_ip **indicates the IP address of the USB ETH port on the Atlas 200 developer board. The default value is 192.168.1.2. In ETH connection mode,  **atlas200dk\_board\_ip **indicates the IP address of the ETH port on the Atlas 200 developer board. The default value is 192.168.0.2.  

3.  Copy the application code to the developer board.

    Go to the root directory of the semantic segmentation application \(python\) code as the  Mind Studio  installation user, for example,  **$HOME/sample-facedetection-python**, and run the following command to copy the application code to the developer board:

    **scp -r ../sample-facedetection-python/ HwHiAiUser@192.168.1.2:/home/HwHiAiUser/HIAI\_PROJECTS**

    Type the password of the developer board as prompted. The default password is** Mind@123**.

4.  Start Presenter Server.

    Run the following command to start the Presenter Server program of the face detection \(Python\) application in the background:

    **bash run\_presenter\_server.sh &**

    Use the pop-up URL to log in to Presenter Server. The following figure indicates that Presenter Server is started successfully.

    **Figure  1**  Home page<a name="en-us_topic_0228757088_fig64391558352"></a>  
    ![](figures/home-page.png "home-page")

    The following figure shows the IP address used by Presenter Server and  Mind Studio  to communicate with the Atlas 200 DK.

    **Figure  2**  IP address example<a name="en-us_topic_0228757088_fig1881532172010"></a>  
    ![](figures/ip-address-example.png "ip-address-example")

    In the preceding figure:

    -   The IP address of the Atlas 200 DK developer board is  **192.168.1.2**  \(connected in USB mode\).
    -   The IP address used by Presenter Server to communicate with the Atlas 200 DK is in the same network segment as the IP address of the Atlas 200 DK on the UI Host server, for example,  **192.168.1.223**.
    -   The following describes how to access the IP address \(such as  **10.10.0.1**\) of Presenter Server using a browser. Because Presenter Server and  Mind Studio  are deployed on the same server, you can access  Mind Studio  through the browser using the same IP address.


## Run<a name="section1578813311309"></a>

1.  Log in to the host side as the  **HwHiAiUser**  user in SSH mode on Ubuntu Server where  Mind Studio  is located.

    **ssh HwHiAiUser@192.168.1.2**

    >![](public_sys-resources/icon-note.gif) **NOTE:**   
    >-   The following uses the USB connection mode as an example. In this case, the IP address is 192.168.1.2. Replace the IP address as required.  

2.  Go to the directory where the application code is stored as the  **HwHiAiUser**  user.

    **cd \~/HIAI\_PROJECTS/sample-facedetection-python**

3.  Run the application.

    **python3 main.py**

    >![](public_sys-resources/icon-note.gif) **NOTE:**   
    >- You can press  **Ctrl**+**C**  to stop the application.  
    >- Currently this case only supports python3.

4.  Use the URL displayed upon the start of the Presenter Server service to log in to Presenter Server.

    Wait for Presenter Agent to transmit data to the server. Click  **Refresh**. When there is data, the icon in the  **Status**  column for the corresponding channel changes to green, as shown in  [Figure 3](#en-us_topic_0228757088_fig113691556202312).

    **Figure  3**  Presenter Server page<a name="en-us_topic_0228757088_fig113691556202312"></a>  
    ![](figures/presenter-server-page.png "presenter-server-page")

    >![](public_sys-resources/icon-note.gif) **NOTE:**   
    >-   The Presenter Server supports a maximum of 10 channels at the same time \(each  _presenter\_view\_app\_name_  parameter corresponds to a channel\).  
    >-   Due to hardware limitations, each channel supports a maximum frame rate of 20 fps. A lower frame rate is automatically used when the network bandwidth is low.  

5.  Click a link in the  **View Name**  column, for example,  **video**  in the preceding figure, and view the result.

