'use server';

import getTokenHeaderValue from "@/utils/getTokenHeader";
import ResponseManager, { responseManagerResponse } from "@/utils/responsemanager";

export default async function FinishStepThree(initialState: responseManagerResponse, args: FormData) {

    const sheet_id= args.get('sheet_id'); 
    
    const format = {
        "ai_generated_sugestion": args.get('ai_generated_suggestions.VALUE'),
        "risk_classification": args.get('risk.VALUE'),
        "final_nurse_notes": args.get('final_nurse_observations.VALUE')
    }

    let res = await fetch(`http://backend_server:3001/triages/${sheet_id}/phase-three`, {
        "method": "POST",
        "body": JSON.stringify(format),
        "headers": {
            "Authorization": await getTokenHeaderValue(),
            'Content-Type': 'application/json'
        }
    })

   return ResponseManager(res)
}