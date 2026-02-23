'use client';
import { useState } from "react";
import styles from '@/components/triagesheet/triagesheet.module.css'
import { ArrowLeft, CheckSquare2Icon, SquareArrowUpRight } from "lucide-react";
import GetQeuePatients from "./getQueuePatients";
import { queueObj, status } from "./types";
import SingleButton from "../singlebutton/singlebutton";
import SidePanel from "./sidepanel";
import QueueElement from "./queueElement";


type triagequeueparams = {
    setCurrentPatientInfo: Function,
    currentSheetId: string|null,
    setStep: Function,
    queue: queueObj[]
}

export default function TriageQueue(params: triagequeueparams)
{
    const new_triages = params.queue.filter((value)=>value.status == 'aguardando_triagem');
    const other = params.queue.filter((value) => value.status != 'aguardando_triagem')

    return <SidePanel position="left">
        <h1 style={{fontSize: "1.3em"}}>Patient Triage Queue</h1>
        {
            new_triages.length > 0 ?
                <div>
                    {...new_triages.map((value, index) => <QueueElement currentSheetId={params.currentSheetId} value={value} index={index} setCurrentPatientInfo={params.setCurrentPatientInfo} setStep={params.setStep}/>)}
                </div> :
                <div>No patients yet in queue!</div>
        }
        <h1 style={{fontSize: "1.3em", marginTop: "3vh", borderTop: "thin grey solid", paddingTop: "1vh"}}>Continue Editing</h1>
        {
            other.length > 0 ?
                <div>
                    {...other.map((value, index) => <QueueElement currentSheetId={params.currentSheetId} value={value} index={index} setCurrentPatientInfo={params.setCurrentPatientInfo} setStep={params.setStep} continueEditing/>)}
                </div> :
                <div>No patients to continue editing. </div>
        }
    </SidePanel>;
}