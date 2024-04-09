
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

export type ChannelInputsSettingChangeData = {
    "channel_idx": number,
    "changed_setting": {
        "field": "switch";
        "switch_state": "on" | "off";
    } | {
        "field": "voltage";
        "voltage_string": string;
    };
};

export class ChannelsDataPanel {
    private mainDiv: HTMLDivElement;
    private lastUpdatedDiv: HTMLDivElement;
    private inputsTablePanel: HTMLDivElement;
    private userChangeListeners: Array<(arg: ChannelInputsSettingChangeData) => void>;

    private channelsAreEditable: boolean | null;
    private tableChannelCount: number | null;
    private inputsTableRows: Array<{
        "switchSelect": HTMLSelectElement;
        "voltageDiv": HTMLDivElement;
        "currentText": HTMLDivElement;
    }>;

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
        this.channelsAreEditable = null;

        this.inputsTableRows = [];
        
        this.userChangeListeners = [];
    }

    public getHtmlElement(): HTMLDivElement {
        return this.mainDiv;
    }

    public onUserChange(listener: (data: ChannelInputsSettingChangeData) => void): void {
        this.userChangeListeners.push(listener);
    }

    public updatePanelFromData(data: PotstatStateData): void {
        const new_n_channels: number | null = data["n_channels"];
        const new_editable: boolean = data["control_mode"] === "manual";

        if (new_n_channels === null)
        {
            this.inputsTablePanel.innerHTML = "";
            this.inputsTableRows = [];
            this.tableChannelCount = null;
            return;
        }

        if (new_n_channels !== this.tableChannelCount ||
            new_editable !== this.channelsAreEditable) {
            this.constructNewChannelPanel(new_n_channels, new_editable);
            this.populateChannelPanelFromData(data);
        } else {
            // Don't need to rebuild the panel, just refresh the contents
            this.populateChannelPanelFromData(data);
        }
    }

    private populateChannelPanelFromData(data: PotstatStateData): void {
        if (this.tableChannelCount === null) {
            throw new Error("No channels in table are currently set up, cannot populate panel");
        }
        if (this.tableChannelCount !== data["n_channels"]) {
            throw new Error("Cannot populate table with data - current tableChannelCount is " + this.tableChannelCount + " but data has " + data["n_channels"] + " channels");
        }

        for (let chanIdx = 0; chanIdx < this.tableChannelCount; chanIdx++) {
            const chanData = data["channels"][chanIdx];

            // Switch
            const newSwitchState = chanData["switch_state"];
            const switchElement = this.inputsTableRows[chanIdx]["switchSelect"];

            if (newSwitchState === null) {
                switchElement.value = "__blankoption";
            } else if (newSwitchState === true) {
                switchElement.value = "switch_on";
            } else {
                switchElement.value = "switch_off";
            }

            // Voltage
            const voltageElement = this.inputsTableRows[chanIdx]["voltageDiv"];
            const newVoltage = chanData["voltage"];
            if (newVoltage === null) {
                voltageElement.innerHTML = "?";
            } else {
                voltageElement.innerHTML = newVoltage.toString();
            }

            // Current
            const currentElement = this.inputsTableRows[chanIdx]["currentText"];
            const newCurrent = chanData["current"];
            if (newCurrent === null) {
                currentElement.innerHTML = "?";
            } else {
                currentElement.innerHTML = newCurrent.toString();
            }
        }
    }

    private static createSwitchSelect(editable: boolean): HTMLSelectElement
    {
        const switchSelector = document.createElement("select");
        
        const defaultBlankOption = new Option("--", "__blankoption");
        switchSelector.appendChild(defaultBlankOption);
        defaultBlankOption.selected = true;
        defaultBlankOption.hidden = true;
        defaultBlankOption.disabled = true;

        // const option_elements = 
        const on_option = new Option("On", "switch_on");
        // if ()
        switchSelector.appendChild(on_option);
        const off_option = new Option("Off", "switch_off");
        switchSelector.appendChild(off_option);

        if (!editable) {
            on_option.disabled = true;
            off_option.disabled = true;
        }

        return switchSelector;
    }

    private static createVoltageDivBox(): HTMLDivElement {
        const voltageInput = document.createElement("div");
        // voltageInput.
        voltageInput.classList.add("chan_voltage_cell_content");

        return voltageInput;
    }

    private static createCurrentReadingBox(): HTMLDivElement {
        const box = document.createElement("div");
        box.classList.add("current_reading");

        return box
    }

    private callChangedListeners(dat: ChannelInputsSettingChangeData) {
        for (const l of this.userChangeListeners) {
            l(dat);
        }
    }

    private userEditedChannel(channelIdx: number, field: "switch" | "voltage", newValue: string)
    {
        if (field == "switch") {
            let datVal: "on" | "off";

            if (newValue === "switch_on") {
                datVal = "on";
            } else if (newValue === "switch_off") {
                datVal = "off";
            } else {
                throw Error("invalid switch value " + newValue);
            }

            // if (newValue !== "switch_on")
            this.callChangedListeners({
                "channel_idx": channelIdx,
                "changed_setting": {
                    "field": "switch",
                    "switch_state": datVal,
                }
            });
        } else if (field === "voltage") {
            this.callChangedListeners({
                "channel_idx": channelIdx,
                "changed_setting": {
                    "field": "voltage",
                    "voltage_string": newValue,
                }
            });
        } else {
            throw Error("Invalid field to edit, '" + field + "'");
        }
    }

    private constructNewChannelPanel(channelCount: number, editable: boolean)
    {
        console.log("Constructing new panel");
        this.tableChannelCount = channelCount;
        this.channelsAreEditable = editable;

        this.inputsTablePanel.innerHTML = "";
        this.inputsTableRows = [];

        const channelTable = document.createElement("table");
        this.inputsTablePanel.appendChild(channelTable);

        // Header
        const headerTr = channelTable.insertRow();
        headerTr.insertCell().appendChild(document.createTextNode("Channel #"));
        headerTr.insertCell().appendChild(document.createTextNode("Switch state"));
        headerTr.insertCell().appendChild(document.createTextNode("Input Voltage"));
        headerTr.insertCell().appendChild(document.createTextNode("Measured ADC Voltage"));

        for (let chanIdx = 0; chanIdx < channelCount; chanIdx++) {
            // const chan
            const chanRow = channelTable.insertRow();
            chanRow.insertCell().appendChild(document.createTextNode(chanIdx.toString()));

            // Selector for the switch state
            const switchSelector = ChannelsDataPanel.createSwitchSelect(editable);
            chanRow.insertCell().appendChild(switchSelector);
            

            switchSelector.addEventListener("change", (ev) => {
                if (ev.target === null) return;

                if (!editable) return; // Shouldn't be getting to this point anyways, but just in case...

                const userPickedOption: string = (ev.target as HTMLSelectElement).value;

                // Wait until the server confirms the change before updating value
                this.userEditedChannel(chanIdx, "switch", userPickedOption);
                // this.userChange(setting_id, userPickedOption);

                switchSelector.value = "__blankoption";
            });


            const voltageCell = chanRow.insertCell();
            voltageCell.classList.add("chan_voltage_cell_content");
            
            const voltageDivBox = ChannelsDataPanel.createVoltageDivBox();
            voltageCell.appendChild(voltageDivBox);
            
            if (editable) {
                const voltageEditButton = document.createElement("button");
                voltageEditButton.textContent = "edit";
                voltageCell.appendChild(voltageEditButton);
                voltageEditButton.onclick = (ev) => {
                    const newVal = prompt("Enter new voltage");
                    if (newVal === null) {
                        alert("No value entered");
                        return;
                    }
                    
                    this.userEditedChannel(chanIdx, "voltage", newVal);
                }
            }



            // throw new Error("Unimplemented change/return listeners on input box")

            const currentReadingBox = ChannelsDataPanel.createCurrentReadingBox();
            chanRow.insertCell().appendChild(currentReadingBox);

            this.inputsTableRows.push({
                "switchSelect": switchSelector,
                "voltageDiv": voltageDivBox,
                "currentText": currentReadingBox,
            });
        }
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