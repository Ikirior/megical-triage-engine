'use server';

import getTokenHeaderValue from "@/utils/getTokenHeader";
import ResponseManager from "@/utils/responsemanager";

export default async function StartTriageSheet(sheet_id: string) {

    let res = await fetch(`http://backend_server:3001/triages/${sheet_id}/start`, {
        "method": "POST",
        "headers": {
            "Authorization": await getTokenHeaderValue(),
            'Content-Type': 'application/json'
        }
    })

    return ResponseManager(res)
}