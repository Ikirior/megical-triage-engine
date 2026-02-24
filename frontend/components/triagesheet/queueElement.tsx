'use client';

import styles from '@/components/triagesheet/triagesheet.module.css'
import { queueObj, STEP_MAPPING } from './types';
import SingleButton from '../singlebutton/singlebutton';
import { CheckSquare2Icon, PlaySquareIcon, SquareArrowUpRight } from 'lucide-react';


type queueElementsParams = {
    value: queueObj,
    currentSheetId: string|null,
    setStep: Function,
    setCurrentPatientInfo: Function,
    index: number,
    continueEditing?: boolean,
    user_role: "nurse"|"doctor"

}

export default function QueueElement(params: queueElementsParams)
{

    const patientFormFunction = async (args:FormData) => {
                                                const sheet_id = args.get('sheet_id') ?? args.get('id');
                                                params.setCurrentPatientInfo({"sheet_id": sheet_id, "patient_id": params.value.patient_id});
                                            }

    return <div className={styles.queueObj}>
                            <div>{params.index+1}</div>
                            <div>
                                <div>{params.value.patient_name}</div>
                                <div className={styles.queueObj_date}>{new Date(params.value.arrival_time ?? params.value.waiting_since).toLocaleTimeString()}</div>
                            </div>
                            <form>
                                
                                <input value={params.value.sheet_id} name="sheet_id" readOnly style={{display: 'none'}}/>
                                {

                                    params.value.sheet_id != params.currentSheetId ?
                                    <SingleButton 
                                        icon={params.continueEditing ? <PlaySquareIcon/> : <SquareArrowUpRight/>} 
                                        clientFormFunction={patientFormFunction} 
                                        submit={true} 
                                        backgroudColor="transparent" 
                                        title={params.continueEditing ? "Continue Patient Triage" : "Start Patient Triage"}
                                    />
                                        :
                                        <CheckSquare2Icon color="green"/>
                                    


                                }

                            </form>
                        </div>
}