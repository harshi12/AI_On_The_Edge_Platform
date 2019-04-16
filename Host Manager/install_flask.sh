pass=$1

echo $pass | sudo -S apt-get update
echo $pass | sudo apt-get install python3
echo $pass | sudo apt-get pip3
echo $pass | sudo pip3 install flask