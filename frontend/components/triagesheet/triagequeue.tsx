'use client';
import { useState } from "react";
import styles from '@/components/triagesheet/triagesheet.module.css'
import { ArrowLeft, CheckSquare2Icon, SquareArrowUpRight } from "lucide-react";
import GetQeuePatients from "./getQueuePatients";
import { queueObj } from "./types";
import SingleButton from "../singlebutton/singlebutton";
import SidePanel from "./sidepanel";


type triagequeueparams = {
    setCurrentPatientInfo: Function,
    currentPatientId: string|null,
    setStep: Function,
    queue: queueObj[]
}

export default function TriageQueue(params: triagequeueparams)
{

    return <SidePanel position="left" text="Patient Triage Queue">
        {
            params.queue.length > 0 ?
                <div>
                    {...params.queue.map((value, index) => 
                        <div className={styles.queueObj}>
                            <div>{index+1}</div>
                            <div>
                                <div>{value.patient_name}</div>
                                <div className={styles.queueObj_date}>{new Date(value.arrival_time).toLocaleTimeString()}</div>
                            </div>
                            <form>
                                <input value={value.sheet_id} name="sheet_id" readOnly style={{display: 'none'}}/>
                                {
                                    params.currentPatientId != value.patient_id ?
                                        <SingleButton icon={<SquareArrowUpRight/>} clientFormFunction={
                                            async (args) => {
                                                const sheet_id = args.get('sheet_id');
                                                params.setCurrentPatientInfo({"sheet_id": sheet_id, "patient_id": value.patient_id});
                                                params.setStep(1);
                                            }
                                        } submit={true} backgroudColor="transparent" title="Start User Triage"/>
                                        :
                                        <CheckSquare2Icon color="green"/>
                                }
                            </form>
                        </div>
                    )}
                </div> :
                <div>No users yet in queue!</div>
        }
    </SidePanel>;
}