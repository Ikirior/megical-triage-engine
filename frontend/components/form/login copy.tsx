'use server';

import getTokenHeaderValue from "@/utils/getTokenHeader";
import ResponseManager, { responseManagerResponse } from "@/utils/responsemanager";
import { decode } from "jsonwebtoken";
import { cookies } from "next/headers";
import { redirect } from "next/navigation";

async function getUser()
{
    const cookiesObj = await cookies();
    const token = cookiesObj.get('session_token');
    if(token)
    {
        type decoded = {id: string}
        const tokenContent = decode(token.value) as decoded;

        console.log(tokenContent);
        /*
        const userInfo = (await fetch(`http://backend_server:3001/users/${tokenContent.id}`, {
            "method": "DELETE",
            "headers": {
                "Authorization": await getTokenHeaderValue(),
                'Content-Type': 'application/json'
            }
        })).json()
        */

        return {};
    }
        return {};
}

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
        
        const userInfo = await getUser();
        //cookies_data.set('username', userInfo.username)
        //const res = NextResponse.next();
        //console.log((await headers()).get('referer'))

        redirect('/');
    }

    return resMan;
}