# B-Hunters-Wayback

**This module is used to gathers subdomains for [B-Hunters Framework](https://github.com/B-Hunters/B-Hunters) using [waymore](https://github.com/xnl-h4ck3r/waymore) , [waybackurls](github.com/tomnomnom/waybackurls), [gau](https://github.com/lc/gau/) .**

## Requirements

To be able to use all the tools remember to update the environment variables with your API keys in `docker-compose.yml` file as some tools will not work well until you add the API keys.

## Usage 

**Note: You can use this tool inside [B-hunters-playground](https://github.com/B-Hunters/B-Hunters-playground)**   
To use this tool inside your B-Hunters Instance you can easily use **docker-compose.yml** file after editing `b-hunters.ini` with your configuration.

# 1. **Build local**
Rename docker-compose.example.yml to docker-compose.yml and update environment variables.

```bash
docker compose up -d
```

# 2. **Docker Image**
You can also run using docker image, You have to add all available API keys you can as this increase the scanning scope
```bash
docker run -d -v $(pwd)/b-hunters.ini:/etc/b-hunters/b-hunters.ini bormaa/b-hunters-wayback:v1.0
```

## How it works

B-Hunters-wayback receives the domain from B-Hunters-subrecon and run scanning on it.   

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/bormaa)