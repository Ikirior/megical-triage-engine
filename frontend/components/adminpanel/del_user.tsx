'use server';

type DelUserParams = {
    id: string
}

export default async function DeleteUser(params: DelUserParams) {
    const delReq = await fetch(`http://backend_server:3001/users/${params.id}`, {
        "method": "DELETE"
    })
    let res = delReq.status;
    return res
}