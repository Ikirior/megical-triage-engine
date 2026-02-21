'use server';

import ResponseManager, { responseManagerResponse } from "@/utils/responsemanager";
import { cookies } from "next/headers";
import { redirect } from "next/navigation";

export default async function Login(initialState: responseManagerResponse, params: FormData) {
    
    console.log(params.get('name'), params.get('password'))
    const payload = {
        "username": params.get('id') as string,
        "password": params.get('password') as string
    }

    const logReq = await fetch(`http://backend_server:3001/auth/login/`, {
        "method": "POST",
        "body": new URLSearchParams(payload)
    })

    const resMan = await ResponseManager(logReq);

    if(resMan.success)
    {
        let logRes = await resMan.content
    
        const cookies_data = await cookies();
    
        cookies_data.set('session_token', logRes.access_token);
        
        //const res = NextResponse.next();
        //console.log((await headers()).get('referer'))

        redirect('/');
    }

    return resMan;
}