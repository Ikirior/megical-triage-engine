import style from '@/app/adminpanel/styles.module.css'
import cell from '@/components/adminpanel/cell';
import UserGroup from '@/components/adminpanel/usergroup';
import PathBar from "@/components/pathbar/pathbar";
import getTokenHeaderValue from '@/utils/getTokenHeader';
import ResponseManager from '@/utils/responsemanager';
import { JSX } from 'react';

export const dynamic='force-dynamic';

async function getUsers()
{
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

export default async function Page() {

  const managerRes = await getUsers();

  // Page Rendering
  let userGroups:JSX.Element[] = [];

  if(managerRes.success)
  {
    let users:cell[] = managerRes.content;
  
    // User Groups (tables)
    // We will create a table for every role...
  
    userGroups = ['receptionist', 'nurse', 'doctor', 'admin'].map(
      (role)=>
        {
          return <UserGroup title={role.toLocaleUpperCase()} users={users.filter((aCell)=>aCell.role == role)} key={role}/>
        })
  }

  return (<>
    <PathBar path="Home > Admin Panel"></PathBar>
    {!managerRes.success && managerRes.msg}
    <div className={style.panel}>
      <h1 style={{"fontSize": "2em"}}>Admin Panel</h1>
      <h2>Create, view and edit users in the system.</h2>
      {...userGroups}
    </div>
  </>
  );
}
