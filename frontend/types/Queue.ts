import { status } from "./Status"

export type queueObj = {
    "sheet_id": string,
    "waiting_since"?: string, // same as arrival_time
    "patient_id": string,
    "patient_name": string,
    "arrival_time": string,
    "status": status
}