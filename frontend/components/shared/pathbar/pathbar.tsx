import styles from "./pathbar.module.css"

type params_type = {
    path: string;
}

export default function PathBar(params: params_type)
{
    return (
        <nav className={styles.pathbar}>
            {params.path}
        </nav>
    )
}