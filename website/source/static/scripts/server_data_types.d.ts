
export type PotstatLoggingData = {
    "lines": Array<{
        "type": "warning" | "log";
        "text": string;
        "timestamp_seconds": number;
    }>;
}

export type PotstatStateData = {
    "n_modules": number | null;
    "n_channels": number | null;
    "channel_switch_states": Array<boolean | null>;
    "channel_output_voltages": Array<number | null>;
    "channel_output_current": Array<number | null>;
};