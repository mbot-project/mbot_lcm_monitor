# MBot LCM Monitor

A web-based tool for monitoring and inspecting Lightweight Communications and Marshalling (LCM) messages in real-time. This system offers functionality similar to LCM Spy, utilizing web technologies for enhanced usability and accessibility.

## Prerequisites

The web-based LCM Monitor depends on the [MBot Bridge Server and API](https://github.com/mbot-project/mbot_bridge/). The server must be running in subscribe-all mode in order to display all the messages.

*Note:* If the MBot Bridge Server is configured to only subscribe to certain channels, only those will be displayed on the LCM Monitor.

## Installation

This installation assumes that you have already installed the [MBot Web App](https://github.com/mbot-project/mbot_web_app), and that it is accessible by going to `http://[MBOT_IP]` in your browser.

### Installing from the Latest Release (Recommended)

You can install the LCM Monitor so that it is accessible at the address `http://[MBOT_IP]/spy`, where `[MBOT_IP]` is replaced with your robot's IP address.

First, download the tar file from the [latest release](https://github.com/mbot-project/mbot_lcm_monitor/releases), then do:
```bash
tar -xvzf mbot_lcm_monitor-[VERSION].tar.gz
cd mbot_lcm_monitor-[VERSION]/
./deploy_app.sh --no-rebuild
```
Follow the printed instructions (or the ones in `mbot_lcm_monitor-[VERSION]/README.txt`) to configure with NGINX.

#### Configuring Nginx
If this is your first time setting up the LCM monitor, you must configure Nginx to find it. Open the configuration file:
```bash
sudo nano /etc/nginx/nginx.conf
```
Then, edit the `server` block within the `http` block, at the end of the file, to add the following `location` configuration:
```bash
location /spy {
    alias /data/www/spy/;
    index index.html index.htm;
    try_files $uri $uri/ =404;
}
```
The whole `server` block (at the end of the `http` block) looks like this:
```bash
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name localhost home.bot www.home.mbot;

    location / {
        root /data/www/mbot;
        index index.html index.htm;
        try_files $uri $uri/ =404;
    }
    # Spy application location block
    location /spy {
        alias /data/www/spy/;
        index index.html index.htm;
        try_files $uri $uri/ =404;
    }

    # Other configurations...
}
```
To see the changes, restart NGINX:
```bash
sudo systemctl restart nginx.service
```

### Installing from Source

To install from source, you will need to [install NPM](https://github.com/mbot-project/mbot_web_app?tab=readme-ov-file#dependencies) on the Raspberry Pi.

1. Clone [MBot Bridge](https://github.com/mbot-project/mbot_bridge/). Then do:
  ```bash
  cd mbot_bridge/mbot_js
  npm install
  npm link
  ```
2. In this repo, do:
  ```bash
  npm install
  npm link mbot-js-api
  ```

To run in development mode, you can do:
```bash
npm run dev
```

To build and install the app, do:
```bash
./scripts/deploy_app.sh [--bridge-path PATH/TO/BRIDGE --no-rebuild]
```
If the `--bridge-path` argument is not provided, this will grab the latest compatible release of the [MBot Bridge](https://github.com/mbot-project/mbot_bridge/). If you want to use a local version of the Bridge API, pass the path to your copy of the MBot Bridge repository. Use `--no-rebuild` if you want to skip rebuilding the app and just install.

Then, follow the same steps to configure Nginx as [above](#configuring-nginx).

## Generating a new release

To generate a new release, do:
```bash
./scripts/generate_release.sh -v vX.Y.Z [-b PATH/TO/BRIDGE]
```
Substitute the correct version for `vX.Y.Z`. Save the generated file `mbot_lcm_monitor-vX.Y.Z.tar.gz` to upload to the release.

The `-b` argument is optional, and lets you pass a path to a local version of the MBot Bridge to compile against. By default, the latest compatible release of the MBot Bridge will be downloaded from source.

## Authors and maintainers
The current maintainer of this project is Jana Pavlasek. Please direct all questions regarding support, contributions, and issues to the maintainer.
