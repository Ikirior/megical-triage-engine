'use client';
import styles from '@/components/triagesheet/triagesheet.module.css'
import Topic from './topic'
import Field from './field'
import { JSX, useEffect, useState } from 'react';
import StartTriageSheet from './startTriageSheet';
import { ServiceSheet, status, status_nums, STEP_MAPPING } from './types';
import SingleButton from '../singlebutton/singlebutton';
import { MessageCircleQuestionIcon, PlusIcon, Rocket, Send } from 'lucide-react';
import GetTriageSheet from './getTriageSheet';
import FinishStepOne from './sheet_actions/FinishStepOne';
import FinishStepTwo from './sheet_actions/FinishStepTwo';
import FinishStepThree from './sheet_actions/FinishStepThree';
import Finish from '../doctorpanel/finish';
import { responseManagerResponse } from '@/utils/responsemanager';
import StartDoctorSheet from '../doctorpanel/startDoctorSheet';
import Markdown from 'react-markdown';
import GetDoctorSheet from '../doctorpanel/getDoctorSheet';

type triagesheetparams = {
    "current_sheet_id": string|null,
    "current_step": status_nums,
    "set_step": Function,
    "user_role": "nurse"|"doctor"
}

export default function TriageSheet(params: triagesheetparams)
{
    const [triageSheet, setTriageSheet] = useState(null as ServiceSheet|null);
    const [extraVitalFields, setExtraVitalFields] = useState([] as JSX.Element[]);

    const loadTriageSheet = () => {
        console.log('Updating Service Sheet for ', params.current_sheet_id);
        
            const loadTriageSheet = async () =>
            {
                if(params.current_sheet_id)
                {
                    let updated_sheet:ServiceSheet|undefined = undefined;

                    // If it's a new patient, start the triage
                    if(params.current_step == 0)
                    {
                        updated_sheet = params.user_role == 'nurse' ? (await StartTriageSheet(params.current_sheet_id)).content : (await StartDoctorSheet(params.current_sheet_id)).content;

                    }

                    // Otherwise, update it to reflect what was last done. If the received value is undefined, try loading it from its ID.
                    if(updated_sheet == undefined)
                    {
                        if(params.user_role == 'nurse')
                            updated_sheet = (await GetTriageSheet(params.current_sheet_id)).content;
                        else if(params.user_role == 'doctor')
                            updated_sheet = (await GetDoctorSheet(params.current_sheet_id)).content
                    }

                    // Set Sheet
                    if(updated_sheet)
                    {
                        // Loading Extra Questions
                        if(updated_sheet.triage_data?.vitals.extras){
                            const extras_obj = updated_sheet.triage_data?.vitals.extras as any;
                            const extra_elements = Object.keys(extras_obj).map((dict_key, i)=>
                                <Field name={'EXTRA-' + extraVitalFields.length} key_name={dict_key} current_sheet_id={params.current_sheet_id ?? ''} value={extras_obj[dict_key]}></Field>)
                            
                            setExtraVitalFields(extra_elements);
                        }
                        else setExtraVitalFields([]);

                        console.log(updated_sheet)
                        setTriageSheet({...updated_sheet});
                        params.set_step(STEP_MAPPING[updated_sheet.status as status])
                    }
                    else setTriageSheet(null);
                }
            }
            loadTriageSheet();

    };

    // If the patient id changes, reload the page with the current content you may find.
    useEffect(loadTriageSheet, [params.current_sheet_id]);

    // Temporary Solution (due to time contraint)
    const ReloadWrapper = (callback: (initialState: responseManagerResponse, args: FormData) => Promise<responseManagerResponse>) =>{
        return (value:FormData) => callback({} as responseManagerResponse, value).then(()=>{loadTriageSheet();})
    }
    
    // The ServiceSheet is one huge form.
    // It is divided into sections, treated by the form with a fieldset.
    // Fieldsets can be disabled according to the step. 
    // Each field is composed of a key (name) and its associated value (except for text areas).
    
    // Field:
    // name: identifier for the form submission. Not intereferred by value.
    //       Any extra fields will be named EXTRA-{index}.KEY or EXTRA-{index}.VALUE.
    //       Preset fields will be named {name}.KEY and {name}.VALUE.
    // value: what to display for the value.
    // key_name: what to display as the key name.

    if(triageSheet == null)
        return <form className={styles.sheet}></form>;

    return <form className={styles.sheet}>
            <h1 style={{'fontSize': "1.6em", "marginLeft": "4px"}}>Triage Sheet</h1>
                <div style={{display: 'none'}}><input name='sheet_id' defaultValue={params.current_sheet_id ?? ''} readOnly></input></div>
            <Topic name="Identification" disabled>
                <Field current_sheet_id={triageSheet.id} name='name' key_name='Name' value={triageSheet.patient.name}/>
                <Field current_sheet_id={triageSheet.id} name='cpf' key_name='CPF' value={triageSheet.patient.cpf}/>
                <Field current_sheet_id={triageSheet.id} name='rg' key_name='RG' value={triageSheet.patient.rg}/>
                <Field current_sheet_id={triageSheet.id} name='companion' key_name='Companion?' value={triageSheet.patient.companion ? 'Yes' : 'No'}/>
                <Field current_sheet_id={triageSheet.id} name='address' key_name='Address' value={triageSheet.patient.address}/>
                <Field current_sheet_id={triageSheet.id} name='birth_date' key_name='Birth Date' value={triageSheet.patient.birth_date} />
                <Field current_sheet_id={triageSheet.id} name='sex' key_name='Sex' value={triageSheet.patient.sex}/>
                <Field current_sheet_id={triageSheet.id} name='phone_number' key_name='Phone Number' value={triageSheet.patient.phone_num}/>
            </Topic>
            <Topic name="Essentials" disabled={params.user_role != 'nurse'}>
                <Field current_sheet_id={triageSheet.id} name='systolic_bp' key_name='Systolic BP' number value={triageSheet.triage_data?.vitals.systolic_bp} readonly={[true, false]}/>
                <Field current_sheet_id={triageSheet.id} name='diastolic_bp'key_name='Diastolic BP' number value={triageSheet.triage_data?.vitals.diastolic_bp} readonly={[true, false]}/>
                <Field current_sheet_id={triageSheet.id} name='heart_rate' key_name='Heart Rate' number value={triageSheet.triage_data?.vitals.diastolic_bp} readonly={[true, false]}/>
                <Field current_sheet_id={triageSheet.id} name='temperature' key_name='Temperature' number value={triageSheet.triage_data?.vitals.temperature} readonly={[true, false]}/>
                <Field current_sheet_id={triageSheet.id} name='oxygen_saturation' key_name='Oxygen Saturation' number value={triageSheet.triage_data?.vitals.diastolic_bp} readonly={[true, false]}/>
                {...extraVitalFields}
            </Topic>

            <Topic name="Observations">
                <Field current_sheet_id={triageSheet.id} key_name='Nurse Observations' name='nurse_observations' value={triageSheet.triage_data?.nurse_initial_observations} textarea readonly={params.user_role != 'nurse' ? [true, false] : [true, true]}/>
            </Topic>
            
            <Topic name="Complementary Analysis with AI">
                {triageSheet.triage_data?.investigation_qa?.map(((ai_question, i) => 
                    <Field key={'ai_question_' + i} ai_info={ai_question} current_sheet_id={triageSheet.id} name={'AI-'+i} key_name={ai_question.question_text} value={ai_question.patient_answer} readonly={params.user_role == 'nurse' ? [true, false] : [true, true]}/>
                ))}
            </Topic>

            <Topic name="AI Suggestions">
                <Field current_sheet_id={triageSheet.id} key_name='ai_generated_suggestions' name='ai_generated_suggestions' value={triageSheet.triage_data?.ai_generated_suggestion} readonly={params.current_step != 3 ? [true, true] : [false, false]} textarea/>
            </Topic>

            <Topic name="Final Observations">
                <Field current_sheet_id={triageSheet.id} key_name='Final Nurse Observations' name='final_nurse_observations' value={triageSheet.triage_data?.final_nurse_notes} readonly={params.current_step != 3 ? [true, true] : [false, false]} textarea/>
            </Topic>

            <Topic name="Risk Evaluation">
                <Field current_sheet_id={triageSheet.id} name='risk' key_name='Risk' value={triageSheet.triage_data?.risk_classification} selector={["Azul", "Verde", "Amarelo", "Laranja", "Vermelho"]} readonly={params.current_step != 3 ? [true, true] : [false, false]}/>
            </Topic>


            <Topic name="AI Pre-Consultation Summary">
                <Field current_sheet_id={triageSheet.id} key_name='ai_pre_consultation_summary' name='ai_pre_consultation_summary' value={triageSheet.doctor_data?.ai_pre_consultation_summary} readonly={[true, true]} textarea/>
            </Topic>

            <Topic name="Doctor Notes">
                <Field current_sheet_id={triageSheet.id} key_name='Doctor Notes' name='doctor_notes' value={triageSheet.doctor_data?.doctor_notes} textarea readonly={params.user_role == 'doctor' ? [false, false] : [true, true]}/>
            </Topic>

            <Topic name="Prescription">
                <Field current_sheet_id={triageSheet.id} key_name='prescription' name='prescription' value={triageSheet.doctor_data?.prescription} textarea readonly={params.user_role == 'doctor' ? [false, false] : [true, true]}/>
            </Topic>

            <nav id="form-actions" className={[styles.actions, styles.form_actions].join(' ')}>
                {
                    params.user_role == 'nurse' && params.current_step == 1 &&
                    <>
                        <SingleButton icon={<MessageCircleQuestionIcon/>} text="Generate Questions" alternativeStyle clientFormFunction={ReloadWrapper(FinishStepOne)} submit/>
                        <div className={styles.plus_button}>
                            <SingleButton icon={<PlusIcon/>} action={() => {
                                setExtraVitalFields([...extraVitalFields, <Field name={'EXTRA-' + extraVitalFields.length} key_name='New Field' current_sheet_id={params.current_sheet_id ?? ''} value='' readonly={params.user_role == 'nurse' && params.current_step == 1 ? [false, false] : [true, true]}></Field>])
                            }}/>
                        </div>
                    </>
                }
                {
                    params.user_role == 'nurse' && params.current_step == 2 &&
                    <>
                        <SingleButton icon={<Rocket/>} text="Generate Analysis"  alternativeStyle clientFormFunction={ReloadWrapper(FinishStepTwo)} submit criticalOverlay/>
                    </>
                }
                {
                    params.user_role == 'nurse' && params.current_step == 3 &&
                    <>
                        <SingleButton icon={<Send/>} text="Send to Queue"  alternativeStyle clientFormFunction={ReloadWrapper(FinishStepThree)} submit criticalOverlay/>
                    </>
                }
                {
                    params.user_role == 'doctor' &&
                    <>
                        <SingleButton icon={<Send/>} text="Finish"  alternativeStyle clientFormFunction={ReloadWrapper(Finish)} submit criticalOverlay/>
                    </>
                }

            </nav>
        </form>
}