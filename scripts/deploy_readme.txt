# MBot LCM Monitor Release

To install the LCM Monitor, first unpack this file with:

  tar -xvzf mbot_lcm_monitor-[VERSION].tar.gz
  cd mbot_lcm_monitor-[VERSION]

Then install the dependencies and deploy:

  ./deploy_app.sh --no-rebuild

Finally, open the NGINX configuration:

  sudo nano /etc/nginx/nginx.conf

Ensure these lines are at the end of the file in the "server" block:

    location /spy {
        alias /data/www/spy/;
        index index.html index.htm;
        try_files $uri $uri/ =404;
    }

Save the file and check that the configuration is correct with:

  sudo nginx -t

Restart the NGINX service:

  sudo systemctl restart nginx.service

Done! The LCM Monitor will be available at http://[MBOT_IP]/spy
