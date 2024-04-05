import { PotstatLoggingData } from "./server_data_types.js";

export class LoggingPanel {
    private mainDiv: HTMLDivElement;

    constructor() {
        this.mainDiv = document.createElement("div");
    }
    
    public getHtmlElement(): HTMLDivElement {
        return this.mainDiv;
    }

    public updateLog(logData: PotstatLoggingData): void {
        console.log("Unimplemented logging");
        console.log(logData)
    }
}