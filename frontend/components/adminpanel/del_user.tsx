'use server';

import getTokenHeaderValue from "@/utils/getTokenHeader";
import ResponseManager, { responseManagerResponse } from "@/utils/responsemanager";

export default async function DeleteUser(initialState: responseManagerResponse, params: FormData) {

    const delReq = await fetch(`http://backend_server:3001/users/${params.get('id')}`, {
        "method": "DELETE",
        "headers": {
            "Authorization": await getTokenHeaderValue(),
            'Content-Type': 'application/json'
        }
    })
    let res = delReq.status;

    console.log('deleted');
    return ResponseManager(delReq)
}