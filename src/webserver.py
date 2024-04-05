from flask import Flask,  render_template
import json
from flask_socketio import SocketIO, send, Namespace
import sys
import os
import time

from potentiostatpy.potentiostat import Potentiostat
from potentiostatpy.logger import CallbackLogger


app = Flask(__name__,
            static_folder=  '../website/build/static',
            template_folder='../website/build/templates')

@app.route('/')
def home():
    return render_template('index.html')


SOCKET_NAMESPACE_STR = '/socket_path'
socketio = SocketIO(app)
            
class PotentiostatNamespace(Namespace):
    def __init__(self, *args):
        super().__init__(*args)
    
    def set_potentiostat(self, potstat):
        self.potentiostat = potstat
        self.potentiostat.on_state_changed(self.send_out_potentiostat_state)
    
    def connect_callback_logger(self, callback_logger):
        # Log messages
        print_log_func = lambda text, timestamp_s : print(text)
        callback_logger.on_log(print_log_func)

        socket_log_func = lambda text, timestamp_s: self.send_out_potentiostat_logging({
            "lines": [{
                "type": "log",
                "text": text,
                "timestamp_seconds": timestamp_s,
            }],
        })
        callback_logger.on_log(socket_log_func)

        # Error messages
        print_error_func = lambda text, timestamp_s : print(text)
        callback_logger.on_error(print_error_func)

        socket_error_func = lambda text, timestamp_s: self.send_out_potentiostat_logging({
            "lines": [{
                "type": "error:",
                "text": text,
                "timestamp_seconds": timestamp_s
            }]
        })
        callback_logger.on_error(socket_error_func)
    
    def on_request_potentiostat_state(self, req_data):
        self.send_out_potentiostat_state(self.potentiostat.get_state())
    
    def on_client_changed_potstat_settings(self, req_data):
        # print(req_data)
        setting_id = req_data["setting_id"];
        option_picked = req_data["option_picked"];
        time.sleep(1)

        self.potentiostat.change_setting(setting_id, option_picked);
    
    def send_out_potentiostat_state(self, new_state):
        socketio.emit("potentiostat_state", new_state, namespace=SOCKET_NAMESPACE_STR)
    
    def send_out_potentiostat_logging(self, logging_data):
        print("sending out potentiostat logging ")
        socketio.emit("potentiostat_logging", logging_data, namespace=SOCKET_NAMESPACE_STR)


potstat_namespace = PotentiostatNamespace(SOCKET_NAMESPACE_STR)
socketio.on_namespace(potstat_namespace)



if __name__ == '__main__':
    using_dummy_hardware = False
    if len(sys.argv) >= 2:
        if sys.argv[1] == "dummy":
            using_dummy_hardware = True
        else:
            raise Exception("Unknown argument {}, should be 'dummy' or no argument".format(sys.argv[1]))
    
    potentiostat = None
    try:
        print("~~~~~~~~~~~~Creating Potentiostat!")
        potstat_logger = CallbackLogger()
        potentiostat = Potentiostat(n_modules=1, use_dummy_hardware=using_dummy_hardware, logger=potstat_logger)
        potstat_namespace.connect_callback_logger(potstat_logger)
        potstat_namespace.set_potentiostat(potentiostat)
        app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
        potentiostat.cleanup()
    except:
        #Try to cleanup potentiostat resources, then raise the exception.
        if potentiostat is not None:
            potentiostat.cleanup()
        raise

