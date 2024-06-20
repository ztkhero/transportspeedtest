from flask import Flask, request, jsonify, send_file, render_template
import subprocess
import threading
import time

app = Flask(__name__)

def run_speedtest(server_ip, results):
    try:
        jitter_result = subprocess.run(
            ['iperf3', '-c', server_ip, '-u', '-b', '1M', '-t', '10', '-i', '1'], capture_output=True, text=True
        )
        download_result = subprocess.run(
            ['iperf3', '-c', server_ip], capture_output=True, text=True
        )
        upload_result = subprocess.run(
            ['iperf3', '-c', server_ip, '-R'], capture_output=True, text=True
        )
        results['jitter'] = extract_jitter(jitter_result.stdout)
        results['download'] = extract_speed(download_result.stdout)
        results['upload'] = extract_speed(upload_result.stdout)
        
    except Exception as e:
        results['error'] = str(e)

def extract_jitter(output):
    temp_jitter='0'
    for line in output.split('\n'):
        if 'ms' in line and 'Datagrams' not in line:
            parts = line.split()
            if float(parts[-5]) >= float(temp_jitter):
                temp_jitter = parts[-5]
    if temp_jitter != '0':
        return temp_jitter
    else:
        return "N/A"

def extract_speed(output):
    for line in output.split('\n'):
        if 'sender' in line or 'receiver' in line:
            parts = line.split()
            return parts[-4] + " " + parts[-3]
    return "N/A"

def run_ping_test(server_ip, results):
    try:
        ping_result = subprocess.run(
            ['ping', '-c', '2', server_ip], capture_output=True, text=True
        )
        results['ping'] = parse_ping(ping_result.stdout)
    except Exception as e:
        results['error'] = str(e)

def parse_ping(output):
    for line in output.split('\n'):
        if 'rtt min/avg/max/mdev' in line:
            parts = line.split('/')
            return {
                'min': parts[3].split('=')[1].strip(),
                'avg': parts[4].strip(),
                'max': parts[5].strip(),
                'mdev': parts[6].strip()
            }
    return "N/A"

@app.route('/test', methods=['POST'])
def test():
    server_ip = request.json['server_ip']
    results = {}

    threads = []
    threads.append(threading.Thread(target=run_speedtest, args=(server_ip, results)))
    threads.append(threading.Thread(target=run_ping_test, args=(server_ip, results)))
    
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    # results={'ping': {'min': '0.234', 'avg': '0.267', 'max': '0.301', 'mdev': '0.033 ms'}, 'jitter': '0.016', 'download': '8.10 Gbits/sec', 'upload': '8.99 Gbits/sec'}
    print(results)
    time.sleep(1)
    return jsonify(results)

@app.route('/', methods=['GET'])
def index():
    results={}
    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
