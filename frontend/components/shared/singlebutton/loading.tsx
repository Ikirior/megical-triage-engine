'use client';

import styles from '@/components/shared/singlebutton/singlebutton.module.css'
import { Loader2Icon } from "lucide-react"

export default function LoadingOverlay()
{
    return (
        <div className={styles.loading}>
            <Loader2Icon color='white'/>
        </div>
    )
}