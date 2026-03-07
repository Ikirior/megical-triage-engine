'use client';

import styles from "@/components/singlebutton/singlebutton.module.css"
import { responseManagerResponse } from "@/utils/responsemanager";
import { JSX, MouseEventHandler, useActionState } from "react"
import Message from "../messages/msg";
import LoadingOverlay from "./loading";
import { Loader2Icon } from "lucide-react";

type singlebutton_params = {
    icon: any,
    backgroudColor?: string,
    text?: string,
    action?: Function,
    submit?: boolean,
    formAction?: (initialState:responseManagerResponse, args:FormData) => Promise<responseManagerResponse>,
    title?: string,
    clientFormFunction?: (args: FormData) => void,
    alternativeStyle?: boolean,
    criticalOverlay?: boolean 
}

export default function SingleButton(params: singlebutton_params)
{
    const error_msg:JSX.Element[] = [];
    let action_func = undefined
    let loading = false;
    let icon:JSX.Element = params.icon
    if(params?.formAction)
        {
            const [state, action, isPending] = useActionState(params.formAction, {"msg": null, "success": false})
            action_func = action;
            loading = isPending;

            if(loading && !params.criticalOverlay)
            {
                icon = <Loader2Icon color={icon.props.color ?? 'black'} className={styles.load_anim}/>
            }

            if(!state.success && state.msg)
                error_msg.push(state.msg)
        }
    
    let styles_obj = {}
    if(params.backgroudColor)
        {
            styles_obj = {
                "backgroundColor": params.backgroudColor
            }
        }

    return (
        <>
            {...error_msg}
            {
                (loading && params.criticalOverlay) &&
                <LoadingOverlay/>
            }
            <button aria-busy={loading} disabled={loading} className={params.alternativeStyle ? styles.alt_button : styles.button} style={styles_obj} title={params?.title} formAction={action_func ?? params.clientFormFunction} onClick={params?.action as MouseEventHandler<HTMLButtonElement>} type={params.submit ? 'submit' : 'button'} value='button'>
                
                {
                    !params.alternativeStyle ?
                    <>
                        {icon}
                        {params.text}
                    </> :
                    <>
                        <div className={styles.alt_figure}>
                            {icon}
                        </div>
                        <div className={styles.alt_text}>{params.text}</div>
                    </>

                }

            </button>
        </>
    )
}