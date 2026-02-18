import styles from "@/components/majorbutton/majorbutton.module.css"

type majorbutton_params = {
    icon: any,
    content: string
}

export default function MajorButton(params: majorbutton_params)
{
    return (
        <button className={styles.button}>
            <div className={styles.figure}>
                {params.icon}
            </div>
            <div className={styles.text}>{params.content}</div>
        </button>
    )
}