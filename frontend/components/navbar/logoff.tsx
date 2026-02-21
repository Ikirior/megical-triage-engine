'use server';

import { cookies } from "next/headers";
import { redirect } from "next/navigation";

export default async function logoff()
{
    const cookiesObj = await cookies();
    cookiesObj.delete('session_token');
    cookiesObj.delete('username');
    redirect('/');
}