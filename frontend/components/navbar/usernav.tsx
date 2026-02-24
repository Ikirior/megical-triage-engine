'use client';
import { Home, UserCircle2Icon } from "lucide-react"
import Link from "next/link"
import { useState } from "react";
import styles from '@/components/navbar/navbar.module.css'
import logoff from "./logoff";

export default function UserNav(params: {username: string})
{
    const [open, setOpen] = useState(false);
    return (
        <button className={"flex gap-2 " + styles.userprofile} onClick={()=>{setOpen(!open)}}> 
        {params.username} 
        <UserCircle2Icon/>
        
        {
            open &&
            <div className={styles.side}>
                <div onClick={logoff}>Log Off</div>
            </div>
        }

        </button>
    )
}