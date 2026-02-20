'use server';

export default async function DeleteUser(params: FormData) {

    const delReq = await fetch(`http://backend_server:3001/users/${params.get('id')}`, {
        "method": "DELETE"
    })
    let res = delReq.status;

    console.log('deleted');
    return res
}