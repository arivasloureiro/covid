# Covid
Test Python Flask with info about Covid-19

# Install on Docker
1. Install Docker
    https://docs.docker.com/engine/install/ubuntu/

2. Install docker-compose
    ```
   sudo curl -L "https://github.com/docker/compose/releases/download/1.25.5/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   sudo chmod +x /usr/local/bin/docker-compose
   ```
3. Build and deploy container:
    
    ```dock-compose up```
    
4. Test in your browser:
    
    http://localhost

# Install on local environment
1. Install pip
    
    ```curl https://bootstrap.pypa.io/get-pip.py | python3```
2. Install pip requirements:

    ```pip -r requirements.txt```
3. Run Flask server:

    ```python3  run.py```

4. Test in your browser:
    
    http://localhost:5000
