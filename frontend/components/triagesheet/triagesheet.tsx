'use client';
import styles from '@/components/triagesheet/triagesheet.module.css'
import Topic from './topic'
import Field from './field'
import { useEffect, useState } from 'react';
import StartTriageSheet from './startTriageSheet';
import { ServiceSheet, status, status_nums, STEP_MAPPING } from './types';
import SingleButton from '../singlebutton/singlebutton';
import { MessageCircleQuestionIcon, PlusIcon, Rocket, Send } from 'lucide-react';
import GetTriageSheet from './getTriageSheet';

type triagesheetparams = {
    "current_sheet_id": string|null,
    "current_step": status_nums,
    "set_step": Function
}

export default function TriageSheet(params: triagesheetparams)
{
    const [triageSheet, setTriageSheet] = useState(null as ServiceSheet|null)

    // If the patient id changes, reload the page with the current content you may find.
    useEffect(() => {
        console.log('Updating Service Sheet for ', params.current_sheet_id);
        
            const loadTriageSheet = async () =>
            {
                if(params.current_sheet_id)
                {
                    let updated_sheet = undefined;

                    // If it's a new patient, start the triage
                    if(params.current_step == 0)
                    {
                        updated_sheet = (await StartTriageSheet(params.current_sheet_id)).content;
                        console.log('Starting: ', updated_sheet);
                    }

                    // Otherwise, update it to reflect what was last done. If the received value is undefined, try loading it from its ID.
                    if(updated_sheet == undefined)
                    {
                        updated_sheet = (await GetTriageSheet(params.current_sheet_id)).content;
                        console.log('Resuming: ', updated_sheet);
                    }

                    // Set Sheet
                    if(updated_sheet)
                    {
                        setTriageSheet(updated_sheet);
                        params.set_step(STEP_MAPPING[updated_sheet.status as status])
                    }
                    setTriageSheet(null);
                }
            }
            loadTriageSheet();

    }, [params.current_sheet_id])

    // The ServiceSheet is one huge form.
    // It is divided into sections, treated by the form with a fieldset.
    // Fieldsets can be disabled according to the step. 
    // Each field is composed of a key (name) and its associated value.
    // In HTML, they are set as 'keyName' for the keys and as 'keyName.Value' for the value.
    // The object sent to the backend server will feature an object following

    return (
        <form className={styles.sheet}>
            <h1 style={{'fontSize': "1.6em", "marginLeft": "4px"}}>Triage Sheet</h1>
            <Topic name="Identification">
                <Field name='ID' value={triageSheet?.patient.name ?? ""}/>
                <Field name='ID' value='Will Rodriguez'/>
                <Field name='ID' value='Will Rodriguez'/>
                <Field name='ID' value='Will Rodriguez'/>
                <Field name='ID' value='Will Rodriguez'/>
            </Topic>
            <Topic name="Essentials">
                <Field name='ID' value='Will Rodriguez'/>
                <Field name='ID' value='Will Rodriguez'/>    
            </Topic>

            <Topic name="Observations">
                <Field name='ID' value='Will Rodriguez'/> 
            </Topic>
            
            <Topic name="Complementary Analysis with AI">

            </Topic>

            <nav id="form-actions" className={[styles.actions, styles.form_actions].join(' ')}>
                <SingleButton icon={<MessageCircleQuestionIcon/>} text="Generate Questions" alternativeStyle/>
                <SingleButton icon={<Rocket/>} text="Generate Analysis"  alternativeStyle/>
                <SingleButton icon={<Send/>} text="Send to Queue"  alternativeStyle/>

                <div className={styles.plus_button}>
                    <SingleButton icon={<PlusIcon/>}/>
                </div>
            </nav>
        </form>
    )
}