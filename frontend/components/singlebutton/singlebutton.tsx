'use client';

import styles from "@/components/singlebutton/singlebutton.module.css"
import { MouseEventHandler } from "react"

type singlebutton_params = {
    icon: any,
    backgroudColor?: string,
    text?: string,
    action?: Function
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
        <button className={styles.button} style={styles_obj} onClick={params.action as MouseEventHandler<HTMLButtonElement>}>
            {params.icon}
            {params.text}
        </button>
    )
}