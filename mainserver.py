from flask import Flask, request
import pickle

app = Flask(__name__)

hosts = []

@app.route("/")
def home():
  return "Please refer to <a href='https://github.com/Ironislife98/PythonChatApp' >Github</a> for api docs"

@app.route('/api/gethosts')
def gethosts():
  print(hosts)
  return str(pickle.dumps(hosts))


@app.route("/api/addserver/<ipaddr>")
def addserver(ipaddr):
  if ipaddr == request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr):
    if ipaddr in hosts:
      return str(pickle.dumps("Already added Host"))
    else:
      hosts.append(request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr))
      return str(pickle.dumps("Added"))
  else:
    return str(pickle.dumps("CANNOT ADD OTHERS IP ADRESS"))


@app.route("/api/deleteserver/<ipaddr>")
def delete(ipaddr):
  if ipaddr == request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr):
    hosts.pop(hosts.index(ipaddr))
  else:
    return str(pickle.dumps("Not your ip"))


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=5000)
