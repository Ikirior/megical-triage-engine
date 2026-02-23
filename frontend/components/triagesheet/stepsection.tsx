'use client';
import styles from '@/components/triagesheet/triagesheet.module.css'
import SidePanel from "./sidepanel";


type stepsectionparams = {
    currentStep: null|1|2|3
}

export default function StepSection(params: stepsectionparams)
{   
    return <SidePanel position="right">
        <div className={styles.step}>
            <div className={styles.step}>1</div>
            <div className={styles.blueline}></div>
        </div>
        <h1>Step {params.currentStep}</h1>
        <div>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Ex quae nihil voluptatem, eaque facilis maxime quibusdam esse perferendis nostrum non ut ab eius iste quis laudantium ratione assumenda magni fugiat!
        </div>
        <div className={styles.blueline}></div>
        <div>
            Lorem ipsum dolor sit amet consectetur, adipisicing elit. Unde mollitia deleniti architecto nesciunt laboriosam, nulla dolor totam tempore explicabo dolores natus vero veritatis nam id eligendi quis eaque sunt! Deserunt?
        </div>
    </SidePanel>
}