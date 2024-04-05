import {
    PotentiostatSettingPanel,
    ChannelInputsPanel,
    PotstatSettingChangeData,
    ChannelInputsSettingChangeData,
} from "./setting_panels.js";
import { LoggingPanel } from "./logging_panel.js";
import { PotstatLoggingData } from "./server_data_types.js";


const SERVER_SOCKET_PATH = `/socket_path`;
const VERSION = "0.1";



class ChannelOutputsPanel {
    private mainDiv: HTMLDivElement;
    private lastUpdatedDiv: HTMLDivElement;
    private inputsTablePanel: HTMLDivElement;

    constructor() {
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

    public getHtmlElement(): HTMLDivElement {
        return this.mainDiv;
    }
}



class PotentiostatView {
    private appDiv: HTMLDivElement;
    private basicPanel: HTMLDivElement;
    private serverInterface: ServerInterface;
    private potstat_setting_panel: PotentiostatSettingPanel;
    private channel_inputs_panel: ChannelInputsPanel;
    private channel_outputs_panel: ChannelOutputsPanel;
    private loggingPanel: LoggingPanel;

    constructor(appDiv: HTMLDivElement, serverInterface: ServerInterface) {
        this.appDiv = appDiv;
        this.serverInterface = serverInterface;

        this.serverInterface.onServerStateChange((newState: PotstatStateData) => { this.updatePotentiostatInfo(newState); });
        this.serverInterface.onPotstatLogging((logData: PotstatLoggingData) => { this.updateWithLoggingData(logData); });

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
        this.loggingPanel = new LoggingPanel();

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

        this.basicPanel = document.createElement("div");
        this.appDiv.appendChild(this.basicPanel);
        

        // Console area
        const loggingDiv = document.createElement("div");
        this.appDiv.appendChild(loggingDiv);
        loggingDiv.classList.add("panel_block");
        loggingDiv.appendChild(this.loggingPanel.getHtmlElement());


        this.serverInterface.requestPotentiostatState();
    }

    private userChangedChannelInputsPanel(data: ChannelInputsSettingChangeData): void {
        // @TODO
        console.log("Unimplemented userChangedChannelInputsPanel");
    }

    private userChangedSettingsPanel(data: PotstatSettingChangeData): void {

        // this.serverInterface.sendPotstatSettingChangeData()
        // // @TODO
        console.log("Unimplemented userChangedSettingsPanel");
    }

    private updatePotentiostatInfo(newPotentiostatState: PotstatStateData): void {
        console.log("Received new state from server:");
        console.log(newPotentiostatState);
        this.basicPanel.innerHTML = "";
        this.basicPanel.appendChild(this.createPotStatSummaryDiv(newPotentiostatState));
    }

    private updateWithLoggingData(logData: PotstatLoggingData): void {
        // console.log("received logging data: ");
        // console.log(logData);
        this.loggingPanel.updateLog(logData);
        // this.loggingPanel.
    }

    private createPotStatSummaryDiv(potentiostatState: PotstatStateData): HTMLDivElement {
        const summaryDiv = document.createElement("div");

        const n_channels: number | null = potentiostatState["n_channels"];
        if (n_channels === null)
        {
            summaryDiv.innerHTML = "Number of channels is undefined";
            return summaryDiv;
        }
        
        const tbl = document.createElement('table');
        summaryDiv.appendChild(tbl);

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
        
        return summaryDiv;
    }
}

type PotstatStateData = {
    "n_modules": number | null;
    "n_channels": number | null;
    "channel_switch_states": Array<boolean | null>;
    "channel_output_voltages": Array<number | null>;
    "channel_output_current": Array<number | null>;
};



declare var io: any;

class ServerInterface {
    private stateChangedListeners: Array<(arg: PotstatStateData) => void>;
    private potstatLoggingListeners: Array<(arg: PotstatLoggingData) => void>;
    private socketio: any;

    constructor() {
        // Socketio should be imported
        this.socketio = io(SERVER_SOCKET_PATH);
        this.stateChangedListeners = [];
        this.potstatLoggingListeners = [];

        this.socketio.on("potentiostat_state", (message: PotstatStateData) => {
            for (const listener of this.stateChangedListeners) {
                listener(message);
            }
        });

        this.socketio.on("potentiostat_logging", (message: PotstatLoggingData) => {
            for (const listener of this.potstatLoggingListeners) {
                listener(message);
            }
        });
    }

    public requestPotentiostatReset(): void {
        this.socketio.emit("request_potentiostat_reset", "")
    }

    public requestPotentiostatState(): void {
        this.socketio.emit("request_potentiostat_state", "");
    }

    public onServerStateChange(listener: (data: PotstatStateData) => void): void {
        this.stateChangedListeners.push(listener);
    }

    public onPotstatLogging(listener: (data: PotstatLoggingData) => void): void {
        this.potstatLoggingListeners.push(listener);
    }
}


function setupApp(appDiv: HTMLDivElement): void {
    const serverInterface = new ServerInterface();
    const pot_view = new PotentiostatView(appDiv, serverInterface);
}

export { setupApp };