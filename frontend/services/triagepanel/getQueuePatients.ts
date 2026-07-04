'use server';

import getTokenHeaderValue from "@/utils/getTokenHeader";
import ResponseManager from "@/utils/responsemanager";

export default async function GetQeuePatients() {

    let res = await fetch(`http://backend_server:3001/triages/queue`, {
        "headers": {
            "Authorization": await getTokenHeaderValue(),
            'Content-Type': 'application/json'
        }
    })

    return ResponseManager(res)
}