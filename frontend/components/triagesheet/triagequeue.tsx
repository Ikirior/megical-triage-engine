'use client';
import { queueObj } from "@/types/Queue";
import SidePanel from "./sidepanel";
import QueueElement from "./queueElement";


type triagequeueparams = {
    setCurrentPatientInfo: Function,
    currentSheetId: string|null,
    setStep: Function,
    queue: queueObj[],
    user_role: "doctor"|"nurse"
}

export default function TriageQueue(params: triagequeueparams)
{
    const new_triages = params.user_role != 'doctor' ? params.queue.filter((value)=>value.status == 'aguardando_triagem') : params.queue;
    const other = params.user_role != 'doctor' ? params.queue.filter((value) => value.status != 'aguardando_triagem') : []

    return <SidePanel position="left">
        <h1 style={{fontSize: "1.3em"}}>Patient Triage Queue</h1>
        {
            new_triages.length > 0 ?
                <div>
                    {...new_triages.map((value, index) => <QueueElement  user_role={params.user_role} currentSheetId={params.currentSheetId} value={value} index={index} setCurrentPatientInfo={params.setCurrentPatientInfo} setStep={params.setStep}/>)}
                </div> :
                <div>No patients yet in queue!</div>
        }
        {
            params.user_role != 'doctor' &&
            <>
                <h1 style={{fontSize: "1.3em", marginTop: "3vh", borderTop: "thin grey solid", paddingTop: "1vh"}}>Continue Editing</h1>
                {
                    other.length > 0 ?
                        <div>
                            {...other.map((value, index) => <QueueElement user_role={params.user_role} currentSheetId={params.currentSheetId} value={value} index={index} setCurrentPatientInfo={params.setCurrentPatientInfo} setStep={params.setStep} continueEditing/>)}
                        </div> :
                        <div>No patients to continue editing. </div>
                }
        
            </>
        }
    </SidePanel>;
}