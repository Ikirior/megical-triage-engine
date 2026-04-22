'use client';
import { RefreshCcwIcon } from "lucide-react"
import styles from './error.module.css'
import SingleButton from "@/components/shared/singlebutton/singlebutton";

type error_params = {
    error: Error & {digest?: string},
    unstable_retry: () => void 
}

export default function ErrorComponent(params: error_params)
{
    return (
        <div className={styles.error_page}>
            <h1>Ops! Houve um <div style={{color: 'red', display: 'inline'}}>erro</div> no sistema.</h1>
            <h2>Por favor, tente novamente e comunique o erro ao administrador responsável.</h2> 
            <SingleButton icon={<RefreshCcwIcon/>} action={params.unstable_retry} text="Tentar Novamente"/>
        </div>
    )
}