
export type PotstatLoggingData = {
    "lines": Array<{
        "type": "warning" | "log";
        "text": string;
        "timestamp_seconds": number;
    }>;
}