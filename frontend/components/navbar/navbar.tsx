import styles from '@/components/navbar/navbar.module.css'
import { Home, UserCircle2Icon } from "lucide-react"
import Link from "next/link"



export default function Navbar()
{
    return (
        <nav className={styles.nav}>
            <Link className="flex gap-2" href="/"><Home/> Home</Link>
            <Link className="flex gap-2" href="/login">Sign In <UserCircle2Icon/></Link>
        </nav>
    )
}