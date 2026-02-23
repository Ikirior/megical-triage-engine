import patient from "../patientregistry/patient"

export type queueObj = {
    "sheet_id": string,
    "patient_id": string,
    "patient_name": string,
    "arrival_time": string
}

export type ServiceSheet = 
{
    created_at: string,
    doctor_data: null,
    id: string,
    patient: patient,
    status: string,
    triage_data: null
}