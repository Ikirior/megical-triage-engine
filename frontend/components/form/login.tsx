'use server';

export default async function Login(params: FormData) {
    
    console.log(params.get('name'), params.get('password'))
    const payload = {
        "username": params.get('name'),
        "password": params.get('password')
    }

    const logReq = await fetch(`http://backend_server:3001/auth/login/`, {
        "method": "POST",
        "body": JSON.stringify(payload)
    })
    let res = logReq.status;

    console.log(await logReq.json())
}