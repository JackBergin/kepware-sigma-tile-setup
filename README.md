# Kepware_SigmaTile_Setup
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
I) Clone repo to RaspberryPi instance and Kepware instance

Following Steps for RaspberryPi Repo Setup:
II) If on old or new RaspberryPi OS, move "past-mfg-tile" or "current-mfg-tile" to "home/{yourUserDirectory}"
III) Rename folder to mfg-tile

Folloing Steps for Kepware Repo Setup:
II) Go into "Kepware_OPF_Instance"
III) Move .opf file to desired location

## Setup For Raspberry Pi - past-mfg-tile
Step I) Once the folder has been moved and renamed with the steps above:
    -  Open terminal and execute command: "$ cd mfg-tile"
    - Next, open the mfg-folder, and then open the launcher.sh file. Modify the path to the python script to match yours.
    - Now go back to terminal and make the "launcher.sh" executable with this command: sudo chmod +x launcher.sh
    - Next, make the "SigmaTile_SenseHat_V5.py" executable with this command: sudo chmod +x SigmaTile_SenseHat_V5.py
Step II) Execution upon RaspberryPI boot:
*** If you would like for your RaspberryPi to autorun the above scripts upon boot, then follow these steps. If no then the setup is complete.
    - 

## Setup For Raspberry Pi - current-mfg-tile
Step I) Once the folder has been moved and renamed with the steps above

## Setup For Kepware - Kepware_OPF_Instance
Step I) Open Kepware
Step II) Navigate to  

Clone this to the RaspberryPi environment and run the install.sh file. If wanted to run on boot, make sure to configure the crontab file properly with the following command: sudo crontab -e. Once exectuing this command, choose nano as your preferred editor and then add the crontab line from the mfg-tile folder to the last line in the nano editor. Once completed, log into kepware, open up the opf file and then change the ip address linked under Channel1 to match the sigma tile's (listed upon execution of the main python script). To execute the Sigma Tile's main script navigate to the mfg-tile folder within the raspberry pi's terminal using cd. type the command "sudo python &lt;pythonfFile.py> and the IP address will be listed. Once this is completed, the sigma tile is connected to kepware. 

Connecting Kepware to Thingworx is the next step in order to create a GUI and Mashup for visualizing the data output from the Sigma Tile. The following link teaches the basics on connecting Kepware to Thingworx and takes very little time to get set up.
https://developer.thingworx.com/en/resources/guides/connect-kepware-server-thingworx-guide
