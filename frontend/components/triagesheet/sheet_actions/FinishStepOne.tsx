'use server';

import getTokenHeaderValue from "@/utils/getTokenHeader";
import ResponseManager from "@/utils/responsemanager";

export default async function FinishStepOne(sheet_id: string) {

    const format = {
    "vitals": {
        "systolic_bp": 0,
        "diastolic_bp": 0,
        "heart_rate": 0,
        "temperature": 0,
        "oxygen_saturation": 100,
        "extras": {
        "additionalProp1": {}
        }
    },
    "nurse_initial_observations": "string"
    }

    let res = await fetch(`http://backend_server:3001/triages/${sheet_id}/phase-one`, {
        "method": "POST",
        "headers": {
            "Authorization": await getTokenHeaderValue(),
            'Content-Type': 'application/json'
        }
    })

    return ResponseManager(res)
}