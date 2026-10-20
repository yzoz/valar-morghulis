'''
function greet {
    echo "Привет, $1! У тебя $# аргументов."
    echo "Все аргументы: $@"
}
'''

rs() {
  rsync -avzPc ~/dev/$1/dist/** srv:/var/www/$1/
}

alias a=". env/bin/activate"

alias lls='cd ~/my && ./llama-server \
  --model "embeddinggemma2-gguf/embeddinggemma-2-Q8_0.gguf" \
  --alias embeddinggemma2 \
  --embeddings \
  --pooling mean \
  --ctx-size 4096 \
  --batch-size 2048 \
  --ubatch-size 2048 \
  --parallel 1 \
  --host 127.0.0.1 \
  --port 8080 \
  -ngl all \
  -fa on'

alias qd="quasar dev -m pwa"
alias qb="quasar build -m pwa"
alias qa="quasar build -m capacitor -T android --ide"

alias tun='autossh -M 0 -o "ServerAliveInterval 30" -o "ServerAliveCountMax 3" -N -L 5901:localhost:5901 srv'
alias view="vncviewer RemoteResize=0 DesktopSize=0 FullScreen=1 -passwd <(vncpasswd -f <<<'PWD') localhost:1"