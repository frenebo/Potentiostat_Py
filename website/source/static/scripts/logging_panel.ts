import { PotstatLoggingData } from "./server_data_types.js";

export class LoggingPanel {
    private mainDiv: HTMLDivElement;
    private logsDiv: HTMLDivElement;

    constructor() {
        this.mainDiv = document.createElement("div");
        
        this.logsDiv = document.createElement("div");
        this.mainDiv.appendChild(this.logsDiv);
        this.logsDiv.classList.add("logging_panel");
    }
    
    public getHtmlElement(): HTMLDivElement {
        return this.mainDiv;
    }

    private addLine(logtype: string, text: string, timestamp_seconds: number) {
        const logtimestamp = new Date(timestamp_seconds * 1000);
        const lineDiv = document.createElement("div");
        const timeString = logtimestamp.toUTCString()+ " ";

        const timeDiv = document.createElement("div");
        lineDiv.appendChild(timeDiv);
        timeDiv.appendChild(document.createTextNode(timeString));
        timeDiv.classList.add("logline_datetime");

        const logTextDiv = document.createElement("div");
        lineDiv.appendChild(logTextDiv);
        logTextDiv.appendChild(document.createTextNode(text));
        logTextDiv.classList.add("logline_text");
        // lineDiv.appendChild(document.createTextNode())
        // lineDiv.appendChild(document.createTextNode(text));
        if (logtype !== "log") {
            logTextDiv.classList.add("log_error");
            timeDiv.classList.add("log_error");
            // logTextDiv.style.color = "red";
            // logTextDiv.style.fontWeight = "bold";
        }
        if (this.logsDiv.children.length == 0) {
            this.logsDiv.appendChild(lineDiv);
        } else {
            this.logsDiv.insertBefore(lineDiv, this.logsDiv.children[0]);
        }
    }

    public updateLog(logData: PotstatLoggingData): void {
        for (const line of logData["lines"]) {
            this.addLine(line["type"], line["text"], line["timestamp_seconds"])
        }
        // const logTextnode = document.createTextNode(logData["lines"][0][])
        
        // console.log("Unimplemented logging");
        // console.log(logData)
    }
}
