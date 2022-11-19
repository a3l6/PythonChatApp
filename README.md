
# Anonymous Chat App
[![MIT License](https://img.shields.io/github/license/Ironislife98/PythonChatApp?style=for-the-badge)](https://choosealicense.com/licenses/mit/)
![Contributers](https://img.shields.io/github/contributors/Ironislife98/PythonChatApp?style=for-the-badge)
![Last Commit](https://img.shields.io/github/last-commit/Ironislife98/PythonChatApp?style=for-the-badge)

A simple python powered chat application with connectivity support to make self hosted servers
or connect to the main server. It is sugested to use Linode's "nanode" service since it is the only one I could get working. Using sockets means port forwarding, but linode just worked. 


I will not be updating this project after this, except for some very small stuff. Have fun if you want to use this code!

## Run Locally

Clone the project

```bash
  git clone https://github.com/Ironislife98/PythonChatApp.git
```

Go to the project directory

```bash
  cd PythonChatApp
```

Start the server

```bash
  python server.py -l
```

## Usage 

🚀🚀Run public server (Use linode)
``` bash
  python server.py -h
```
⛔Delete server from public server
``` bash
python server.py -d
```

## ⚠️WARNING⚠️
When server runs with flag -h, your public ip address is broadcast to everyone, make sure you want this!


## Bugs
- Cannot connect again once disconnected
- Server throws broken pipe error


## Authors

- [@Ironislife98](https://www.github.com/Ironislife98)

