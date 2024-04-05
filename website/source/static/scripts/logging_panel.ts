import { PotstatLoggingData } from "./server_data_types.js";

export class LoggingPanel {
    private mainDiv: HTMLDivElement;

    constructor() {
        this.mainDiv = document.createElement("div");
    }
    
    getHtmlElement() {
        return this.mainDiv;
    }

    public updateLog(logData: PotstatLoggingData) {
        console.log("Unimplemented logging");
        console.log(logData)
    }
}