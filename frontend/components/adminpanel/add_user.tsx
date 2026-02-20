'use server';

import { randomUUID } from "crypto";
import cell from "./cell";

type addUserParams = {
    id: string,
    fields: cell
}

export default async function AddUser(params: addUserParams) {
    const addReq = await fetch(`http://backend_server:3001/users/${params.id}`, {
        "method": "POST",
        "body": JSON.stringify({...params.fields, password: randomUUID.call(params.fields)})
    })
    let res = addReq.status;
    console.log(res, {...params.fields, password: randomUUID.call(params.fields)});
    return res
}