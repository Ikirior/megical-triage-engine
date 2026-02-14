import { colors } from "@/utils"
import styles from "@/components/singlebutton/singlebutton.module.css"

type singlebutton_params = {
    icon: any
}

export default function SingleButton(params: singlebutton_params)
{
    return (
        <button className={styles.button}>
            {params.icon}
        </button>
    )
}