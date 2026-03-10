'use client';

import styles from "@/components/adminpanel/adminpanel.module.css"
import SingleButton from "@/components/shared/singlebutton/singlebutton"
import { Trash2Icon, SaveIcon, UserPlus2Icon } from "lucide-react"
import { cell } from "@/types/Cell";
import DeleteUser from "../../services/adminpanel/del_user"
import UpdateUser from "../../services/adminpanel/update_user";
import AddUser from "../../services/adminpanel/add_user";

type usersection_params = {
    cell?: cell,
    newUser?: boolean,
    role?: string,
    setUsers?: Function,
    usersState?: cell[]
}

export default function UserSection(params: usersection_params)
{
    let node_id = params.cell?.id.toWellFormed() ?? 'new';

    return (
        <form className={styles.usersection}>
            <div className={styles.content}>
                
                    <input type="text" name="id" id={node_id+'id'} value={params.cell?.id} placeholder="---" readOnly/>
                    <input type="text" name="rg" id={node_id+'rg'} defaultValue={params.cell?.rg} placeholder="00.000.000-0" pattern="\d{2}.\d{3}.\d{3}-\d" readOnly={!params.newUser} required={params.newUser}/>
                    <input type="text" name="cpf" id={node_id+'cpf'} defaultValue={params.cell?.cpf} placeholder="000.000.000-00" pattern="\d{3}.\d{3}.\d{3}-\d{2}" readOnly={!params.newUser} required={params.newUser}/>
                    <input type="text" name="name" id={node_id+'name'} defaultValue={params.cell?.name} placeholder="Dr. Anne" pattern="([a-zA-Z]|\s|\.)+" required={params.newUser}/>
                    <input type="email" name="email" id={node_id+'email'} defaultValue={params.cell?.email} placeholder="example@example.com" required={params.newUser}/>
                    <input type="text" name="specialization" id={node_id+'specialization'} defaultValue={params.cell?.specialization} placeholder="Dermatology"/>
                    <input type="text" name="role" id={node_id+'role'} value={params.role ?? params.cell?.role} readOnly placeholder="---" required={params.newUser}/>
                    <input type="text" name="created_at" id={node_id+'created_at'} value={params.cell?.created_at && new Date(params.cell?.created_at).toString()} placeholder="---" readOnly/>

                    <input type="password" name="password" id={node_id+'password'} placeholder={params.newUser ? 'Insert New Password' : 'Click to change password'} required={params.newUser} pattern=".{8}.*"/>
            </div>
            <div className={styles.sectionbuttons}>
                {
                    !params.newUser && 
                    <>
                        <SingleButton icon={<Trash2Icon/>} backgroudColor="#ff5145" submit={true} formAction={async (initialState, args) => {
                            
                            const resMan = await DeleteUser(initialState, args);
                            if(resMan.success && params.setUsers && params.usersState)
                                // Update users with all but the deleted one
                                params.setUsers([...params.usersState].filter(
                                    (user) => user.id != params.cell?.id
                                ))
                            return resMan;
                            
                            }} title="delete user"/>
                        <SingleButton icon={<SaveIcon/>} successMessage={`User updated successfully.`} backgroudColor="#5eff79" submit={true} formAction={async (initialState, args) => {
                            
                            const resMan = await UpdateUser(initialState, args);
                            if(resMan.success && params.setUsers && params.usersState)
                            {
                                // Replace user with updated version
                                params.setUsers(params.usersState.map(
                                    (user) => user.id == params.cell?.id ? resMan.content : user
                                ))
                            }
                            return resMan;
                            
                            }} title="update user"/>
                    </>
                }
                {
                    params.newUser && 
                    <>
                        <SingleButton icon={<UserPlus2Icon/>} text='Save User' backgroudColor="#dcff5e" submit={true} formAction={async (initialState, args) => {
                            
                            const resMan = await AddUser(initialState, args);
                            if(resMan.success && params.setUsers && params.usersState)
                                params.setUsers([...params.usersState, resMan.content])
                            return resMan;
                            
                            }} title="save new user"/>
                    </>
                }
            </div>
        </form>
    )
}