'use client';
import styles from '@/components/triagesheet/triagesheet.module.css'
import Topic from './topic'
import Field from './field'
import { useEffect, useState } from 'react';
import GetTriageSheet from './getTriageSheet';
import { ServiceSheet } from './types';
import SingleButton from '../singlebutton/singlebutton';
import { MessageCircleQuestionIcon, PlusIcon, Rocket, Send } from 'lucide-react';

type triagesheetparams = {
    "current_sheet_id": string|null
}

export default function TriageSheet(params: triagesheetparams)
{
    const [triageSheet, setTriageSheet] = useState(null as ServiceSheet|null)
    useEffect(() => {
        console.log(params.current_sheet_id);
        if(params.current_sheet_id)
            GetTriageSheet(params.current_sheet_id).then((value) => {
                console.log(value.content);
                setTriageSheet(value.content);
            })
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