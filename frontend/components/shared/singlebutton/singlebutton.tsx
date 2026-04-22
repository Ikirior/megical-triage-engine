'use client';

import styles from "@/components/shared/singlebutton/singlebutton.module.css"
import { responseManagerResponse } from "@/utils/responsemanager";
import { JSX, MouseEventHandler, useActionState } from "react"
import Message from "../messages/msg";
import LoadingOverlay from "./loading";
import { Loader2Icon } from "lucide-react";

type singlebutton_params = {
    icon: any,
    backgroudColor?: string,
    /**
     * Button text.
     */
    text?: string,
    /**
     * Client function or server action to execute. This does not come with automatic error display.
     */
    action?: Function,
    /**
     * Is this a submit button for a Form element?
     */
    submit?: boolean,
    /**
     * A function that runs a form action associated with a server request. Automatically exposes an error if it is returned by the ResponseManager.
     * > Warning: this function requires the returned value to come from `ResponseManager`. Therefore, only use this if you are going to make a request to the backend server.
     * > Warning: to submit, make sure submit=true.
     * @param initialState Its first value.
     * @param args FormData.
     * @returns 
     */
    formAction?: (initialState:responseManagerResponse, args:FormData) => Promise<responseManagerResponse>,
    
    /**
     * Text to display on hover.
     */
    title?: string,

    /**
     * Form function.
     * @param args 
     * @returns 
     */
    clientFormFunction?: (args: FormData) => void,
    /**
     * Switch to an alternative style.
     */
    alternativeStyle?: boolean,
    /**
     * If true, covers the screen during loading, to avoid any other actions.
     */
    criticalOverlay?: boolean,
    /**
     * If set, it is shown upon form action success.
     */
    successMessage?: string
}

export default function SingleButton(params: singlebutton_params)
{
    const error_msg:JSX.Element[] = [];
    let action_func = undefined
    let loading = false;
    let icon:JSX.Element = params.icon;
    let showSuccessMessage = false;
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
            else if(state.success && params.successMessage)
                showSuccessMessage = true;
        
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
            {showSuccessMessage && params.successMessage && !loading && <Message backgroundColor="rgb(146, 255, 179)" text={params.successMessage}/>}
            {
                (loading && params.criticalOverlay) &&
                <LoadingOverlay/>
            }
            <button aria-busy={loading} 
                    disabled={loading} 
                    className={params.alternativeStyle ? styles.alt_button : styles.button} 
                    style={styles_obj} title={params?.title} 
                    formAction={action_func ?? params.clientFormFunction} 
                    onClick={params?.action as MouseEventHandler<HTMLButtonElement>} 
                    type={params.submit ? 'submit' : 'button'} 
                    value='button'>
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