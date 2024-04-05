
export type PotstatLoggingData = {
    "lines": Array<{
        "type": "warning" | "log";
        "text": string;
        "timestamp_seconds": number;
    }>;
}

export type ControlModeString = "manual" | "cyclic";

export type PotstatStateData = {
    "n_modules": number | null;
    "n_channels": number | null;
    "control_mode": ControlModeString;
    "channel_switch_states": Array<boolean | null>;
    "channel_output_voltages": Array<number | null>;
    "channel_output_current": Array<number | null>;
};

// type PotstatSettings = 

export type UserChangedPotstatSettingsData = {
    setting_id: string;
    option_picked: string;
};
