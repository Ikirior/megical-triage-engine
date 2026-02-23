'use client';
import TriageSheet from "@/components/triagesheet/triagesheet";
import { Send, Rocket, PlusIcon, MessageCircleQuestionIcon } from "lucide-react";
import SingleButton from "@/components/singlebutton/singlebutton";
import { useState } from "react";
import TriageQueue from "./triagequeue";
import { queueObj } from "./types";
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
    const [current_step, setStep] = useState(null as 1|2|3|null)

    return <div className={styles.panel}>
        <h1 style={{"margin": "4vh 0 0 2vh", "fontSize": "2em"}}>&lt;Patient&gt;'s Triage Sheet</h1>
        <TriageSheet current_sheet_id={current_patient_info.sheet_id}></TriageSheet>
        <TriageQueue queue={params.queue} setCurrentPatientInfo={setCurrentPatientInfo} currentPatientId={current_patient_info.patient_id} setStep={setStep}/>
        <StepSection currentStep={current_step}/>
    </div>
}