'use server';

import getTokenHeaderValue from "@/utils/getTokenHeader";
import ResponseManager, { responseManagerResponse } from "@/utils/responsemanager";

export default async function FinishStepOne(initialState: responseManagerResponse, args: FormData) {

    const sheet_id =args.get('sheet_id'); 
    const args_keys = args.keys()
    const extras = {} as any
    for(let key of args_keys)
    {
        if(key.startsWith('EXTRA-'))
        {
            const name = key.match(/EXTRA-\d+/)?.[0]
            const value = args.get(name + '.VALUE')?.toString();
            const key_name = args.get(name + '.KEY')?.toString() ?? '';
            extras[key_name] = value; 
        }
    }

    const format = {
        "vitals": {
            "systolic_bp": args.get('systolic_bp.VALUE'),
            "diastolic_bp": args.get('diastolic_bp.VALUE'),
            "heart_rate": args.get('heart_rate.VALUE'),
            "temperature": args.get('temperature.VALUE'),
            "oxygen_saturation": args.get('oxygen_saturation.VALUE'),
            "extras": extras
        },
        "nurse_initial_observations": args.get('nurse_observations.VALUE')
    }

    let res = await fetch(`http://backend_server:3001/triages/${sheet_id}/phase-one`, {
        "method": "POST",
        "body": JSON.stringify(format),
        "headers": {
            "Authorization": await getTokenHeaderValue(),
            'Content-Type': 'application/json'
        }
    })

    return ResponseManager(res)
}