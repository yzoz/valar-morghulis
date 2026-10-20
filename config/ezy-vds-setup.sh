# Don’t launch it as it is!

adduser user
usermod -aG sudo user
su - user
cd

mkdir .ssh
touch .ssh/authorized_keys
echo 'YOUR KEY' >> .ssh/authorized_keys
sudo tee /etc/ssh/sshd_config.d/50-cloud-init.conf <<EOF
PasswordAuthentication no
PermitRootLogin no
ClientAliveInterval 60
ClientAliveCountMax 5
EOF
sudo service ssh restart

sudo apt update
sudo apt upgrade -y

sudo apt install zsh git nginx tmux python3.12-venv -y

sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
echo 'alias a=". env/bin/activate"' >> .zshrc

sudo apt-get install ca-certificates curl -y
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
  
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y

sudo usermod -aG docker $USER
newgrp docker

sudo chown -R $USER:$USER /var/www
sudo chmod -R 755 /var/www
mkdir /var/www/1ncript0.ru

sudo tee /etc/nginx/sites-enabled/1ncript0.ru <<EOF
server {
    listen 80;
    server_name 1ncript0.ru;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    http2 on;
    server_name 1ncript0.ru;

    ssl_certificate     /etc/nginx/ssl/origin.crt;
    ssl_certificate_key /etc/nginx/ssl/origin.key;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers off;

    root /var/www/1ncript0.ru;
    index index.html;

    location / {
        try_files \$uri \$uri/ =404;
    }

    # location / {
        # proxy_pass http://localhost:3000;
        # proxy_set_header Host $host;
        # proxy_set_header X-Real-IP $remote_addr;
        # proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        # proxy_set_header X-Forwarded-Proto $scheme;
    # }
}
EOF

sudo snap install --classic certbot
sudo ln -s /snap/bin/certbot /usr/bin/certbot

sudo tee /etc/systemd/system/dockrun.service <<EOF
[Unit]
Description=Docker Run
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/var/www
ExecStart=/usr/bin/docker compose up -d
ExecStop=/usr/bin/docker compose down
ExecReload=/usr/bin/docker compose restart
TimeoutStartSec=0
Restart=on-failure
RestartSec=30

[Install]
WantedBy=multi-user.target
EOF
sudo systemctl enable dockrun.service
sudo service dockrun start
