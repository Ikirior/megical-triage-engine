'use client';
import { Home, UserCircle2Icon } from "lucide-react"
import Link from "next/link"
import { useState } from "react";
import styles from '@/components/shared/navbar/navbar.module.css'
import logoff from "@/services/navbar/logoff";

export default function UserNav(params: {username: string})
{
    const [open, setOpen] = useState(false);
    return (
        <button className={"flex gap-2 " + styles.userprofile} onClick={()=>{setOpen(!open)}}> 
            <div className={styles.userinfo}>
                <div id="username" className={styles.username}>
                    {params.username} 
                </div>
                <UserCircle2Icon/>
            </div>
            {
                open &&
                <div className={styles.side} onPointerLeave={()=>{setOpen(false)}}>
                    <div>You</div>
                    <div onClick={logoff}>Log Off</div>
                </div>
            }
        </button>
    )
}