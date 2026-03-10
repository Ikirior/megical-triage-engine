'use server';

import getTokenHeaderValue from "@/utils/getTokenHeader";
import ResponseManager from "@/utils/responsemanager";

export default async function StartDoctorSheet(sheet_id: string) {

    let res = await fetch(`http://backend_server:3001/doctors/${sheet_id}/start`, {
        "method": "POST",
        "headers": {
            "Authorization": await getTokenHeaderValue(),
            'Content-Type': 'application/json'
        }
    })

    return ResponseManager(res)
}