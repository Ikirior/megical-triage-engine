'use client';

import styles from "@/components/adminpanel/adminpanel.module.css"
import SingleButton from "@/components/singlebutton/singlebutton";
import { Trash2Icon, SaveIcon, UserPlus2Icon, ListPlusIcon } from "lucide-react"
import UpdatePatient from "./update_patient";
import AddPatient from "./add_patient";
import patient from "./patient";
import SendToQueue from "./sendtoqueue";

type usersection_params = {
    cell?: patient,
    newUser?: boolean,
    role?: string,
    setUsers?: Function,
    usersState?: patient[]
}

export default function PatientSection(params: usersection_params)
{
    let node_id = params.cell?._id.toWellFormed() ?? 'new';

    return (
        <form className={styles.usersection}>
            <div className={styles.content}>
                    
                    <input type="text" name="_id" id={node_id+'id'} value={params.cell?._id} placeholder="---" readOnly/>
                    <input type="text" name="rg" id={node_id+'rg'} defaultValue={params.cell?.rg} placeholder="00.000.000-0" pattern="\d{2}.\d{3}.\d{3}-\d" readOnly={!params.newUser} required={params.newUser}/>
                    <input type="text" name="cpf" id={node_id+'cpf'} defaultValue={params.cell?.cpf} placeholder="000.000.000-00" pattern="\d{3}.\d{3}.\d{3}-\d{2}" readOnly={!params.newUser} required={params.newUser}/>
                    <input type="text" name="name" id={node_id+'name'} defaultValue={params.cell?.name} placeholder="Ana Paula" pattern="([a-zA-Z]|\s|\.)+" readOnly={!params.newUser} required={params.newUser}/>
                    <input type="date" name="birth_date" id={node_id+'birth_date'} defaultValue={params.cell?.birth_date} min="1900-01-01" max={new Date().toDateString()} readOnly={!params.newUser} required={params.newUser}/>
                    <input type="text" name="address" id={node_id+'address'} defaultValue={params.cell?.address} required={params.newUser}/>
                    <input type="checkbox" style={{height: '50%', marginTop: '1.25vh'}} name="companion" id={node_id+'companion'} defaultChecked={!!params.cell?.companion}/>
                    <select name="race" id={node_id+'race'} defaultValue={params.cell?.race} required={params.newUser}>
                        <option value="branca">Branca</option>
                        <option value="preta">Preta</option>
                        <option value="parda">Parda</option>
                        <option value="amarela">Amarela</option>
                        <option value="indigena">Indígena</option>
                        <option value="ignorado">Ignorado</option>
                    </select>
                    <select name="sex" id={node_id+'sex'} defaultValue={params.cell?.sex} required={params.newUser}>
                        <option value="M">M</option>
                        <option value="F">F</option>
                        <option value="outro">Outro</option>
                    </select>
                    <input type="text" name="phone_num" id={node_id+'phone'} defaultValue={params.cell?.phone_num} required={params.newUser}/>

            </div>
            <div className={styles.sectionbuttons}>
                {
                    !params.newUser && 
                    <>
                        <SingleButton icon={<ListPlusIcon/>} backgroudColor="#5ebfff" submit={true} formAction={async (initialState, args) => {
                                
                                const resMan = await SendToQueue(initialState, args);
                                if(resMan.success)
                                {
                                    alert(params.cell?.name + ' was sent to the queue.');
                                }
                                return resMan;
                                
                                }} title="send user to queue"/>
                        <SingleButton icon={<SaveIcon/>} backgroudColor="#5eff79" submit={true} formAction={async (initialState, args) => {
                            
                            const resMan = await UpdatePatient(initialState, args);
                            if(resMan.success && params.setUsers && params.usersState)
                            {
                                // Replace user with updated version
                                params.setUsers(params.usersState.map(
                                    (user) => user._id == params.cell?._id ? resMan.content : user
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
                            
                            const resMan = await AddPatient(initialState, args);
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