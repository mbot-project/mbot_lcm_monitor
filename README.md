# MBot LCM Monitor
> Currently only support mbot apriltag message.

## Description
A web-based tool for monitoring and inspecting Lightweight Communications and Marshalling (LCM) messages in real-time. This system offers functionality similar to LCM Spy, utilizing web technologies for enhanced usability and accessibility.

## Installation
```bash
sudo apt install python3-flask-socketio
```

## Usage and Features
```python3
python3 main.py
```
- The main.py is the entry point.


## Authors and maintainers
The current maintainer of this project is Shaw Sun. Please direct all questions regarding support, contributions, and issues to the maintainer.

## Node App with MBot Bridge

To use the pure Node.js + React application, which uses the MBot Bridge, the MBot Javascript API must be linked. To do this, clone the `mbot_bridge` package then do:
```bash
cd mbot_bridge/mbot_js
npm link
```
Then, in this repository, do:
```bash
npm install
npm link mbot-js-api
```
To test locally, do:
```bash
npm run dev
```

**Note:** The MBot Bridge Server must be running for this to work. See instructions for running the server [here](https://github.com/mbot-project/mbot_bridge/).
