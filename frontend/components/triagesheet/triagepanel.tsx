'use client';
import TriageSheet from "@/components/triagesheet/triagesheet";
import { useState } from "react";
import TriageQueue from "./triagequeue";
import { queueObj } from "@/types/Queue";
import { status_nums } from "@/types/Status";
import StepSection from "./stepsection";
import styles from '@/components/triagesheet/triagesheet.module.css'

// current_patient_id
// current_step

type triagepanelparams = {
    queue: queueObj[]
}


export default function TriagePanel(params: triagepanelparams)
{

    const [current_patient_info, setCurrentPatientInfo] = useState({"sheet_id": null, "patient_id": null} as {"sheet_id":string|null, "patient_id": string|null})
    const [current_step, setStep] = useState(0 as status_nums)

    return <div className={styles.panel}>
        <h1 style={{"margin": "4vh 0 0 2vh", "fontSize": "2em"}}>Patient's Triage Sheet</h1>
        <TriageSheet user_role="nurse" current_sheet_id={current_patient_info.sheet_id} current_step={current_step} set_step={setStep}></TriageSheet>
        <TriageQueue user_role="nurse" queue={params.queue} setCurrentPatientInfo={setCurrentPatientInfo} currentSheetId={current_patient_info.sheet_id} setStep={setStep}/>
        <StepSection currentStep={current_step}/>
    </div>
}