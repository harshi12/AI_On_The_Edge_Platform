user=$1
ip=$2
pswd=$3

sshpass -p $3 ssh -o "StrictHostKeyChecking no" $1@$2 'exit'

cmd1="sshpass -p $3 scp install_TFS.sh $1@$ip:/home/$1/"
echo $cmd1
$cmd1

cmd2="sshpass -p $3 scp install_sshfs.sh $1@$ip:/home/$1/"
echo $cmd2
$cmd2

cmd3="sshpass -p $3 scp NFS_Mount1.sh $1@$ip:/home/$1/"
echo $cmd3
$cmd3

cmd6="sshpass -p $3 scp install_NFSC.sh $1@$ip:/home/$1/"
echo $cmd6
$cmd6

cmd4="sshpass -p $3 ssh $1@$2 bash /home/$1/install_TFS.sh $3"
echo $cmd4
$cmd4
echo "TFS INSTALLATION DONE"

cmd7="sshpass -p $3 ssh $1@$2 bash /home/$1/install_NFSC.sh $3"
echo $cmd7
$cmd7
echo "NFC CLIENT INSTALLATION DONE!"

cmd5="sshpass -p $3 ssh -t $1@$2 bash /home/$1/install_sshfs.sh $3"
echo $cmd5
$cmd5
echo "SSHFS INSTALLATION DONE"

sshpass -p $3 ssh -t $1@$2 bash /home/$1/NFS_Mount1.sh
echo "NFS_MOUNT DONE"