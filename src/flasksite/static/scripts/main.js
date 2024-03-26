


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
        this.appDiv.innerHTML = "";
        this.appDiv.appendChild(this.createPotStatSummaryDiv(newPotentiostatState));
        // this.appDiv.appendChild(this.createPotStatSummaryDiv(newPotentiostatState))
    }

    createPotStatSummaryDiv(potentiostatState)
    {
        const n_channels = potentiostatState["n_channels"];
        // const body = document.body,
        const tbl = document.createElement('table');
        tbl.style.width = '100px';
        tbl.style.border = '1px solid black';
      
        for (let i = 0; i < n_channels; i++) {
          const tr = tbl.insertRow();
        //   for (let j = 0; j < 2; j++) {
            const switch_td = tr.insertCell();
            const switch_state = potentiostatState["channel_switch_states"][i];
            let on_off_text = "";
            if (switch_state === null) on_off_text = "?";
            else if (switch_state === true) on_off_text = "On";
            else if (switch_state === false) on_off_text = "Off";
            else throw Error("Invalid switch state " + switch_state);

            // if ()
            switch_td.appendChild(document.createTextNode(on_off_text));
            switch_td.style.border = '1px solid black'
            // if (i === 2 && j === 1) {
            //   break;
            // } else {
            //   const td = tr.insertCell();
            //   td.appendChild(document.createTextNode(`Cell I${i}/J${j}`));
            //   td.style.border = '1px solid black';
            //   if (i === 1 && j === 1) {
            //     td.setAttribute('rowSpan', '2');
            //   }
            // }
        }
        
        return tbl;
        // body.appendChild(tbl);

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