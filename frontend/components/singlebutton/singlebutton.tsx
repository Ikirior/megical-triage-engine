import styles from "@/components/singlebutton/singlebutton.module.css"

type singlebutton_params = {
    icon: any,
    backgroudColor?: string,
    text?: string,
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
        <button className={styles.button} style={styles_obj}>
            {params.icon}
            {params.text}
        </button>
    )
}