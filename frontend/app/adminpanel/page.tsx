import style from '@/app/adminpanel/styles.module.css'
import cell from '@/components/adminpanel/cell';
import UserGroup from '@/components/adminpanel/usergroup';
import PathBar from "@/components/pathbar/pathbar";

export const dynamic='force-dynamic';

export default async function Page() {

  let usersReq = await fetch('http://backend_server:3001/users/')
  let users:cell[] = await usersReq.json();

  // User Groups (tables)
  // We will create a table for every role...

  let userGroups = ['receptionist', 'nurse', 'doctor', 'admin'].map(
    (role)=>
      {
        return <UserGroup title={role.toLocaleUpperCase()} users={users.filter((aCell)=>aCell.role == role)} key={role}/>
      })

  return (<>
    <PathBar path="Home > Admin Panel"></PathBar>
    <div className={style.panel}>
      <h1 style={{"fontSize": "2em"}}>Admin Panel</h1>
      <h2>Create, view and edit users in the system.</h2>
      {...userGroups}
    </div>
  </>
  );
}
