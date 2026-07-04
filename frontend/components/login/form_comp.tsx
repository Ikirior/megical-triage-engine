'use client';
import styles from "@/components/login/form_comp.module.css"
import Link from "next/link"
import Login from "./login"
import { useActionState, useState } from "react";

export default function FormComp()
{
    const [state, action, isPending] = useActionState(Login, {"msg": null, "success": false})
    
    return (
        <form className={styles.login_form} action={action}>

            {!state.success && state.msg}

            <h1 style={{"fontSize": "1.6em", "margin": "auto"}}>Login</h1>

            <div className={styles.input_group}>
                <label htmlFor="id">E-mail or Username</label>
                <input type="text" name="id" id="id" />
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