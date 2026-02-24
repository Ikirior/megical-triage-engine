'use client';
import styles from '@/components/triagesheet/triagesheet.module.css'
import SidePanel from "./sidepanel";


type stepsectionparams = {
    currentStep: number|null
}

const CONTENT = {
    0:{
        "description": <>Start by choosing a triage from the <b>queue</b>. The <b>queue</b> contains both the information of patients who are waiting for their triage to start, but also of those whose triage has started, but was left unfinished.</>,
        "next_step": <>During step 1, you'll fill in the <b>Essentials</b> (vitals) topic and add <b>Observations</b>.</>
    },
    1: {
        "description": <>Fill in the <b>Essentials</b> and <b>Observations</b> fields.</>,
        "next_step": <>During step 2, you'll receive <b>Question Suggestions</b> made by MedGemma.</>
    },
    2: {
        "description": <>Ask the <b>Questions</b> returned by MedGemma ​​that you deem necessary for patient and write down the answers. Some additional information obtained by MedGemma ​​can be accessed by clicking the arrow in the upper corner of each question.</>,
        "next_step": <>During step 3, you'll receive <b>Suggestions</b> based on the patient's condition returned by MedGemma.</>
    },
    3: {
        "description": <>Evaluate the MedGemma <b>Suggestions</b> regarding the patient's condition and context critically, modifying, writing, or deleting content as needed.</>,
        "next_step": <>Finalize the triage by adding the risk classification related to the patient's observed condition.</>
    }
}

export default function StepSection(params: stepsectionparams)
{   

    const step_num = params.currentStep as keyof typeof CONTENT ?? 0;

    return <SidePanel position="right">
        <div className={styles.step}>
            <div className={styles.step}>{step_num}</div>
            <div className={styles.blueline}></div>
        </div>
        <h1>Step {step_num}</h1>
        <div>
            {CONTENT[step_num].description}
        </div>
        <div className={styles.blueline}></div>
        <div>
            {CONTENT[step_num].next_step}
        </div>
    </SidePanel>
}