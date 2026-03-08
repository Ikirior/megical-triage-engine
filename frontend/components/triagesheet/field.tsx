'use client';

import styles from '@/components/triagesheet/triagesheet.module.css'
import { ArrowDown, ArrowDownIcon, BrainCircuitIcon } from 'lucide-react';
import { useState } from 'react';
import { investigation_qa_obj } from './types';
import Markdown from 'react-markdown';

type field_params = {
    name: string,
    value: number|string|null|undefined,
    key_name: string,
    readonly?: [boolean, boolean],

    textarea?: boolean
    number?: boolean,
    current_sheet_id: string,
    ai_info?: investigation_qa_obj,
    selector?: string[]
}

export default function Field(params: field_params)
{
    // Showing the reasoning popup
    const [showReasoning, setShowReasoning] = useState(false);

    // State used to allow for markdown editing
    const [markdownProp, setMarkdownProp] = useState({
        'content': params.value?.toString() ?? '',
        'editingActive': false
    });

    // params.name is an identifier for the form submission

    let new_key_name = params.name + '.KEY';
    let new_value_name = params.name + '.VALUE';

    // Elements _______________________________________________________

    // Selector ------------------
    if(params.selector)
        return <div className={styles.field} style={{width: "100%"}}>
            <div>{params.key_name}</div>
            <select name={new_value_name}  defaultValue={params.value?.toString()} disabled={params.readonly?.at(0) || params.readonly?.at(1)}>
                {params.selector.map((optString, i)=><option key={'option' + i} value={optString.toLocaleLowerCase()}>{optString}</option> )}
            </select>
        </div>

    // Textarea ------------------
    if(params.textarea)
    {
        const readOnly = params.readonly?.at(0) || params.readonly?.at(1)
        const displayEditingView = !markdownProp.editingActive || readOnly
        let custom_styles = {}
    
        if(displayEditingView) custom_styles = {visibility: 'hidden', position: 'fixed'}
        
        const textAreaElement = 
        <textarea 
            name={new_value_name} 
            className={styles.textarea} 
            id="" 
            readOnly={readOnly} 
            defaultValue={markdownProp.content} 
            style={custom_styles}   
            onChange={(e)=>{setMarkdownProp({...markdownProp, content: e.target.value})}}
            onBlur={(e)=>{setMarkdownProp({...markdownProp, editingActive: false})}}
            ></textarea>
        
        // If the field is read-only or editingActive is true, render it as markdown.
        if(displayEditingView)
        {
            return <>
                {textAreaElement}
                <div className={styles.textarea} onClick={() => {setMarkdownProp({...markdownProp, editingActive: true})}}>
                    <Markdown>
                        {`${markdownProp.content}`}
                    </Markdown>
                </div>
                
            </>
        }
        else return textAreaElement
    }

    // Standard Field ------------
    return (
        <div className={params.ai_info ? styles.ai_question : styles.field} key={new_key_name + params.current_sheet_id}>
            
            {
                params.ai_info && <>
                    <input style={{display: 'none'}} name={params.name + '.ID'} type='text' defaultValue={params.ai_info.question_id} readOnly/>
                    <input style={{display: 'none'}} name={params.name + '.REASON'} type='text' defaultValue={params.ai_info.ai_reasoning} readOnly/>
                    <button className={styles.ai_button} onClick={(e) => {e.preventDefault(); setShowReasoning(!showReasoning)}}><ArrowDownIcon/></button>
                    {showReasoning && <div className={styles.ai_reasoning}>{params.ai_info.ai_reasoning}</div>}
                </>
            }
            <input name={new_key_name} type='text' defaultValue={params.key_name} readOnly={params.readonly?.at(0)}/>
            <input name={new_value_name} type={params.number ? 'number' : 'text'} defaultValue={params.value ?? ''} readOnly={params.readonly?.at(1)} required/>
        </div>
    )
}