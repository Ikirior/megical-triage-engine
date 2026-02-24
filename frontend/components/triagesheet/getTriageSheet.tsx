'use server';

import getTokenHeaderValue from "@/utils/getTokenHeader";
import ResponseManager from "@/utils/responsemanager";

export default async function GetTriageSheet(sheet_id: string) {

    let res = await fetch(`http://backend_server:3001/triages/${sheet_id}/session`, {
        "headers": {
            "Authorization": await getTokenHeaderValue(),
            'Content-Type': 'application/json'
        }
    })

    return ResponseManager(res)
}