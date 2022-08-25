# SigmaTile and Kepware Setup
## Overview:
In this repository, there are 4 folders; "past-mfg-tile", "recent-mfg-tile", "SigmaTile_Case_STLS", and "Kepware_OPF_Instance". The first two folders contain the necessary scripts for setting up the RaspberryPi for outputting data to Kepware via pymodbus. The third folder, "SigmaTile_Case_STLs", contains the STL files for printing the RaspberryPi 3 and RaspberryPi 4 cases (top case is the same for both). The final folder contains the .OPF file which one will open with Kepware in order to create the necessary links to the RaspberryPis. 

## Folder Breakdown

    "past-mfg-tile"         

        - "SigmaTile_SenseHat_V5.py": The primary python script.
        - "mycron.tab": Crontab instance for execution of launch file upon boot of the RaspberryPi.
        - "launcher.sh": Launcher file.

    "recent-mfg-tile"   

        - "get-pip.py": The pip installer for the corresponding python script version.  
        - "SigmaTile_SenseHat_V6.py": The primary python script.
        - "mycron.tab": Crontab instance for execution of launch file upon boot of the RaspberryPi.
        - "launcher.sh": Launcher file.

    "SigmaTile_Case_STLS"   

        - "Bottom_Casing_PI3.stl": Bottom casing for PI3
        - "Bottom_Casing_PI4.stl": Bottom casing for PI4
        - "Top_Casing_PI3_PI4.stl": Top casing for the PI3 and PI4
        - "Vuforia_Assembly.stl": Used within AR Experience

    "Kepware_OPF_Instance" 

        - Contains the .opf file for the Kepware setup of the Sigma Tile.

## Repository and Folder Setup 

    Step I) Clone repo to RaspberryPi instance and Kepware instance

    Following Steps for RaspberryPi Repo Setup:
    
        Step II-a)  If on old or new RaspberryPi OS, move "past-mfg-tile" or "current-mfg-tile" to "home/{yourUserDirectory}"
        Step III-a) Rename folder to mfg-tile

    Folloing Steps for Kepware Repo Setup:
    
        Step II-b)  Go into "Kepware_OPF_Instance"
        Step III-b) Move .opf file to desired location

## Setup For Raspberry Pi - past-mfg-tile

    Step I) Once the folder has been moved and renamed with the steps above:
    
        - Open terminal and execute command: "$ cd mfg-tile"
        - Next, open the mfg-folder, and then open the launcher.sh file. Modify the path to the python script to match yours.
        - Now go back to terminal and make the "launcher.sh" executable with this command: sudo chmod +x launcher.sh
        - Next, make the "SigmaTile_SenseHat_V5.py" executable with this command: sudo chmod +x SigmaTile_SenseHat_V5.py
        
    Step II) Execution upon RaspberryPI boot:
        
        *** If you would like for your RaspberryPi to autorun the above scripts upon boot, then follow these steps. If no then the setup is complete.
    
        - Pull up terminal to edit crontab (the startup execution script) with the following command: sudo crontab -e
        - Select option 1 to edit in nano
        - Open the mfg-tile folder and open the "mycron.tab" file.
        - Correct the directory of the launcher.sh file accordingly and then copy this line.
        - Past this line into the terminal at the very last line of crontab.
        - Hit ctrl-x to save and enter to exit
        - Once complete, the RasperryPi has been fully set up.

## Setup For Raspberry Pi - current-mfg-tile

    Step I) Once the folder has been moved and renamed with the steps above:
    
        - Open terminal and execute command: "$ cd mfg-tile"
        - Next, open the mfg-folder, and then open the launcher.sh file. Modify the path to the python script to match yours.
        - Now go back to terminal and make the "launcher.sh" executable with this command: sudo chmod +x launcher.sh
        - Next, make the "SigmaTile_SenseHat_V6.py" executable with this command: sudo chmod +x SigmaTile_SenseHat_V5.py
        - Finally, make the "get-pip.py" executable with this command: sudo chmod +x get-pip.py

    Step II) Configure python instance with proper packages
    
        - Open terminal adn install twister along with pymodbus using: 
            - pip3 install pymodbus
            - pip3 install twister
        - If these are installed within a separate path more setup is required parts of the "SigmaTile_SenseHat_V6.py" script
            - There are two ways to check:
            - The first is upon install of the above libraries, you will have a warning messae giving you a separate diectory for install.
            - If this is not visible and you are still unsure, stay in terminal and execute the following commands:
                - python3
                - import sys
                - sys.path
            - If your "site-packages" path is not in path with the python interpreter then we can add it to the "SigmaTile_SenseHat_V6.py" script
            - Click on the "SigmaTile_SenseHat_V6.py" to edit
                - You will notice these commands at the top of the script:
                    - import sys
                    - sys.path.append("pathToPython/site-packages")
                - Change the path to match your directory to site-packages and save the script before closing.
         - Now the Python script should run.

    Step III) Execution upon RaspberryPI boot:
        
        *** If you would like for your RaspberryPi to autorun the above scripts upon boot, then follow these steps. If no then the setup is complete.
    
        - Pull up terminal to edit crontab (the startup execution script) with the following command: sudo crontab -e
        - Select option 1 to edit in nano
        - Open the mfg-tile folder and open the "mycron.tab" file.
        - Correct the directory of the launcher.sh file accordingly and then copy this line.
        - Past this line into the terminal at the very last line of crontab.
        - Hit ctrl-x to save and enter to exit
        - Once complete, the RasperryPi has been fully set up.
        
## Setup For Kepware - Kepware_OPF_Instance (Easiest Part)

    Step I) Open Kepware
    Step II) Navigate to file
    Step III) Select open, choose the OPF, and then open
    Step IV) Create more or delete devices
        - To make more right click the channel, copy, right click the project, press paste
        - To delete, right click the channel, press delete
    Step V) Configure the IP address to each device under each channel
        - First, navigate to the channel, left click on it and then select the device. 
        - Right click on the device, go down to the bottom of the tab and click properties.
        - From there edit, the IP address listed to match the one displayed on the SigmaTile
        - This is also where you can edit the device's name
        
    Now you're all set up with Kepware and the Sigma Tile if all of the steps were followed correcly!
    

# Kepware to ThingWorx Setup

    Step I) Open Kepware and right click on the Project within the Kepware .opf
    Step II) Left click on "properties", left click on the last selection; "ThingWorx"
    Step III) Proceed to the following image
   ![Screen Shot 2022-08-25 at 12 18 19 PM](https://user-images.githubusercontent.com/81708456/186717496-c2a7d106-39c0-45f4-aa22-be92072ce5d1.png)
       
        4) In the Property Editor pop-up, click ThingWorx.
        5) In the Enable field, select Yes from the drop-down.
        6) In the Host field, enter the URL or IP address of your ThingWorx Foundation server, Do not enter http:// 
        7) Enter the Port number. If you are using the "hosted" Developer Portal trial, enter 443.
        8) In the Application Key field, copy and paste the Application Key you created in ThingWorx (if not created go make one!). 
        9) In the Trust self-signed certificates field, select Yes from the drop-down. 
        10) In the Trust all certificates field, select Yes from the drop-down. 
        11) In the Disable encryption field, select No from the drop-down if you are using a secure port. Select Yes if you are using an http port. 
        12) Type IndConn_Server in the Thing name field, including matching capitalization. 
        13) If you are connecting with a remote instance of ThingWorx Foundation and expect breaks or latency in connection, enable Store and Forward. 
        14) Left click "Apply" in the pop-up.
        15) Left click "Ok", and now you have Kepware connected to ThingWorx
