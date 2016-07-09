#! /bin/bash

# Setting strings

archiveCommand="tar --create --verbose --preserve-permissions --file" ;
bakFolder="/media/jeffseif/backup" ;
homeFolder="/home/jeffseif" ;
bakShFilename="bak.sh" ;
rootFolders="\
  etc" ;
skipVisible="\
  \*.\*
  Desktop
  Dropbox
  git
  tmp" ;

# Check if external HDD is mounted

[ ! -d ${bakFolder} ] && touch ${homeFolder}/Desktop/$(date "+%F")_do_bak && exit ;

# Shebang

cd ${homeFolder} ;
bakSource="#! /bin/bash\n\n" ;

# Installed Packages

bakSource="${bakSource}echo 'Extracting installed packages...'\n" ;
bakSource="${bakSource}rm -f ${bakFolder}/installed_packages.txt\n" ;
bakSource="${bakSource}dpkg -l | tr -s ' ' | cut -d' ' -f2 | sed -n '6,\$p' > ${bakFolder}/installed_packages.txt\n\n" ;

# Sources List

bakSource="${bakSource}echo 'Extracting apt sources...'\n" ;
bakSource="${bakSource}rm -f ${bakFolder}/sources.list\n" ;
bakSource="${bakSource}cp /etc/apt/sources.list ${bakFolder}/\n\n" ;

# Wifi passwords

bakSource="${bakSource}echo 'Archiving wifi passwords'\n" ;
bakSource="${bakSource}sudo ${archiveCommand} ${bakFolder}/wifi.tar /etc/NetworkManager/system-connections/ \n\n" ;

# Home content

# ...visible

bakSource="${bakSource}echo 'Archiving home folders...'\ncd ${homeFolder}\n\n" ;
hideString="" ;
for folder in ${skipVisible} ; do
    hideString="${hideString} --hide=${folder}" ;
done
echo "Sizing ${homeFolder} folders..." ;
for folder in $(\ls ${hideString}) ; do
    echo "...${folder}..." ;
    folderSize=$(du -s ${folder} | cut -f1 ) ;
    if [ ${folderSize} -le 1000000000 ]; then
        bakSource="${bakSource}echo '...${folder}...'\n" ;
        bakSource="${bakSource}if [ ! -s ${bakFolder}/${folder}.tar ] || find ${folder} -newer ${bakFolder}/${folder}.tar | grep . ; then\n" ;
        bakSource="${bakSource} ${archiveCommand} ${bakFolder}/${folder}.tar ${folder}\n" ;
        bakSource="${bakSource}fi\n" ;
    fi
done
bakSource="${bakSource}\n" ;

# ...dotted

dottedString="\ls -A | grep -e '^\.'" ;
bakSource="${bakSource}echo '...Dotted...'\n" ;
bakSource="${bakSource}${archiveCommand} ${bakFolder}/Dotted.tar $(eval ${dottedString});" ;

# Create and run backup script

rm -vf ${bakFolder}/${bakShFilename} ;
echo "writing \`${bakFolder}/${bakShFilename}'" ;
echo -e ${bakSource} > ${bakFolder}/${bakShFilename} ;
chmod 755 ${bakFolder}/${bakShFilename} ;
bash ${bakFolder}/${bakShFilename} ;
