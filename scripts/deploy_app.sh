#!/bin/bash
set -e  # Quit on error.

if [[ "$@" == *"--no-rebuild"* ]]; then
  echo "LCM Monitor will be installed from the dist/ folder without rebuild."
else
  # Build the webapp.
  echo "#############################"
  echo " Building the LCM Monitor..."
  echo "#############################"
  npm install
  npm link mbot-js-api
  npm run build
fi

echo
echo "Installing the LCM Monitor..."
echo

if [ ! -d "/data/www/spy" ]; then
    sudo mkdir /data/www/spy
fi

# Remove any old files to ensure we don't make duplicates.
sudo rm -rf /data/www/spy/*
# Move the build files into the public repo.
sudo cp -r dist/* /data/www/spy/

NGINX_CONFIG="location /spy {
    alias /data/www/spy/;
    index index.html index.htm;
    try_files \$uri \$uri/ =404;
}"

echo
echo "Done! Edit the NGINX config:"
echo "  $ sudo nano /etc/nginx/nginx.conf"
echo
echo "and make sure the following lines are added to the server block:"
echo
echo -e "$NGINX_CONFIG"
echo
echo "then restart the NGINX server:"
echo "  $ sudo systemctl restart nginx.service"
echo
echo "Once complete, the LCM monitor will be available at:"
echo "  http://[MBOT_IP]/spy"
