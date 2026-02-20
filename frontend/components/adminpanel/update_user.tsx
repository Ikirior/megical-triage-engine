'use server';

import cell from "./cell";

type UpdateUserParams = {
    id: string
    fields: cell
}

export default async function UpdateUser(params: UpdateUserParams) {
    let uptReq = await fetch(`http://backend_server:3001/users/${params.id}`, {
        "method": "PUT",
        "body": JSON.stringify(params.fields)
    })
    let res = uptReq.status;
    return res
}