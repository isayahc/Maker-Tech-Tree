# download belnder 
wget https://download.blender.org/release/Blender4.0/blender-4.0.2-linux-x64.tar.xz

# Extract the downloaded archive:

tar xf blender-4.0.2-linux-x64.tar.xz

rm -fr blender-4.0.2-linux-x64.tar.xz

# Move the extracted folder to the desired location (for example, /opt):
sudo mv blender-4.0.2-linux-x64 /opt/blender-4.0.2

# Create a symbolic link to the Blender executable:
sudo ln -s /opt/blender-4.0.2/blender /usr/local/bin/blender

sudo apt-get update
sudo apt-get install libxxf86vm1 -y
sudo apt-get install libgl1-mesa-glx -y
sudo apt-get install libegl-mesa0 -y
sudo apt-get install libegl1 -y