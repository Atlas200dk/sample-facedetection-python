EN|[CN](README_cn.md)

Developers can deploy the application on the Atlas 200 DK to collect camera data in real time and predict facial information in the video.

## Prerequisites

Before using an open source application, ensure that:

-   The Atlas 200 DK developer board version must be 887 at least and the board should connect camra with Channel1.
-   The Atlas 200 DK developer board complete the necessary configuration of Python environment and system.

## Enviroment Configuration
-   Step 1 Configure the relevant environment in UIHost.

    Switch to root user in UIHost，and enter the directory sample-facedetection-python/script,execute terminal commands bash install_uihost.sh to finish the configuration.
-   Step 2 Obtain the source code package.

    Download all the code in the sample-facedetection repository at  [https://github.com/Ascend/sample-facedetection-python]
    (https://github.com/Ascend/sample-facedetection-python)  to any directory on Ubuntu Server where MindSpore Studio is located as the MindSpore 
    Studio installation user, for example,  _/home/ascend/sample-facedetection/_.

## Deployment
	The deployment should be in UIHost.
-   Step 1 Switch to root user,then switch to the directory sample-facedetection-python/script，excute the following commands.

	input bash deploy.sh in terminal to finish deplotment.
	
	input bash install_host.sh to finish the dependency.
	
	input bash network_uihost.sh USB name Extranet address to finish network configuration.
	
	for example：The following figure shown，the command should be bash network_uihost.sh ens33 ens35u1.

	input ./network_host.sh to finish upgrade and dependency.
	
-   Step 2 Strat Presenter Server。

	Switch to root user,then switch to the directory sample-facedetection-python/script，excute the following commands to run the presenter saerver
	
	bash run_presenterserv.sh

	**figure 1**  Start Presenter Server  
	Use the URL shown in the preceding figure to log in to Presenter Server \( only the Chrome browser is supporte \). The IP address is 
	that entered in  [Figure 3](#en-us_topic_0167089636_fig64391558352)  and the default port number is  **7007**. The following figure 
	indicates that Presenter Server is started successfully.

	**figure 2**  HomePage for Presenter Server
      

## Running
-   Step 1 Run sample-facedetection-python application。
	Switch to root user,then switch to the directory sample-facedetection-python/script，excute the following commands to run the application
	bash run.sh
-   Step 2 Use the URL that is displayed when you start the Presenter Server service to log in to the Presenter Server website. For details, see the Deployment Step 2
	Wait for Presenter Agent to transmit data to the server. Click  **Refresh**. When there is data, the icon in the  **Status**  column for the corresponding channel changes to green, as shown in following figure.

	**figure 3**  Presenter Sever Interface


    >-   The Presenter Server of the face detection application supports a maximum of 10 channels at the same time , each  presenter\_view\_app\_name  parameter corresponds to a channel.  
    >-   Due to hardware limitations, the maximum frame rate supported by each channel is 20fps,  a lower frame rate is automatically used when the network bandwidth is low.  
-   Step 3 Click  **image**  or  **video**  in the  **View Name**  column and view the result. The confidence of the detected face is marked.

## Follow-up Operations

-   **Stop Face Detection Application**

    The face detection application is running continually after being executed. To stop it, perform the following operation:
    
	bash stop.sh

-   **Stop Presenter Server Service**

    The Presenter Server service is always in the running state after being started. To stop the Presenter Server service of the face detection application, perform the following operations:
    
	bash stop_presenterserver.sh
