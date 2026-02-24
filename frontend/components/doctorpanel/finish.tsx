'use server';

import getTokenHeaderValue from "@/utils/getTokenHeader";
import ResponseManager, { responseManagerResponse } from "@/utils/responsemanager";

export default async function Finish(initialState: responseManagerResponse, args: FormData) {

    const sheet_id =args.get('sheet_id'); 

    const format = {
        "ai_pre_consultation_summary": args.get('ai_pre_consultation_summary.VALUE'),
        "doctor_notes": args.get('doctor_notes.VALUE'),
        "diagnosis_cid": args.get('diagnosis_cod.VALUE'),
        "prescription": args.get('prescription.VALUE')
    }

    let res = await fetch(`http://backend_server:3001/doctors/${sheet_id}/finish`, {
        "method": "POST",
        "body": JSON.stringify(format),
        "headers": {
            "Authorization": await getTokenHeaderValue(),
            'Content-Type': 'application/json'
        }
    })

    return ResponseManager(res)
}