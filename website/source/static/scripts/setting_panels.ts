import { UserChangedPotstatSettingsData } from "./server_data_types.js";

export class PotentiostatSettingPanel {
    private mainDiv: HTMLDivElement;
    private settingsTablePanel: HTMLDivElement;
    private settingsTbl: HTMLTableElement;
    private userChangeListeners: Array<(data: UserChangedPotstatSettingsData) => void>;

    private multipleChoicesettings: {[key: string]: {
        tableRow: HTMLTableRowElement;
        selectElement: HTMLSelectElement;
        option_elements: {[option_id: string]:  HTMLOptionElement},
        // options_info: Array<{
        //     "id": string,
        //     "display": string,
        //     "option_element": HTMLOptionElement,
        // }>,
    }} = {};

    constructor() {
        this.mainDiv = document.createElement("div");

        const titleBar = document.createElement("div");
        titleBar.innerHTML = "Settings";
        this.mainDiv.appendChild(titleBar);

        this.settingsTablePanel = document.createElement("div");
        this.settingsTablePanel.classList.add('potstat_settings_table_panel');
        this.mainDiv.appendChild(this.settingsTablePanel);

        this.settingsTbl = document.createElement("table");
        this.settingsTablePanel.appendChild(this.settingsTbl);
        // this.settingsTbl.style.width = '100px';
        // this.settingsTbl.style.border = '1px solid black';

        this.addMultipleChoiceSetting("control_mode", "Control Mode", [
            {"id": "manual", "displayname": "Manual"},
            {"id": "cyclic", "displayname": "Cyclic Voltammetry"},
        ]);

        this.userChangeListeners = [];
    }

    public getHtmlElement(): HTMLDivElement {
        return this.mainDiv;
    }

    public onUserChange(listener: (arg: UserChangedPotstatSettingsData) => void): void {
        this.userChangeListeners.push(listener);
    }

    public updateSettingValue(setting_id: string, new_val: string)
    {
        const settingContents = this.multipleChoicesettings[setting_id];
        if (settingContents === undefined)
        {
            console.log("Could not update setting '" + setting_id + "', unknown setting id");
        }

        const optionElementToSelect = settingContents["option_elements"][new_val];
        // settingContents.
        if (optionElementToSelect === undefined)
        {
            console.log("Could not find option element '" + new_val + "' in the dropdown for setting '" + setting_id + "'");
        }

        settingContents["selectElement"].value = new_val;
    }

    // public setControlMode()
    // {
    //     // this.
    // }

    private addMultipleChoiceSetting(setting_id: string, setting_display_name: string, options: Array<{"id": string, "displayname": string}>): void {
        const choiceTableRow = this.settingsTbl.insertRow();
        
        choiceTableRow.insertCell().appendChild(document.createTextNode(setting_display_name));
        
        const sel = document.createElement("select");
        choiceTableRow.insertCell().appendChild(sel);

        // Until data is received, this is left blank
        const defaultBlankOption = new Option("--", "__blankoption");
        sel.appendChild(defaultBlankOption);
        defaultBlankOption.selected = true;
        defaultBlankOption.hidden = true;
        defaultBlankOption.disabled = true;

        const option_elements: {[key: string]: HTMLOptionElement} = {};

        for (const opt_contents of options) {
            const option_id = opt_contents["id"];
            const optionHTMLElement = new Option(
                opt_contents["displayname"],
                option_id,
            );
            sel.appendChild(optionHTMLElement);
            option_elements[option_id] = optionHTMLElement;
        }

        sel.addEventListener("change", (ev) => {
            if (ev.target === null) return;
            const userPickedOption: string = (ev.target as HTMLSelectElement).value;

            // Wait until the server confirms the change before updating value
            this.callSettingChangeListeners(setting_id, userPickedOption);

            sel.value = "__blankoption";
        });

        this.multipleChoicesettings[setting_id] = {
            "tableRow": choiceTableRow,
            "selectElement": sel,
            "option_elements": option_elements,
        };
    }


    private callSettingChangeListeners(setting_id: string, option_picked_id: string): void {
        for (const l of this.userChangeListeners)
        {
            l({
                "setting_id": setting_id,
                "option_picked": option_picked_id,
            });
        }
    }
}

export type ChannelInputsSettingChangeData = {};
export class ChannelsDataPanel {
    private mainDiv: HTMLDivElement;
    private lastUpdatedDiv: HTMLDivElement;
    private inputsTablePanel: HTMLDivElement;
    private userChangeListeners: Array<(arg: ChannelInputsSettingChangeData) => void>;

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
        
        this.userChangeListeners = [];
    }

    public getHtmlElement(): HTMLDivElement {
        return this.mainDiv;
    }

    public onUserChange(listener: (data: ChannelInputsSettingChangeData) => void): void {
        this.userChangeListeners.push(listener);
    }
}
