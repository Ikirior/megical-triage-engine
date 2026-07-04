'use server';

import getTokenHeaderValue from "@/utils/getTokenHeader";
import ResponseManager from "@/utils/responsemanager";

export default async function getUsers()
{
  'use server';
    // Handling User Fetch
  let res = await fetch('http://backend_server:3001/users/',
    {
      headers: {
        'Authorization': `${await getTokenHeaderValue()}`
      }
    }
  )
  const managerRes = await ResponseManager(res);

  return managerRes;

}