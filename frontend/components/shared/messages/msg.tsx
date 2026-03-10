'use client';

import styles from '@/components/shared/messages/msg.module.css'
import { MessageSquareWarningIcon, X } from "lucide-react"
import { useState } from 'react';


type messageParams = {
    backgroundColor: string,
    text: string
}

export default function Message(params: messageParams)
{
    const [state, setState] = useState({'appear': true});

    return (
        state.appear && 
        <aside className={styles.msg} style={{backgroundColor: params.backgroundColor}}>
            <div className={styles.msg_icon}>
                <MessageSquareWarningIcon/> 
                <button onClick={() => {setState({appear: false})}} style={{cursor: "pointer"}}><X size="1em"/></button>
            </div>
            <div className={styles.msg_content}>{params.text}</div>
        </aside>
    )
}