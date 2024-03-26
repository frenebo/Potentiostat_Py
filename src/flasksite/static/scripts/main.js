


const SERVER_SOCKET_PATH = `/socket_path`;


class PotentiostatView
{
    constructor(appDiv, serverInterface)
    {
        this.appDiv = appDiv;
        this.serverInterface = serverInterface;

        this.serverInterface.onServerStateChange(this.updatePotentiostatInfo);

        const titleBar = document.createElement('div');

        this.appDiv.appendChild(titleBar);

        this.serverInterface.requestPotentiostatState();
    }

    updatePotentiostatInfo(newPotentiostatState)
    {
        console.log("Received new state from server:");
        console.log(newPotentiostatState);
    }
}

class ServerInterface
{
    constructor()
    {
        // Socketio should be imported
        this.socketio = io(SERVER_SOCKET_PATH);
        this.stateChangedListeners = [];

        this.socketio.on("potentiostat_state", (message) => {
            for (const listener of this.stateChangedListeners) {
                listener(message);
            }
        });
    }

    requestPotentiostatState()
    {
        this.socketio.emit("request_potentiostat_state", "");
    }

    onServerStateChange(listener)
    {
        this.stateChangedListeners.push(listener);
    }
}


function setupApp(appDiv)
{
    const serverInterface = new ServerInterface();
    const pot_view = new PotentiostatView(appDiv, serverInterface);
}

export { setupApp };