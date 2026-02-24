'use server';

import getTokenHeaderValue from "@/utils/getTokenHeader";
import ResponseManager, { responseManagerResponse } from "@/utils/responsemanager";
import { investigation_qa_obj } from "../types";

export default async function FinishStepTwo(initialState: responseManagerResponse, args: FormData) {

    const sheet_id =args.get('sheet_id'); 
    const args_keys = args.keys()
    const investigation_qa = [] as investigation_qa_obj[];
    for(let key of args_keys)
    {
        if(key.startsWith('AI-') && key.endsWith('.VALUE'))
        {
            const name = key.match(/AI-\d+/)?.[0]
            const value = args.get(name + '.VALUE')?.toString();
            const key_name = args.get(name + '.KEY')?.toString() ?? '';
            const id = args.get(name + '.ID')?.toString() ?? '';
            const reasoning = args.get(name + '.REASON')?.toString() ?? '';
            investigation_qa.push({
                "question_text": key_name ?? '',
                "patient_answer": value ?? '',
                "ai_reasoning": reasoning,
                "question_id": id
                
            });
        }
    }
    
    const format = {
        "investigation_qa": investigation_qa
    }

    let res = await fetch(`http://backend_server:3001/triages/${sheet_id}/phase-two`, {
        "method": "POST",
        "body": JSON.stringify(format),
        "headers": {
            "Authorization": await getTokenHeaderValue(),
            'Content-Type': 'application/json'
        }
    })

   return ResponseManager(res)

}