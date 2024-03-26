from flask import Flask,  render_template
import json
from flask_socketio import SocketIO, send, Namespace
import sys
import os

# print(os.path.join(os.path.dirname(sys.path[0]), 'potentiostatpy'))

# sys.path.append(os.path.join(os.path.dirname(sys.path[0]), 'potentiostatpy'))
from potentiostatpy.potentiostat import Potentiostat

app = Flask(__name__,
            # static_url_path='', 
            static_folder=  'flasksite/static',
            template_folder='flasksite/templates')

            

socketio = SocketIO(app)

SOCKET_NAMESPACE_STR = '/socket_path'

@app.route('/')
def home():
    return render_template('index.html')



class PotentiostatNamespace(Namespace):
    def __init__(self, *args):
        super().__init__(*args)
    
    def set_potentiostat(potstat):
        self.potentiostat = potstat
    
    def on_request_potentiostat_state(self, req_data):
        # print(req_data)
        # parsed = json.loads(req_data)
        print(req_data)
        print("on_request_potentiostat_state")

        potentiostat_state = {
            "n_modules": self.potentiostat.n_modules,
            "n_channels": self.potentiostat.n_channels,
            "channel_switch_states": self.potentiostat.get_channel_switch_states(),
            "channel_output_voltages": self.potentiostat.get_channel_output_voltages(),
        }
        socketio.emit("potentiostat_state", potentiostat_state, namespace=SOCKET_NAMESPACE_STR)

    
    # def on_model_request(self, data):

        # print(data)

        # self.server_interface = GraphServerInterface()
        # self.server_interface.on_graph_change = self.on_graph_change
        # self.server_interface.on_request_response = self.on_request_response

    # def on_request_response(self, response, request_id):
    #     # obj = {
    #     #     "request_id": request_id,
    #     #     "response": response,
    #     # }
    #     # socketio.emit("model_req_response", obj, namespace=SOCKET_NAMESPACE_STR)

    # def on_graph_change(self, new_graph_data_obj):
    #     # socketio.emit("graph_changed", new_graph_data_obj, namespace=SOCKET_NAMESPACE_STR)

    # def on_model_request(self, data):
    #     # self.server_interface.send_model_req(request.sid, data)

potstat_namespace = PotentiostatNamespace(SOCKET_NAMESPACE_STR)
socketio.on_namespace(potstat_namespace)


# @app.route('/static/')


if __name__ == '__main__':
    potentiostat = Potentiostat(n_modules=1)
    potstat_namespace.set_potentiostat(potentiostat)
    app.run(debug=True, host='0.0.0.0', port=5000)
