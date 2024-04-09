import { PotentiostatSettingPanel } from "./setting_panels.js";
import { ChannelsDataPanel  } from "./channel_panel.js";
import { LoggingPanel } from "./logging_panel.js";
import {
    PotstatLoggingData,
    PotstatStateData,
    UserChangedPotstatSettingsData,
    ChannelInputsSettingChangeData,
} from "./server_data_types.js";


const SERVER_SOCKET_PATH = `/socket_path`;
const VERSION = "0.1";


class PotentiostatView {
    private appDiv: HTMLDivElement;
    private basicPanel: HTMLDivElement;
    private serverInterface: ServerInterface;
    private potstat_setting_panel: PotentiostatSettingPanel;
    private channels_data_panel: ChannelsDataPanel;
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


        // Set up the control panels
        this.potstat_setting_panel = new PotentiostatSettingPanel();
        this.channels_data_panel = new ChannelsDataPanel();
        this.loggingPanel = new LoggingPanel();

        this.potstat_setting_panel.onUserChange((data) => { this.userChangedSettingsPanel(data); });
        this.channels_data_panel.onUserChange((data) => { this.userChangedChannelInputsPanel(data); });
        

        // Three panels - control panel, channel data panel, output panel
        const panelDiv = document.createElement("div");
        this.appDiv.appendChild(panelDiv);
        panelDiv.classList.add("panels_row");


        // Settings panel
        const settingsPanelDiv = document.createElement("div");
        panelDiv.appendChild(settingsPanelDiv);
        settingsPanelDiv.classList.add("panel_block");
        settingsPanelDiv.appendChild(this.potstat_setting_panel.getHtmlElement());
        

        // Channels data panel
        const channelsDataPanelDiv = document.createElement("div");
        panelDiv.appendChild(channelsDataPanelDiv);
        channelsDataPanelDiv.classList.add("panel_block");        
        channelsDataPanelDiv.appendChild(this.channels_data_panel.getHtmlElement());


        this.basicPanel = document.createElement("div");
        this.appDiv.appendChild(this.basicPanel);
        

        // Console area
        const loggingDiv = document.createElement("div");
        this.appDiv.appendChild(loggingDiv);
        // loggingDiv.classList.add("panel_block");
        loggingDiv.appendChild(this.loggingPanel.getHtmlElement());


        this.serverInterface.requestPotentiostatState();
    }

    private userChangedChannelInputsPanel(data: ChannelInputsSettingChangeData): void {
        // console.log("Unimplemented userChangedChannelInputsPanel");
        this.serverInterface.sendUserEditedChannelValues(data);
    }

    private userChangedSettingsPanel(data: UserChangedPotstatSettingsData): void {
        this.serverInterface.sendChangedPotstatSettings(data);
    }

    private updatePotentiostatInfo(newPotentiostatState: PotstatStateData): void {
        console.log("Received new state from server:");
        console.log(newPotentiostatState);

        this.potstat_setting_panel.updateSettingValue("control_mode", newPotentiostatState["control_program"]["type"])
        this.channels_data_panel.updatePanelFromData(newPotentiostatState);
        // this.channels_data_panel.updateChannelData(newPotentiostatState[])
    }

    private updateWithLoggingData(logData: PotstatLoggingData): void {
        this.loggingPanel.updateLog(logData);
    }

}




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
            console.log(message);
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

    public sendChangedPotstatSettings(data: UserChangedPotstatSettingsData): void {
        this.socketio.emit("client_changed_potstat_settings", data);
    }

    public sendUserEditedChannelValues(data: ChannelInputsSettingChangeData): void {
        this.socketio.emit("client_edited_channel_values", data);
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
