from flask import Flask, render_template, request, jsonify, json
import uuid
import requests
import config

app = Flask(__name__)

apiurl = "https://api.digitalocean.com/v2/"

@app.route('/regions', methods=['GET'])
def regions():
    getRegions = requests.get(apiurl+"regions", headers=config.headers)
    if getRegions.status_code == 200:
        parseRegions = json.loads(getRegions.text)
        regions = []

        for region in parseRegions['regions']:
            reg = {'name': region['name'], 'slug': region['slug']}
            regions.append(reg)

        return render_template('regions.html', regions=regions)

    else:
        return 'Could not load regions.'


@app.route('/', methods=['GET'])
def index():
   return render_template('index.html')

@app.route('/list', methods=['GET'])
def listDroplets():
    listD = requests.get(apiurl+"droplets?tag_name=vpn", headers=config.headers)

    if listD.status_code == 200:
        droplets = json.loads(listD.text)

        servers = []
        for s in droplets['droplets']:
            nid = {"name": s['name'], "id": str(s['id']), "status": s['status'],
                    "IPv4": s['networks']['v4'][0]['ip_address'],
                    "IPv6": s['networks']['v6'][0]['ip_address']}
            servers.append(nid)

        if not servers:
            return "No servers running currently. This info will refresh itself."
        else:
            return render_template('list.html', servers=servers)
    else:
        return 'Could not list droplets.'

@app.route('/launch', methods=['POST'])
def launch(reg=None):
    reg = request.form['region']

    getKeys = requests.get(apiurl+"account/keys", headers=config.headers)
    if getKeys.status_code == 200:
        keys = json.loads(getKeys.text)
    else:
        return 'Could not load SSH Keys.'

    sshKeys = []
    for kid in keys['ssh_keys']:
        sshKeys.append(str(kid['id']))

    tags = ["vpn"]

    file = open('userdata.txt', 'r')
    userdata = file.read()

    payload = {
                  "name": "vpn-"+str(uuid.uuid4()),
                  "image": "ubuntu-16-04-x64",
                  "region": reg,
                  "size": "512mb",
                  "backups": "false",
                  "ipv6": "true",
                  "ssh_keys": sshKeys,
                  "tags": tags,
                  "user_data": userdata
              }

    createDroplet = requests.post(apiurl+"droplets", headers=config.headers, json=payload)
    if createDroplet.status_code == 202:
        return 'Droplet created, ID: %s' % str(json.loads(createDroplet.text)['droplet']['id'])
    else:
        return 'Could not start image: %s' % str(json.loads(createDroplet.text)['message'])

@app.route('/actions/<dropletID>/<action>', methods=['POST'])
def act(action=None, dropletID=None):
    if action == 'reboot':
        payload = {"type":"reboot"}
        rebootDroplet = requests.post(apiurl+"droplets/"+dropletID+"/actions", headers=config.headers, json=payload)
        if rebootDroplet.status_code == 201:
            return "done."

    if action == 'shutoff':
        payload = {"type":"shutdown"}
        shutdownDroplet = requests.post(apiurl+"droplets/"+dropletID+"/actions", headers=config.headers, json=payload)
        if shutdownDroplet.status_code == 201:
            return "done."

    if action == 'boot':
        payload = {"type":"power_on"}
        bootDroplet = requests.post(apiurl+"droplets/"+dropletID+"/actions", headers=config.headers, json=payload)
        if bootDroplet.status_code == 201:
            return "done."

    if action == 'delete':
        bootDroplet = requests.delete(apiurl+"droplets/"+dropletID, headers=config.headers)
        if bootDroplet.status_code == 204:
            return "done."

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)
