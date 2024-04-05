
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
    "channels": Array<{
        "switch_state": boolean | null;
        "voltage": number | null;
        "current": number | null;
    }>;
};

// type PotstatSettings = 

export type UserChangedPotstatSettingsData = {
    setting_id: string;
    option_picked: string;
};
