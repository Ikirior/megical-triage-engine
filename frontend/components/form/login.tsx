'use server';

import getTokenHeaderValue from "@/utils/getTokenHeader";
import ResponseManager, { responseManagerResponse } from "@/utils/responsemanager";
import { decode } from "jsonwebtoken";
import { cookies } from "next/headers";
import { redirect } from "next/navigation";

async function getUser(token:any)
{

    type decoded = {sub: string}

    const tokenContent = decode(token) as decoded;

    const userInfo = await (await fetch(`http://backend_server:3001/users/${tokenContent.sub}`, {
        "headers": {
            "Authorization": await getTokenHeaderValue(),
            'Content-Type': 'application/json'
        }
    })).json();

    return userInfo;
}

export default async function Login(initialState: responseManagerResponse, params: FormData) {

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
        
        const userInfo = await getUser(logRes.access_token);
        cookies_data.set('username', userInfo.name);

        //const res = NextResponse.next();
        //console.log((await headers()).get('referer'))

        if(userInfo.role == 'admin')
            redirect('/adminpanel');
        else if(userInfo.role == 'receptionist')
            redirect('/patientregistry')
        else if(userInfo.role == 'nurse')
            redirect('/triagepanel')
        else
            redirect('/')
    }

    return resMan;
}