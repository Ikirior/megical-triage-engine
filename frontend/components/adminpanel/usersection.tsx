'use client';

import styles from "@/components/adminpanel/adminpanel.module.css"
import SingleButton from "../singlebutton/singlebutton"
import { Trash2Icon, Pencil, SaveIcon, UserPlus2Icon } from "lucide-react"
import cell from "./cell"
import DeleteUser from "./del_user"
import { InputEventHandler, SyntheticEvent, useState } from "react";
import UpdateUser from "./update_user";
import AddUser from "./add_user";
import { randomBytes } from "crypto";

type usersection_params = {
    cell: cell,
    newUser?: boolean 
}

const READ_ONLY_FIELDS = [
    'id', 'created_at', 'role'
]

export default function UserSection(params: usersection_params)
{
    const [state, setState] = useState({...params.cell})

    function updateField(e: React.ChangeEvent<HTMLInputElement>, keyName: keyof cell)
    {
        let value :string|number= e.target.value;
        let newState = {...state} as cell

        newState[keyName] = value

        setState(newState)
    }

    let keys = Object.keys(params.cell).sort();
    let cellNodes = [];
    
    for (let cellKey of keys)
    {
        // https://stackoverflow.com/questions/57086672/element-implicitly-has-an-any-type-because-expression-of-type-string-cant-b
        let value = params.cell[cellKey as keyof cell];
        let node_id = params.cell.id.toWellFormed()+cellKey;
    
        if(READ_ONLY_FIELDS.includes(cellKey))
            cellNodes.push(<input type="text" defaultValue={value} placeholder={'---'} id={node_id} key={node_id}  readOnly={true} />)
        else if(!params.newUser)
            cellNodes.push(<input type="text" defaultValue={value} id={node_id} key={node_id}  onChange={(e) => {updateField(e, cellKey as keyof cell)}}/>)
        else
            cellNodes.push(<input type="text" placeholder={value?.toString()} id={node_id} key={node_id}  onChange={(e) => {updateField(e, cellKey as keyof cell)}}/>)
            
    }


    return (
        <form className={styles.usersection}>
            <div className={styles.content}>
                {...cellNodes}
            </div>
            <div className={styles.sectionbuttons}>
                {
                    !params.newUser && 
                    <>
                        <SingleButton icon={<Trash2Icon/>} backgroudColor="#ff5145" action={() => DeleteUser({'id': params.cell.id})}/>
                        <SingleButton icon={<SaveIcon/>} backgroudColor="#5eff79" action={ () => { UpdateUser({id: params.cell.id, fields: state}) } }/>
                    </>
                }
                {
                    params.newUser && 
                    <>
                        <SingleButton icon={<UserPlus2Icon/>} text='Save User' backgroudColor="#dcff5e" action={ () => { AddUser({id: params.cell.id, fields: state}) } }/>
                    </>
                }
            </div>
        </form>
    )
}