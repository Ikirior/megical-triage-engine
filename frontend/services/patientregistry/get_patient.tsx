'use server';

import getTokenHeaderValue from "@/utils/getTokenHeader";
import ResponseManager, { responseManagerResponse } from "@/utils/responsemanager";

export default async function GetPatient(params:FormData)
{
  const cpf= params.get('cpf_search');

    // Handling User Fetch
    let res = await fetch(`http://backend_server:3001/patients/${cpf}`,
    {
      headers: {
        'Authorization': await getTokenHeaderValue(),
      }
    }
  )

  return ResponseManager(res);
}