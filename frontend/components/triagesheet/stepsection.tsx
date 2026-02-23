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
        "next_step": <>During step 2, you'll receive question suggestions made by MedGemma.</>
    },
    2: {
        "description": "",
        "next_step": ""
    },
    3: {
        "description": "",
        "next_step": ""
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