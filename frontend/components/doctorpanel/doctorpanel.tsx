'use client';
import TriageSheet from "@/components/triagesheet/triagesheet";
import { useEffect, useState } from "react";
;
import StepSection from "../triagesheet/stepsection";
import styles from '@/components/triagesheet/triagesheet.module.css'
import { queueObj, status_nums } from "../triagesheet/types";
import TriageQueue from "../triagesheet/triagequeue";

// current_patient_id
// current_step

type doctorPanelParams = {
    queue: queueObj[]
}

export default function DoctorPanel(params: doctorPanelParams)
{

    const [current_patient_info, setCurrentPatientInfo] = useState({"sheet_id": null, "patient_id": null} as {"sheet_id":string|null, "patient_id": string|null})
    const [current_step, setStep] = useState(0 as status_nums)

    return <div className={styles.panel}>
        <h1 style={{"margin": "4vh 0 0 2vh", "fontSize": "2em"}}>Patient's Service Sheet</h1>
        <TriageSheet user_role='doctor' current_sheet_id={current_patient_info.sheet_id} current_step={current_step} set_step={setStep}></TriageSheet>
        <TriageQueue queue={params.queue} setCurrentPatientInfo={setCurrentPatientInfo} currentSheetId={current_patient_info.sheet_id} setStep={setStep}/>
    </div>
}