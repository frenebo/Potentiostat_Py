
export type PotstatSettingChangeData = {
    setting_id: string;
    option_picked: string;
};
export class PotentiostatSettingPanel {
    private mainDiv: HTMLDivElement;
    private settingsTablePanel: HTMLDivElement;
    private settingsTbl: HTMLTableElement;
    private userChangeListeners: Array<(data: PotstatSettingChangeData) => void>;

    private multipleChoicesettings: Array<{
        tableRow: HTMLTableRowElement;
        selectElement: HTMLSelectElement;
        options_info: Array<{"id": string, "display": string}>,
    }> = [];

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
            {"id": "manual", "display": "Manual"},
            {"id": "cyclic", "display": "Cyclic Voltammetry"},
        ]);

        this.userChangeListeners = [];
    }

    private addMultipleChoiceSetting(setting_id: string, setting_display_name: string, options_info: Array<{"id": string, "display": string}>): void {
        const choiceTableRow = this.settingsTbl.insertRow();
        
        choiceTableRow.insertCell().appendChild(document.createTextNode(setting_display_name));
        
        const sel = document.createElement("select");
        choiceTableRow.insertCell().appendChild(sel);

        for (const opt_info of options_info) {
            sel.appendChild(new Option(
                opt_info["display"],
                opt_info["id"],
            ));
        }

        sel.addEventListener("change", (ev) => {
            if (ev.target === null) return;
            const userPickedOption: string = (ev.target as HTMLSelectElement).value;

            this.callSettingChangeListeners(setting_id, userPickedOption);
        });

        this.multipleChoicesettings.push({
            "tableRow": choiceTableRow,
            "selectElement": sel,
            "options_info": options_info,
        });
    }

    public getHtmlElement(): HTMLDivElement {
        return this.mainDiv;
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

    public onUserChange(listener: (arg: PotstatSettingChangeData) => void): void {
        this.userChangeListeners.push(listener);
    }
}

export type ChannelInputsSettingChangeData = {};
export class ChannelInputsPanel {
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