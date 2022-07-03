zip -r pythonScripts.zip pythonScripts
zip -r site.zip site
scp ./pythonScripts.zip ./server.js ./site.zip 192.168.0.29:/home/azazel/Desktop/server
rm ./site.zip
rm ./pythonScripts.zip
