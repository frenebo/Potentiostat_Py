
export type PotstatLoggingData = {
    "lines": Array<{
        "type": "warning" | "log" | "error";
        "text": string;
        "timestamp_seconds": number;
    }>;
}

export type ControlModeString = "manual" | "cyclic";

export type PotstatStateData = {
    "n_modules": number | null;
    "n_channels": number | null;
    "timestamp_seconds": number;
    "control_program": {
        "type": "manual";
    } | {
        "type": "cyclic";
    }
    // "control_mode": ControlModeString;
    "channels": Array<{
        "switch_state": boolean | null;
        "voltage": number | null;
        "current": number | null;
    }>;
};


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


// type PotstatSettings = 

export type UserChangedPotstatSettingsData = {
    setting_id: string;
    option_picked: string;
};
