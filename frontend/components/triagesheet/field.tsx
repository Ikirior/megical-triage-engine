import styles from '@/components/triagesheet/triagesheet.module.css'

type field_params = {
    name: string,
    value: string
}

export default function Field(params: field_params)
{
    return (
        <div className={styles.field}>
            <div>{params.name}</div>
            <div>{params.value}</div>
        </div>
    )
}