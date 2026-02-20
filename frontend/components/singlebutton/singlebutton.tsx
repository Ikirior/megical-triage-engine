'use client';

import styles from "@/components/singlebutton/singlebutton.module.css"
import { MouseEventHandler } from "react"

type singlebutton_params = {
    icon: any,
    backgroudColor?: string,
    text?: string,
    action?: Function,
    submit?: boolean,
    formAction?: (args:FormData) => void,
    title?: string
}

export default function SingleButton(params: singlebutton_params)
{
    let styles_obj = {}

    if(params.backgroudColor)
        {
            styles_obj = {
                "backgroundColor": params.backgroudColor
            }
        }

    return (
        <button className={styles.button} style={styles_obj} title={params?.title} formAction={params?.formAction} onClick={params?.action as MouseEventHandler<HTMLButtonElement>} type={params.submit ? 'submit' : 'button'} value='button'>
            {params.icon}
            {params.text}
        </button>
    )
}