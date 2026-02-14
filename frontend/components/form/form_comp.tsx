import styles from "@/components/form/form_comp.module.css"
import Link from "next/link"

export default function FormComp()
{
    return (
        <form className={styles.login_form} method="POST">

            <h1 style={{"fontSize": "1.6em", "margin": "auto"}}>Login</h1>

            <div className={styles.input_group}>
                <label htmlFor="id">E-mail or Username</label>
                <input type="email" name="id" id="id" />
            </div>

            <div className={styles.input_group}>
                <label htmlFor="password">Password</label>
                <input type="password" name="password" id="password" />
                
                <Link className={styles.sublink} href="/forgotpassword">
                    Forgot my password
                </Link>
            </div>


            <input type="submit"></input>
        </form>
    )
}