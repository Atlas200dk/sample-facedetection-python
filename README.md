EN|[CN](README_cn.md)

Developers can deploy the application on the Atlas 200 DK to collect camera data in real time and predict facial information in the video.
Note:uihost refers to the Ubuntu PC server; host refers to altas200dk development board; device refers to ascend310 chip

## Prerequisites

Before using an open source application, ensure that:

-   The Atlas 200 DK developer board version must be 887 at least 
-   The board should connect camra with CAMERA0
-   Login the development board through the Ubuntu server SSH is avaliable
-   The Atlas 200 DK developer board complete the necessary configuration of Python environment and system

## Enviroment Configuration
-  Get Code  
Download all the code in the sample-facedetection repository at https://github.com/Ascend/sample-facedetection-python  to any directory on Ubuntu PC Server, for example,  _/home/ascend/sample-facedetection/_.
-  Install dependency

	Switch to root user,enter the directory sample-facedetection-python/script，excute the following command:

	bash install.sh board-ip internet-ip usb-network-ip
	
	board-ip: the developer board ip. The default ip is 192.168.1.2 when connect with usb
	
	internet-ip: the Ubuntu PC server ip that link to internet
	
	usb-network-ip: the Ubuntu PC server ip that link to developer board
	
	The install.sh script performs the following operations:
	
	1.Install the python package dependency of the presenter server
	
	2.Configure the developer board and Ubuntu pc server network so that the developer board can connect to the Internet. Both the Ubuntu pc server and the developer board network configuration need to be executed as root user, so you need to switch to the root account on the Ubuntu pc server to execute the install.sh script. In addition, the install.sh script on the developer board will also switch to the root account to execute the configuration command. When switching, the user will be prompted to enter the root account password of the developer board. The default password is "mind @ 123";
	
	3.Upgrade and update the Linux system of the developer board. In order to install the Python package dependency in developer board, the install.sh script will automatically execute the commands "apt-get update" and "apt-get upgrade" on the development board. According to the status of the network and the developer board, such as whether the update has been executed, the execution time of this step may exceed 20 minutes. During the installation, if arise query or interact, select y or default
	
	4.Install the model inference Python package hiai, and it's Python packages dependency such as Python-dev, numpy, Pip, esasy_install, enum34, funcsigns, future. Because numpy is compiled and installed in a long time, the installation time will be more than 10 minutes. During the installation process, there will be installation query interaction. Enter y
	
	Note: the installation environment only needs to be executed in the following two scenarios: 
	
	(1) Running the face detection sample for the first time; 
	
	(2) Running the face detection sample after upgrading the developer board with make startup card afresh.
	
	You do not need to perform after a successful installation
  

## Deployment
	The deployment should be in UIHost.
-   Step 1 Switch to normal user,then switch to the directory sample-facedetection-python/script，excute the following commands:

	bash deploy.sh board-ip usb-network-ip 
	
	board-ip: the developer board ip that link to Ubuntu PC server
	
	usb-network-ip: the Ubuntu Pc server ip that link to developer board
	
	for example：The following figure shown,ip is 192.168.1.2 and usb network ip is 192.168.1.223.the command should be 
    
    bash deploy.sh 192.168.1.2 192.168.1.223

	
-   Step 2 Strat Presenter Server。

	Switch to root user,then switch to the directory sample-facedetection-python/script，excute the following commands to run the presenter server
	
	bash run_presenterserv.sh

	**figure 1**  Start Presenter Server  
	Use the URL shown in the preceding figure to log in to Presenter Server \( only the Chrome browser is supporte \). The IP address is 
	that entered in  [Figure 3](#en-us_topic_0167089636_fig64391558352)  and the default port number is  **7007**. The following figure 
	indicates that Presenter Server is started successfully.

	**figure 2**  HomePage for Presenter Server
      

## Running
-   Step 1 Run sample-facedetection-python application。
	Switch to root user,then switch to the directory sample-facedetection-python/script，excute the following commands to run the application

	bash run_facedetectionapp.sh username@ip
    
    Tips:running the shell need to input password twice.first time ,the password is the username's password,the second ,the password is the root user's password.if paramter not given,the default is HwHiAiUser@192.168.1.2

-   Step 2 Use the URL that is displayed when you start the Presenter Server service to log in to the Presenter Server website. For details, see the Deployment Step 2
	Wait for Presenter Agent to transmit data to the server. Click  **Refresh**. When there is data, the icon in the  **Status**  column for the corresponding channel changes to green, as shown in following figure.

	**figure 3**  Presenter Sever Interface


    >-   The Presenter Server of the face detection application supports a maximum of 10 channels at the same time , each  presenter\_view\_app\_name  parameter corresponds to a channel.  
    >-   Due to hardware limitations, the maximum frame rate supported by each channel is 20fps,  a lower frame rate is automatically used when the network bandwidth is low.  
-   Step 3 Click  **image**  or  **video**  in the  **View Name**  column and view the result. The confidence of the detected face is marked.

## Follow-up Operations

-   **Stop Face Detection Application**

    The face detection application is running continually after being executed. To stop it, perform the following operation:
    
	bash stop_facedetectionapp.sh username@ip
    
    Tips:running the shell need to input password twice. first time ,the password is the username's password,the second ,the password is the root user's password.if paramter not given,the default is HwHiAiUser@192.168.1.2

-   **Stop Presenter Server Service**

    The Presenter Server service is always in the running state after being started. To stop the Presenter Server service of the face detection application, perform the following operations:
    
	bash stop_presenterserver.sh
