import patient from "../patientregistry/patient"

export type queueObj = {
    "sheet_id": string,
    "patient_id": string,
    "patient_name": string,
    "arrival_time": string,
    "status": status
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


export const STEP_MAPPING = {
    "aguardando_triagem": 0,
    "em_triagem_fase_1": 1,
    "em_triagem_fase_2": 2,
    "em_triagem_fase_3": 3,
    "aguardando_medico": 4,
    "em_atendimento": 5,
    "finalizado": 6
}

export type status =  keyof typeof STEP_MAPPING;
export type status_nums = typeof STEP_MAPPING[status]