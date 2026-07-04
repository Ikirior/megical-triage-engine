'use server';

import getTokenHeaderValue from "@/utils/getTokenHeader";
import ResponseManager, { responseManagerResponse } from "@/utils/responsemanager";

export default async function SendToQueue(initialState:responseManagerResponse, params: FormData) {

    const payload = {
        "patient_id": params.get('_id'),
    }

    const addReq = await fetch(`http://backend_server:3001/patients/${payload.patient_id}/triage`, {
        "method": "POST",
        "body": JSON.stringify(payload),
        "headers": {
            "Authorization": await getTokenHeaderValue(),
            'Content-Type': 'application/json'
        }
    })

    return ResponseManager(addReq)
}