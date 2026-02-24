import patient from "../patientregistry/patient"

export type queueObj = {
    "sheet_id": string,
    "waiting_since"?: string, // same as arrival_time
    "patient_id": string,
    "patient_name": string,
    "arrival_time": string,
    "status": status
}

export type investigation_qa_obj = {
            ai_reasoning: string,
            patient_answer: string|null,
            question_id: string,
            question_text: string
        };

export type ServiceSheet = 
{
    created_at: string,
    id: string,
    patient: patient,
    status: string,
    triage_data?: {
        vitals:
        {
            systolic_bp: number,
            diastolic_bp: number,
            heart_rate: number,
            temperature: number,
            oxygen_saturation: number
            extras: any
        },
        nurse_initial_observations?: string,
        investigation_qa?: investigation_qa_obj[],
        ai_generated_suggestion?: string,
        risk_classification?: string,
        final_nurse_notes?: string
    },
    doctor_data?: {
        ai_pre_consultation_summary: string,
        doctor_notes: string,
        diagnosis_cid: string,
        prescription: string
    }

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