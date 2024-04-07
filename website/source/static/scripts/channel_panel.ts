
import { PotstatStateData } from "./server_data_types.js"

// export class ChannelMonitorPanel {
//     // private channelVoltages = 
//     private channelRows: Array<{
//         // switch_input:
//         // "switch_state": boolean | undefined;
//         // "voltage": number | undefined;
//         // "current": number | undefined;
//         // "switch_editable": boolean;
//         // "voltage_editable": boolean;
//     }> = [];
//     constructor() {
//     }
// }

export type ChannelInputsSettingChangeData = {};

export class ChannelsDataPanel {
    private mainDiv: HTMLDivElement;
    private lastUpdatedDiv: HTMLDivElement;
    private inputsTablePanel: HTMLDivElement;
    private userChangeListeners: Array<(arg: ChannelInputsSettingChangeData) => void>;
    private tableChannelCount: number | null;

    constructor() {
        this.mainDiv = document.createElement("div");

        const titleBar = document.createElement("div");
        titleBar.innerHTML = "Inputs (Volts)";
        this.mainDiv.appendChild(titleBar);

        this.lastUpdatedDiv = document.createElement("div");
        this.mainDiv.appendChild(this.lastUpdatedDiv);

        this.inputsTablePanel = document.createElement("div");
        this.inputsTablePanel.classList.add('input_table_panel');
        this.mainDiv.appendChild(this.inputsTablePanel);

        this.tableChannelCount = null;
        
        this.userChangeListeners = [];
    }

    public getHtmlElement(): HTMLDivElement {
        return this.mainDiv;
    }

    public onUserChange(listener: (data: ChannelInputsSettingChangeData) => void): void {
        this.userChangeListeners.push(listener);
    }

    public updateChannelData(data: PotstatStateData): void {
        if (data["n_channels"] === null)
        {
            this.inputsTablePanel.innerHTML = "";
            this.tableChannelCount = null;
            return;
        }

        if (data["n_channels"] !== this.tableChannelCount) {
            this.setupNewChannelPanel(data["n_channels"]);
        }

        // Populate the stuff here
        throw new Error("unimplemented");
    }

    private setupNewChannelPanel(channelCount: number)
    {
        this.inputsTablePanel.innerHTML = "";

        this.tableChannelCount = channelCount;
    }
}

    // private createPotStatSummaryDiv(potentiostatState: PotstatStateData): HTMLDivElement {
    //     const summaryDiv = document.createElement("div");

    //     const n_channels: number | null = potentiostatState["n_channels"];
    //     if (n_channels === null)
    //     {
    //         summaryDiv.innerHTML = "Number of channels is undefined";
    //         return summaryDiv;
    //     }
        
    //     const tbl = document.createElement('table');
    //     summaryDiv.appendChild(tbl);

    //     tbl.style.width = '100px';
    //     tbl.style.border = '1px solid black';

    //     // Header
    //     const headerTr = tbl.insertRow();
    //     headerTr.insertCell().appendChild(document.createTextNode("Channel #"));
    //     headerTr.insertCell().appendChild(document.createTextNode("Switch state"));
    //     headerTr.insertCell().appendChild(document.createTextNode("Input Voltage"));
    //     headerTr.insertCell().appendChild(document.createTextNode("Measured ADC Voltage"));
    //     for (let i = 0; i < n_channels; i++) {
    //         const tr = tbl.insertRow();

    //         // Name
    //         tr.insertCell().appendChild(document.createTextNode(i.toString()));

    //         // On/off state
    //         const switch_td = tr.insertCell();
    //         const switch_state = potentiostatState["channel_switch_states"][i];
    //         let on_off_text = "";
    //         if (switch_state === null) on_off_text = "?";
    //         else if (switch_state === true) on_off_text = "On";
    //         else if (switch_state === false) on_off_text = "Off";
    //         else throw Error("Invalid switch state " + switch_state);

    //         switch_td.appendChild(document.createTextNode(on_off_text));
    //         switch_td.style.border = '1px solid black';

    //         // Voltage
    //         const voltage_td = tr.insertCell();
    //         const voltage_state = potentiostatState["channel_output_voltages"][i];
    //         let voltage_text = "";
    //         if (voltage_state === null) voltage_text = "?";
    //         else voltage_text = voltage_state.toString();

    //         voltage_td.appendChild(document.createTextNode(voltage_text));
    //         voltage_td.style.border = '1px solid black';

    //         // Current
    //         const current_td = tr.insertCell();
    //         const current_state = potentiostatState["channel_output_current"][i];
    //         let current_text = "";
    //         if (current_state === null) current_text = "?";
    //         else current_text = current_state.toString();

    //         current_td.appendChild(document.createTextNode(current_text));
    //         current_td.style.border = '1px solid black';
    //     }
        
    //     return summaryDiv;
    // }