import styles from '@/components/triagesheet/triagesheet.module.css'

type topic_params = {
    name: string,
    children?: React.ReactNode,
    disabled?: boolean
}

export default function Topic(params: topic_params)
{
    return (<>
        <h1 className={styles.topic}>
            {params.name}
        </h1>
        <fieldset className={styles.fieldset} disabled={params.disabled}>
            {params.children}
        </fieldset>
    </>
    )
}