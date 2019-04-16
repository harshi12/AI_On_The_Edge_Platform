# pass="S2j1ar1in63"
# read -p 'Server_Username: ' username
# read -p 'Server_IP: ' ip_addr
# read -sp "Local_Machine_Password: " Pass
# read -p "Enter Server Path: " Path
pass=$1

#scp -r  $username@$ip_addr:$Path ./
echo $pass | sudo -S apt-get update
echo $pass | sudo apt-get install python3
echo $pass | sudo apt-get pip3
echo $pass | sudo pip3 install numpy
echo $pass | sudo pip3 install pandas
echo $pass | sudo pip3 install tensorflow
echo $pass | sudo apt-get install tensorflow-model-server


#read -p "Enter test dataset path" CSV_Path
echo "Installation Done"
#python3 ./Hackthon/Tester.py CSV_Path
