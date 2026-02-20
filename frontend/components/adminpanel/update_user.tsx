'use server';

export default async function UpdateUser(params: FormData) {

    let payload = {
        "name": params.get('name'),
        "email": params.get('email'),
        "cpf": params.get('cpf'),
        "rg": params.get('rg'),
        "role": params.get('role'),
        "specialization": params.get('specialization'),
        "password": params.has('password') ? params.get('password') : null
    }

    let uptReq = await fetch(`http://backend_server:3001/users/${params.get('id')}`, {
        "method": "PUT",
        "body": JSON.stringify(payload)
    })
    let res = uptReq.status;

    console.log('updated')

    return res
}