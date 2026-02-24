import styles from '@/app/home.module.css'
import { cookies } from 'next/headers';
import { decode } from 'jsonwebtoken';
import SingleButton from '@/components/singlebutton/singlebutton';
import { Link2, LogInIcon } from 'lucide-react';
import Link from 'next/link';

async function getCurrentUserRole()
{
  const cookieObj = await cookies();
  
  if(cookieObj.has('session_token'))
  {
    const token = decode(cookieObj.get('session_token')?.value ?? '') as {sub: string, role: string, exp: number}|null;
    return token?.role;
  }
  return null
}

export default async function Home() {
  
  const role = await getCurrentUserRole();
  const buttonMsg = {
    "admin": ["Load Admin Panel", '/adminpanel'],
    "nurse": ["Load Triage Panel", '/triagepanel'],
    "receptionist": ["Load Patient Registry", '/patientregistry'],
    "doctor": ["Load Doctor Panel", '/doctorpanel']
  }

  return (
    <main className={styles.home}>
        <div>Welcome to</div>
        <h1>Megical Assistant</h1>
        <h2>An application designed to facilitate the management of patients and medical workflow.</h2>
        <div className={styles.buttons}>
          {
            !role &&
            <Link href='/login'><SingleButton text='Sign In' icon={<LogInIcon/>}/></Link>
          }
          {
            role &&
            <Link href={(role ? buttonMsg[role as keyof typeof buttonMsg].at(1) : '/login') ?? '/login'}><SingleButton text={buttonMsg[role as keyof typeof buttonMsg].at(0)} icon={<Link2/>}/></Link>
          }
        </div>
    </main>
  );
}
