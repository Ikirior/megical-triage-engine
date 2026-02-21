'use server';

import Message from "@/components/messages/msg";
import { cookies, headers } from "next/headers";
import { redirect } from "next/navigation";
import { JSX } from "react";

export type responseManagerResponse = {
    success: boolean,
    msg: JSX.Element|null,
    content?: any
}

/**
 * Function used to handle responses from the backend server.
 * Wraps responses, for convenience, in a way that redirects to a login page if unauthorized.
 * Also exposes other errors.
 * If it returns anything at all, it will be a msg component to be rendered or the .
 */
export default async function ResponseManager(res: Response) : Promise<responseManagerResponse> {

    console.log("RESPONSE RESULT", res.status)
    if(res.ok)
    {
        let content = await res.text();
        try
        {
            content = JSON.parse(content);
        }
        catch(exception)
        {
            console.log('Not valid JSON: ', exception)
        }

        return {
            "success": true,
            "msg": null,
            "content": content
        };
    }
    else if(res.status == 401)
    {
        console.log('<!> Response manager redicted route for unauthorized access.');
        redirect('/login/');
    }
    else
    {
        const json_content = await res.json();
        return {"success": false, "msg": <Message backgroundColor="red" text={json_content.detail}/>}
    }
}