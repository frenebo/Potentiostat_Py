


const SERVER_SOCKET_PATH = `/socket_path`;
const VERSION = "0.1";

class PotentiostatSettingPanel
{
    constructor()
    {
        this.mainDiv = document.createElement("div");

        this.userChangeListeners = [];

        // @TODO implement
    }

    getHtmlElement()
    {
        return this.mainDiv;
    }

    onUserChange(listener)
    {
        this.userChangeListeners.push(listener);
    }
}

class ChannelInputsPanel
{
    constructor()
    {
        this.mainDiv = document.createElement("div");

        const titleBar = document.createElement("div");
        titleBar.innerHTML = "Inputs (Volts)";
        this.mainDiv.appendChild(titleBar);

        this.lastUpdatedDiv = document.createElement("div");
        this.mainDiv.appendChild(this.lastUpdatedDiv);

        this.inputsTablePanel = document.createElement("div");
        this.inputsTablePanel.classList.add('input_table_panel');
        this.mainDiv.appendChild(this.inputsTablePanel);
        
        this.userChangeListeners = [];
    }

    getHtmlElement()
    {
        return this.mainDiv;
    }

    onUserChange(listener)
    {
        this.userChangeListeners.push(listener);
    }
}

class ChannelOutputsPanel
{
    constructor()
    {
        this.mainDiv = document.createElement("div");

        const titleBar = document.createElement("div");
        titleBar.innerHTML = "Outputs (current)";
        this.mainDiv.appendChild(titleBar);

        this.lastUpdatedDiv = document.createElement("div");
        this.mainDiv.appendChild(this.lastUpdatedDiv);

        this.inputsTablePanel = document.createElement("div");
        this.inputsTablePanel.classList.add('output_table_panel');
        this.mainDiv.appendChild(this.inputsTablePanel);
    }

    getHtmlElement()
    {
        return this.mainDiv;
    }
}


class PotentiostatView
{
    constructor(appDiv, serverInterface)
    {
        this.appDiv = appDiv;
        this.serverInterface = serverInterface;

        this.serverInterface.onServerStateChange((newState) => { this.updatePotentiostatInfo(newState); });

        const titleBar = document.createElement('div');
        titleBar.classList.add('big_title');
        titleBar.innerHTML="PotentiostatPy v" + VERSION.toString();
        this.appDiv.appendChild(titleBar);

        const subtitleBar = document.createElement('div');
        subtitleBar.classList.add('big_subtitle_text');
        subtitleBar.innerHTML = "Paul Kreymborg, Atkinson Lab, Princeton University, 2024. https://github.com/frenebo/Potentiostat_Py";
        this.appDiv.appendChild(subtitleBar);

        const resetButton = document.createElement("input");
        resetButton.type = "button";
        resetButton.value = "request new state";
        resetButton.onclick = () => { this.serverInterface.requestPotentiostatReset(); };


        // Set up the control, inputs, outputs channels
        this.potstat_setting_panel = new PotentiostatSettingPanel();
        this.channel_inputs_panel = new ChannelInputsPanel();
        this.channel_outputs_panel = new ChannelOutputsPanel();

        this.potstat_setting_panel.onUserChange((data) => { this.userChangedSettingsPanel(data); });
        this.channel_inputs_panel.onUserChange((data) => { this.userChangedChannelInputsPanel(data); });
        



        // Three panels - control panel, input panel, output panel

        const panelDiv = document.createElement("div");
        this.appDiv.appendChild(panelDiv);
        panelDiv.classList.add("panels_row");


        // Settings panel
        const settingsPanelDiv = document.createElement("div");
        panelDiv.appendChild(settingsPanelDiv);
        settingsPanelDiv.classList.add("panel_block");
        settingsPanelDiv.appendChild(this.potstat_setting_panel.getHtmlElement());
        

        // Inputs panel
        const inputPanelDiv = document.createElement("div");
        panelDiv.appendChild(inputPanelDiv);
        inputPanelDiv.classList.add("panel_block");        
        inputPanelDiv.appendChild(this.channel_inputs_panel.getHtmlElement());

        // Outputs panel
        const outputPanelDiv = document.createElement("div");
        panelDiv.appendChild(outputPanelDiv);
        outputPanelDiv.classList.add("panel_block");
        outputPanelDiv.appendChild(this.channel_outputs_panel.getHtmlElement());

        this.serverInterface.requestPotentiostatState();
    }

    userChangedChannelInputsPanel(data)
    {
        // @TODO
        console.log("Unimplemented userChangedChannelInputsPanel");
    }

    userChangedSettingsPanel(data)
    {
        // @TODO
        console.log("Unimplemented userChangedSettingsPanel");
    }

    updatePotentiostatInfo(newPotentiostatState)
    {
        console.log("Received new state from server:");
        console.log(newPotentiostatState);
        this.appDiv.innerHTML = "";
        this.appDiv.appendChild(this.createPotStatSummaryDiv(newPotentiostatState));
    }

    createPotStatSummaryDiv(potentiostatState)
    {
        const n_channels = potentiostatState["n_channels"];
        // const body = document.body,
        const tbl = document.createElement('table');
        tbl.style.width = '100px';
        tbl.style.border = '1px solid black';

        // Header
        const headerTr = tbl.insertRow();
        headerTr.insertCell().appendChild(document.createTextNode("Channel #"));
        headerTr.insertCell().appendChild(document.createTextNode("Switch state"));
        headerTr.insertCell().appendChild(document.createTextNode("Input Voltage"));
        headerTr.insertCell().appendChild(document.createTextNode("Measured ADC Voltage"));
        for (let i = 0; i < n_channels; i++) {
            const tr = tbl.insertRow();

            // Name
            tr.insertCell().appendChild(document.createTextNode(i.toString()));

            // On/off state
            const switch_td = tr.insertCell();
            const switch_state = potentiostatState["channel_switch_states"][i];
            let on_off_text = "";
            if (switch_state === null) on_off_text = "?";
            else if (switch_state === true) on_off_text = "On";
            else if (switch_state === false) on_off_text = "Off";
            else throw Error("Invalid switch state " + switch_state);

            switch_td.appendChild(document.createTextNode(on_off_text));
            switch_td.style.border = '1px solid black';

            // Voltage
            const voltage_td = tr.insertCell();
            const voltage_state = potentiostatState["channel_output_voltages"][i];
            let voltage_text = "";
            if (voltage_state === null) voltage_text = "?";
            else voltage_text = voltage_state.toString();

            voltage_td.appendChild(document.createTextNode(voltage_text));
            voltage_td.style.border = '1px solid black';

            // Current
            const current_td = tr.insertCell();
            const current_state = potentiostatState["channel_output_current"][i];
            let current_text = "";
            if (current_state === null) current_text = "?";
            else current_text = current_state.toString();

            current_td.appendChild(document.createTextNode(current_text));
            current_td.style.border = '1px solid black';
        }
        
        return tbl;
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

    requestPotentiostatReset()
    {
        this.socketio.emit("request_potentiostat_reset", "")
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