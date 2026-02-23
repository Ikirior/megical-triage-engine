'use client';
import React, { JSX, useState } from "react";
import styles from '@/components/triagesheet/triagesheet.module.css'
import { ArrowLeft, ArrowRight} from "lucide-react";


type triagequeueparams = {
    children: React.ReactNode,
    position: "left"|"right",
    text?: string
}

export default function SidePanel(params: triagequeueparams,)
{

    const [panelOpen, setOpen] = useState(true);

    const content_classes = [
        styles.queue_panel_content,
    ]
    if(!panelOpen) content_classes.push(styles.queue_content_closed)

    const panel_classes = [
        styles.queue_panel,
        params.position == 'right' ? styles.queue_panel_right : styles.queue_panel_left
    ]

    const arrow = params.position == 'right' ? <ArrowRight color="white"/>:  <ArrowLeft color="white"/>
    const content_section = <div className={content_classes.join(' ')}>
            <h1 style={{fontSize: "1.3em"}}>{params.text}</h1>
            {
                params.children
            }
        </div>;
    
    return <div className={panel_classes.join(' ')}>
        {params.position == 'left' && content_section}
        <div className={styles.shift_button} onClick={() => {setOpen(!panelOpen)}}>
            <button 
            className={!panelOpen ? styles.shift_button_closed : ""}
            > {arrow} </button>
        </div>
        {params.position == 'right' && content_section}
    </div>
}