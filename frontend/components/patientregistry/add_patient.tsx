'use server';

import getTokenHeaderValue from "@/utils/getTokenHeader";
import ResponseManager, { responseManagerResponse } from "@/utils/responsemanager";

export default async function AddPatient(initialState:responseManagerResponse, params: FormData) {

    const payload = {
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

    const addReq = await fetch(`http://backend_server:3001/patients/`, {
        "method": "POST",
        "body": JSON.stringify(payload),
        "headers": {
            "Authorization": await getTokenHeaderValue(),
            'Content-Type': 'application/json'
        }
    })

    return ResponseManager(addReq)
}