'use server';

export default async function AddUser(params: FormData) {

    const payload = {
        "name": params.get('name'),
        "email": params.get('email'),
        "cpf": params.get('cpf'),
        "rg": params.get('rg'),
        "role": params.get('role'),
        "specialization": params.get('specialization'),
        "password": params.get('password')
    }

    const addReq = await fetch(`http://backend_server:3001/users/${params.get('id')}`, {
        "method": "POST",
        "body": JSON.stringify(payload)
    })
    let res = addReq.status;

    console.log('added');

    return res
}