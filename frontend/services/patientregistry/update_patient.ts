'use server';

import getTokenHeaderValue from "@/utils/getTokenHeader";
import ResponseManager, { responseManagerResponse } from "@/utils/responsemanager";

export default async function UpdatePatient(initialState: responseManagerResponse, params: FormData) {

    let payload = {
        "name": params.get('name'),
        "cpf": params.get('cpf'),
        "rg": params.get('rg'),
        "birth_date": params.get('birth_date'),
        "address": params.get('address'),
        "companion": params.has('companion'),
        "race": params.get('race'),
        "sex": params.get('sex'),
        "phone_num": params.get('phone_num')
    }

    let uptReq = await fetch(`http://backend_server:3001/patients/${params.get('_id')}`, {
        "method": "PUT",
        "body": JSON.stringify(payload),
        "headers": {
            "Authorization": await getTokenHeaderValue(),
            'Content-Type': 'application/json'
        }
    })

    return ResponseManager(uptReq)
}