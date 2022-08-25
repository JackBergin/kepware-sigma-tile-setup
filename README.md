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
    Step II) Navigate to  
