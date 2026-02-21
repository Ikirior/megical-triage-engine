import styles from '@/components/navbar/navbar.module.css'
import { Home, UserCircle2Icon } from "lucide-react"
import { cookies } from 'next/headers'
import Link from "next/link"
import {decode} from 'jsonwebtoken'
import UserNav from './usernav'

async function getUsername()
{
    const cookiesObj = await cookies();
    const token = cookiesObj.get('session_token')?.value;
    if(token)
    {
        return cookiesObj.get('username')?.value;
    }
    else return undefined;

}

export default async function Navbar()
{

    const username = await getUsername();

    return (
        <nav className={styles.nav}>
            <Link className="flex gap-2 " href="/"><Home/> Home</Link>
            {
                !username ? <Link className="flex gap-2" href="/login">Sign In <UserCircle2Icon/></Link>:
                <UserNav username={username}/>
            }
        </nav>
    )
}