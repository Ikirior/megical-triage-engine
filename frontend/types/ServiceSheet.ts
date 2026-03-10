import { investigation_qa_obj } from "./InvestigationQA"
import { patient } from "./Patient"

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