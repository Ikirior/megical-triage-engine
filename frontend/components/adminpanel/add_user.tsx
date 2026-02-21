'use server';

import getTokenHeaderValue from "@/utils/getTokenHeader";
import ResponseManager, { responseManagerResponse } from "@/utils/responsemanager";

export default async function AddUser(initialState:responseManagerResponse, params: FormData) {

    const payload = {
        "name": params.get('name'),
        "email": params.get('email'),
        "cpf": params.get('cpf'),
        "rg": params.get('rg'),
        "role": params.get('role'),
        "specialization": params.get('specialization'),
        "password": params.get('password')
    }

    const addReq = await fetch(`http://backend_server:3001/users/`, {
        "method": "POST",
        "body": JSON.stringify(payload),
        "headers": {
            "Authorization": await getTokenHeaderValue(),
            'Content-Type': 'application/json'
        }
    })
    let res = addReq.status;

    console.log('added');

    return ResponseManager(addReq)
}